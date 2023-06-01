"sag generator"

from typing import Callable
import numpy as np
from datetime import datetime
from dataclasses import dataclass
import random
from colorama import Fore
import os

from modules.formulagenerator import FormulaGenerator
from main_generative import degreeBoolGenerator, constantsGenerator
from modules.coordinatesgenerator import CoordinatesGenerator, normalizeCoordinates
from modules.singulargrahvisualizer import SingularGraphVisualizer
from modules.contextmanaging import GraphContextSaver
from modules.contexttemplates import ExtendedGraphContext
from modules.formulaparser import FormulaParser

from distanceEvaluator import meanDistance
from colorEvaluator import pixelWantedColorCount, WANTED_COLORS
from vectordirectionEvaluator import checkVectorDirectionRepetition, checkVectorDirectionClustering

@dataclass
class DifferenceEquation:
    formulaPair: tuple[Callable, ...]
    formulaPairStr: tuple[str, ...]
    name: str = None

    def __init__(self, formulaPair, formulaPairStr, name=None):
        self.formulaPair = formulaPair
        self.formulaPairStr = formulaPairStr
        self.name = name or self.generate_default_name()

    @staticmethod
    def generate_default_name():
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")
        random_number = random.randint(1, 10000)
        return f"{timestamp}_{random_number}"

class DifferenceEquationHandler:
    def __init__(self, diffEq: DifferenceEquation):
        self.diffEq = diffEq
        self.vis = SingularGraphVisualizer({})

        self.coordinates = None
        self.coordinatesList = None
        self.rating = None
        self.formulaMap = None
        self.metrics = None
    
    def generateCoordinates(self, n: int, start: tuple[int, int] = (0,0)):
        cg = CoordinatesGenerator(list(self.diffEq.formulaPair), start)
        self.coordinates = normalizeCoordinates(cg.generatePointsAsNumpyArray(n))
        self.coordinatesList = self.coordinates.tolist()

    def generateFormulaMap(self, obligatoryVariableExponentPairs = {"a": [1,2], "b": [1,2], "yShift": [1]}):
        fp = FormulaParser()
        self.formulaMap = fp.outputParsedComponents(self.diffEq.formulaPairStr, obligatoryVariableExponentPairs)
    
    def setRating(self, rating: float, keepBounds: bool):
        if keepBounds and rating < 0 or rating > 1:
            raise ValueError(f"Rating must be between 0 and 1, is {rating}")
        self.rating = rating

    def setMetrics(self, metrics: dict[str, float]):
        self.metrics = metrics
    
    def saveGraph(self, dirLoc: str, fileName: str = None):
        fileName = fileName or (self.diffEq.name + ".png")
        self.vis.drawCoordinates2D_seq(self.coordinatesList)
        self.vis.save(fileName, dirLoc)
    
    def saveInfoFile(self, outerDirLoc: str, batchName: str, fileName: str = None, allowOverwrite: bool = False):
        assert self.diffEq.formulaPairStr != None
        assert self.formulaMap != None
        assert self.coordinatesList != None
        assert self.metrics != None

        context = ExtendedGraphContext(list(self.diffEq.formulaPairStr), self.formulaMap, self.metrics, self.rating or -1, self.coordinatesList)
        
        gs = GraphContextSaver(fileName or self.diffEq.name, batchName, context, outerDirLoc)
        gs.save(allowOverwrite)


