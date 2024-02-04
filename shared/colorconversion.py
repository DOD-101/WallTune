"""
Shared function of the project to convert rgb values to hex values.
"""

from typing import Tuple


def rgb_to_hex(rgbvalue: Tuple[int, int, int]) -> str:
    """Convert an RGB tuple to a hexadecimal color string."""
    return f"#{rgbvalue[0]:02x}{rgbvalue[1]:02x}{rgbvalue[2]:02x}"
