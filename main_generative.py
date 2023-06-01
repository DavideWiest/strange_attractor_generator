from modules.coordinatesgenerator import CoordinatesGenerator, normalizeCoordinates
from modules.singulargrahvisualizer import SingularGraphVisualizer
from modules.formulagenerator import FormulaGenerator
from modules.contextmanaging import BatchContextSaver, GraphContextSaver
from modules.contexttemplates import BasicBatchContext, BasicGraphContext

import numpy as np
from tqdm import tqdm

from modules.constants import *

constantsGenerator = lambda size: np.round(np.random.normal(0, 1, size), 3)

# old version, treating all degrees equally
# degreeBoolGenerator = lambda degrees: np.random.choice([True, False], size=degrees)

def degreeBoolGenerator(shape):
    result = np.random.choice([True, False], size=shape)
    result = applyDecresedProbabilitiesForHigherDegrees(result, DIM)
    return result

def applyDecresedProbabilitiesForHigherDegrees(arr, dim):
    shape = arr.shape
    flattened = arr.flatten()
    for i in range(len(flattened)):
        if i % dim != 0:
            if np.random.rand() > (1/(i%dim)**2):
                flattened[i] = False
    return flattened.reshape(shape)

if __name__ == "__main__":
    fg = FormulaGenerator(DIM, MAX_DEGREE, constantsGenerator, degreeBoolGenerator)
    formulaPairs = fg.generate(GRAPH_NUM)

    batchContext = BasicBatchContext(DIM, MAX_DEGREE, GRAPH_NUM, POINTS_NUM, STARTING_VALUES)

    bs = BatchContextSaver(BATCHNAME, batchContext, OUTERDIRLOC)
    bs.save(ALLOW_BATCH_OVERWRITE)

    for i, formulaPair in tqdm(enumerate(formulaPairs), total=len(formulaPairs)):
        formulasLambda = [formulaTuple[0] for formulaTuple in formulaPair]
        formulasString = [formulaTuple[1] for formulaTuple in formulaPair]
        gen = CoordinatesGenerator(tuple(formulasLambda), STARTING_VALUES)
        coordinates = gen.generatePointsAsNumpyArray(POINTS_NUM)
        coordinates = normalizeCoordinates(coordinates)

        visSettings = {}
        vis = SingularGraphVisualizer(visSettings)

        if GENERATE_GRAPH:
            if DIM == 2:
                vis.drawCoordinates2D(coordinates)
            elif DIM == 3:
                vis.drawCoordinates3D(coordinates)
            else:
                raise NotImplementedError(f"drawCoordinates function not yet implemented for DIM={DIM}")
        
        context = BasicGraphContext(formulasString, coordinates.tolist())
        gs = GraphContextSaver(str(i), BATCHNAME, context, OUTERDIRLOC)
        gs.save(ALLOW_GRAPH_OVERWRITE)

        if GENERATE_GRAPH:
            vis.save(str(i)+".png", OUTERDIRLOC + "/" + BATCHNAME)
