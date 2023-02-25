import pandas as pd
import numpy as np
from scipy.stats import norm
from functools import partial
import time


def get_gaussian_training_matrix(data: pd.DataFrame):
    means = data.groupby(['class']).mean()
    stds = data.groupby(['class']).std()
    labels = means.index.values
    return pd.DataFrame({
        col: zip(means[col], stds[col]) for col in means.columns
    }).applymap(lambda x: partial(norm.pdf, loc=x[0], scale=x[1])), labels


def train(train_data: pd.DataFrame, test_data: pd.DataFrame):
    class_prob = (train_data['class'].value_counts() / len(train_data)).to_numpy()
    gaussian_matrix, class_labels = get_gaussian_training_matrix(train_data)

    result = test_data \
        .apply(lambda row: gaussian_matrix.apply(lambda funcs: np.prod([f(x) for f, x in zip(funcs, row)]), axis=1),
               axis=1) \
        .apply(lambda row: pd.Series(np.multiply(row.to_numpy(), class_prob)), axis=1)

    labels = test_data.loc[:, 'class']
    result.columns = class_labels
    result['predicted_label'] = result.apply(lambda x: class_labels[np.argmax(x)], axis=1)
    result['true_label'] = labels
    return result


if __name__ == '__main__':
    data = pd.read_csv("iris.data")
    dfs = []
    for train_frac in np.arange(0.1, 1.0, 0.1):
        start = time.process_time()
        train_data = data.sample(frac=train_frac, random_state=2137)
        test_data = data.drop(train_data.index)
        result = train(train_data, test_data)
        result_data = pd.DataFrame(result.groupby(['true_label', 'predicted_label']).size())
        end = time.process_time()
        result_data['train_len'] = len(train_data)
        result_data['test_len'] = len(test_data)
        result_data['time'] = end - start
        dfs.append(result_data)
    pd.concat(dfs).to_csv(f"results.csv", header=['value', 'train_len', 'test_len', 'time'])
