import numpy as np

if __name__ == '__main__':
    a = np.array([[1, 2, 3], [4, 5, 6]]).transpose()
    b = np.array([1, -1])
    alpha = np.array([2, 3])
    c = a.dot(b)
    kernel = lambda x, y: x.transpose().dot(y)
    Y = np.identity(2) * b[..., None]
    kernel_matrx = np.apply_along_axis(
        lambda xi: np.apply_along_axis(
            lambda xj: kernel(xi, xj), 0, a
        ), 0, a
    )
    w = alpha[..., None] * Y * kernel_matrx * Y * alpha
    h = Y * kernel_matrx*Y
    w2 = alpha[..., None]*h*alpha
