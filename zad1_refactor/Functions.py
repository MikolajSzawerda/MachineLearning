import autograd.numpy as np


class ParametrizedFunction:
    def __init__(self, function, alpha):
        self.alpha = alpha
        self.function = function

    def _func(self, *X):
        return self.function(self.alpha, *X)

    def getFunc(self):
        return self._func


def quadratic(x):
    return x[0]**2+x[1]**2


def bell_function(x):
    return np.exp(-(x[0]**2+x[1]**2))


def exp_function(x):
    return (1 - x[0]**2 + x[1]**3)*np.exp(-(x[0]**2 + x[1]**2))


def example_function(alpha, x):
    n = len(x)
    return sum([alpha**((i-1)/n) * x_i**2 for i,x_i in enumerate(x, 1)])