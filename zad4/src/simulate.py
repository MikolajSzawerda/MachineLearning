import joblib
import numpy as np
import pandas as pd


class Model:
    def __init__(self, w, b, decisive):
        self.w = w
        self.b = b
        self.decisive = decisive

    def predict(self, x):
        return self.decisive(np.dot(self.w, x)-self.b)


def decision(x):
    return 1 if x > 0 else -1


if __name__ == '__main__':
    model = joblib.load("model.pkl")
    df = pd.read_csv("../data/winedata.csv")[1000:2000]
    features = df[df.columns[1:-1]].to_numpy()
    labels = df[df.columns[-1]].to_numpy()
    results = []
    good = 0
    for row, label in zip(features, labels):
        prediction = model.predict(row)
        if prediction == label:
            good += 1
        results.append((label, prediction))

    print(good/len(results))