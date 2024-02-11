"""
A CLI to take in a file/files and adjust the brightness conditionally.
"""

import argparse
from sys import path
from os import makedirs, remove
from os.path import splitext, join, basename, abspath, dirname
from PIL import Image, ImageEnhance
from colorama import Fore

path.append(abspath(join(dirname(__file__), "..")))

# pylint: disable=wrong-import-position

from shared.brightness import (
    getbrightness,
)

from shared import folders

# pylint: enable=wrong-import-position


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


def _mainlogic(file, condition, mod, output, **kwargs):
    """
    Internal logic of the main function. Responsible for checking brightness and applying modifier.
    """
    is_max = kwargs.get("is_max", False)
    move = kwargs.get("move", False)

    # Check if the file ends with .jpg or .png
    if splitext(file)[1] in [".jpg", ".png"]:
        img = Image.open(file)
        brightness = getbrightness(img)
        if meetcondition(brightness, condition, is_max):
            img = adjustbrightness(img, mod)
        else:
            mod = 1

        outpathtype = folders.check_path_type(output)

        if outpathtype == folders.PathType.NEW_DIR:
            makedirs(output)

        if outpathtype in [folders.PathType.DIRECTORY, folders.PathType.NEW_DIR]:
            output = join(output, basename(file))

        img.save(output)
        print(f"Saved {output} having modified {file} by {mod}.")

        if move:
            remove(file)
            print(f"Deleted {file}")


def main(files, output, condition, mod, **kwargs):
    """
    Main function for executing the appropriate functions given the parameters.
    """
    recursive = kwargs.get("recursive", False)
    is_max = kwargs.get("is_max", False)
    move = kwargs.get("move", False)

    inpathtype = folders.check_path_type(files)

    if inpathtype == folders.PathType.DIRECTORY and recursive:
        fileslist = folders.list_all_contents(files)
        for file in fileslist:
            _mainlogic(file, condition, mod, output, move=move, is_max=is_max)
    elif inpathtype == folders.PathType.FILE:
        _mainlogic(files, condition, mod, output, move=move, is_max=is_max)
    elif inpathtype == folders.PathType.DIRECTORY and not recursive:
        print(
            Fore.RED
            + "Error: "
            + Fore.RESET
            + "To iterate over a directory set the -r flag."
        )
    elif inpathtype in [folders.PathType.NEW_DIR, folders.PathType.NEW_FILE]:
        print(Fore.RED + "Error: " + Fore.RESET + "Input cannot be empty.")
    else:
        print(Fore.RED + "Error: " + Fore.RESET + f"An Error has ocurred. {files}")


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
        help="Mean brightness of image needed to convert it using the modifier. \
        Should be a value between 0-255. Default: None",
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

    parser.add_argument(
        "--move", action="store_true", help="Moves the files instead of copying them."
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
        move=args.move,
    )
