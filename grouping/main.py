"""
A CLI to group images into either a light or dark category and moves them into the
apropriate folders.

TO-DO:
    -give the options to: overwrite files, do not create directories,
        create all directories regarless of content
    -deal with edge cases such as .. and ~
"""

import argparse
import json
from typing import Tuple
from sys import path
from os.path import splitext, join, basename
from os import listdir, makedirs
import shutil
from colorama import Fore
from pyciede2000 import ciede2000

path.append("..")

from imageaverage.main import main as average  # pylint: disable=wrong-import-position


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


def _mainlogic(file, options_dict, threashold, fallback_path, copy):
    average_c = average(file, 1, False)[0]
    deltas = {
        key: calculate_delta_e(options_dict[key], average_c)
        for key in options_dict.keys()
    }

    lowest_delta_key = min(deltas, key=deltas.get)
    if deltas[lowest_delta_key] > threashold:
        save_path = fallback_path
    else:
        save_path = lowest_delta_key

    makedirs(save_path, exist_ok=True)

    if copy:
        shutil.copy(file, join(save_path, basename(file)))
    else:
        shutil.move(file, join(save_path, basename(file)))


def main(
    files,
    json_path: str,
    fallback_path: str = None,
    threashold: float = 1000,  # max value is 100 an delta e scale
    **kwargs
):
    """
    Main function for executing the appropriate functions given the parameters.
    """
    copy = kwargs.get("copy", False)
    recursive = kwargs.get("recurssive", True)

    with open(json_path, "r", encoding="utf-8") as file:
        options_dict = json.load(file)

    _, ext = splitext(files)
    if ext == "" and recursive:
        for file in listdir(files):
            file = join(files, file)
            _mainlogic(file, options_dict, threashold, fallback_path, copy)
    elif ext == "":
        print(
            Fore.RED
            + "Error: "
            + Fore.RESET
            + "To iterate over a directory set the -r flag."
        )
    elif ext != "":
        _mainlogic(files, options_dict, threashold, fallback_path, copy)


rgb_target = (230, 50, 50)  # Example RGB color
rgb_options_dict = {
    "dark": [0, 0, 0],
    "light": [255, 255, 255],
}
# print(main(rgb_target, rgb_options_dict))

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
        "--threashold",
        metavar="",
        default=1000,
        type=float,
        help="The Delta-E threashold. Should be a value between 1-100. Default: None",
    )

    parser.add_argument(
        "-f",
        "--fallback",
        type=str,
        metavar="",
        help="Where to store files that over the Delta-E threashold ",
    )

    parser.add_argument(
        "-r",
        action="store_true",
        help="Recursive operation. Applies the command to directories \
            and their contents recursively.",
    )

    parser.add_argument(
        "-c",
        "--copy",
        action="store_true",
        help="Copies the files instead of moving them.",
    )

    args = parser.parse_args()

    # endregion

    main(
        args.path,
        args.json_path,
        args.fallback,
        args.threashold,
        recurssive=args.r,
        copy=args.copy,
    )
