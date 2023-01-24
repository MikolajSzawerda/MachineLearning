import pandas as pd
import numpy as np
from scipy.stats import norm
from functools import partial


def get_gaussian_training_matrix(data: pd.DataFrame):
    means = data.groupby(['class']).mean()
    stds = data.groupby(['class']).std()
    return pd.DataFrame({
        col: zip(means[col], stds[col]) for col in means.columns
    }).applymap(lambda x: partial(norm.pdf, loc=x[0], scale=x[1]))


def train(data: pd.DataFrame):
    labels = data.loc[:, 'class']
    class_labels = labels.unique()
    gaussian_matrix = get_gaussian_training_matrix(data)
    result = data \
        .apply(lambda row: gaussian_matrix.apply(lambda funcs: np.prod([f(x) for f, x in zip(funcs, row)]), axis=1), axis=1) \
        .apply(lambda row: pd.Series(np.multiply(row.to_numpy(), class_prob)), axis=1)
    result.columns = class_labels
    result['predicted_label'] = result.apply(lambda x: class_labels[np.argmax(x)], axis=1)
    result['true_label'] = labels
    return result


if __name__ == '__main__':
    data = pd.read_csv("iris.data")
    labels = data.loc[:, 'class']
    means = data.groupby(['class']).mean()
    stds = data.groupby(['class']).std()
    class_prob = (data['class'].value_counts() / len(data)).to_numpy()
    df = pd.DataFrame({
        col: zip(means[col], stds[col]) for col in means.columns
    }).applymap(lambda x: partial(norm.pdf, loc=x[0], scale=x[1]))
    class_labels = means.index.values
    b = data\
        .apply(lambda row: df.apply(lambda funcs: np.prod([f(x) for f, x in zip(funcs, row)]), axis=1), axis=1)\
        .apply(lambda row: pd.Series(np.multiply(row.to_numpy(), class_prob)), axis=1)
    b.columns = class_labels
    b['predicted_label'] = b.apply(lambda x: class_labels[np.argmax(x)], axis=1)
    b['true_label'] = labels
    oc = b.groupby(['true_label', 'predicted_label']).size()

    pass
