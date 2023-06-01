import os
import json
from dataclasses import asdict

from modules.contexttemplates import BatchContextTemplate, GraphContextTemplate

from modules.constants import *


class BatchContextSaver():
    def __init__(self, batchName: str, context: BatchContextTemplate, outerDirLoc: str ="graphsBatches"):
        outerDirLoc += "/"
        self.batchName = batchName
        self.context = context
        self.outerDirLoc = outerDirLoc

    def save(self, allowOverwrite=False):
        finalLocation = self.outerDirLoc + "/" + self.batchName + "/" + GENERAL_INFO_FILENAME

        if os.path.exists(finalLocation) and not allowOverwrite:
            raise Exception(f"Cannot overwrite batch-context-file with finalLocation={finalLocation} and allowOverwrite=False")
        
        with open(finalLocation, "w") as f:
            json.dump(asdict(self.context), f, indent=4)

class BatchContextLoader():
    pass



class GraphContextSaver():
    def __init__(self, id: str, batchName: str, context: GraphContextTemplate, outerDirLoc: str ="graphsBatches"):
        outerDirLoc += "/"
        self.id = id
        self.batchName = batchName
        self.context = context
        self.outerDirLoc = outerDirLoc

    def save(self, allowOverwrite=False):
        finalLocation = self.outerDirLoc + "/" + self.batchName + "/" + self.id + ".json"

        if os.path.exists(finalLocation) and not allowOverwrite:
            raise Exception(f"Cannot overwrite graph-context-file with finalLocation={finalLocation} and allowOverwrite=False")
        
        with open(finalLocation, "w") as f:
            json.dump(asdict(self.context), f, indent=4)

class GraphContextLoader():
    pass
