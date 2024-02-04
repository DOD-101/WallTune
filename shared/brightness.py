"""
Shared function for getting the mean brightness of an image.
"""

from PIL import Image, ImageStat


def getbrightness(img: Image.Image) -> float:
    """Gets the mean brightness of an image by converting it to grayscale."""
    im = img.convert("L")
    stat = ImageStat.Stat(im)
    return stat.mean[0]
