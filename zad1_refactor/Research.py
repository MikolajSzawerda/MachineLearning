from math import log
from Plotter import Plotter
from GradientDescent import RandomFixedStepGradient, BacktrackStepGradient
from Functions import *
import time
from utils import message


def conduct_example_experiment():
    plotter = Plotter()
    domain = [[-100, 100] for _ in range(10)]
    func = ParametrizedFunction(example_function, 10).getFunc()
    start = time.perf_counter()
    experiment = RandomFixedStepGradient(0.001, 0.01, 1000, num_of_steps=10).solver(func, domain)
    end = time.perf_counter()
    plotter.plot(experiment)
    message(experiment, end-start)


def compare_step_strategies():
    plotter = Plotter()
    domain = [[-100, 100] for _ in range(10)]
    x0 = [100.0 for _ in range(10)]
    for param in [(1, 0.1, 1.0), (10, 0.01, 0.001), (100, 0.001, 0.01)]:
        func = ParametrizedFunction(example_function, param[0]).getFunc()
        start = time.perf_counter()
        fixedStep = RandomFixedStepGradient(param[1], param[2], 1000, num_of_points=1, num_of_steps=10, label="Random fixed step "+str(param[0])).solver(func, domain)
        end = time.perf_counter()
        message(fixedStep, end-start)
        start = time.perf_counter()
        backtrackStep = BacktrackStepGradient(1000, num_of_points=10, label="Backtrack step "+str(param[0])).solver(func, domain)
        end = time.perf_counter()
        message(backtrackStep, end-start)
        plotter.plot(fixedStep)
        plotter.plot(backtrackStep)
        # plotter.comparison_plot(fixedStep, backtrackStep)


def compare_step_strategies_exponential_func():
    plotter = Plotter()
    domain = [[-1, 1] for _ in range(2)]
    func = exp_function
    start = time.perf_counter()
    fixedStep = RandomFixedStepGradient(0.1, 1.0, 1000, num_of_points=10, num_of_steps=10).solver(func, domain)
    end = time.perf_counter()
    message(fixedStep, end-start)
    start = time.perf_counter()
    backtrackStep = BacktrackStepGradient(1000, num_of_points=10).solver(func, domain)
    end = time.perf_counter()
    message(backtrackStep, end-start)
    plotter.comparison_plot(fixedStep, backtrackStep)
    plotter.plot_path(fixedStep.best_recorder, func)


if __name__ == "__main__":
    compare_step_strategies()