"""
A simmple CLI for getting your most recent songs images from spotify via the API.

TO-DO:
    - allow users to use an album instead of the liked songs
"""

import argparse
from os import getcwd
from os.path import join
from urllib.request import urlretrieve

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

# region argsparse

parser = argparse.ArgumentParser(
    description="A simmple CLI for getting your most recent songs images from spotify via the API.",
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

# endregion

SCOPE = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))

args = parser.parse_args()

results = sp.current_user_saved_tracks(limit=args.amount)
for idx, item in enumerate(results["items"]):
    track = item["track"]
    print(idx, track["artists"][0]["name"], " - ", track["name"])
    urlretrieve(
        track["album"]["images"][0]["url"],
        join(args.path, f"{track['name']}_albumCover.jpg"),
    )
