"""
A CLI to group images into either a light or dark category and moves them into the
apropriate folders.

TO-DO:
    -give the options to: overwrite files, do not create directories,
        create all directories regardless of content
    -deal with edge cases such as .. and ~
"""

import argparse
import json
from typing import Tuple
from sys import path
from os.path import join, basename, abspath, dirname
from os import makedirs
import shutil
from colorama import Fore
from pyciede2000 import ciede2000

path.append(abspath(join(dirname(__file__), "..")))

# pylint: disable=wrong-import-position

from imageaverage.main import main as average

from shared import folders

# pylint: enable=wrong-import-position


def calculate_delta_e(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """
    First converts the rgb values to sRGB and then uses pyciede2000 to get Delta-E.
    """
    # Convert RGB to sRGB
    srgb1 = [val / 255 for val in rgb1]
    srgb2 = [val / 255 for val in rgb2]

    # Calculate delta E using CIEDE2000
    delta_e = ciede2000(tuple(srgb1), tuple(srgb2))["delta_E_00"]

    return delta_e


def _mainlogic(file, options_dict, threshold, fallback_path, move):
    average_c = average(file, 1, False)[0]
    deltas = {
        key: calculate_delta_e(options_dict[key], average_c)
        for key in options_dict.keys()
    }

    lowest_delta_key = min(deltas, key=deltas.get)
    if deltas[lowest_delta_key] > threshold:
        save_path = fallback_path
    else:
        save_path = lowest_delta_key

    makedirs(save_path, exist_ok=True)

    if move:
        shutil.move(file, join(save_path, basename(file)))
    else:
        shutil.copy(file, join(save_path, basename(file)))


def main(
    files,
    json_path: str,
    fallback_path: str = None,
    threshold: float = 1000,  # max value is 100 an delta e scale
    **kwargs,
):
    """
    Main function for executing the appropriate functions given the parameters.
    """
    move = kwargs.get("move", False)
    recursive = kwargs.get("recursive", True)

    with open(json_path, "r", encoding="utf-8") as file:
        options_dict = json.load(file)

    inpathtype = folders.check_path_type(files)
    if inpathtype == folders.PathType.DIRECTORY and recursive:
        filelist = folders.list_all_contents(files)
        for file in filelist:
            _mainlogic(file, options_dict, threshold, fallback_path, move)
    elif inpathtype == folders.PathType.DIRECTORY:
        print(
            Fore.RED
            + "Error: "
            + Fore.RESET
            + "To iterate over a directory set the -r flag."
        )
    elif inpathtype == folders.PathType.FILE:
        _mainlogic(files, options_dict, threshold, fallback_path, move)
    elif inpathtype in [folders.PathType.NEW_DIR, folders.PathType.NEW_FILE]:
        print(Fore.RED + "Error: " + Fore.RESET + "Input cannot be empty.")
    else:
        print(Fore.RED + "Error: " + Fore.RESET + f"An Error has ocurred. {files}")


if __name__ == "__main__":

    # regions argparse

    parser = argparse.ArgumentParser(
        description="Sorts images based on their lowest delta E value to given options.",
        usage="<path> <json path> [options]",
    )

    parser.add_argument("path", metavar="path", help="The path to the file(s)")

    parser.add_argument(
        "json_path",
        metavar="json path",
        help="Path to the Json containing the paths : color value",
    )

    parser.add_argument(
        "-t",
        "--threshold",
        metavar="",
        default=1000,
        type=float,
        help="The Delta-E threshold. Should be a value between 1-100. Default: None",
    )

    parser.add_argument(
        "-f",
        "--fallback",
        type=str,
        metavar="",
        help="Where to store files that are over the Delta-E threshold ",
    )

    parser.add_argument(
        "-r",
        action="store_true",
        help="Recursive operation. Applies the command to directories \
            and their contents recursively.",
    )

    parser.add_argument(
        "--move",
        action="store_true",
        help="Moves the files instead of moving them.",
    )

    args = parser.parse_args()

    # endregion

    main(
        args.path,
        args.json_path,
        args.fallback,
        args.threshold,
        recursive=args.r,
        move=args.move,
    )
