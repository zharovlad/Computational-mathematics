import matplotlib.pyplot as plt
from math import cos, sin, pi, inf
from numpy import linspace
output_file_name = 'output.txt'
amount_of_dots = 5000  # для построения графика, если нужно построить бОльший интервал -> увеличить


class Test:
    def __init__(self, system, y0, begin, end, step, eps):
        self.system = system
        self.y0 = y0
        self.begin = begin
        self.end = end
        self.step = step
        self.eps = eps

    def solve_with_constant_step(self):
        """ Решение системы с постоянным шагом self.step
        Возвращает 2 списка """
        x = self.begin
        y = self.y0
        y_array = []
        x_array = []

        while x <= self.end:
            x_array.append(x)
            y_array.append(y)
            if x == self.end:
                break
            k1 = self.k1(x, y)
            k2 = self.k2(x, y, k1)
            k3 = self.k3(x, y, k2)
            k4 = self.k4(x, y, k3)
            y = self.new_y(y, k1, k2, k3, k4)

            # проверим, чтобы не было выхода за пределы интегрирования
            if x + self.step >= self.end and x != self.end:
                x = self.end
            else:
                x += self.step
                # округление, чтобы убрать машинные арифметические ошибки
                x = round(x, 5)
        return x_array, y_array

    def solve_with_auto_step(self):
        """ Решение системы с автоматическим выбором шага для точности self.eps
        Возвращает 2 списка """

        x = self.begin
        y = self.y0
        y_array = []
        x_array = []
        while x <= self.end:
            x_array.append(x)
            y_array.append(y)
            if x == self.end:
                break
            step = self.calculate_step(x, y)
            k1 = self.k1(x, y, step)
            k2 = self.k2(x, y, k1, step)
            k3 = self.k3(x, y, k2, step)
            k4 = self.k4(x, y, k3, step)
            y = self.new_y(y, k1, k2, k3, k4)
            if x + step > self.end:
                x = self.end
            else:
                x += step

        return x_array, y_array

    def calculate_step(self, current_x, y):
        """ Считает шаг для решения системы с автоматическим выбором шага вложенным методом """

        step = self.end - current_x
        while True:
            k1 = self.k1(current_x, y, step)
            k2 = self.k2(current_x, y, k1, step)
            k3 = self.k3(current_x, y, k2, step)
            k4 = self.k4(current_x, y, k3, step)
            E = max([abs(2 / 3 * (k1[i] - k2[i] - k3[i] + k4[i])) for i in range(len(k1))])

            if E < self.eps / 32:
                step *= 2

            elif E > self.eps:
                step /= 2

            else:
                break

        return step

    # функции, которые считают ki для четвертого порядка погрешности. Подробности в отчете

    def k1(self, x, y, step=None):
        if not step:
            step = self.step
        return [step * f(x, *y) for f in self.system]

    def k2(self, x, y, k1, step=None):
        if not step:
            step = self.step
        x += step / 2
        y = [y[i] + k1[i] / 2 for i in range(len(y))]
        return [step * f(x, *y) for f in self.system]

    def k3(self, x, y, k2, step=None):
        if not step:
            step = self.step
        x += step / 2
        y = [y[i] + k2[i] / 2 for i in range(len(y))]
        return [step * f(x, *y) for f in self.system]

    def k4(self, x, y, k3, step=None):
        if not step:
            step = self.step
        x += step
        y = [y[i] + k3[i] for i in range(len(y))]
        return [step * f(x, *y) for f in self.system]

    def new_y(self, y, k1, k2, k3, k4):
        return [y[i] + 1 / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(self.system))]

    def image_function(self, x_array, y_array):#, xa_array, ya_array, u):
        fig, ax = plt.subplots()

        for i in range(len(y_array)):
            ax.plot(x_array, y_array[i], label='y' + str(i + 1))

        #for i in range(len(ya_array)):
        #    ax.plot(xa_array, ya_array[i], label='ya' + str(i + 1))

        # if u != None:
        #     x = linspace(self.begin, self.end, amount_of_dots)
        #     for i in range(len(u)):
        #         y = [u[i](x) for x in x]
        #         ax.plot(x, y, label='u' + str(i + 1))
        #     plt.title('Шаг = ' + str(self.step) + '\nТочность = ' + str(self.eps) +
        #               '\nНорма глобальной погрешности для \nпостоянного шага = ' +
        #               str(calculate_global_error_norm(x_array, y_array, u) * 100) +
        #               '\nавтоматического шага = ' +
        #               str(calculate_global_error_norm_(xa_array, ya_array, u)))

        plt.legend()
        plt.show()


def transform(y):
    """ Преобразует аргументы y так, чтобы графика можно было вывести на экран"""
    result = []
    for j in range(len(y[0])):
        array = []
        for i in range(len(y)):
            array.append(y[i][j])
        result.append(array)
    return result


def calculate_global_error_norm(x, y, f):
    """ Считает норму глобальной погрешности """
    norm = -inf
    for i in range(len(f)):
        for j in range(len(y)):
            if abs(y[i][j] - f[i](x[j])) > norm:
                norm = abs(y[i][j] - f[i](x[j]))
    return norm

def calculate_global_error_norm_(x, y, f):
    """ Считает норму глобальной погрешности """
    norm = -inf
    for i in range(len(f)):
        for j in range(len(y[i])):
            if abs(y[i][j] - f[i](x[j])) > norm:
                norm = abs(y[i][j] - f[i](x[j]))
    return norm



if __name__ == '__main__':
    system = [
        lambda x, y: -30 * y
    ]
    u = None
    interval_begin = 0
    interval_end = 1


    # system = [
    #     lambda x, y: 2 * x + y - x ** 2
    # ]
    #
    # u = [
    #     lambda x: x ** 2
    # ]
    # interval_begin = -10
    # interval_end = 10

    # system = [
    #     lambda x, y1, y2: y2,
    #     lambda x, y1, y2: -y1
    # ]
    #
    # u = [
    #     lambda x: sin(x),
    #     lambda x: cos(x)
    # ]

    # interval_begin = 0
    # interval_end = 2 * pi

    # y0 = [f(interval_begin) for f in u]
    y0 = [1]

    step = 1 / 11  #
    #step = 0.1
    eps = 0.001

    test1 = Test(system, y0, interval_begin, interval_end, step, eps)

    x, y = test1.solve_with_constant_step()
    y = transform(y)

    #xa, ya = test1.solve_with_auto_step()
    #ya = transform(ya)

    test1.image_function(x, y)#, xa, ya, u)

# with open(output_file_name, 'w') as w:
#     for i in range(len(x)):
#         w.write(str(round(x[i], 7)).ljust(10) + ' ')
#         for f in u:
#             w.write(str(round(f(x[i]), 7)).ljust(10) + ' ')
#         for arg in y:
#             w.write(str(round(arg[i], 7)).ljust(10) + ' ')
#         w.write('\n')
#
#     w.write('\n' + '*' * 80 + '\n')
#
#     for i in range(len(xa)):
#         w.write(str(round(xa[i], 7)).ljust(10) + ' ')
#         for f in u:
#             w.write(str(round(f(xa[i]), 7)).ljust(10) + ' ')
#         for arg in ya:
#             w.write(str(round(arg[i], 7)).ljust(10) + ' ')
#         w.write('\n')
