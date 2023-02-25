from autograd import grad, jacobian
import autograd.numpy as np
from math import isclose


def differentiate(func):
    return grad(func)


def calculateGradient(func, x):
    return differentiate(func)(x)


def getHessian(func):
    return jacobian(grad(func))


def calculateHessian(func, x):
    return getHessian(func)(x)


def calculate_step_bound(func, x):
    hessian = calculateHessian(func, x)
    eigenvalues, eigv = np.linalg.eig(hessian)
    max_eigen = max(eigenvalues)
    return abs(1/max_eigen) if not isclose(max_eigen, 0.0, abs_tol=1e-9)  else 1.0