class SAG():
    def __init__(self, batchDirName: str, outerDirLoc: str, 
                 metricFnMap: dict[str, Callable], metricsPassedFn: Callable, \
                 formulaGeneratorInit: list = [2, 2, constantsGenerator, degreeBoolGenerator],
                 numCoordinates: int = 300, 
                 obligatoryVariableExponentPairs: dict[str, list[int]] = { "a": [1, 2],"b": [1, 2],"yShift": [1] }):
        
        "metricFnMap: dict with name as key, evaluation fn as value (which takes DiffEq and Coordinates as numpy array as inputs) \n metricsPassedFn: fn that takes a dict of name:returned-data of the metricFnMap and returns a bool, and a dict for each metric with bool as key (passed overall and passed by metric)"

        self.batchDirName = batchDirName
        self.outerDirLoc = outerDirLoc
        self.metricFnMap = metricFnMap
        self.metricsPassedFn = metricsPassedFn
        self.fg = FormulaGenerator(*formulaGeneratorInit)
        self.generationBatchSize = 20
        self.numCoordinates = numCoordinates
        self.obligatoryVariableExponentPairs = obligatoryVariableExponentPairs
    
    def generate(self, limit: int = float("inf")):
        i = 0
        while True:
            if i >= limit-1:
                print("Reached generation limit. Stopping process.")
                break
            acceptedNum = self.generateBatch(i)
            i += acceptedNum

    def generateBatch(self, index: int):
        formulaPairs = self.fg.generate(self.generationBatchSize)
        acceptedNum = 0
        for i, fp in enumerate(formulaPairs):
            diffEq = DifferenceEquation(tuple([t[0] for t in fp]), tuple([t[1] for t in fp]))
            diffEqHandler = DifferenceEquationHandler(diffEq)
            diffEqHandler.generateCoordinates(self.numCoordinates)
            metrics = self.generateMetrics(diffEq, diffEqHandler.coordinates)
            passedOverall, passedByMetric = self.metricsPassedFn(metrics)
            if passedOverall:
                self.save(diffEqHandler, metrics)
                acceptedNum += 1
            self.printInfoMsg(diffEq.name, index+i, passedOverall, passedByMetric)
        return acceptedNum

    def printInfoMsg(self, name, index: int, passedOverall: bool, passedIndependently: dict):
        indentendentPassedStr = ",".join([
            f"{Fore.GREEN if passed else Fore.RED}{metric}{Fore.RESET}" for metric, passed in passedIndependently.items()
        ])
        print(f"[{index+1}] DiffEq {name} [{Fore.GREEN if passedOverall else Fore.RED}{passedOverall}{Fore.RESET}] [{indentendentPassedStr}]")

    def boolWithColor(self, boolean: bool, text: str) -> str:
        return f"{Fore.GREEN if boolean else Fore.RED}{text}{Fore.RESET}"

    def generateMetrics(self, diffEq: DifferenceEquation, coordinates: np.ndarray):
        return {
            name: fn(diffEq, coordinates) for name, fn in self.metricFnMap.items()
        }
    
    def save(self, handler: DifferenceEquationHandler, metrics: dict):

        handler.setMetrics(metrics)
        handler.generateFormulaMap(self.obligatoryVariableExponentPairs)
        handler.saveGraph(dirLoc=self.outerDirLoc + "/" + self.batchDirName)
        handler.saveInfoFile(self.outerDirLoc, self.batchDirName)



vis = SingularGraphVisualizer({})

SAG_OUTER_DIRLOC = "_sag"
SAG_DIR_BATCHNAME = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
SAG_METRICS = {
    "distance": lambda diffEq,coordinates: meanDistance(coordinates),
    # "pixels": lambda diffEq,coordinates: pixelWantedColorCount(vis, coordinates.tolist(), WANTED_COLORS),
    "vectorClustering": lambda diffEq,coordinates: checkVectorDirectionClustering(coordinates),
    "vectorDirection": lambda diffEq,coordinates: checkVectorDirectionRepetition(coordinates)
}
def SAG_METRICS_PASSED_FN(metrics):
    result = {
        "distance": metrics["distance"] > 0.45,
        # "pixels": metrics["pixels"] > 6_000,
        "vectorClustering": metrics["vectorClustering"] < 0.5,
        "vectorDistance": metrics["vectorDirection"] > 13
    }
    return all(list(result.values())), result


if __name__ == "__main__":
    os.makedirs(SAG_OUTER_DIRLOC + "/" + SAG_DIR_BATCHNAME)

    sag = SAG(SAG_DIR_BATCHNAME, SAG_OUTER_DIRLOC, SAG_METRICS, SAG_METRICS_PASSED_FN)
    sag.generate(200)