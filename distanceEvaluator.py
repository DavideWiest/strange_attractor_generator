from modules.constants import *
from trainingdata_ui import getAllGraphFilesInDir
from modules.singulargrahvisualizer import SingularGraphVisualizer

import json
import numpy as np
import matplotlib.pyplot as plt

def getCoordinatesRatingMap(batches: list[str], outerDirLoc: str) -> list[tuple[list, float]]:
    coordinatesRatingMap = []
    for batch in batches:
        files = getAllGraphFilesInDir(outerDirLoc + "/" + batch)
        for file in files:
            with open(outerDirLoc + "/" + batch + "/" + file, "r") as f:
                contents = json.load(f)
            coordinatesRatingMap.append((np.array(contents["coordinates"]), contents["rating"]))
    return coordinatesRatingMap

def meanDistance(coordinates) -> np.float32:
    # Calculate the pairwise Euclidean distances between coordinates
    distances = np.linalg.norm(coordinates[:, None] - coordinates, axis=2)

    distances = np.nan_to_num(distances, nan=0)

    # Calculate the average distance
    avg_distance = np.mean(distances)

    return avg_distance

def visualizeCorrelation(xyArr: np.ndarray):
    vis = SingularGraphVisualizer({})
    vis.drawCoordinates2D(xyArr, doPlot=False)

    slope, intercept = np.polyfit(xyArr[:, 0], xyArr[:, 1], deg=1)
    # slope, intercept = slope.astype(float), intercept.astype(float)
    correlation = np.corrcoef(xyArr[:, 0], xyArr[:, 1])[0, 1]

    print("Correlation:", correlation)
    print("Line equation: y =", slope, "* x +", intercept)

    start = np.min(xyArr[:, 0]).astype(float)
    stop = np.max(xyArr[:, 0]).astype(float)
    plt.plot([x for x in np.arange(start, stop, 0.1)], \
             [slope*x+intercept for x in np.arange(start, stop, 0.1)])

    vis.show()

def saveWithPolyfit(xyArr: np.ndarray, filename):
    slope, intercept = np.polyfit(xyArr[:, 0], xyArr[:, 1], deg=1)
    xyArr[:, 0] = xyArr[:, 0] * slope
    xyArr[:, 0] = xyArr[:, 0] + intercept

    save_first_column(xyArr, filename)

def save_first_column(array, filename):
    first_column = array[:, 0]
    np.savetxt(filename, first_column, fmt='%.8f', delimiter='\n')

if __name__ == "__main__":
    crm = getCoordinatesRatingMap(BATCHES, OUTERDIRLOC)
    drm = np.array([
        (meanDistance(np.array(pair[0])), pair[1]) for pair in crm
    ])
    drm[:, 0] = drm[:, 0] ** 2
    # print(drm.tolist())
    visualizeCorrelation(drm)
    saveWithPolyfit(drm, "data/distance.txt")
