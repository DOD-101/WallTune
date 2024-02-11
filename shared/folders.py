"""
Module for handling work with files / folders across the project.
"""

from os import walk
from os.path import join, isfile, isdir, splitext
from enum import IntEnum, auto


class PathType(IntEnum):
    """
    Enum constants for determining PathType.
    """

    FILE = auto()
    DIRECTORY = auto()
    NEW_FILE = auto()
    NEW_DIR = auto()
    ERROR = auto()


def list_all_contents(path: str) -> list:
    """
    Lists the content of the dir and all sub dirs.
    """
    file_list = []
    # Walk through the directory
    for root, _, files in walk(path):
        for file in files:
            # Construct full file path
            file_path = join(root, file)
            # Add file path to the list
            file_list.append(file_path)
    return file_list


def check_path_type(path: str) -> str:
    """
    Checks the type of path provided and returns the apropriate PathType enum.
    """
    if isfile(path):
        return PathType.FILE

    if isdir(path):
        return PathType.DIRECTORY

    if splitext(path)[1] == "":
        return PathType.NEW_DIR

    if splitext(path)[1] != "":
        return PathType.NEW_FILE

    return PathType.ERROR
