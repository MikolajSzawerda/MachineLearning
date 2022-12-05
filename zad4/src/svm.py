import numpy as np
import scipy as scp
from scipy.optimize import minimize, LinearConstraint, NonlinearConstraint
import pandas as pd
from math import isclose
import joblib


# def objective_func(alpha, features, labels, kernel):
#     data = zip(alpha, features, labels)
#     return sum(
#         0.5 * sum(yi * yj * ai * aj * kernel(xi, xj) for aj, xj, yj in data) - ai
#         for ai, xi, yi in data
#     )

def objective_func(alpha, kernel_matrix):
    return 0.5*alpha[...,None]*kernel_matrix*alpha-alpha.sum()


def func_grad(alpha, features, labels, kernel):
    data = zip(alpha, features, labels)
    return np.ones_like(alpha) - 0.5*sum(ai*xi*yi for ai, xi, yi in data)


class Model:
    def __init__(self, w, b, decisive):
        self.w = w
        self.b = b
        self.decisive = decisive

    def predict(self, x):
        return self.decisive(np.dot(self.w, x)-self.b)


def support_vectors(features, alphas, labels):
    for row, a, l in zip(features, alphas, labels):
        if not isclose(a, 0.0):
            yield (row, l)


def decision(x):
    return 1 if x> 0 else -1


if __name__ == '__main__':
    C = 1.0
    df = pd.read_csv("../data/winedata.csv")
    df = df[1:50]
    N = df.shape[0]
    alpha = np.ones(N)
    features = df[df.columns[1:-1]].to_numpy()
    labels = df[df.columns[-1]].to_numpy()
    kernel = lambda u, v: np.dot(u.transpose(), v)
    labels_matrix = np.identity(labels.shape(0))*labels[..., None]
    labeled_kernel_matrix = labels_matrix*np.apply_along_axis(
        lambda xi: np.apply_along_axis(
            lambda xj: kernel(xi, xj), 0, features
        ), 0, features
    ) * labels_matrix
    result = minimize(objective_func,
                      alpha,
                      method='SLSQP',
                      args=(features, labels, kernel),
                      bounds=((0, C) for _ in range(N)),
                      # constraints=NonlinearConstraint(lambda a: np.dot(labels, a), 0.0, 0.0),
                      constraints=(
                          {'type': 'eq', 'fun': lambda a: np.dot(labels, a)}
                      )
                      )
    if result['success']:
        labels = labels[..., None]
        xw = result['x'][..., None]
        w = (labels * xw * features).sum(axis=0)
        idx = [i for i, item in enumerate(features)
               if not isclose(xw[i], 0.0)]
        b = np.median([np.abs(y-kernel(w, x))
                      for x, y in support_vectors(features, xw, labels)])
        model = Model(w, b, decision)
        joblib.dump(model, 'model.pkl', compress=1)
        print(np.dot(w, features[0])-b)
    else:
        print("Failed...")