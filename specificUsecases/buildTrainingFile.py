from trainingdata_ui import getAllGraphFilesInDir
from modules.constants import *
from modules.formulaparser import FormulaParser

import json
import csv

from train import TRAIN_DATA_FILENAME


def getParsedFormulaAndComponentNames(fp, fileLoc):
    with open(fileLoc, "r") as f:
        contents = json.load(f)

    parsedFormulaPair = fp.outputParsedComponents([f.split(": ")[1] for f in contents["formulaStr"]], {"a": [1,2], "b": [1,2], "yShift": [1]})
    
    return contents["rating"], parsedFormulaPair, [sorted(list(ks)) for ks in parsedFormulaPair]

def extractTrainingData(fp, fileLoc):
    rating, parsedFormulaPair, keysSorted = getParsedFormulaAndComponentNames(fp, fileLoc)

    result = []
    for formulaKeys, fp in zip(keysSorted, parsedFormulaPair):
        result += [fp[k] for k in formulaKeys]

    result.append(rating)

    return result

if __name__ == "__main__":
    files = []
    for batch in BATCHES:
        files += getAllGraphFilesInDir(OUTERDIRLOC + "/" + batch)

    
    fp = FormulaParser()
    _, _, headerList = getParsedFormulaAndComponentNames(fp, OUTERDIRLOC + "/" + batch + "/" + files[0])
    header = [str(item) for sublist in headerList for item in sublist]
    header.append("rating")

    trainingData = [
        extractTrainingData(fp, OUTERDIRLOC + "/" + batch + "/" + fileLoc) for fileLoc in files
    ]

    with open("data/" + TRAIN_DATA_FILENAME, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(trainingData)
