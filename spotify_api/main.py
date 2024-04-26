"""
A simple CLI for getting your most recent songs images from spotify via the API.

TO-DO:
    - allow users to use an album instead of the liked songs
"""

import argparse
from sys import exit as sysexit
from os import getcwd, makedirs
from os.path import join
from urllib.request import urlretrieve
from urllib.parse import quote
from re import sub

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from colorama import Fore

load_dotenv()

SCOPE = "user-library-read"


def sanitize_filename(filename):
    """
    Makes sure all files have valid names to be saved.
    """
    safe_filename = quote(filename.encode("utf-8"), safe=" ")
    # Replace any character that is not alphanumeric, dash, underscore, or space with an underscore
    safe_filename = sub(r"[^a-zA-Z0-9\-\s]", "_", safe_filename)
    return safe_filename


def main(save_path: str, amount: int, offset: int, create_no_dirs: bool):
    """Main function to get and save the images."""

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))

    if not create_no_dirs:
        makedirs(save_path, exist_ok=True)

    total_fetched = 0
    while total_fetched < amount:
        limit = min(50, amount - total_fetched)
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        total_fetched += len(results["items"])
        offset += limit

        for idx, item in enumerate(results["items"]):
            track = item["track"]
            safe_track_name = sanitize_filename(track["name"])
            print(idx, track["artists"][0]["name"], " - ", track["name"])
            try:
                urlretrieve(
                    track["album"]["images"][0]["url"],
                    join(save_path, f"{safe_track_name}_albumCover.jpg"),
                )
            except Exception as e:
                if create_no_dirs and isinstance(e, FileNotFoundError):
                    print(
                        Fore.RED
                        + "Error: "
                        + Fore.RESET
                        + f"Directory {save_path} doesn't exist and -n / --create-no-dirs is set."
                    )
                    sysexit(1)

                raise e

    print("Total fetched:", total_fetched)


if __name__ == "__main__":

    # region argsparse

    parser = argparse.ArgumentParser(
        description="A simple CLI for getting your most recent songs images via the spotify API.",
        usage="<path> [options]",
    )

    parser.add_argument(
        "path",
        metavar="path",
        type=str,
        default=join(getcwd(), "imgs"),
        help="Where to save the files.",
    )

    parser.add_argument(
        "-a",
        "--amount",
        metavar="",
        type=int,
        default=20,
        help="The amount of images to get. Default: 20",
    )

    parser.add_argument(
        "-o",
        "--offset",
        metavar="",
        type=int,
        default=0,
        help="The offset of your most recent liked songs to start from.",
    )

    parser.add_argument(
        "--create-no-dirs",
        "-n",
        action="store_true",
        help="The opposite of -d. Disallows the creation of any directories.",
    )

    args = parser.parse_args()

    # endregion

    main(
        args.path,
        args.amount,
        args.offset,
        args.create_no_dirs,
    )
