from distanceEvaluator import getCoordinatesRatingMap, visualizeCorrelation, saveWithPolyfit
from modules.constants import *
from modules.singulargrahvisualizer import SingularGraphVisualizer

import math
import numpy as np

maxRepetition = 30
defaultNoRepetitionValue = 100

def getVectorDirectionRatingMap(crm: list[tuple[list, float]]):
    vectorRatingMap = []
    # vis = SingularGraphVisualizer()
    for pair in crm:
        v = checkVectorDirectionRepetition(pair[0])
        print(v)
        # vis.drawCoordinates2D_seq(pair[0])
        # vis.show()
        vectorRatingMap.append((v, pair[1]))
    return vectorRatingMap


def checkVectorDirectionRepetition(coordinates: np.ndarray) -> int:
    """
    Check if the vectors' directions repeat themselves after a certain number of iterations.

    Args:
        coordinates (ndarray): Numpy array of coordinates (shape: (n, 2)).

    Returns:
        int: The number of iterations after which the vectors' directions repeat,
             or -1 if no repetition is found.
    """
    n = coordinates.shape[0]
    directions = np.zeros((n - 1,))

    directions = coordinatesToDirection(coordinates)

    # print(directions)

    stop = min(round((n - 1) / 2)+1, maxRepetition)
    for i in range(2, stop):
        for offset in range(stop):
            if np.allclose(directions[offset::i], directions[offset], atol=1e-3):
                return i

    return defaultNoRepetitionValue

def checkVectorDirectionClustering(coordinates, threshold=1e-3):
    directions = coordinatesToDirection(coordinates)
    cluster_dict = findPointsCluster(directions, threshold)
    res = cluster_dict[max(cluster_dict, key=cluster_dict.get)]/coordinates.shape[0]
    print(res)
    return res

def findPointsCluster(arr1d, threshold):
    sortedArr = np.sort(arr1d)
    clusterDict = {}
    i = 0
    j = 0
    while i < sortedArr.shape[0]-1:
        while j <= sortedArr.shape[0]-1 and sortedArr[i] + threshold * 2 >= sortedArr[j]:
            j += 1
        clusterDict[sortedArr[math.floor((j+i)/2)]] = j-i
        i = j
    
    return clusterDict

def coordinatesToDirection(coordinates):
    directions = np.arctan2(coordinates[1:, 1] - coordinates[:-1, 1], coordinates[1:, 0] - coordinates[:-1, 0])
    directions = np.nan_to_num(directions, nan=0)
    return directions

if __name__ == "__main__":
    array = np.array([1, 2, 3, 5, 6, 8, 9])
    print(checkVectorDirectionClustering(array, threshold=2))

if __name__ == "__main__2":
    crm = getCoordinatesRatingMap(BATCHES, OUTERDIRLOC)
    vrm = getVectorDirectionRatingMap(crm)
    vrm = np.array(vrm)
    visualizeCorrelation(vrm)
    saveWithPolyfit(vrm, "data/vectordirection.txt")