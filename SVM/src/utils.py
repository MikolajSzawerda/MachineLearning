import numpy as np
from sklearn.preprocessing import StandardScaler, Normalizer
import pandas as pd
from collections import namedtuple

Stats = namedtuple("Stats", "success kernel kernel_param penalty_param time N model_path model_name")


class Model:
    def __init__(self, w, b, decisive, scaler):
        self.w = w
        self.b = b
        self.decisive = decisive
        self.scaler = scaler

    def predict(self, x):
        x = self.scaler.transform(x.to_numpy().reshape(1, -1)).reshape(-1)
        return self.decisive(np.dot(self.w, x) + self.b)


def decision(x):
    return 1 if x > 0 else -1


def preprocess(features):
    scaler = StandardScaler()
    scaler.fit(features)
    return pd.DataFrame(scaler.transform(features), columns=features.columns,
                        index=features.index), scaler
