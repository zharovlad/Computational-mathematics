from numpy import linspace
from math import pi
from math import cos
from math import sin
from math import acos
import matplotlib.pyplot as plt
from random import uniform

amount_of_dots = 5000  # для построения графика, если нужно построить бОльший интервал -> увеличить

class Test:
    def __init__(self, xt, arc, yt, dyt, x_left, x_right, amount_of_t, square_side, amount_of_dots):

        # функция для вычисления площади интеграла методом Симпсона
        self.f = lambda x: xt(x) * dyt(x)

        # функции заданные параметрически x = x(t), y = y(t)
        self.xt = xt
        self.yt = yt

        # обратные функции
        self.arcxt = arc

        self.square_side = square_side
        self.amount_of_dots = amount_of_dots

        # пределы интегрирования
        self.x_left = x_left
        self.x_right = x_right

        # создание точек x и y
        self.t = linspace(x_left, x_right, amount_of_t)
        self.x = [cos(x) for x in self.t]
        self.y = [sin(x) for x in self.t]

        # создание сплайнов
        self.spline_x = Test.get_splines(self.t, self.x)
        self.spline_y = Test.get_splines(self.t, self.y)

        dots = []
        for _ in range(amount_of_dots):
            dots.append([uniform(-square_side, square_side)])
        self.dots = sorted(dots)
        for i in range(amount_of_dots):
            self.dots[i].insert(0, uniform(-square_side, square_side))

        self.i = 0
        self.image_functions()

    @staticmethod
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

    def image_functions(self):
        """ Изображает функцию заданную параметрически сплайнами """
        fig, ax = plt.subplots()

        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('y')

        x = Test.get_values_from_splines(self.t, self.spline_x)
        y = Test.get_values_from_splines(self.t, self.spline_y)

        simpson_res = self.simpson()

        ax.plot(x, y)
        amount = 0

        for dot in self.dots:
            t = self.arcxt(dot[0])
            y = self.get_values_from_splines_for_dot(t)
            if abs(y) > abs(dot[1]):
                plt.scatter(dot[0], dot[1], s=3, color='green')
                amount += 1
            else:
                plt.scatter(dot[0], dot[1], s=3, color='red')

        carlo_res = 4 * self.square_side * self.square_side * amount / self.amount_of_dots
        plt.title('Simpson = ' + str(simpson_res) + '\nMonte Carlo = ' + str(carlo_res) + '\nAmount of dots = ' +
                  str(self.amount_of_dots))
        plt.legend()
        plt.show()

    @staticmethod
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

    def get_values_from_splines_for_dot(self, x):
        """ Вычисляет y для полученных сплайнов """
        while x < self.spline_y[self.i].x:
             self.i -= 1
        while x > self.spline_y[self.i].x:
            self.i += 1
        xi = x - self.spline_y[self.i].x
        yi = float(self.spline_y[self.i].a + self.spline_y[self.i].b * xi + self.spline_y[self.i].c / 2
                   * xi * xi + self.spline_y[self.i].d / 6 * xi * xi * xi)
        return yi

    def simpson(self):
        """ Считает приблизительное значение определенного интеграла методом Симпсона """
        result = 0.0
        h = self.t[1] - self.t[0]
        for i in range(len(self.t) - 1):
            result += (h / 6) * (self.f(self.t[i]) + 4 * self.f(self.t[i] + h / 2) + self.f(self.t[i + 1]))
        return result


class Spline:
    def __init__(self, x=0, a=0, b=0, c=0, d=0):
        self.x = x
        self.a = a
        self.b = b
        self.c = c
        self.d = d


if __name__ == '__main__':
    test1 = Test(cos, acos, sin, cos, -pi, pi, 100, 1, 500)
