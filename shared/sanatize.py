"""
Module for handeling the sanatizing of filenames.
"""

from urllib.parse import quote
from re import sub


def sanitize_filename(filename: str):
    """
    Makes sure all files have valid names to be saved.
    """
    safe_filename = quote(filename.encode("utf-8"), safe=" ")
    # Replace any character that is not alphanumeric, dash, underscore, or space with an underscore
    safe_filename = sub(r"[^a-zA-Z0-9\-\s]", "_", safe_filename)
    return safe_filename
