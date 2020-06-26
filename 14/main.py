from math import pi, tan, inf
import matplotlib.pyplot as plt
from numpy import linspace
amount_of_dots = 5000  # для построения графика, если нужно построить бОльший интервал -> увеличить


def get_system(rho=0.5, theta=0.05, alpha=6*pi/180, beta=0.2):
    """ Поставленная задача, преобразованная в систему уравнений """
    return [
        lambda r, u, z: z,
        lambda r, u, z: (beta * u ** 4) / ((1 - r) * tan(alpha) + theta) -
        z * (1 / (r + rho) - tan(alpha) / ((1 - r) * tan(alpha) + theta))
    ]


def find_solution(system, start_conditions, approximation_interval, step, eps):
    """ Решаем задачу Коши на отрезке approximation_interval"""
    left_border, right_border = approximation_interval

    R_begin, R_end = start_conditions[0][0], start_conditions[1][0]

    new_solution = Runge_Kutta(system, [start_conditions[0][1], left_border], R_begin, R_end)
    new_solution = new_solution[-1][1]
    old_solution = new_solution

    # если решение находится на полученном интервале, то значения на границах решения будут с разным знаком
    while old_solution * new_solution > 0:
        old_solution = new_solution

        # если достигли границы исследуемого отрезка, выйти из программы
        # иначе следует изменить отрезок
        if left_border + step > right_border:
            return None
        left_border += step
        # округление, чтобы исправить погрешности вычислений ЭВМ
        left_border = round(left_border, 5)

        # Задача Коши решается методом Рунге-Кутта
        temp = Runge_Kutta(system, [start_conditions[0][1], left_border], R_begin, R_end)
        new_solution = temp[-1][1]
    right_border = left_border
    left_border -= step
    left_border = round(left_border, 5)

    # получаем точное решение методом деление отрезка пополам
    solution = bisection(system, start_conditions, eps, left_border, right_border)

    return solution


def bisection(system, start_conditions, eps, left_border, right_border):
    """ Получение точного решения методом деление отрезка пополам """
    R_begin, R_end = start_conditions[0][0], start_conditions[1][0]
    solution = inf
    center = (left_border + right_border) / 2
    while abs(solution - start_conditions[1][1]) > eps:
        center_solution = Runge_Kutta(system, [start_conditions[0][1], center], R_begin, R_end)
        solution = center_solution[-1][1]
        if solution > start_conditions[1][1]:
            right_border = center
        else:
            left_border = center
        center = (left_border + right_border) / 2

    return center_solution


def Runge_Kutta(system, y0, begin, end):
    """ Решение системы методом Рунге-Кутта с постоянным шагом
    Метод взят из прошлой лабораторной работы и слегка модернизирован """
    step = 0.001
    x = begin
    y = y0
    y_array = []

    while x <= end:
        y_array.append(y)
        if x == end:
            break
        y = calculate_new_y(system, x, y, step)

        # проверим, чтобы не было выхода за пределы интегрирования
        if x + step >= end and x != end:
            x = end
        else:
            x += step
            # округление, чтобы убрать машинные арифметические ошибки
            x = round(x, 5)

    return y_array


# функции, которые считают k1,2,3,4 и yn+1 для метода Рунге-Кутта четвертого порядка погрешности.
def calculate_k1(system, x, y, step):
    return [step * f(x, *y) for f in system]


def calculate_k2(system, x, y, step, k1):
        x += step / 2
        y = [y[i] + k1[i] / 2 for i in range(len(y))]
        return [step * f(x, *y) for f in system]


def calculate_k3(system, x, y, step, k2):
    x += step / 2
    y = [y[i] + k2[i] / 2 for i in range(len(y))]
    return [step * f(x, *y) for f in system]


def calculate_k4(system, x, y, step, k3):
        x += step
        y = [y[i] + k3[i] for i in range(len(y))]
        return [step * f(x, *y) for f in system]


def calculate_new_y(system, x, y, step):
    k1 = calculate_k1(system, x, y, step)
    k2 = calculate_k2(system, x, y, step, k1)
    k3 = calculate_k3(system, x, y, step, k2)
    k4 = calculate_k4(system, x, y, step, k3)
    return [y[i] + 1 / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(system))]


def transform(y):
    """ Преобразует аргументы y так, чтобы графика можно было вывести на экран"""
    result = []
    for j in range(len(y[0])):
        array = []
        for i in range(len(y)):
            array.append(y[i][j])
        result.append(array)
    return result


def image_function(start_conditions, y, beta):
    """ Выводит полученные функции на экран """
    fig, ax = plt.subplots()
    x = linspace(start_conditions[0][0], start_conditions[0][1], 1001)

    ax.plot(x, y[0], label='U(R)')
    ax.plot(x, y[1], label='U\'(R)')
    plt.title('Beta = ' + str(beta))

    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    beta = 1.0

    start_conditions = [
        [0, 1],  # u(0) = 1
        [1, 0]  # u'(1) = 0
    ]

    system = get_system(beta=beta)
    approximation_interval = [-2, 0]
    step = 0.1
    eps = 0.001

    solution = find_solution(system, start_conditions, approximation_interval, step, eps)
    if solution:
        solution = transform(solution)
        image_function(start_conditions, solution, beta)

