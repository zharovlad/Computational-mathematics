import matplotlib.pyplot as plt
from numpy import linspace
import math

# функции для построения таблицы и интервалы для них
functions = [[abs, -1.0, 1.0], [lambda x: math.e ** (-x * x), -4.0, 4.0], [math.sin, -math.pi, math.pi],
             [math.sqrt, 0.0, 4.0], [lambda x: x ** 3, -2.0, 2.0], [lambda x: x, -1.0, 4.0], [lambda x: 3 ** x, 0.0, 3.0],
             [lambda x: 1 / x, 0.1, 3.0], [lambda x: x, -3.0, 3.0]]
amount_of_dots = 5000  # для построения графика, если нужно построить бОльший интервал -> увеличить
input_file_name = 'input.txt'
output_file_name = 'output.txt'


def reading_data_from_file():
    """ Возвращает функцию для построения таблицы y(вместе с интервалами), количество точек """
    with open(input_file_name, 'r') as read:
        # в файле хранится индекс функции из списка functions
        func = read.readline().split()
        dots = read.readline().split()
    return int(func[0]), [float(i) for i in dots]


def image_functions(f, fL, x_left, x_right, splines):
    """ Изображает функцию f на интервале (xmin, xmax) """
    fig, ax = plt.subplots()

    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('y')

    # создание массива с координатами x
    # пример для xmin = -pi / 2, xmax = pi / 2, amount_of_dots = 5
    # [-1.57079633 -0.78539816  0.          0.78539816  1.57079633]
    # [-pi / 2, - pi / 4, 0, pi / 4, pi / 2]
    x = linspace(x_left, x_right, amount_of_dots)

    # создание массива с координатами y
    # для этого же примера
    # (0.7071067811865475 = sqrt(2) / 2)
    # [-1.0, -0.7071067811865475 , 0.0, 0.7071067811865475, 1.0]
    y = list(map(lambda each: f(each), x))
    ax.plot(x, y, label='function')

    # массив y для многочлена Лагранжа
    #yL = list(map(lambda each: fL(each), x))
    #ax.plot(x, yL, label='lagrange')

    # массив у для сплайнов
    yS = get_values_from_splines(x, splines)
    ax.plot(x, yS, label='spline')
    plt.legend()
    plt.show()


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


def get_Lagrange_polynomial(x_tabl, y_tabl):
    """ Получает функцию для рисования её графика """
    def get_Lagrange_polynomial_value(x):
        """ Получает значение полинома Лагранжа для таблицы значений и x"""
        sizee = int(len(y_tabl))
        L = 0
        for k in range(sizee):
            numerator = 1
            denominator = 1
            for j in range(sizee):
                if j != k:
                    numerator *= x - x_tabl[j]
                    denominator *= x_tabl[k] - x_tabl[j]
            L += y_tabl[k] * numerator / denominator
        return L
    return get_Lagrange_polynomial_value


def determine_y(f, x_array):
    """ Находим y по заданной функции и массиву точек x """
    return [f(x) for x in x_array]


class Spline:
    def __init__(self, x=0, a=0, b=0, c=0, d=0):
        self.x = x
        self.a = a
        self.b = b
        self.c = c
        self.d = d


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


if __name__ == '__main__':
    func, x = reading_data_from_file()
    f, x_left, x_right = functions[func][0], functions[func][1], functions[func][2]

    # таблица значений x
    # x = list(linspace(x_left, x_right, dots))

    # таблица значений y, заданная функцией
    y = determine_y(f, x)

    # таблица значений y, заданная интерполяционным многочленом Лагранжа
    fL = get_Lagrange_polynomial(x, y)

    # кубические сплайны
    splines = get_splines(x, y)

    image_functions(f, fL, x_left, x_right, splines)
