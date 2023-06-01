from typing import Callable, Iterable
import numpy as np

import traceback

from modules.constants import *

class CoordinatesGenerator():
    """
    
    """
    def __init__(self, lambdas: list[Callable], startingValues: tuple[int, int]=None, behaviorOnOverflow: OverflowBehavior = OverflowBehavior.backToZero):
        startingValues = startingValues or [1 for i in range(len(lambdas))]
        assert len(startingValues) == len(lambdas), "startingValues and the lambdas list must have the same length"
        self.dims = len(lambdas)
        self.lambdas = lambdas
        self.prevNums = startingValues
        self.behaviorOnOverflow = behaviorOnOverflow
    
    def generatePointsAsNumpyArray(self, max: int=250) -> np.ndarray:
        arr = np.zeros((max, self.dims))
        for i in range(max):
            arr[i] = self._generateNextPoint()
        return arr

    def generatePointsAsTuples(self, max: int=250) -> Iterable[tuple[int, int]]:
        for _ in range(max):
            yield self._generateNextPoint()

    def _generateNextPoint(self):
        currentNums = [self.nextIntegerSafe(self.lambdas[i], self.prevNums) for i in range(self.dims)]
        self.prevNums = currentNums
        return currentNums
        
    def nextIntegerSafe(self, generativeLambda: Callable, nums: tuple) -> float:
        try:
            return generativeLambda(*nums)
        except OverflowError:
            if self.behaviorOnOverflow == OverflowBehavior.backToZero:
                return 0
            elif self.behaviorOnOverflow == OverflowBehavior.setToMax:
                return 1.7976931348623157e+308
            else:
                raise NotImplementedError(f"self.behaviorOnOverflow={self.behaviorOnOverflow} not implemented yet")
        except ZeroDivisionError:
            traceback.format_exc()
            print(nums)


def normalizeCoordinates_old(array):
    x_min, y_min = np.min(array, axis=0)
    x_max, y_max = np.max(array, axis=0)

    x_range = x_max - x_min
    y_range = y_max - y_min

    shifted_array = np.copy(array)
    if x_range != 0:
        shifted_array[:, 0] = (shifted_array[:, 0] - x_min) / x_range
    else:
        shifted_array[:, 0] = shifted_array[:, 0] - shifted_array[0, 0]

    if y_range != 0:
        shifted_array[:, 1] = (shifted_array[:, 1] - y_min) / y_range
    else:
        shifted_array[:, 1] = shifted_array[:, 1] - shifted_array[0, 1]

    shifted_array[:, 0] = shifted_array[:, 0] * 2 - 1
    shifted_array[:, 1] = shifted_array[:, 1] * 2 - 1

    return shifted_array

def normalizeCoordinates(array):
    min_vals = np.min(array, axis=0)
    max_vals = np.max(array, axis=0)

    scaled_array = 2 * (array - min_vals) / (max_vals - min_vals) - 1

    return scaled_array