from typing import List, Callable

import matplotlib.pyplot as plt
from sympy import lambdify, Symbol, Pow, Mul

from create_graph import create_pointed_graph, find_points, create_continuous_graph, add_title_to_plot

x: Symbol = Symbol('x')
y: Pow = x ** 3 + x ** 2 - 5
y_prime: Mul = y.diff(x)

contraction_mapping: Callable = lambdify(x, x - y / y_prime, 'numpy')
polynomial_function: Callable = lambdify(x, y, 'numpy')

start_point: float = 5
x_points:  List[float]
y_points: List[float]
x_points, y_points = find_points(start_point=start_point, contraction_mapping=contraction_mapping,
                                 f=polynomial_function)

create_pointed_graph(x_points=x_points, y_points=y_points)
create_continuous_graph(f=polynomial_function)
add_title_to_plot(y)
plt.show()
