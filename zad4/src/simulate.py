import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, Normalizer
from utils import Model, decision
from collections import namedtuple

ConfusionStat = namedtuple("ConfusionStat", "TP TN FP FN")


def evaluate_model(df_test, model: Model):
    features = df_test[df_test.columns[1:-1]].to_numpy()
    labels = df_test[df_test.columns[-1]].to_numpy()
    results = {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0}
    for x, label in zip(features, labels):
        prediction = model.predict(x)
        label_1 = 'T' if label == prediction else 'F'
        label_2 = 'P' if label == 1 else 'N'
        results[label_1+label_2] += 1
    print((results['TP']+results['TN'])/sum(results.values()))
    return ConfusionStat(**results)


if __name__ == '__main__':
    model = joblib.load("../models/linear_01.pkl")
    df_test = pd.read_csv("../data/winedata-white_mapped.csv")[2000:]
    stats = evaluate_model(df_test, model)
    print(stats)
    print((stats[0]+stats[1])/sum(stats))
    # model = joblib.load("model.pkl")
    # df_test = pd.read_csv("../data/winedata.csv")[1000:5000]
    # df = df[df.columns[2:4]]
    # features = df_test[df_test.columns[1:-1]].to_numpy()
    # labels = df_test[df_test.columns[-1]].to_numpy()
    # results = []
    # good = 0
    # for row, label in zip(features, labels):
    #     prediction = model.predict(row)
    #     if prediction == label:
    #         good += 1
    #     results.append((label, prediction))
    #
    # print(good/len(results))