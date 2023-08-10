from ast import List
import math
from typing import Tuple
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
        return self.y - (a * self.x + b)
x_points = [0, 1, 2]
y_points = [0, 1, 2]
# plt.plot(x_points, y_points)

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