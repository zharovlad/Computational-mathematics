# lab 2 by @zharovlad
def print_message(message):
    # печать сообщения в файл
    writef = open('output.txt', 'a')
    writef.write(message)
    writef.close()
    return


def read_matrix():
    # чтение из файла матрицы
    readf = open(input_file_name, 'r')
    matr = []
    for line in readf.readlines():
        array = []
        s = line.split()
        for each in s:
            number = float(each)
            array.append(number)
        matr.append(array)
    readf.close()
    return matr


def print_matrix(message, matrix, isEx):
    # вывод матрицы, isEx - расширена или нет матрица
    sizee = len(matrix)
    size2 = sizee
    if isEx:
        size2 += 1
    message += '\n'
    for i in range(sizee):
        for j in range(size2):
            if j == sizee and isEx:
                message += ' | '
            s = '%.5f' % matrix[i][j]
            message += s.ljust(15)
        message += '\n'
    print_message(message)
    return


def inversee(matrix):
    # нахождение обратной матрицы
    sizee = len(matrix)
    inv = [[0 for i in range(sizee)] for j in range(sizee)]
    for i in range(sizee):
        for j in range(sizee):
            if i == j:
                matrix[j][sizee] = 1.0
            else:
                matrix[j][sizee] = 0.0
        q = copy.deepcopy(matrix)
        vec_sol = sqroot(q)  # метод квадратного корня
        for k in range(len(vec_sol)):
            inv[k][i] = vec_sol[k]
    return inv


def get_vector_b(matrix):
    # получение вектора b из расширенной матрицы
    sizee = len(matrix)
    vector_b = []
    for i in range(sizee):
        vector_b.append(matrix[i][sizee])
    return vector_b


def print_vector(vector, symbol):
    # вывод вектора
    message = ''
    for i, val in enumerate(vector):
        message += symbol + "%x" % (i + 1) + " = %5.5f\n" % val
    print_message(message)
    return


def matrix_mul(a, x):
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


def get_G(a):
    # находим матрицу G
    sizee = int(len(a))
    g = [[0.0 for i in range(sizee)] for j in range(sizee)]
    g[0][0] = math.sqrt(a[0][0])
    for i in range(1, sizee):
        g[0][i] = a[0][i] / g[0][0]

    for i in range(sizee):
        if i != 0:
            temp = 0
            for k in range(i):
                temp = temp + g[k][i] ** 2.0
            g[i][i] = math.sqrt(a[i][i] - temp)
        for j in range(sizee):
            if i >= j:
                continue
            temp = 0.0
            for k in range(i):
                temp += g[k][i] * g[k][j]
            g[i][j] = (a[i][j] - temp) / g[i][i]
    return g


def determinant(g):
    # нахождение определителя
    sizee = len(g)
    det = 1
    for i in range(sizee):
        det *= g[i][i]
    if det < eps:
        det = 0.0
    return det * det


def search_solution(G, b):
    # методом обратного хода
    # G*Y = B, Gt*X = Y
    sizee = len(G)
    y = [0 for i in range(sizee)]
    y[0] = b[0] / G[0][0]
    for i in range(1, sizee):
        temp = 0
        for k in range(i):
            temp += G[k][i] * y[k]
        y[i] = (b[i] - temp) / G[i][i]
    x = [0 for i in range(sizee)]
    x[sizee - 1] = y[sizee - 1] / G[sizee - 1][sizee - 1]
    for i in range(sizee - 2, -1, -1):
        temp = 0
        for k in range(i + 1, sizee):
            temp += G[i][k] * x[k]
        x[i] = (y[i] - temp) / G[i][i]
    return x


def sqroot(a):
    # метод квадратного корня
    b = get_vector_b(a)
    G = get_G(a)
    det = determinant(G)

    if det == 0.0:
        print_message('Singular matrix.\n')
        exit(1)

    solution = search_solution(G, b)
    return solution


def discrepancy(a, b):
    # нахождение невязки
    result = []
    sizee = len(b)
    for i in range(sizee):
        result.append(b[i] - a[i])
    return result


def norm(matrix):
    # вычисление нормы
    sizee = len(matrix)
    max = 0
    for i in range(sizee):
        sum = 0
        for j in range(sizee):
            sum += abs(matrix[i][j])
            if max < sum:
                max = sum
    return max


if __name__ == '__main__':
    import numpy
    import math
    import copy
    eps = 1e-10  # погрешность
    input_file_name = 'input3.txt'
    output_file_name = 'output.txt'

    f = open(output_file_name, 'w')  # очистим файл вывода
    f.close()
    del (f)

    a = numpy.loadtxt(input_file_name, float)
    print_matrix('System of linear equations: ', a, True)
    clean_matrix = copy.deepcopy(a)
    b = get_vector_b(a)
    G = get_G(a)
    print_matrix('\nGT: ', G, False)
    det = determinant(G)
    message = '\nDeterminant = %5.5f\n' % det
    print_message(message)

    if det == 0.0:
        print_message('Singular matrix.\n')
        exit(1)

    print_message('\nSolution of the system: \n')
    solution = search_solution(G, b)
    print_vector(solution, 'x')

    res = matrix_mul(clean_matrix, solution)
    print_message('\nMultiplication AX: \n')
    print_vector(res, 'ax')
    dis = discrepancy(res, b)
    print_message("\nDiscrepancy: \n")
    print_vector(dis, 'dis')

    inv = inversee(a)
    print_matrix('\nInverse: ', inv, False)

    # нахождение числа обусловленности
    n = norm(clean_matrix)
    message = '\nNorm input matrix = %5.5f\n' % n
    n = norm(inv)
    message += 'Norm inverse matrix = %5.5f\n' % n
    message += 'Condition number = %5.5f\n' % (n * norm(clean_matrix))
    print_message(message)
