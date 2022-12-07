import numpy as np
from scipy.optimize import minimize
import pandas as pd
import joblib
from utils import Model, decision, preprocess
from collections import namedtuple
from time import process_time

MODEL_PATH = '../models/'
Stats = namedtuple("Stats", "success kernel kernel_param penalty_param time N model_path")


def linear_func(vector, df, c):
    w = vector[:-1]
    return 0.5 * w.dot(w) + c * np.apply_along_axis(
        lambda x: max(0, 1 - x[-1] * (w.dot(x[:-1]) + vector[-1])), 1, df
    ).sum()


def linear(df, **kwargs):
    start = process_time()
    N = df.shape[0]
    vector = np.ones(df.shape[1] - 1)
    features, scaler = preprocess(df[df.columns[1:-1]])
    labels = df[df.columns[-1]]
    features['labels'] = labels
    features = features.to_numpy()
    result = minimize(lambda a: linear_func(a, features, kwargs['C']),
                      vector,
                      method='SLSQP',
                      options={'maxiter': 500, 'disp': True}
                      )
    if result['success']:
        print(f"{kwargs['model_name']} succeed!")
        model = Model(result.x[:-1], result.x[-1], decision, scaler)
        end = process_time()
        filename = f'{MODEL_PATH}{kwargs["model_name"]}.pkl'
        joblib.dump(model, filename, compress=1)
    else:
        print(f"{kwargs['model_name']} failed...")
        filename = None
        end = process_time()
    return Stats(result['success'], kwargs['kernel'],
                 kwargs['kernel_param'], kwargs['C'],
                 end - start, N, filename)


if __name__ == '__main__':
    C = 10.0
    param = 2
    df = pd.read_csv("../data/winedata-red_mapped.csv")
    df = df[:2000]
    linear(df, **{
        'C': 0.5,
        'kernel': 'linear',
        'kernel_param': None,
        'model_name': 'linear_01'
    })
