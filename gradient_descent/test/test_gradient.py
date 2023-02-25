from pytest import approx
from source.gradient import calculateGradient, calculateHessian, calculate_step_bound
import autograd.numpy as np


def test_calculating_gradient():
    func = lambda x: x[0]**2 + x[1]**2
    x0 = np.array([1.0, 1.0])
    gradient = calculateGradient(func, x0)
    assert gradient[0] == approx(2.0, 0.1)
    assert gradient[1] == approx(2.0, 0.1)


def test_calculating_hessian():
    func = lambda x: x[0]**4 +x[0]**2 + x[1]**3
    x0 = np.array([1.0, 1.0])
    hessian = calculateHessian(func, x0)
    assert np.isclose(hessian, np.array([[14.0, 0.0], [0.0, 6.0]])).all()


def test_calculating_bound():
    func = lambda x: x[0]**4 +x[0]**2 + x[1]**3
    x0 = np.array([1.0, 1.0])
    bound = calculate_step_bound(func, x0)
    assert bound == approx(1.0/14.0, 0.01)