import pandas as pd
from collections import namedtuple
from svm_dual import Stats, train as d_train
from experiments import EXPERIMENTS
from simulate import evaluate_model, ConfusionStat

FullStat = namedtuple("FullStat", Stats._fields + ConfusionStat._fields)


def cross_validation(df, **kwargs):
    N = df.shape[0] // kwargs['k']
    for i in range(kwargs['k']):
        pointA = i * N
        pointB = (i + 1) * N
        test_set = df[pointA:pointB]
        splitA = df[:pointA] if pointA > 0 else None
        splitB = df[pointB:] if pointB < df.shape[0] else None
        training_set = pd.concat([splitA, splitB])
        yield training_set, test_set


def train_models(experiments, df, results_path, **kwargs):
    results = []
    for experiment in experiments:
        model_name = experiment['model_name']
        for i, (df_train, df_test) in enumerate(cross_validation(df, **kwargs)):
            experiment['model_id'] = f'{model_name}_{str(i)}'
            model, stats = d_train(df_train, **experiment)
            confusion_stat = evaluate_model(df_test, model) if stats.success else None
            results.append(FullStat(*(stats + confusion_stat)))
    pd.DataFrame(results).to_csv(results_path)


if __name__ == '__main__':
    df = pd.read_csv('../data/winedata_mapped.csv')
    df = df[:500]
    resuts_filename = "../results/results2.csv"
    train_models(EXPERIMENTS, df, resuts_filename, **{'k': 5})
