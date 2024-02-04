"""
A CLI to take in a file/files and adjust the brightness conditionally.
"""

import argparse
from sys import path
from sys import exit as sysexit
from os import listdir
from os.path import isdir, splitext, join, basename
from PIL import Image, ImageEnhance
from colorama import Fore

path.append("..")

from shared.brightness import (  # pylint: disable=wrong-import-position
    getbrightness,
)


def adjustbrightness(img: Image.Image, mod: float) -> Image.Image:
    """Adjusts the brightness of the given image by the modifier."""
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(mod)
    return img


def meetcondition(value: float, condition: float, is_max: bool = False) -> bool:
    """Checks if the given value meets the condition."""
    meet = value > condition
    if is_max:
        return not meet
    return meet


def _mainlogic(file, condition, is_max, mod, output):
    """
    Internal logic of the main function. Responsible for checking brightness and applying modifier.
    """
    # Check if the file ends with .jpg or .png
    if splitext(file)[1] in [".jpg", ".png"]:
        img = Image.open(file)
        brightness = getbrightness(img)
        if meetcondition(brightness, condition, is_max):
            img = adjustbrightness(img, mod)
        else:
            mod = 1
        if isdir(output):
            output = join(output, basename(file))
        img.save(output)
        print(f"Saved {output} having modified {file} by {mod}.")


def main(files, output, condition, mod, **kwargs):
    """
    Main function for executing the appropriate functions given the parameters.
    """
    recursive = kwargs.get("recursive", False)
    is_max = kwargs.get("is_max", False)

    if isdir(files) and recursive:
        for file in listdir(files):
            file = join(files, file)
            _mainlogic(file, condition, is_max, mod, output)
    elif not isdir(files):
        _mainlogic(files, condition, is_max, mod, output)
    elif isdir(files) and not recursive:
        print(
            Fore.RED
            + "Error: "
            + Fore.RESET
            + "To iterate over a directory set the -r flag."
        )
    else:
        sysexit()


if __name__ == "__main__":

    # region argparse

    parser = argparse.ArgumentParser(
        description="Takes in a file / directory and adjusts the brightness conditionally.",
        usage="<input path> <output path> [options]",
    )

    parser.add_argument(
        "path", metavar="path", type=str, help="Path to the input file(s)."
    )

    parser.add_argument(
        "destination",
        metavar="destination",
        type=str,
        help="Path to the save location of the file(s).",
    )

    parser.add_argument(
        "-m",
        "--mod",
        metavar="",
        type=float,
        default=1,
        help="Value for modifying the brightness. Default: 1",
    )

    parser.add_argument(
        "-c",
        "--condition",
        type=float,
        metavar="",
        default=255,
        help="Mean brightness of image needed to convert it using the modifier. Default: None",
    )

    parser.add_argument(
        "-r",
        action="store_true",
        help="Recursive operation. Applies the command to directories \
            and their contents recursively.",
    )

    parser.add_argument(
        "-x",
        "--max",
        action="store_true",
        default=False,
        help="Changes the condition from being the minimum to be being the maximum value.",
    )

    args = parser.parse_args()

    # endregion

    main(
        args.path,
        args.destination,
        args.condition,
        args.mod,
        recursive=args.r,
        is_max=args.max,
    )
