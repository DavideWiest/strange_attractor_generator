from distanceEvaluator import getCoordinatesRatingMap, visualizeCorrelation, saveWithPolyfit
from modules.constants import *
from modules.singulargrahvisualizer import SingularGraphVisualizer

from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

from collections.abc import Sequence

def getPixelRatingMap(crm: list[Sequence[list, float]], wantedColors: list[tuple[int, int, int]]) -> list[tuple[int, float]]:
    vis = SingularGraphVisualizer({})
    prm = []
    for pair in crm:
        count = pixelWantedColorCount(vis, pair[0], wantedColors)
        print(count)
        prm.append((count, pair[1]))
    return prm

def pixelWantedColorCount(vis: SingularGraphVisualizer, coordinates: list, wantedColors: list[tuple[int, int, int]]) -> int:
    vis.drawCoordinates2D_seq(coordinates)
    img = convertPlotToImg()
    
    return countPixelsByColors(img, wantedColors)

def convertPlotToImg() -> Image:
    canvas = FigureCanvasAgg(plt.gcf())
    canvas.draw()
    buffer = canvas.buffer_rgba()
    width, height = canvas.get_width_height()

    return Image.frombuffer('RGBA', (width, height), buffer, 'raw', 'RGBA', 0, 1)


def countPixelsByColors(img: Image, rgbColors: list[tuple[int, int, int]]) -> int:
    # Convert the image to RGB mode (if necessary)
    image = img.convert("RGB")

    # Convert the image to a NumPy array
    image_array = np.array(image)

    # Compare the target color with each pixel color
    # Count the number of True values (matching pixels)
    pixel_count = sum(
        np.sum(np.all(image_array == color, axis=2)) for color in rgbColors
    )
    
    return int(pixel_count)

def printUniqueRGBValues(img: Image):
    # Convert the image to RGB mode (if necessary)
    image = img.convert("RGB")
    image_array = np.array(image)

    reshaped_array = image_array.reshape(-1, 3)
    unique_values = np.unique(reshaped_array, axis=0)

    print("----")
    for rgb in unique_values:
        if rgb[2] > 150:
            print(rgb)

def replaceColors(img: Image, from_color: tuple[int, int, int], to_color: tuple[int, int, int]) -> Image:
    # Convert the image to RGB mode (if necessary)
    image = img.convert("RGB")

    # Convert the image to a NumPy array
    image_array = np.array(image)

    # Create a mask of pixels matching the "from_color"
    mask = np.all(image_array == from_color, axis=2)

    # Replace the matching pixels with the "to_color"
    image_array[mask] = to_color

    # Create a new image from the modified array
    replaced_image = Image.fromarray(image_array)

    return replaced_image

WANTED_COLORS = [
    [31, 119, 180],
    [32, 120, 180],
    [33, 120, 180],
    [34, 121, 181],
    [35, 121, 181],
    [36, 122, 181],
    [37, 122, 182],
    [37, 123, 182],
    [38, 123, 182],
    [40, 124, 183],
    [41, 125, 183],
    [42, 125, 183],
    [44, 126, 184],
    [45, 127, 184],
    [47, 129, 185],
    [48, 129, 185],
    [49, 130, 186],
    [51, 131, 186],
    [51, 131, 187],
    [52, 132, 187],
    [53, 132, 187],
    [55, 133, 188],
    [56, 134, 188],
    [58, 135, 189],
    [59, 136, 189],
    [60, 137, 189],
    [61, 137, 190],
    [62, 138, 190],
    [63, 138, 190]
]

if __name__ == "__main__":
    crm = getCoordinatesRatingMap(BATCHES, OUTERDIRLOC)
    prm = getPixelRatingMap(crm, WANTED_COLORS)
    prm = np.array(prm)
    visualizeCorrelation(prm)
    saveWithPolyfit(prm, "data/pixelcount.txt")