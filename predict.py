from ml_modules import ModelManager
import torch
import json
from pathlib import Path
from modules.logger import logging
from model import BasicModel, BasicModelWithSigmoid, SimpleModel


class PredictorInterface():
    def __init__(self, model_class, data_mode="normal", model_feature_param="model", model_subdir=None):
        # self.load_data_normal(data_mode)

        self.initialize_model(model_class, model_feature_param, model_subdir)

    def _get_feature_list_config(self, filename="config.json", key="model"):
        BASE_DIR = Path(__file__).resolve().parent
        CONFIG_JSON_PATH = BASE_DIR / filename

        with open(CONFIG_JSON_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
            mconfig = config[key]

        return [mconfig["input_features"], mconfig["hidden_units"], mconfig["output_features"]]

    # def load_data_normal(self, data_mode):
    #     if data_mode == "normal":
    #         with open("data/example.csv", "r", encoding="utf-8") as f:
    #             examplefile = f.read().split("\n")

    #         self.exampledict = {line.split(",")[2]: line.split(",")[1] for line in examplefile[1:]}
        
        
    def initialize_model(self, model_class, model_feature_param="model", model_subdir=None):
        if isinstance(model_feature_param, str):
        
            features_out = self._get_feature_list_config("config.json", model_feature_param)
            
            input_features, hidden_units, output_features = features_out
        elif isinstance(model_feature_param, list) or isinstance(model_feature_param, tuple):
            assert len(model_feature_param) == 3, "Function parameter model_feature_param must be None or numerical list of [input_features, hidden_units, output_features]"
            input_features, hidden_units, output_features = model_feature_param

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.mm = ModelManager(logging)

        self.model = model_class(input_features, output_features, hidden_units).to(self.device)
        self.statedict, path = self.mm.load(name=self.model.__class__.__name__, load_best_metric="loss", subdir=model_subdir)
        
        if self.statedict != None:
            self.model.load_state_dict(self.statedict)
        else:
            logging.info("Warning: No saved state dicts found")

    def predict(self, input, do_print=True):

        params = input

        y_pred = self.pass_into_model(params)
        
        if do_print:
            print(y_pred)

        return y_pred
        

    def pass_into_model(self, params):
        params = [float(i) for i in params]
        params = torch.tensor(params, dtype=torch.float32).to(self.device)

        y_pred = self.model(params)
        return y_pred.cpu().detach().numpy().astype(float)


if __name__ == "__main__":
    pi = PredictorInterface(SimpleModel)
    test = """-0.691,1.093,0,0.426,0.986,0,0,-0.831,0,-2.32,58,1537,0.039120740225661504,0.5
-0.878,0,-0.338,0,-0.43,-0.383,0,0,0,-1.507,7,4205,0.5093185858225127,0.4
1.503,0,0,0,0.533,0,0,0,-0.487,0.876,32,5601,0.1552975694547107,0.4
0,0,0.813,0,-0.092,0.871,0,2.097,0,-0.157,12,3759,0.5070558441227158,0.4
2.091,0.331,0.73,0,-0.344,0,1.158,0,0,1.955,11,1399,0.46329636303342603,0.1
-0.457,-0.24,0,0.062,-1.677,2.253,0,1.452,-0.3,-2.243,15,1427,0.03941345482993712,0.1
0.503,0,0,-0.375,-1.528,-0.067,0,0.101,-0.369,0.497,66,2494,0.05400497449374447,0.4
-0.915,0.545,1.883,0,-1.375,1.533,0,0,-0.659,-0.613,10,1044,0.03628005501439233,0.5
-0.931,0,0,-0.004,-2.938,0,0,0.662,0,0.394,11,1399,0.46329636303342603,0.6
0,0,0,1.141,-3.031,0,0,0,0,-0.46,12,1391,0.39244426355853396,0.1
0,0,0,0,0.509,0.329,0,0,0,1.608,1,1097,0.020172657040744786,0.1
-1.602,0,0,0,0.424,0,0,0.243,0,-0.246,3,1393,0.41634447276263925,0.4
0.915,1.291,0.725,-1.021,-0.082,0,0,-1.458,-1.987,-0.724,29,946,0.02919232365438466,0.5
1.418,-1.707,0.004,0.422,0.809,0,-0.265,0,0,-2.216,12,6253,0.12405799348835389,0.1
0.844,0,0,0,2.21,0.588,1.894,0,0,1.068,54,1020,0.026656087912567558,0.4"""

    for i in test.split("\n"):
        print(round(pi.predict(i.split(",")[:-1], False)[0], 2), i.split(",")[-1])
