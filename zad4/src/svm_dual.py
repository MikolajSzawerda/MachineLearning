import numpy as np
import scipy as scp
from scipy.optimize import minimize, LinearConstraint, NonlinearConstraint
import pandas as pd
from math import isclose
import joblib
from utils import Model, decision, preprocess
from collections import namedtuple
from time import process_time

MODEL_PATH = '../models/'
Stats = namedtuple("Stats", "success kernel kernel_param penalty_param time N model_path")


kernels = {
    'linear': lambda u, v, p: np.dot(u, v),
    'polynomial': lambda u, v, p: np.float_power((1 + np.dot(u, v)), p),
    'rbf': lambda u, v, sigma: np.exp(-(np.dot(u - v, u - v) / (2.0 * sigma ** 2)))
}


def prepare_labeled_kernel_matrix(features, labels, kernel):
    labels_matrix = np.identity(labels.shape[0]) * labels[..., None]
    kernel_matrix = np.apply_along_axis(
        lambda xi: np.apply_along_axis(
            lambda xj: kernel(xi, xj), 0, features
        ), 0, features
    )
    return np.matmul(np.matmul(labels_matrix, kernel_matrix), labels_matrix)


def objective_func(alpha, kernel_matrix):
    return 0.5 * np.dot(np.matmul(alpha, kernel_matrix), alpha) - alpha.sum()


def gradient(alpha, kernel_matrix):
    return alpha.dot(kernel_matrix)-np.ones_like(alpha)


def extract_model(result, features, labels, scaler, kernel) -> Model:
    svm_idx = np.where(result['x'] > 1e-8)
    print(len(svm_idx))
    svm_matrix = np.c_[result['x'][svm_idx], labels[svm_idx], features[svm_idx]]
    w = np.apply_along_axis(lambda x: x[0] * x[1] * x[2:], 1, svm_matrix).sum(axis=0)
    b = np.median(
        np.apply_along_axis(lambda row: np.abs(row[1] - kernel(w, row[2:])), 1, svm_matrix)
    )
    return Model(w, b, decision, scaler)


def train(df, **kwargs):
    start = process_time()
    kernel = lambda u, v: kernels[kwargs['kernel']](u, v, kwargs['kernel_param'])
    N = df.shape[0]
    alpha = np.full(N, min(1.0, 0.5 * kwargs['C']))
    features, scaler = preprocess(df[df.columns[1:-1]])
    features = features.to_numpy()
    labels = df[df.columns[-1]].to_numpy()
    labeled_kernel_matrix = prepare_labeled_kernel_matrix(features.transpose(), labels, kernel)
    result = minimize(lambda a: objective_func(a, labeled_kernel_matrix),
                      alpha,
                      method='SLSQP',
                      jac=lambda a: gradient(a, labeled_kernel_matrix),
                      # args=labeled_kernel_matrix,
                      bounds=((0, kwargs['C']) for _ in range(N)),
                      constraints=(
                          {'type': 'eq', 'fun': lambda a: np.dot(labels, a)}
                      ),
                      options={'maxiter': 5000, 'disp': True}
                      )
    if result['success']:
        print(f"{kwargs['model_name']} succeed!")
        model = extract_model(result, features, labels, scaler, kernel)
        end = process_time()
        filename = f'{MODEL_PATH}{kwargs["model_name"]}.pkl'
        joblib.dump(model, filename, compress=1)
    else:
        print(f"{kwargs['model_name']} failed...")
        filename = None
        end = process_time()
    return Stats(result['success'], kwargs['kernel'],
                 kwargs['kernel_param'], kwargs['C'],
                 end-start, N, filename)
