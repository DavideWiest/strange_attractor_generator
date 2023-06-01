"""
model training execution file
"""
from modules.logger import logging
from pathlib import Path
import os, json
import torch
from torch import nn

from ml_modules import test_step, train_step, train_full_fn, accuracy_fn_regression, accuracy_fn_variance
from ml_modules import ModelManager

from model import BasicModel, BasicModelWithSigmoid, SimpleModel

from sklearn.model_selection import train_test_split
import pandas as pd

# 1. Instantiate Model
# 2. Define Loss function and optimizer
# 3. Get data (more to device)
# 4. use train_full_fn
# 5. analyze?

TRAIN_DATA_FILENAME = "train_1k_Reg_simplified.csv"


if __name__ == '__main__':
    BASE_DIR = Path(__file__).resolve().parent
    BASE_DIR_NAME = os.path.dirname(Path(__file__).resolve())
    CONFIG_JSON_PATH = BASE_DIR / "config.json"

    device = "cuda" if torch.cuda.is_available() else "cpu"

    NUM_WORKERS = os.cpu_count()

    with open(CONFIG_JSON_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
        mconfig = config["model"]

    EPOCHS = mconfig["epochs"]
    SAVE_EACH = mconfig["save_each"]
    EARLY_STOP_EPOCH = mconfig["early_stop_epoch"]
    COMPARE_SAVED_METRIC = mconfig["compare_saved_metric"]
    BATCH_SIZE = config["computation"]["batch_size"]

    OUT_FTS = mconfig["output_features"]
    IN_FTS = mconfig["input_features"]
    HDN_UNITS = mconfig["hidden_units"]

    model = SimpleModel(mconfig["input_features"], mconfig["output_features"], mconfig["hidden_units"]).to(device)

    modelname = model.__class__.__name__
    # modelname = ""

    loss_fn = nn.L1Loss().to(device)

    optimizer = torch.optim.SGD(model.parameters(), lr=mconfig["lr"])

    mm = ModelManager(logging)
    model_statedict, path = mm.load(modelname, load_best_metric=COMPARE_SAVED_METRIC)

    if model_statedict != None:
        try:
            model.load_state_dict(model_statedict)
            logging.info(f"Loaded previous model (path: {path})")
        except:
            logging.info(f"Failed to load previous model (likely different layer and feature structure) (path: {path})")
    else:
        logging.info(f"Could not load any previous model for {modelname}")

    df = pd.read_csv("data/" + TRAIN_DATA_FILENAME, header=0)
    cols = df.shape[1]

    train_dataloader, test_dataloader = train_test_split(df, test_size=0.2, random_state=42)
    train_dataloader = (torch.tensor(train_dataloader.iloc[:, :-1].values, dtype=torch.float32), torch.tensor(train_dataloader.iloc[:, -1].values, dtype=torch.float32))
    test_dataloader = (torch.tensor(test_dataloader.iloc[:, :-1].values, dtype=torch.float32), torch.tensor(test_dataloader.iloc[:, -1].values, dtype=torch.float32))

    MODELS_SUBDIR = "first_sigmoid"

    output = train_full_fn(model, train_dataloader, test_dataloader, optimizer, loss_fn, accuracy_fn_regression, EPOCHS, device, save_each=SAVE_EACH, models_subdir=MODELS_SUBDIR)


