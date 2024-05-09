"""
A simple CLI for getting the image of the currently playing song / episode via the Spotify API. 
"""

import argparse
from os import makedirs
from os.path import join, abspath, dirname, isdir
from sys import path
from sys import exit as sysexit
from time import sleep
from urllib.request import urlretrieve

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from colorama import Fore

path.append(abspath(join(dirname(__file__), "..")))

# pylint: disable=wrong-import-position

from shared.sanitize import sanitize_filename

# pylint: enable=wrong-import-position

SCOPE = "user-read-currently-playing"

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))


def main(save_path: str, interval: int, create_no_dirs: bool):
    """
    The main function for getting the image of the currently playing song / episode.
    """
    if not create_no_dirs:
        makedirs(save_path, exist_ok=True)
    elif not isdir(save_path):
        print(
            Fore.RED
            + "Error: "
            + Fore.RESET
            + f"Directory {save_path} doesn't exist and -n / --create-no-dirs is set."
        )
        sysexit(1)
    data = {}
    while True:
        last_data = data or {}
        data = sp.currently_playing(additional_types="episode") or {}
        if last_data.get("item", {}).get("id", None) == data.get("item", {}).get(
            "id", None
        ):
            print("NO")
            sleep(interval)
            continue

        if data.get("item", {}).get("type", None) == "track":
            print("S ", data["item"]["name"])
            urlretrieve(
                data["item"]["album"]["images"][0]["url"],
                join(
                    save_path,
                    f"{sanitize_filename(data["item"]["name"])}_albumCover_current.png",
                ),
            )
        else:
            print("P ", data["item"]["name"])

            urlretrieve(
                data["item"]["images"][0]["url"],
                join(
                    save_path,
                    f"{sanitize_filename(data["item"]["name"])}_podcastCover_current.png",
                ),
            )


if __name__ == "__main__":

    # region argsparse

    parser = argparse.ArgumentParser(
        description="A simple CLI for getting your most recent songs images via the Spotify API.",
        usage="<path> [options]",
    )

    parser.add_argument(
        "path",
        metavar="path",
        type=str,
        help="Where to save the files.",
    )

    parser.add_argument(
        "-i",
        "--interval",
        metavar="",
        type=int,
        default=10,
        help="How frequently the Spotify API should be called for the playback. Default: 10 (sec)",
    )

    parser.add_argument(
        "-n",
        "--create-no-dirs",
        action="store_true",
        help="Disallows the creation of any directories.",
    )

    args = parser.parse_args()

    # endregion

    main(args.path, args.interval, args.create_no_dirs)
