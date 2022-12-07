import numpy as np
import scipy as scp
from scipy.optimize import minimize, LinearConstraint, NonlinearConstraint
import pandas as pd
from math import isclose
import joblib
from utils import Model, decision, preprocess
from collections import namedtuple
from time import process_time
from svm_dual import Stats, train
from experiments import EXPERIMENTS
from simulate import evaluate_model, ConfusionStat


def train_models(experiments, df, results_path):
    results = []
    for experiment in experiments:
        results.append(train(df_train, **experiment))
    pd.DataFrame(results).to_csv(results_path)


def evaluate_models(results_path, end_path):
    df = pd.read_csv(results_path)
    results = []
    for filename in df['model_path']:
        if filename != "":
            model = joblib.load(filename)
            results.append(evaluate_model(df_train, model))
        else:
            results.append(ConfusionStat(0, 0, 0, 0))
    confusion_df = pd.DataFrame(results)
    pd.concat([df, confusion_df], join='inner', axis=1).to_csv(end_path)


if __name__ == '__main__':
    df = pd.read_csv('../data/winedata-white_mapped.csv')
    df_train = df[3000:]
    df = df[:500]
    resuts_filename = "../results/results.csv"
    end_filename = "../results/enriched_results.csv"
    train_models(EXPERIMENTS, df, resuts_filename)
    evaluate_models(resuts_filename, end_filename)
