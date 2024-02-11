"""
Takes in a file / directory and get the average color of each file.

TO-DO:
    - Give user the option to modify the output color more than just brightness
"""

import argparse
from typing import Tuple
from sys import path
from sys import exit as sysexit
from os.path import isdir, splitext, join, abspath, dirname

from PIL import Image
import numpy as np
from colorama import Fore

path.append(abspath(join(dirname(__file__), "..")))

# pylint: disable=wrong-import-position

from shared.colorconversion import (
    rgb_to_hex,
)

from shared import folders

# pylint: enable=wrong-import-position

RGB = "RGB"


def get_average_color(image_path: str) -> Tuple[int, int, int]:
    """
    Gets the average color of an image and returns it as an rgb value.

    Will auto-convert the file to RGB.
    """
    img = Image.open(image_path)
    img = img.convert("RGB")  # Ensure image is in RGB mode
    pixels = np.array(img)
    avg_color = np.mean(pixels, axis=(0, 1))
    rounded_avg_color = tuple(map(round, avg_color))
    return rounded_avg_color


def modify(
    colors: Tuple[int, int, int], mod: float, no_warnings: bool = True
) -> Tuple[int, int, int]:
    """
    Takes in an rgb value tuple and darkens every color be the modifier.
    """

    g = 0
    return_colors = []

    if 0 > mod:
        print(Fore.RED + "ERROR: " + Fore.RESET + "mod cannot be less than 1.")
        sysexit()

    for i in colors:
        i = i * mod
        if i > 255:
            i = 255
            if not no_warnings:
                print(
                    Fore.YELLOW
                    + "Warning: "
                    + Fore.RESET
                    + f"{RGB[g]} value was capped at 255."
                )
        g += 1

        return_colors.append(round(i))

    return tuple(return_colors)


def main(files, mod: int, recursive: bool = False, no_warnings: bool = False):
    """
    Main function for executing the appropriate functions given the parameters.
    """
    returnoutput = []
    if isdir(files) and recursive:
        filelist = folders.list_all_contents(files)
        for file in filelist:
            # Check if the file ends with .jpg or .png
            if splitext(file)[1] in [".jpg", ".png"]:
                colors = get_average_color(file)
                colors = modify(colors, mod, no_warnings)
                returnoutput.append(colors)
    elif not isdir(files):
        colors = get_average_color(files)
        colors = modify(colors, mod)
        returnoutput.append(colors)
    elif isdir(files) and not recursive:
        print(
            Fore.RED
            + "Error: "
            + Fore.RESET
            + "To iterate over a directory set the -r flag."
        )
    else:
        sysexit()

    return returnoutput


if __name__ == "__main__":

    # region argparse

    parser = argparse.ArgumentParser(
        description="Takes in a file / directory and get the average color of each file.",
        usage="<path> [options]",
    )

    parser.add_argument("path", metavar="path", type=str, help="Path to the file(s)")

    parser.add_argument(
        "-m",
        "--mod",
        metavar="",
        type=float,
        default=1,
        help="Value for modifying the RGB values. (Changes brightness) Default: 1",
    )

    parser.add_argument(
        "--hex", action="store_true", help="Converts the output value from RGB to hex."
    )

    parser.add_argument(
        "-r",
        action="store_true",
        help="Recursive operation. Applies the command to directories \
            and their contents recursively.",
    )

    parser.add_argument(
        "--no-warnings", action="store_true", help="Omits any warnings."
    )

    args = parser.parse_args()

    # endregion

    output = main(args.path, args.mod, args.r, args.no_warnings)

    for o in output:
        if args.hex:
            print(rgb_to_hex(o))
        else:
            print(o)
