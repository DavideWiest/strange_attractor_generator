from enum import Enum

# filenames 

GENERAL_INFO_FILENAME = "_INFO.json"

# graph attributes and related module behavior

OUTERDIRLOC = "graphBatches"
BATCHNAME = "b11"

ALLOW_BATCH_OVERWRITE = True
ALLOW_GRAPH_OVERWRITE = True

DIM = 2
MAX_DEGREE = 2
GRAPH_NUM = 500
POINTS_NUM = 200
STARTING_VALUES = (0, 0)

GENERATE_GRAPH = False

ALLOW_RATING_OVERWRITE = True
RECOGNIZE_EXISTING_RATINGS = False # Skip the graphs where the ratings already exist

GENERAL_RATING_FILENAME = "_RATINGS.txt"


BATCHES = ["b" + str(i) for i in range(1, 12)]



class OverflowBehavior(Enum):
    backToZero = 1
    setToMax = 2
