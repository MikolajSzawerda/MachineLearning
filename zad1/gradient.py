from math import isclose, isinf, isnan
from random import random
from autograd import elementwise_grad as egrad
import autograd.numpy as np
from matplotlib import pyplot as plt
import concurrent.futures
from random import random, uniform
from plotter import plot_path
from utils import Conductor, Listener, ParametrizedFunction, DataPoint
from functions import *
from multiprocessing import Manager


def gradient(func, x: tuple):
    return np.array([deriv(*x) for deriv in (egrad(func, i) for i in range(len(x)))])


def differentiate(func, n):
    return [deriv for deriv in (egrad(func, i) for i in range(n))]


def calculateGradient(gradient, x):
    return np.array([func(*x) for func in gradient])


def calculate_step_bound(func, x):
    n = len(x)
    derivs = np.array([calculateGradient(differentiate(f, n), x) for f in differentiate(func, n)])
    values, vectors = np.linalg.eig(derivs)
    max_eigen = max(values)
    return abs(1/max_eigen) if not isclose(max_eigen, 0.0, abs_tol=1e-9)  else random()


def validate_number(number):
    return not (isnan(number) or isinf(number))


# def solver(func, x0, step=0.6, iterations = 100):
#     listener = Listener(step)
#     traversing_point = x0
#     iteration_count = 1
#     optimaized_value = func(*x0)
#     gradient = differentiate(func, len(x0))
#     while iteration_count <= iterations and validate_number(optimaized_value):
#         listener.pushLog(DataPoint(iteration_count, traversing_point, optimaized_value))
#         traversing_point = traversing_point - np.dot(step, calculateGradient(gradient, traversing_point))
#         optimaized_value = func(*traversing_point)
#         iteration_count += 1
#     listener.saveResult(optimaized_value)
#     return listener


# def optimize(func, domain:"list[tuple]", x0=None):
#     num_of_steps = 10
#     vector = [uniform(a, b) for a,b in domain] if x0 is None else x0
#     step_bound = calculate_step_bound(func, vector)
#     min_step = step_bound/num_of_steps
#     steps = np.arange(min_step, step_bound, min_step)
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         conductor = Conductor()
#         requests = [executor.submit(solver, func, vector, step, 1000) for step in steps]
#         for job in concurrent.futures.as_completed(requests):
#             conductor.appendListener(job.result())
#     return conductor

def backtrack_search(x, func, gradient):
    alpha = 0.15
    beta = 0.5
    param = 1
    gradient_value = calculateGradient(gradient, x)
    arg = x - np.dot(param, gradient_value)
    change = alpha*param*np.linalg.norm(gradient_value)**2
    while func(*arg) > func(*x)-change:
        param *= beta
        gradient_value = calculateGradient(gradient, x)
        arg = x - np.dot(param, gradient_value)
        change = alpha*param*np.linalg.norm(gradient_value)**2
    return param

def solver(func, x0, step_strategy, iterations = 100):
    listener = Listener("backtrack search")
    traversing_point = x0
    iteration_count = 1
    optimaized_value = func(*x0)
    gradient = differentiate(func, len(x0))
    gradient_value = calculateGradient(gradient, traversing_point)
    while iteration_count <= iterations and validate_number(optimaized_value) and np.linalg.norm(gradient_value) > 1e-5:
        listener.pushLog(DataPoint(iteration_count, traversing_point, optimaized_value))
        step = step_strategy(traversing_point, func, gradient)
        gradient_value = calculateGradient(gradient, traversing_point)
        traversing_point = traversing_point - np.dot(step, gradient_value)
        optimaized_value = func(*traversing_point)
        iteration_count += 1
    listener.saveResult(optimaized_value)
    return listener


def optimize(func, domain:"list[tuple]", num_of_points=10, x0=None):
    points = [[uniform(a, b) for a,b in domain] for _ in range(num_of_points)] if x0 is None else [x0]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        conductor = Conductor()
        requests = [executor.submit(solver, func, point, backtrack_search, 1000) for point in points]
        for job in concurrent.futures.as_completed(requests):
            conductor.appendListener(job.result())
    return conductor


if __name__ == "__main__":
    for param in [100]:
        func = ParametrizedFunction(example_function, param).getFunc()
        conductor = optimize(func, [(-100, 100) for _ in range(10)])
        print(list(conductor.listeners.values())[0].result)
        conductor.dump(f"results/results_{param}.json")
        conductor.plot(f"results/plot_{param}.png")
    # conductor = optimize(crazy_function, [(-5.0, 5.0) for _ in range(2)], num_of_points=10, x0=[0.0, -1.0])
    # conductor.plot("conv.png")
    # best_listener = min(conductor.listeners.values(), key=lambda x: x.result)
    # print(best_listener.result)
    # plot_path(crazy_function, best_listener)
    # conductor.dump()
