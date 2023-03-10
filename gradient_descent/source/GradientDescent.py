from abc import ABC, abstractmethod
from source.gradient import differentiate
import autograd.numpy as np
from math import isnan, isinf
import concurrent.futures
from source.Experiment import Experiment, Recorder, DataPoint
from source.constants import (CONVERGENCE_EPSILON, CONVERGENCE_TEST, GRADIENT_EPSILON,
                       BACKTRACK_ALPHA, BACKTRACK_BETA, BACKTRACK_START)


class ABCGradient(ABC):

    def __init__(self, lower_bound, upper_boud, max_iterations, num_of_points = 10, num_of_steps = 10, label=""):
        self.step_lower_bound = lower_bound
        self.step_upper_bound = upper_boud
        self.max_iterations = max_iterations
        self.num_of_steps = num_of_steps
        self.num_of_points = num_of_points
        self.label = label

    def generate_steps(self, n=1):
        return np.random.uniform(self.step_lower_bound, self.step_upper_bound, n)

    def generate_points(self, domain):
        matrix = [np.random.uniform(x[0], x[1], self.num_of_points) for x in domain]
        return np.rot90(matrix)

    @abstractmethod
    def solver(self, func, *args):
        pass

    @abstractmethod
    def solve(self, func, x0):
        pass

    @abstractmethod
    def stop_condition(self, *args):
        pass

    def validate_number(self, number):
        return not (isnan(number) or isinf(number))

    def has_converged(self, values):
        if len(values) <= 1: return False
        return abs(min(values)-max(values))<=CONVERGENCE_EPSILON


class RandomFixedStepGradient(ABCGradient):

    def __init__(self, lower_bound, upper_boud, max_iterations, num_of_points = 10, num_of_steps = 10, label="Random fixed step"):
        super().__init__(lower_bound, upper_boud, max_iterations, num_of_points, num_of_steps)
        self.label = label

    def _process_many_steps(self, func, x0, steps):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            jobs = [executor.submit(self.solve, func, x0, step) for step in steps]
            experiment = Experiment(func, self.label)
            for job in concurrent.futures.as_completed(jobs):
                experiment.appendRecorder(job.result())
            return experiment

    def _iterate_steps(self, func, point, steps):
        results = []
        for step in steps:
            results.append(self.solve(func, point, step))
        return results

    def _process_many_points(self, func, points, steps):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            experiment = Experiment(func, self.label)
            jobs = [executor.submit(self._iterate_steps, func, point, steps) for point in points]
            for job in concurrent.futures.as_completed(jobs):
                for recorder in job.result():
                    experiment.appendRecorder(recorder)
            return experiment

    def solver(self, func, domain, x0=None) -> "Experiment":
        steps = self.generate_steps(self.num_of_steps)
        points = self.generate_points(domain) if x0 is None else [x0]
        if self.num_of_points == 1:
            return self._process_many_steps(func, points[0], steps)
        return self._process_many_points(func, points, steps)

    def solve(self, func, x0, step) -> "Recorder":
        traversing_point = x0
        iteration_count = 1
        optimized_value = func(x0)
        gradient = differentiate(func)
        recorder = Recorder(str(round(step, 4))+" "+str(round(np.linalg.norm(x0), 2)))
        recorder.pushLog(DataPoint(iteration_count, traversing_point, optimized_value))
        while self.stop_condition(iteration_count, optimized_value, recorder):
            traversing_point = traversing_point - np.dot(step, gradient(traversing_point))
            optimized_value = func(traversing_point)
            iteration_count += 1
            recorder.pushLog(DataPoint(iteration_count, traversing_point, optimized_value))
        recorder.saveResult(optimized_value)
        return recorder

    def stop_condition(self, iteration_count, optimized_value, recorder: "Recorder"):
        return self.validate_number(optimized_value) and not self.has_converged(recorder.getLastValues(CONVERGENCE_TEST)) and iteration_count <= self.max_iterations


class BacktrackStepGradient(ABCGradient):

    def __init__(self, max_iterations, num_of_points=10, label="Backtrack dynamic step"):
        super().__init__(0.0, 1.0, max_iterations, num_of_points, 1)
        self.label = label

    def _process_many_points(self, func, points):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            experiment = Experiment(func, self.label)
            jobs = [executor.submit(self.solve, func, point) for point in points]
            for job in concurrent.futures.as_completed(jobs):
                experiment.appendRecorder(job.result())
            return experiment

    def solver(self, func, domain, x0=None) -> "Experiment":
        points = self.generate_points(domain) if x0 is None else [x0]
        return self._process_many_points(func, points)

    def backtrack_search(self, x, func, gradient):
        alpha = BACKTRACK_ALPHA
        beta = BACKTRACK_BETA
        param = BACKTRACK_START
        gradient_value = gradient(x)
        arg = x - np.dot(param, gradient_value)
        change = alpha*param*np.linalg.norm(gradient_value)**2
        while func(arg) > func(x)-change:
            param *= beta
            gradient_value = gradient(x)
            arg = x - np.dot(param, gradient_value)
            change = alpha*param*np.linalg.norm(gradient_value)**2
        return param

    def solve(self, func, x0) -> "Recorder":
        traversing_point = x0
        iteration_count = 1
        optimized_value = func(x0)
        gradient = differentiate(func)
        gradient_value = gradient(traversing_point)
        recorder = Recorder(str(np.linalg.norm(x0)))
        recorder.pushLog(DataPoint(iteration_count, traversing_point, optimized_value))
        while self.stop_condition(iteration_count, optimized_value, gradient_value):
            step = self.backtrack_search(traversing_point, func, gradient)
            gradient_value = gradient(traversing_point)
            traversing_point = traversing_point - np.dot(step, gradient_value)
            optimized_value = func(traversing_point)
            iteration_count += 1
            recorder.pushLog(DataPoint(iteration_count, traversing_point, optimized_value))
        recorder.saveResult(optimized_value)
        return recorder

    def stop_condition(self, iteration_count, optimized_value, gradient_value):
        return self.validate_number(optimized_value) and np.linalg.norm(gradient_value) > GRADIENT_EPSILON and iteration_count <= self.max_iterations
