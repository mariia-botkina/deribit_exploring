from typing import List, Callable

import numpy as np
import matplotlib.pyplot as plt
from sympy import Pow


def find_points(start_point: float, contraction_mapping: Callable, f: Callable) -> (List[float], List[float]):
    x_points: List[float] = [start_point]
    y_points: List[float] = [f(x_points[-1])]

    for i in range(50):
        x_points.append(contraction_mapping(x_points[-1]))
        y_points.append(f(x_points[-1]))

    return x_points, y_points


def create_pointed_graph(x_points: List[float], y_points: List[float]):
    x = np.array(x_points)
    y = np.array(y_points)

    plt.scatter(x, y)


def create_continuous_graph(f: Callable):
    x = np.linspace(start=-8, stop=8, num=40)
    y = [f(val) for val in x]

    plt.plot(x, y)


def add_title_to_plot(func: Pow):
    title = str(func).replace('**', '^')
    title = title.replace(' * ', '')
    plt.title(title)
