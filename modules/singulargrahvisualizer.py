
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from collections.abc import Sequence


defaultSettings = {

}

class SingularGraphVisualizer():
    """
    
    """
    def __init__(self, settings: dict = {}):
        self.settings: dict = {**defaultSettings, **settings}

    def drawCoordinates2D_seq(self, coordinates: list[Sequence[float, float]], doPlot: bool = True):       
        plt.close("all")
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.scatter([c[0] for c in coordinates], [c[1] for c in coordinates])
        if doPlot:
            ax.plot([c[0] for c in coordinates], [c[1] for c in coordinates])

    def drawCoordinates2D(self, coordinates: np.ndarray, doPlot: bool = True):       
        plt.close("all")
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.scatter(coordinates[:, 0], coordinates[:, 1])
        if doPlot:
            ax.plot(coordinates[:, 0], coordinates[:, 1])
    
    def drawCoordinates3D(self, coordinates: np.ndarray, doPlot: bool = True):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')
        ax.scatter(coordinates[:, 0], coordinates[:, 1], coordinates[:, 2])
        if doPlot:
            ax.plot(coordinates[:, 0], coordinates[:, 1], coordinates[:, 2])

    def show(self):
        plt.show()

    def save(self, filename: str, dirLoc: str = None):
        plt.savefig(dirLoc + "/" + filename if dirLoc else filename)





class SingularGraphVisualizerSeaborn():
    """
    
    """
    def __init__(self, settings: dict):
        self.settings: dict = {**defaultSettings, **settings}
        sns.set(style = "darkgrid")

    def drawCoordinates2D(self, coordinates: list[tuple[int, int]]):       
        a = sns.scatterplot(data=coordinates, marker=".", s=400)
        a.legend_.remove()
    
    def drawCoordinates3D(self, coordinates: list[tuple[int, int, int]]):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')
        ax.scatter(coordinates[:, 0], coordinates[:, 1], coordinates[:, 2])

    def show(self):
        plt.show()

    def save(self, filename: str, dirLoc: str = None):
        plt.savefig(dirLoc + "/" + filename if dirLoc else filename)