import matplotlib.pyplot as plt
from numpy import linspace
import math

# функции для построения таблицы и интервалы для них
functions = [[abs, -1, 1], [lambda x: math.e ** (-x * x), -4, 4], [math.sin, -math.pi, math.pi], [math.sqrt, 0, 4],
             [lambda x: x ** 2, -2, 2], [lambda x: x, -1, 4], [lambda x: 3 ** x, 0, 3], [lambda x: 1 / x, 0.1, 3]]
amount_of_dots = 5000  # для построения графика, если нужно построить бОльший интервал -> увеличить
input_file_name = 'input.txt'
output_file_name = 'output.txt'


def clear_output_file():
    """ Очищение выходного файла от предыдущего результата работы программы """
    _ = open(output_file_name, 'w')
    _.close()
    return


def image_functions(f, fL, x_left, x_right):
    """ Изображает функцию f на интервале (xmin, xmax) """
    fig, ax = plt.subplots()
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
    ax.plot(x, y)
    yL = list(map(lambda each: fL(each), x))
    ax.plot(x, yL)
    plt.show()


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


def reading_data_from_file():
    """ Возвращает данные в зависимости от режима работы
    Если 1: возвращает массив значений x, y, и точку x, в которой необходимо определить приблеженное значение
    Если 2: возвращает функцию для построения таблицы y(вместе с интервалами), массив значений x """
    read = open(input_file_name, 'r')
    list = []
    list.append(int(read.readline()))
    if list[0] == 1:
        s = read.readline()
        s = s.split()
        x_arr = []
        for each in s:
            x_arr.append(float(each))
        list.append(x_arr)

        s = read.readline()
        s = s.split()
        y_arr = []
        for each in s:
            y_arr.append(float(each))
        list.append(y_arr)

        list.append(float(read.readline()))
    else:
        # в файле хранится индекс функции из списка functions
        list.append(functions[int(read.readline())])

        s = read.readline()
        s = s.split()
        x_arr = []
        for each in s:
            x_arr.append(float(each))
        list.append(x_arr)
    read.close()
    return list


def print_result_1(x_array, y_array, x, L):
    write = open(output_file_name, 'w')
    write.write('x table = ' + str(x_array) + '\n')
    write.write('y table = ' + str(y_array) + '\n')
    write.write('x = ' + str(x) + '\n')
    write.write('L = ' + str(L) + '\n')


def determine_y(f, x_array):
    """ Находим y по заданной функции и массиву точек x """
    return [f(x) for x in x_array]


if __name__ == '__main__':
    clear_output_file()
    data = reading_data_from_file()
    if data[0] == 1:
        x_array, y_array, x = data[1], data[2], data[3]
        f = get_Lagrange_polynomial(x_array, y_array)
        L = f(x)
        print_result_1(x_array, y_array, x, L)
    else:
        f, x_left, x_right, x_array = data[1][0], data[1][1], data[1][2], data[2]
        y_array = determine_y(f, x_array)
        fL = get_Lagrange_polynomial(x_array, y_array)
        image_functions(f, fL, x_left, x_right)




