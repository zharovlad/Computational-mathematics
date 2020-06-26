from numpy import linspace
from math import pi
import matplotlib.pyplot as plt
from random import uniform
from math import inf
from math import nan


class Test:
    def __init__(self, spline_x, spline_y, spline_dy, t, amount_of_dots, x_min, x_max, y_min, y_max):

        # создание сплайнов
        self.spline_x = spline_x
        self.spline_y = spline_y
        self.spline_dy = spline_dy
        self.t = t

        # функция для вычисления площади интеграла методом Симпсона
        #self.f = lambda x: get_value_from_splines(x, spline_x) * get_value_from_splines(x, spline_dy)

        # функции заданные параметрически x = x(t), y = y(t)
        self.xt = xt
        self.yt = yt

        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        self.amount_of_dots = amount_of_dots

        self.dots = [Dot(uniform(x_min, x_max), uniform(y_min, y_max)) for _ in range(amount_of_dots)]

        self.i = 0
        self.image_functions()

    def image_functions(self):
        """ Изображает функцию заданную параметрически сплайнами """
        fig, ax = plt.subplots()

        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('y')

        t = linspace(self.t[0], self.t[-1], 5000)
        x = get_values_from_splines(t, self.spline_x)
        y = get_values_from_splines(t, self.spline_y)

        #simpson_res = self.simpson()
        simpson_res = 'is not defined'
        ax.plot(x, y)
        amount = 0
        for dot in self.dots:
            if is_dot_in_area(dot.x, dot.y, x, y):
                plt.scatter(dot.x, dot.y, s=3, color='green')
                amount += 1
            else:
                plt.scatter(dot.x, dot.y, s=3, color='red')

        carlo_res = (self.y_max - self.y_min) * (self.x_max - self.x_min) * amount / self.amount_of_dots
        plt.title('Simpson = ' + str(simpson_res) + '\nMonte Carlo = ' + str(carlo_res) + '\nAmount of dots = ' +
                  str(self.amount_of_dots))
        plt.show()

    # def simpson(self):
    #     """ Считает приблизительное значение определенного интеграла методом Симпсона """
    #     result = 0.0
    #     h = self.t[1] - self.t[0]
    #     for i in range(len(self.t) - 1):
    #         result += (h / 6) * (self.f(self.t[i]) + 4 * self.f(self.t[i] + h / 2) + self.f(self.t[i + 1]))
    #     return result


def get_splines(x, y):
    """ Создает сплайны для заданной таблицы """
    # присвоим каждому i-ому сплайну значения x = x[i] и a = y[i]
    splines = [Spline(x[i], y[i]) for i in range(len(x))]

    # находим c[i] по соответствующей формуле методом прогонки
    alpha = [0.0]
    beta = [0.0]

    for i in range(1, len(x) - 1, 1):
        hi = x[i] - x[i - 1]
        hi1 = x[i + 1] - x[i]
        A = hi
        B = 2.0 * (hi + hi1)
        C = hi1
        F = 6.0 * ((y[i + 1] - y[i]) / hi1 - (y[i] - y[i - 1]) / hi)

        alpha.append(-C / (A * alpha[i - 1] + B))
        beta.append((F - A * beta[i - 1]) / (A * alpha[i - 1] + B))

    for i in range(len(x) - 2, 0, -1):
        splines[i].c = alpha[i] * splines[i + 1].c + beta[i]

    # теперь вычисляем
    # d[i], зная c[i] и
    # b[i], зная c[i] и d[i]

    for i in range(len(x)):
        hi = x[i] - x[i - 1]
        splines[i].d = (splines[i].c - splines[i - 1].c) / hi
        splines[i].b = (hi / 2.0 * splines[i].c) - (hi * hi / 6.0 * splines[i].d) + ((y[i] - y[i - 1]) / hi)

    return splines


def get_values_from_splines(x, splines):
    """ Вычисляет y для полученных сплайнов """
    i = 0
    y = []
    for each in x:
        if each > splines[i].x:
            i = i + 1
        xi = each - splines[i].x
        yi = float(splines[i].a + splines[i].b * xi + splines[i].c / 2 * xi * xi + splines[i].d / 6 * xi * xi * xi)
        y.append(yi)
    return y


# def get_value_from_splines(x, splines):
#     """ Вычисляет y для полученных сплайнов """
#     i = 1
#     while x > splines[i].x and i < len(splines) - 1:
#         i = i + 1
#     xi = x - splines[i].x
#     yi = float(splines[i].a + splines[i].b * xi + splines[i].c / 2 * xi * xi + splines[i].d / 6 * xi * xi * xi)
#     return yi


def is_dot_in_area(x, y, x_array, y_array):
    """ Метод трассировки лучей """
    is_cross_over = False
    for i in range(len(x_array) - 1):
        if is_cross(x, y, inf, y, x_array[i], y_array[i], x_array[i + 1], y_array[i + 1]):
            is_cross_over = not is_cross_over
    return is_cross_over


def direction(x0, y0, x1, y1, x2, y2):
    return (x2 - x0) * (y1 - y0) - (y2 - y0) * (x1 - x0)


def is_cross(x1, y1, x2, y2, x3, y3, x4, y4):
    d1 = direction(x3, y3, x4, y4, x1, y1)
    d2 = direction(x3, y3, x4, y4, x2, y2)
    d3 = direction(x1, y1, x2, y2, x3, y3)
    d4 = direction(x1, y1, x2, y2, x4, y4)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    return False


class Spline:
    def __init__(self, x=0, a=0, b=0, c=0, d=0):
        self.x = x
        self.a = a
        self.b = b
        self.c = c
        self.d = d


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def get_first_derivative(x_array, y_array):
    h = x_array[1] - x_array[0]
    derivative = [nan]
    for i in range(1, len(x_array) - 1, 1):
        derivative.append((y_array[i + 1] - y_array[i - 1]) / (2 * h))
    derivative.append(nan)
    return derivative


if __name__ == '__main__':
    # (0, 0)
    # (0.5, 1)
    # (1, 1.3)
    # (1.5, 2)
    # (2, 1.6)
    # (1.8, 1)
    # (2.1, 0.8)
    # (1.5, 0.5)
    # (1.3, 0.9)
    # (1.1, 0.7)
    # (0.8, 0.5)
    # (0.5, 0.7)
    # (0.3,-0.2)
    # (0,0)

    # пределы функции
    t_left = -pi
    t_right = pi

    # заданные точки
    x = [0.0, 0.5, 1.0, 1.5, 2.0, 1.8, 2.1, 1.5, 1.3, 1.1, 0.8, 0.5, 0.3, 0.0]
    y = [0.0, 1.0, 1.3, 2.0, 1.6, 1.0, 0.8, 0.5, 0.9, 0.7, 0.5, 0.7, -0.2, 0.0]

    # создаем сплайны через параметр t
    t = list(linspace(t_left, t_right, len(x)))
    xt = get_splines(t, x)
    yt = get_splines(t, y)

    # находим производную первого порядка
    dyt = get_first_derivative(t, y)

    test1 = Test(xt, yt, dyt, t, 10000, min(x), max(x), min(y), max(y))
