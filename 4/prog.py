# lab 4 by @zharovlad
# во входном файле - 1 число размерность матрицы
# затем матрица
# точность eps
# начальный вектор строкой


def read_data():
    # чтение из файла входных данных
    readf = open(input_file_name, 'r')
    matr = []
    sizee = int(readf.readline())
    for i in range(sizee):
        line = readf.readline()
        s = line.split()
        array = [float(s[i]) for i in range(sizee)]
        matr.append(array)
    eps = float(readf.readline())
    line = readf.readline()
    s = line.split()
    vector = [float(s[i]) for i in range(sizee)]
    readf.close()
    return sizee, matr, eps, vector


def print_message(message):
    # печать сообщения в файл
    writef = open('output.txt', 'a')
    writef.write(message)
    writef.close()
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


def print_vector(vector, symbol):
    # вывод вектора
    message = ''
    for i, val in enumerate(vector):
        message += symbol + "%x" % (i + 1) + " = %5.5f\n" % val
    print_message(message)
    return


def scalar_product(v1, v2):
    # скалярное произведение
    s = 0
    if len(v1) != len(v2):
        s = None
    else:
        for each in range(len(v1)):
            s += v1[each] * v2[each]
    return s


def matrix_mul_vector(a, x):
    # умножение матрицы на вектор
    n = len(a)
    m = len(x)
    result = []
    for i in range(n):
        s = 0
        for j in range(m):
            s += x[j] * a[i][j]
        result.append(s)
    return result


def vector_norm(x):
    # поиск нормы вектора
    s = 0
    for each in x:
        s += each * each
    return math.sqrt(s)


def normed_vector(x):
    # нормирование вектора
    norm = vector_norm(x)
    for i in range(sizee):
        x[i] = x[i] / norm
    return x


def search_max_eigenvalue(a, eps, x):
    # поиск максимального собственного числа (lambda 1)
    # степенной метод
    matr = copy.deepcopy(a)
    for i in range(sizee):
        matr[i][i] += 3
    x_old = copy.deepcopy(x)
    e = LIMIT
    eigenvalue = LIMIT
    n = 0
    while e > eps:
        x_new = normed_vector(x_old)
        x_new = matrix_mul_vector(a, x_new)
        eigenvalue_new = scalar_product(x_new, x_old) / scalar_product(x_old, x_old)
        e = math.fabs(eigenvalue - eigenvalue_new)
        eigenvalue = math.fabs(eigenvalue_new)
        x_old = x_new
        n = n + 1
    return eigenvalue - 3, x_old, n


def column_x_string(a, b):
    # умножение столбца на строку (результат матрица)
    sizee = len(a)
    matrix = []
    for i in range(sizee):
        string = []
        for j in range(sizee):
            string.append(float(a[i] * b[j]))
        matrix.append(string)
    return matrix


def identify_symbol(a, eigenvalue):
    # определение знака собственного числа
    matr = copy.deepcopy(a)
    for i in range(len(matr)):
        matr[i][i] -= eigenvalue
    if numpy.linalg.det(matr) > 0.1:
        eigenvalue = -eigenvalue
    return eigenvalue


def search_second_eigenvalue(a, eps, x, sizee, eigenvalue_1, eigenvector_1):
    # поиск второго собственного числа и вектора
    # метод исчерпывания (матричный)
    # сначала ищем матрицу B = A - lambda1/(g1,e1) * e1 * g1(T)
    B = copy.deepcopy(a)
    p = copy.deepcopy(x)
    for i in range(sizee):
        p[i] = 1 / p[i]
        for j in range(sizee):
            B[i][j], B[j][i] = B[j][i], B[i][j]

    z , ev, p = search_max_eigenvalue(B, eps, p)
    const = eigenvalue_1 / scalar_product(eigenvector_1, ev)
    matr = column_x_string(eigenvector_1, ev)
    for i in range(sizee):
        for j in range(sizee):
            B[i][j] = a[i][j] - const * matr[i][j]

    # x2 = [x[i] - (scalar_product(x, eigenvector) / scalar_product(eigenvector, eigenvector) * eigenvector[i])
    #      for i in range(sizee)]

    # # Транспаниируем матрицу А
    #
    # matrix = copy.deepcopy(a)
    # for i in range(sizee):
    #     for j in range(i):
    #         matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # b, eigenvector_2, c = search_max_eigenvalue(matrix, eps, a[0])
    # const = eigenvalue_1 / scalar_product(eigenvector_1, eigenvector_2)
    # right_matrix = [[(i * j * const) for j in eigenvector_2] for i in eigenvector_1]
    # for i in range(sizee):
    #     for j in range(sizee):
    #         matrix[i][j] = a[i][j] - right_matrix[i][j]

    # у матрицы B те же собственные вектора, что и у матрицы A, а собственные числа 0,λ2,λ3,…,λm,
    # то есть наибольшим по модулю является собственное число  λ2. Применяя теперь степенной метод к матрице B,
    # найдем λ2 и e2.

    return search_max_eigenvalue(B, eps, x)



if __name__ == '__main__':
    LIMIT = 100000
    import copy
    import math
    import numpy
    input_file_name = 'input1.txt'
    output_file_name = 'output.txt'

    f = open(output_file_name, 'w')  # очистим файл вывода
    f.close()
    del (f)
    sizee, matr, eps, vector = read_data()
    print_message('Matrix:\n')
    print_matrix(matr, sizee)
    print_message('\nEps: ' + str(eps) + '\n')
    print_message('\nVector x0:\n')
    print_vector(vector, 'x')

    eigenvalue, eigenvector, amount_of_iteration = search_max_eigenvalue(matr, eps, vector)
    eigenvalue2 = identify_symbol(matr, eigenvalue)
    print_message('\nMax eigenvalue: \n' + str(eigenvalue2) + '\n')
    print_message('\nAppropriate eigenvector:\n')
    print_vector(eigenvector, 'e_')
    print_message('Amount of iteration: ' + str(amount_of_iteration) + '\n')

    matr2 = copy.deepcopy(matr)
    for i in range(sizee):
        matr2[i][i] -= eigenvalue
    eigenvalue2, eigenvector2, amount_of_iteration = search_max_eigenvalue(matr2, eps, vector)
    print_message('\nMin eigenvalue: \n' + str(eigenvalue2 + eigenvalue) + '\n')
    print_message('\nAppropriate eigenvector:\n')
    print_vector(eigenvector2, 'e_')
    print_message('Amount of iteration: ' + str(amount_of_iteration) + '\n')

    eigenvalue2, eigenvector2, amount_of_iteration = search_second_eigenvalue(matr2, eps, vector, sizee, eigenvalue,
                                                                            eigenvector)
    print_message('\nSecond modulus of eigenvalue: ' + str(eigenvalue2) + '\n')
    print_message('\nAppropriate eigenvector:\n')
    print_vector(eigenvector2, 'e2_')
    print_message('\nAmount of iteration: ' + str(amount_of_iteration) + '\n')
