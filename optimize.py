import math
from typing import Tuple, List
import scipy
import numpy as np
import matplotlib.pyplot as plt

def volatility_curve(xsabcde):
    x, s, a, b, c, d, e = xsabcde
    y = x - s
    return a + b * (1 - math.e ** (-c * y ** 2)) + d * math.atan(e * y) / e

# def func(xy):
#     x, y = xy
#     return np.sin(x) * np.sin(y)

# result = scipy.optimize.minimize(volatility_curve, (2,1,1,1,1,1,1))
# result = scipy.optimize.minimize(func, (-1, 1))
# print(result)
# print(result.x)

def line(ab, x):
    a, b = ab
    return a * x + b 

class Fit:
    def __init__(self, x: List[float], y: List[float]) -> None:
        self.x: List[float] = x
        self.y: List[float] = y
    
    def minimize_line(self, params: Tuple[float]):
        a, b = params
        return a * x + b

    def goal_function(self, params: Tuple[float]):
        error: float = 0.
        for x_value, y_value in zip(self.x, self.y):
            error += abs(y_value - self.line_equation(params, x_value))
        return error

    def fit(self):
        optimized = scipy.optimize.minimize(self.goal_function, x0=np.array([0., 0.]))
        return optimized


class SquaredFit:
    def __init__(self, x_array: List[float], y_array: List[float]) -> None:
        self.x_array: List[float] = x_array
        self.y_array: List[float] = y_array
        self.length: int = 2

    def get_inversed_matrix_of_equations_coefficients(self) -> np.matrix:
        coefficients = []
        for i in range(1, self.length + 1):
            row = []
            for j in range(1, self.length + 1):
                c = 0
                for x_value in self.x_array:
                    c += x_value ** (i + j - 2)
                row.append(c)
            coefficients.append(row)
        matrix = np.matrix(coefficients)
        inversed_matrix = np.linalg.inv(matrix)
        return inversed_matrix

    def get_matrix_of_intercept_terms(self) -> np.matrix:
        intercept_terms = []
        for i in range(1, self.length + 1):
            d = 0
            for x_value, y_value in zip(self.x_array, self.y_array):
                d += x_value ** (i - 1) * y_value
            intercept_terms.append([d])
        matrix = np.matrix(intercept_terms)
        return matrix

    def squared_fit(self):
        linear_equation_coefficients = np.dot(self.get_inversed_matrix_of_equations_coefficients(),
                                              self.get_matrix_of_intercept_terms())
        return linear_equation_coefficients


x_points = [1, 1, 2]
y_points = [0.1, 0.9, 2.1]

result = scipy.optimize.minimize(Fit(x_points[1], y_points[1]).minimize_line, (1, 3))
print(result)
print(result.x[0], result.x[1])

x = np.linspace(0, 3)
y = result.x[0] * x + result.x[1]

ax = plt.axes()
plt.grid()
# ax.plot(x, y)
ax.plot(x_points, x_points, 'o')
# ax.scatter(x=[0, 1, 2], y=[0, 1, 2])
print(line(result.x, 0))
print(line(result.x, 2))
plt.show()