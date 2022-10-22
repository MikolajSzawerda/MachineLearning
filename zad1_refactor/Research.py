from math import log
from Messenger import Messenger
from Plotter import Plotter
from GradientDescent import RandomFixedStepGradient, BacktrackStepGradient
from Functions import *
import time
from utils import message

def conduct_example_experiment():
    plotter = Plotter()
    domain = [[-100, 100] for _ in range(10)]
    x0 = [100.0 for _ in range(10)]
    for param, lb, ub in [(10, 0.001, 0.01)]:
        func = ParametrizedFunction(example_function, param).getFunc()
        start = time.perf_counter()
        experiment = RandomFixedStepGradient(lb, ub, 1000, num_of_steps=10).solver(func, domain, x0)
        end = time.perf_counter()
        message(experiment, end-start)
        print(str(param)+": "+experiment.best_recorder.label)


def compare_step_strategies():
    plotter = Plotter()
    domain = [[-100, 100] for _ in range(10)]
    x0 = [100.0 for _ in range(10)]
    for param in [(1, 0.1, 1.0), (10, 0.01, 0.001), (100, 0.001, 0.01)]:
        # func = ParametrizedFunction(example_function, param[0]).getFunc()
        func = exp_function
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


def conduct_algorithms_comparison():
    path = "results/one_run"
    plotter = Plotter(path)
    domain = [[-100, 100] for _ in range(10)]
    x0 = [100.0 for _ in range(10)]
    for param, step in [(1, 0.5), (10, 0.097), (100, 0.009)]:
        messenger = Messenger(path)
        func = ParametrizedFunction(example_function, param).getFunc()
        start = time.perf_counter()
        fixedStep = RandomFixedStepGradient(0.001, 0.01, 1000, num_of_steps=1, num_of_points=1).solve(func, x0, step)
        end = time.perf_counter()
        messenger.pushMessage(message(fixedStep, end-start, "Fixed step")).printLast()
        start = time.perf_counter()
        backtrackStep = BacktrackStepGradient(1000, num_of_points=1).solve(func, x0)
        end = time.perf_counter()
        messenger.pushMessage(message(backtrackStep, end-start, "Backtrack step")).printLast()
        plotter.plot_recorder(fixedStep, "Fixed step "+str(param))
        plotter.plot_recorder(backtrackStep, "Backtrack step "+str(param))
        messenger.dump("times_"+str(param)+".png")


def conduct_algorithms_full_run():
    path = "results/full_run"
    plotter = Plotter(path)
    domain = [[-100, 100] for _ in range(10)]
    for param, lb, ub in [(1, 0.1, 1.0), (10, 0.01, 0.1), (100, 0.001, 0.01)]:
        messenger = Messenger(path)
        func = ParametrizedFunction(example_function, param).getFunc()
        start = time.perf_counter()
        fixedStep = RandomFixedStepGradient(lb, ub, 1000, num_of_steps=5, num_of_points=4).solver(func, domain)
        end = time.perf_counter()
        messenger.pushMessage(message(fixedStep, end-start)).printLast()
        start = time.perf_counter()
        backtrackStep = BacktrackStepGradient(1000, num_of_points=20).solver(func, domain)
        end = time.perf_counter()
        messenger.pushMessage(message(backtrackStep, end-start)).printLast()
        plotter.plot(fixedStep, "Fixed step "+str(param))
        plotter.plot(backtrackStep, "Backtrack step "+str(param))
        messenger.dump("times_"+str(param)+".png")


def conduct_algorithms_2D():
    path = "results/2d_run"
    plotter = Plotter(path)
    messenger = Messenger(path)
    domain = [[-3, 3] for _ in range(2)]
    func = exp_function
    start = time.perf_counter()
    fixedStep = RandomFixedStepGradient(0.1, 1.0, 1000, num_of_steps=5, num_of_points=50).solver(func, domain)
    end = time.perf_counter()
    messenger.pushMessage(message(fixedStep, end-start)).printLast()
    start = time.perf_counter()
    backtrackStep = BacktrackStepGradient(1000, num_of_points=50).solver(func, domain)
    end = time.perf_counter()
    messenger.pushMessage(message(backtrackStep, end-start)).printLast()
    plotter.plot(fixedStep, "Fixed step ", percentage=0.05)
    plotter.plot(backtrackStep, "Backtrack step ", percentage=0.20)
    plotter.plot_paths(fixedStep, domain, "Fixed step contour", 0.1)
    plotter.plot_paths(backtrackStep, domain, "Backtrack step contour", 0.20)
    messenger.dump("times.png")



if __name__ == "__main__":
    conduct_algorithms_comparison()
    conduct_algorithms_full_run()
    conduct_algorithms_2D()