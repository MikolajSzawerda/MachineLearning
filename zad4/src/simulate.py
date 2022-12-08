from utils import Model, decision
from collections import namedtuple

ConfusionStat = namedtuple("ConfusionStat", "TP TN FP FN")


def evaluate_model(df_test, model: Model):
    results = {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0}
    for row in df_test.iterrows():
        row = row[1]
        features = row[1:-1]
        label = row[-1]
        prediction = model.predict(features)
        label_1 = 'T' if label == prediction else 'F'
        label_2 = 'P' if label == 1 else 'N'
        results[label_1 + label_2] += 1
    print((results['TP'] + results['TN']) / sum(results.values()))
    return ConfusionStat(**results)
