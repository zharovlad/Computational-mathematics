# lab 3 by @zharovlad
# во входном файле - 1 число размерность матрицы
# затем расширенная матрица
# последнее число точность eps


def read_matrix():
    # чтение из файла матрицы
    readf = open(input_file_name, 'r')
    matr = []
    sizee = int(readf.readline())
    b = []
    for i in range(sizee):
        line = readf.readline()
        array = []
        s = line.split()
        for each in s:
            number = float(each)
            array.append(number)
        matr.append(array)
        b.append(matr[i][sizee])
    eps = float(readf.readline())
    readf.close()
    return matr, b, eps, sizee


def print_message(message):
    # печать сообщения в файл
    writef = open('output.txt', 'a')
    writef.write(message)
    writef.close()
    return


def print_system(matrix, sizee, b):
    # вывод системы
    message = ''
    for i in range(sizee):
        for j in range(sizee):
            s = '%.5f' % matrix[i][j]
            message += s.ljust(15)
        message += '| ' + '%.5f' % b[i] + '\n'
    print_message(message)
    return


def print_matrix(matrix, sizee):
    # вывод системы
    message = ''
    for i in range(sizee):
        for j in range(sizee):
            s = '%.5f' % matrix[i][j]
            message += s.ljust(15)
        message += '\n'
    print_message(message)
    return


def print_iteration(x, n, sizee):
    print_message('Iteration #' + str(n) + '\n')
    for i in range(sizee):
        print_message('x' + str(i + 1) + ' = %.5f \n' % x[i])
    print_message('\n')
    return


def jacobi(a, vector_b, eps, sizee):
    # Метод Якоби
    print_message('\nMethod Jacobi: \n')
    c = [vector_b[i] / a[i][i] for i in range(sizee)]  # b[i] / a[i][i]
    matrix_a = [[a[i][j] / a[i][i] for j in range(sizee)] for i in range(sizee)]  # a[i][j] / a[i][i]
    x = copy.deepcopy(c)  # начальное приближение
    # x = [1 for i in range(sizee)]
    norm = 1.0
    k = 0
    while norm > eps and k < LIMIT:
        k = k + 1
        norm = 0.0
        x_new = []
        for i in range(sizee):
            s = copy.deepcopy(c[i])
            for j in range(sizee):
                if j == i:
                    continue
                s -= matrix_a[i][j] * x[j]
            x_new.append(s)  # x_new[i] = b[i] / a[i][i] - сумма a[i][j] / a[i][i] * x[i], если i != j
            if math.fabs(x_new[i] - x[i]) > norm:  # считаем норму
                norm = math.fabs(x_new[i] - x[i])
        x = x_new
    print_message('Amount of iterations is ' + str(k) + '\n')
    if k == LIMIT:
        x = None
    return x


def zeidel(a, vector_b, eps, sizee):
    # Метод Зейделя
    print_message('\nMethod Zeidel: \n')
    c = [vector_b[i] / a[i][i] for i in range(sizee)]  # b[i] / a[i][i]
    matrix_a = [[a[i][j] / a[i][i] for j in range(sizee)] for i in range(sizee)]  # a[i][j] / a[i][i]
    x = copy.deepcopy(c)  # первая итерация x[i] = b[i] / a[i][i]
    #x = [1 for i in range(sizee)]
    norm = 1.0
    k = 0
    while norm > eps and k < LIMIT:
        k = k + 1
        norm = 0.0
        for i in range(sizee):
            x_new = c[i]
            for j in range(sizee):
                if j == i:
                    continue
                x_new -= matrix_a[i][j] * x[j]  # x_new[i] = b[i] / a[i][i] - сумма a[i][j] / a[i][i] * x[i],
                                                # если i != j
            if math.fabs(x_new - x[i]) > norm:  # считаем норму
                norm = math.fabs(x_new - x[i])
            x[i] = x_new
    print_message('Amount of iterations is ' + str(k) + '\n')
    if k == LIMIT:
        x = None
    return x


def print_vector(vector, symbol):
    # вывод вектора
    message = ''
    for i, val in enumerate(vector):
        message += symbol + "%x" % (i + 1) + " = %5.5f\n" % val
    print_message(message)
    return


if __name__ == '__main__':
    LIMIT = 100000
    import copy
    import math
    input_file_name = 'input4.txt'
    output_file_name = 'output.txt'

    f = open(output_file_name, 'w')  # очистим файл вывода
    f.close()
    del (f)
    a, b, eps, sizee = read_matrix()
    print_message('System of linear equations: \n')
    print_system(a, sizee, b)
    print_message('Eps = ' + str(eps) + '\n')
    solution = jacobi(a, b, eps, sizee)
    if not solution:
        print_message('Doesn\'t fit')
        exit(0)
    print_vector(solution, 'xj')
    solution = zeidel(a, b, eps, sizee)
    print_vector(solution, 'xz')