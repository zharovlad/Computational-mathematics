# lab 1 by @zharovlad


def printMessage(message):
    # печать сообщения в файл
    writef = open('output.txt', 'a')
    writef.write(message)
    writef.close()
    return


def readMatrix():
    # чтение из файла матрицы
    readf = open(inputFileName, 'r')
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


def printMatrix(message, matrix, isEx):
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
    printMessage(message)
    return


def triangle(matrix):
    # приведение матрицы к треугольному виду
    sizee = len(matrix)
    countSwap = 0  # для подсчета количества перестановок строк
    for j in range(sizee):
        countSwap = maxElem(matrix, j, countSwap)
        for i in range(j + 1, sizee):
            c = float(matrix[i][j] / matrix[j][j])  # c - const, чтобы получить в j-ой строке 0
            subtraction(matrix, i, j, c)
    return countSwap


def maxElem(matrix, column, countSwap):
    # ищем максимальный элемент в столбце и
    # перемещам строку так, чтобы этот элемент был на главной диагонали
    sizee = len(matrix)
    maxEl = matrix[column][column]
    maxRow = column
    for i in range(column + 1, sizee):
        # поиск максимального
        if abs(matrix[i][column]) > maxEl:
            maxEl = abs(matrix[i][column])
            maxRow = i
    if maxRow != column:
        # меняем местами если нужно и увеличиваем счетчик
        swap(matrix, maxRow, column, column)
        countSwap += 1
    return countSwap


def swap(matrix, row1, row2, elem):
    # меняем местами row1 и row2 начиная с elem (0 не меняем местами)
    sizee = len(matrix) + 1
    for i in range(elem, sizee):
        temp = matrix[row1][i]
        matrix[row1][i] = matrix[row2][i]
        matrix[row2][i] = temp
    return


def subtraction(matrix, row1, row2, c):
    # вычитание row1 - row2 * c
    for i in range(row2, len(matrix[0])):
        matrix[row1][i] -= matrix[row2][i] * c
        if abs(matrix[row1][i]) <= eps:
            matrix[row1][i] = 0.0
    return


def determinant(matrix, count):
    # нахождение определителя
    sizee = len(matrix)
    det = 1
    for i in range(sizee):
        det *= matrix[i][i]
    if count % 2:
        det *= -1
    if abs(det) <= eps:
        det = 0.0
    return det


def inversee(matrix):
    # нахождение обратной матрицы методом Жордана-Гаусса
    sizee = len(matrix)
    inv = [[0 for i in range(sizee)] for j in range(sizee)]
    for i in range(sizee):
        for j in range(sizee):
            if i == j:
                matrix[j][sizee] = 1.0
            else:
                matrix[j][sizee] = 0.0
        q = copy.deepcopy(matrix)
        vec_sol = gauss(q)
        for k in range(len(vec_sol)):
            inv[k][i] = vec_sol[k]
    return inv


def gauss(matrix):
    # метод Гаусса
    count_swap = triangle(matrix)
    det = determinant(matrix, count_swap)
    if abs(det) < eps:
        printMessage("\nSingular matrix\n")
        exit(1)
    x = searchSolution(matrix)
    return x


def searchSolution(matrix):
    # находим решение из полученной треугольной матрицы методом обратного хода
    sizee = len(matrix)
    solution = [0 for i in range(sizee)]
    for i in range(sizee - 1, -1, -1):
        solution[i] = matrix[i][sizee] / matrix[i][i]
        for j in range(i - 1, -1, -1):
            matrix[j][sizee] -= matrix[j][i] * solution[i]
    return solution


def getVectorB(matrix):
    # получение вектора b из расширенной матрицы
    sizee = len(matrix)
    vectorB = []
    for i in range(sizee):
        vectorB.append(matrix[i][sizee])
    return vectorB


def printVector(vector, symbol):
    # вывод вектора
    message = ''
    for i, val in enumerate(vector):
        message += symbol + "%x" % (i + 1) + " = %5.5f\n" % val
    printMessage(message)
    return


def matrixMul(a, x):
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
    import copy
    eps = 1e-10  # погрешность
    inputFileName = 'input4.txt'
    outputFileName = 'output.txt'

    f = open(outputFileName, 'w')  # очистим файл вывода
    f.close()
    del (f)

    matrix = numpy.loadtxt(inputFileName, float)
    printMatrix('System of linear equations: ', matrix, True)
    cleanMatrix = copy.deepcopy(matrix)

    # приведем к треугольной матрице
    countSwap = triangle(matrix)
    printMatrix('\n\nTriangle matrix: ', matrix, True)

    # считаем определитель
    det = determinant(matrix, countSwap)
    message = '\nDeterminant = %5.5f\n' % det
    printMessage(message)

    if det == 0.0:
        printMessage('Singular matrix.\n')
        exit(1)

    # ищем решение системы
    printMessage('\nSolution of the system: \n')
    solution = searchSolution(matrix)
    printVector(solution, 'x')

    # ищем невязку
    b = getVectorB(cleanMatrix)
    printMessage('\nVector B:\n')
    printVector(b, 'b')
    res = matrixMul(cleanMatrix, solution)
    message = '\nMultiplication AX: \n'
    printMessage(message)
    printVector(res, 'ax')
    dis = discrepancy(res, b)
    printMessage("\nDiscrepancy: \n")
    printVector(dis, 'dis')

    # обратная матриица
    inv = inversee(cleanMatrix)
    printMatrix('\nInverse matrix', inv, False)

    # нахождение числа обусловленности
    n = norm(cleanMatrix)
    message = '\nNorm input matrix = %5.5f\n' % n
    n = norm(inv)
    message += 'Norm inverse matrix = %5.5f\n' % n
    message += 'Condition number = %5.5f\n' % (n * norm(cleanMatrix))
    printMessage(message)
