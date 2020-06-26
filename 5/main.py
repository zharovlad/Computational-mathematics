from math import fabs
from math import sqrt
from copy import deepcopy

input_file_name = 'input.txt'
output_file_name = 'output.txt'
SQ = sqrt(0.5)  #


def create_test():
    """ Создает диагональную матрицу 200 * 200 """
    from random import randint
    m = []
    for i in range(200):
        arr = []
        for j in range(200):
            if i < j:
                arr.append(0)
            else:
                arr.append(randint(1, 20))
        m.append(arr)
    return m


def reading_from_text_file():
    """ Чтение данных"""
    inp = open(input_file_name)

    eps = float(inp.readline())
    number_of_tests = int(inp.readline())
    tests = []
    for _ in range(number_of_tests):
        matrix = []
        matrix_size = int(inp.readline())
        if matrix_size == 200:
            tests.append(create_test())
        else:
            for __ in range(matrix_size):
                string = inp.readline()
                string = string.split()
                array = [float(string[i]) for i in range(matrix_size)]
                matrix.append(array)
            tests.append(matrix)
    inp.close()
    return number_of_tests, tests, eps


def clear_output_file():
    """ очищение выходного файла от предыдущего результата работы программы """
    _ = open(output_file_name, 'w')
    _.close()
    return


def print_result(eigenvalues, eigenvectors, matrix, eps):
    """ Печать резултата работы программы в файл """
    message = 'eps = ' + str(eps) + '\nMatrix:\n'
    print_message(message)
    print_matrix(matrix, len(matrix))

    message = '\n'
    for i in range(len(eigenvalues)):
        message += 'value ' + str(i) + ' = ' + '%.10f' % eigenvalues[i] + '\n'
    print_message(message)

    message = '\n'
    for i in range(len(eigenvectors)):
        message += '\nvector ' + str(i) + ' :\n'
        for j in range(len(eigenvectors[i])):
            message += '%.10f' % eigenvectors[i][j] + '\n'
    print_message(message)

    dis = discrepancy(eigenvalues, eigenvectors, matrix)
    message = '\n'
    for i in range(len(dis)):
        message += '\ndiscrepancy ' + str(i) + ' :\n'
        for j in range(len(dis[i])):
            message += '%.10f' % dis[i][j] + '\n'
    print_message(message + 80 * '*' + '\n')
    return


def print_matrix(matrix, sizee):
    """ Печать матрицы в файл """
    message = ''
    for i in range(sizee):
        for j in range(sizee):
            s = '%.5f' % matrix[i][j]
            message += s.ljust(15)
        message += '\n'
    print_message(message)
    return


def print_message(message):
    """ Печать сообщения в файл """
    writef = open(output_file_name, 'a')
    writef.write(message)
    writef.close()
    return


def discrepancy(eigenvalues, eigenvectors, matrix):
    """ Нахождение невязки. Сравнение результатов умножения числа на вектор с матрицей на вектор """
    results = []
    for i in range(len(matrix)):
        matr_x_vect = matrix_mul_vector(matrix, eigenvectors[i])
        value_x_vect = [x * eigenvalues[i] for x in eigenvectors[i]]
        array = list(map(lambda m, n: fabs(m - n), matr_x_vect, value_x_vect))
        results.append(array)
    return results


def matrix_mul_vector(a, x):
    """ Умножение матрицы на вектор """
    n = len(a)
    m = len(x)
    result = []
    for i in range(n):
        s = 0
        for j in range(m):
            s += x[j] * a[i][j]
        result.append(s)
    return result


def search_eigenvalues_and_eigenvectors(matrix, eps):
    """ Находим все собственные числа методом вращения """
    sizee = len(matrix)

    # сначала ищем суммы квадратов недиагональных элементов для каждой строки матрицы
    sum_off_diag = []
    for i in range(sizee):
        s = 0
        for j in range(sizee):
            s += matrix[i][j] ** 2 if i != j else 0
        sum_off_diag.append(s)

    N = 0  # число вращений
    D = create_E_matrix(sizee)  # матрица для нахождения собственных векторов

    while (1 - (2 / (sizee * (sizee - 1)))) ** N > eps:
    #while max(sum_off_diag) > eps:

        # находим индекс строки с наибольшей суммой недиагональных элементов (k)
        k = sum_off_diag.index(max(sum_off_diag))
        # и индекс наибольшего элемента в этой строке l != k
        s = -99999999
        l = None
        for i in range(sizee):
            if fabs(matrix[k][i]) > s and i != k:
                l = i
                s = fabs(matrix[k][i])

        # считаем α и β по формулам
        alpha = None
        beta = None
        if matrix[k][k] == matrix[l][l]:
            alpha = beta = SQ
        else:
            mu = 2 * matrix[k][l] / (matrix[k][k] - matrix[l][l])
            alpha = sqrt(0.5 * (1 + 1 / sqrt(1 + mu ** 2)))
            beta = sqrt(0.5 * (1 - 1 / sqrt(1 + mu ** 2))) if mu > 0 else -sqrt(0.5 * (1 - 1 / sqrt(1 + mu ** 2)))

        # создаем Ukl матрицу
        Ukl = create_E_matrix(sizee)
        Ukl[k][k] = Ukl[l][l] = alpha
        Ukl[k][l] = -beta
        Ukl[l][k] = beta

        # и транспонированную Ukl
        Ukl_transposed = deepcopy(Ukl)
        Ukl_transposed[k][l], Ukl_transposed[l][k] = Ukl_transposed[l][k], Ukl_transposed[k][l]

        # изменяем matrix
        matrix = matrix_multiplication([Ukl_transposed, matrix, Ukl])

        # пересчитываем суммы в строках k и l
        sum_off_diag[k] = sum_off_diag[l] = 0
        for i in range(sizee):
            if i == k:
                sum_off_diag[l] += matrix[l][i] ** 2
            elif i == l:
                sum_off_diag[k] += matrix[k][i] ** 2
            else:
                sum_off_diag[k] += matrix[k][i] ** 2
                sum_off_diag[l] += matrix[l][i] ** 2
        N += 1

        # вычисляем собственные вектора
        D = matrix_multiplication([D, Ukl])

    print(N)
    return [matrix[i][i] for i in range(sizee)], [[D[j][i] for j in range(sizee)] for i in range(sizee)]


def create_E_matrix(matrix_size):
    """ Cоздаем единичную матрицу.
    Она понадобится для создания Ukl матрицы, чтобы каждый раз не создавать её заново, сделаем образец """
    E = []
    for i in range(matrix_size):
        arr = []
        for j in range(matrix_size):
            arr.append(1) if i == j else arr.append(0)
        E.append(arr)
    return E


def matrix_multiplication(matrixes):
    """ Перемножает все матрицы из списка """
    while len(matrixes) > 1:
        result = []
        for i in range(len(matrixes[0])):
            array = []
            for j in range(len(matrixes[0])):
                s = 0
                for k in range(len(matrixes[0])):
                    s += matrixes[0][i][k] * matrixes[1][k][j]
                array.append(s)
            result.append(array)
        matrixes[0] = result
        matrixes.pop(1)
    return matrixes[0]



if __name__ == "__main__":
    clear_output_file()
    number_of_tests, tests, eps = reading_from_text_file()
    matrixes = deepcopy(tests)
    for i in range(number_of_tests):
        eigenvalues, eigenvectors = search_eigenvalues_and_eigenvectors(matrixes[i], eps)
        print_result(eigenvalues, eigenvectors, matrixes[i], eps)
