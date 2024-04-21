"""
Takes in a file / directory and get the average color of each file.
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


def _modify_inner(value: int, mod: int, color: str, no_warnings: bool) -> int:
    """
    Internal logic of the modify function. For changeing an RGB channel.
    """
    return_value = value * mod

    if return_value > 255:
        if return_value > 255:
            return_value = 255
            if not no_warnings:
                print(
                    Fore.YELLOW
                    + "Warning: "
                    + Fore.RESET
                    + f"{color} value was capped at 255."
                )

    return return_value


def modify(
    color: Tuple[int, int, int], mod: float, no_warnings: bool, **kwargs
) -> Tuple[int, int, int]:
    """
    Takes in an rgb value tuple and darkens every color by the modifier.
    """
    red = kwargs.get("red", mod)
    green = kwargs.get("green", mod)
    blue = kwargs.get("blue", mod)

    return_colors = []

    if 0 > mod:
        print(Fore.RED + "Error: " + Fore.RESET + "mod cannot be less than 0.")
        sysexit(1)

    return_colors.append(_modify_inner(color[0], red, "red", no_warnings))
    return_colors.append(_modify_inner(color[1], green, "green", no_warnings))
    return_colors.append(_modify_inner(color[2], blue, "blue", no_warnings))

    return tuple(return_colors)


def main(files, mod: int, recursive: bool = False, no_warnings: bool = False, **kwargs):
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
                colors = modify(colors, mod, no_warnings, **kwargs)
                returnoutput.append(colors)
    elif not isdir(files):
        colors = get_average_color(files)
        colors = modify(colors, mod, no_warnings, **kwargs)
        returnoutput.append(colors)
    elif isdir(files) and not recursive:
        print(
            Fore.RED
            + "Error: "
            + Fore.RESET
            + "To iterate over a directory set the -r flag."
        )
    else:
        sysexit(1)

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
        help="Value for modifying the RGB values. The individual color flags overwrite this. \
              (Changes brightness) Default: 1",
    )

    parser.add_argument(
        "--red",
        metavar="",
        type=float,
        help="Value for modifying the red value.",
    )

    parser.add_argument(
        "--green",
        metavar="",
        type=float,
        help="Value for modifying the green value.",
    )

    parser.add_argument(
        "--blue",
        metavar="",
        type=float,
        help="Value for modifying the blue value.",
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

    if args.red is None:
        args.red = args.mod

    if args.green is None:
        args.green = args.mod

    if args.blue is None:
        args.blue = args.mod

    # endregion

    output = main(
        args.path,
        args.mod,
        args.r,
        args.no_warnings,
        red=args.red,
        green=args.green,
        blue=args.blue,
    )

    for o in output:
        if args.hex:
            print(rgb_to_hex(o))
        else:
            print(o)
