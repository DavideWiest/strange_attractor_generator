from trainingdata_ui import RatingSaver
from modules.constants import *


rs = RatingSaver(BATCHNAME, "graphBatches", True)
rs.loadAndDistributeRatings()