from source.Messenger import Messenger
from source.Plotter import Plotter
from source.GradientDescent import RandomFixedStepGradient, BacktrackStepGradient
from source.Functions import example_function, exp_function, ParametrizedFunction
import time
from source.utils import message
from source.constants import MAX_ITERATION


def conduct_algorithms_comparison():
    path = "results/one_run"
    plotter = Plotter(path)
    x0 = [100.0 for _ in range(10)]
    for param, step in [(1, 0.5), (10, 0.097), (100, 0.009)]:
        messenger = Messenger(path)
        func = ParametrizedFunction(example_function, param).getFunc()

        start = time.perf_counter()
        fixedStep = RandomFixedStepGradient(0.001, 0.01, MAX_ITERATION, num_of_steps=1, num_of_points=1).solve(func, x0, step)
        end = time.perf_counter()
        messenger.pushMessage(message(fixedStep, end-start, "Fixed step")).printLast()

        start = time.perf_counter()
        backtrackStep = BacktrackStepGradient(MAX_ITERATION, num_of_points=1).solve(func, x0)
        end = time.perf_counter()
        messenger.pushMessage(message(backtrackStep, end-start, "Backtrack step")).printLast()

        badStep = RandomFixedStepGradient(0.001, 0.01, MAX_ITERATION, num_of_steps=1, num_of_points=1).solve(func, x0, 1.4*step)

        plotter.plot_recorder(fixedStep, "Fixed step "+str(param))
        plotter.plot_recorder(backtrackStep, "Backtrack step "+str(param))
        plotter.plot_recorder(badStep, "Bad Fixed step "+str(param))
        messenger.dump("times_"+str(param)+".png")


def conduct_algorithms_full_run():
    path = "results/full_run"
    plotter = Plotter(path)
    domain = [[-100, 100] for _ in range(10)]
    for param, lb, ub in [(1, 0.1, 1.0), (10, 0.01, 0.1), (100, 0.001, 0.01)]:
        messenger = Messenger(path)
        func = ParametrizedFunction(example_function, param).getFunc()

        start = time.perf_counter()
        fixedStep = RandomFixedStepGradient(lb, ub, MAX_ITERATION, num_of_steps=5, num_of_points=4).solver(func, domain)
        end = time.perf_counter()
        messenger.pushMessage(message(fixedStep, end-start)).printLast()

        start = time.perf_counter()
        backtrackStep = BacktrackStepGradient(MAX_ITERATION, num_of_points=20).solver(func, domain)
        end = time.perf_counter()
        messenger.pushMessage(message(backtrackStep, end-start)).printLast()

        plotter.plot(fixedStep, "Fixed step "+str(param))
        plotter.plot(backtrackStep, "Backtrack step "+str(param))
        messenger.dump("times_"+str(param)+".png")


def conduct_algorithms_2D():
    path = "results/2d_run"
    plotter = Plotter(path)
    messenger = Messenger(path)
    domain = [[-5, 5] for _ in range(2)]
    func = exp_function

    start = time.perf_counter()
    fixedStep = RandomFixedStepGradient(0.5, 1.5, MAX_ITERATION, num_of_steps=5, num_of_points=4).solver(func, domain)
    end = time.perf_counter()
    messenger.pushMessage(message(fixedStep, end-start)).printLast()

    start = time.perf_counter()
    backtrackStep = BacktrackStepGradient(MAX_ITERATION, num_of_points=20).solver(func, domain)
    end = time.perf_counter()
    messenger.pushMessage(message(backtrackStep, end-start)).printLast()

    plotter.plot(fixedStep, "Fixed step ", scale="linear")
    plotter.plot(backtrackStep, "Backtrack step ", scale="linear")
    plotter.plot_paths(fixedStep, domain, "Fixed step contour")
    plotter.plot_paths(backtrackStep, domain, "Backtrack step contour")
    messenger.dump("times.png")


if __name__ == "__main__":
    conduct_algorithms_comparison()
    conduct_algorithms_full_run()
    conduct_algorithms_2D()
