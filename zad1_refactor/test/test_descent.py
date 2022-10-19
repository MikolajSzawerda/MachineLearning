from GradientDescent import BacktrackStepGradient, RandomFixedStepGradient
import autograd.numpy as np
import pytest


def test_random_fixed_step_gradient_solve():
    func = lambda x: x[0]**2 + x[1]**2
    x0 = np.array([1.0, 1.0])
    stepGradient = RandomFixedStepGradient(0.01, 1.1, 1000)
    recorder = stepGradient.solve(func, x0, 0.5)
    assert recorder.result == pytest.approx(0.0, 0.000001)
    assert len(recorder.logs) > 0


def test_backtrack_step_gradient_solve():
    func = lambda x: x[0]**2 + x[1]**2
    x0 = np.array([1.0, 1.0])
    stepGradient = BacktrackStepGradient(1000)
    recorder = stepGradient.solve(func, x0)
    assert recorder.result == pytest.approx(0.0, 0.000001)
    assert len(recorder.logs) > 0



def generate_steps(x, y):
        return np.arange(0.1, 1.0, 0.1)


def generate_points(x, y):
        return [[1.0, 1.0], [2.0, 2.0]]


def func(x):
    return x[0]**2 + x[1]**2


def test_random_fixed_step_gradient_many_points(monkeypatch):
    stepGradient = RandomFixedStepGradient(0.01, 1.1, 10)
    monkeypatch.setattr("GradientDescent.RandomFixedStepGradient.generate_steps", generate_steps)
    monkeypatch.setattr("GradientDescent.RandomFixedStepGradient.generate_points", generate_points)
    experiment = stepGradient.solver(func, [[-10, 10], [-10, 10]])
    assert len(experiment.recorders) > 0


def test_random_fixed_step_gradient_many_steps(monkeypatch):
    x0 = np.array([1.0, 1.0])
    stepGradient = RandomFixedStepGradient(0.01, 1.1, 10)
    monkeypatch.setattr("GradientDescent.RandomFixedStepGradient.generate_steps", generate_steps)
    experiment = stepGradient.solver(func, [[-10, 10], [-10, 10]], x0)
    assert len(experiment.recorders) > 0
