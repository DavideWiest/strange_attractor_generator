from dataclasses import dataclass, asdict

# BATCHES

@dataclass
class BatchContextTemplate():
    pass

@dataclass
class BasicBatchContext(BatchContextTemplate):
    # dimension, 2 recommended
    dim: int
    # maximal degree, low numbers recommended
    maxDegree: int
    graphNum: int
    pointsNum: int
    startingValues: tuple[int, ...]

# GRAPHS

@dataclass
class GraphContextTemplate():
    pass

@dataclass
class BasicGraphContext(GraphContextTemplate):
    # lambda formula as string for each variable (number of variables = dim)
    formulaStr: list
    coordinates: list[tuple[int, int]]

@dataclass
class ExtendedGraphContext(GraphContextTemplate):
    # lambda formula as string for each variable (number of variables = dim)
    formulaStr: list
    formulaMap: dict[str, float]
    metrics: dict[str, float]
    rating: float
    coordinates: list[tuple[int, int]]




