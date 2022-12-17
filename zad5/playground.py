import matplotlib.pyplot as plt
import numpy as np
import numpy.random as npr
import pandas as pd
from tqdm import tqdm

def orig_func(x):
    return np.power(x, 2)*np.sin(x)+50*np.sin(2*x)
    # return np.power(x, 2)

def func(x):
    return 0.005*orig_func(5.0*x) + 0.5
    # return np.power(x, 2)


activation = {
    'relu': (lambda x: np.maximum(0, x), lambda x: (x > 0)*1),
    'sigmoid': (lambda x: 1/(1+np.exp(-x)), lambda x: np.exp(x)/np.power(1+np.exp(x), 2)),
    'gaussian': (lambda x: np.exp(-np.power(x, 2)), lambda x: np.multiply(-2*x, np.exp(-np.power(x, 2)))),
    'linear': (lambda x: x, lambda x: 1)
}


def init_network(topology, a_func):
    results = []
    for i, func in enumerate(a_func, 1):
        neuron = (npr.uniform(-10, 10, (topology[i], topology[i-1])),
                  npr.uniform(-10, 10, (topology[i], 1)),
                  *activation[func])
        results.append(neuron)
    return results


def predict(x, neurons):
    a = x
    for neuron in neurons:
        z = np.matmul(neuron[0], a)+neuron[1]
        a = neuron[2](z)
    return a


def train(X, Y, x_test, y_test, **kwargs):
    neurons = init_network(kwargs['topology'], kwargs['activ_func'])
    mse_rate = []
    epoch = range(kwargs['epoch'])
    batch_size = int(np.ceil(X.shape[0] / kwargs['batch_size']))
    for _ in tqdm(epoch):
        for x_batch, y_batch in zip(np.array_split(X, batch_size), np.array_split(Y, batch_size)):
            x = np.asmatrix(x_batch)
            y = np.asmatrix(y_batch)
            n = x.shape[1]
            rate = -kwargs['learning_rate']/n
            a = x
            layers = []

            for neuron in neurons:
                z = np.matmul(neuron[0], a)+neuron[1]
                a = neuron[2](z)
                layers.append((z, a))

            back_prop = zip(reversed(layers), reversed(neurons))
            (next_z, next_a), next_neuron = back_prop.__next__()
            delta = np.multiply(next_a-y, next_neuron[3](next_z))
            deltas = [delta]
            for ((z, a), neuron) in back_prop:
                delta = np.multiply(neuron[3](z), next_neuron[0].transpose().dot(delta))
                next_neuron = neuron
                deltas.append(delta)

            error_prop = zip(layers, reversed(deltas))
            prev_a = x
            errors = []
            for ((z, a), delta) in error_prop:
                error = delta.dot(prev_a.transpose())
                errors.append(error)
                prev_a = a

            update_prop = zip(neurons, reversed(deltas), errors)
            for i, ((weight, bias, f, fp), delta, error) in enumerate(update_prop):
                new_weight = weight + rate*error
                new_bias = bias + rate*np.sum(delta, 1)
                neurons[i] = (new_weight, new_bias, f, fp)

        y_predict = predict(x_test, neurons)
        mse_rate.append(np.average(np.power(y_predict-y_test, 2)))
    return mse_rate, neurons


if __name__ == '__main__':
    params = {
        'topology': (1, 5, 5, 1),
        'activ_func': ('gaussian', 'gaussian', 'linear'),
        'epoch': 5000,
        'batch_size': 1,
        'learning_rate': 0.5,
    }
    x = np.arange(-1, 1, 0.01)
    np.random.shuffle(x)
    y = np.apply_along_axis(func, 0, x)
    split_index = int(0.5 * x.shape[0])
    x_train, x_test = x[:split_index], x[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]
    mse_rate, neurons = train(x_train, y_train, np.asmatrix(x_test), np.asmatrix(y_test), **params)
    # pd.DataFrame(mse_rate).plot()
    print(neurons)
    aprox = pd.DataFrame(data=[
            x_test,
            np.asarray(predict(np.asmatrix(x_test), neurons)).reshape(-1),
            np.apply_along_axis(func, 0, x_test)
        ]
    ).transpose().sort_values(by=0)
    aprox.rename(columns={0: 'x', 1: 'y_predict', 2: 'y'}, inplace=True)
    aprox.plot('x', ['y', 'y_predict'])
    plt.show()
