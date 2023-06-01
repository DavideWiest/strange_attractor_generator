from trainingdata_ui import RatingSaver
from modules.constants import *


def incrementAllRatings(batches, x, outerDirLoc=OUTERDIRLOC):
    for batch in batches:
        with open(outerDirLoc + "/" + batch + "/" + GENERAL_RATING_FILENAME, "r") as f:
            file = f.read().split("\n")[:-1]
        file = [str(round(float(n)+x, 1)) for n in file]
        file = "\n".join(file) + "\n"
        with open(outerDirLoc + "/" + batch + "/" + GENERAL_RATING_FILENAME, "w") as f:
            f.write(file)
        rs = RatingSaver(batch, outerDirLoc, True)
        rs.loadAndDistributeRatings()

if __name__ == "__main__":
    # batches = ["b" + str(i+1) for i in range(10)]
    batches = ["b11"]
    incrementAllRatings(batches, 0.1)