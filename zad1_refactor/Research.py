from Plotter import Plotter
from GradientDescent import RandomFixedStepGradient, BacktrackStepGradient
from Functions import *
import time
from utils import message


def conduct_example_experiment():
    plotter = Plotter()
    domain = [[-100, 100] for _ in range(10)]
    func = ParametrizedFunction(example_function, 100).getFunc()
    start = time.process_time()
    experiment = RandomFixedStepGradient(0.001, 0.01, 1000, num_of_steps=10).solver(func, domain)
    end = time.process_time()
    plotter.plot(experiment)
    message(experiment, end-start)


def compare_step_strategies():
    plotter = Plotter()
    domain = [[-100, 100] for _ in range(10)]
    x0 = [100.0 for _ in range(10)]
    func = ParametrizedFunction(example_function, 100).getFunc()
    start = time.perf_counter()
    fixedStep = RandomFixedStepGradient(0.001, 0.01, 1000, num_of_points=1, num_of_steps=10).solver(func, domain, x0)
    end = time.perf_counter()
    message(fixedStep, end-start)
    start = time.perf_counter()
    backtrackStep = BacktrackStepGradient(1000, num_of_points=1).solver(func, domain, x0)
    end = time.perf_counter()
    message(backtrackStep, end-start)
    plotter.comparison_plot(fixedStep, backtrackStep)


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
    compare_step_strategies_exponential_func()