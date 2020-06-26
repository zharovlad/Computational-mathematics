from numpy import array
from numpy.linalg import solve
from math import sin, cos
output_file_name = 'output.txt'


class Test:
    def __init__(self, functions, jacobi_matrix, eps, initial_approximation):

        # список уравнений
        self.functions = functions

        # количество уравнений
        self.size = len(functions)

        # матрица якоби
        self.jacobi_matrix = jacobi_matrix

        # точность
        self.eps = eps

        # начальное приближение
        self.approximation = array(initial_approximation, dtype='float')

        self.amount_of_iterations = 0
        self.solution = None

    def solve_system(self):
        last_vector = self.approximation
        vector = last_vector + solve(self.get_jacobi_matrix(last_vector), self.get_B(last_vector))
        while self.amount_of_iterations < 10000 and max(abs(vector - last_vector)) > self.eps:
            self.amount_of_iterations += 1
            last_vector = vector
            vector = last_vector + solve(self.get_jacobi_matrix(last_vector), self.get_B(last_vector))
        self.solution = vector

    def print_result(self):
        with open(output_file_name, 'w') as w:
            w.write('Accuracy = ' + str(self.eps) + '\n')
            w.write('Initial approximation = ' + str(self.approximation) + '\n')
            w.write('Amount of iterations = ' + str(self.amount_of_iterations) + '\n')
            w.write('Solution: ' + str(self.solution) + '\n')
            discrepancy = abs(self.functions[0](*self.solution) - self.functions[1](*self.solution))
            w.write('Discrepancy: ' + str(discrepancy) + '\n')

    def get_jacobi_matrix(self, vector):
        matrix = []
        for row in self.jacobi_matrix:
            new_row = []
            for derivative in row:
                new_row.append(derivative(*vector))
            matrix.append(new_row)
        return array(matrix, dtype='float')

    def get_B(self, vector):
        result = []
        for f in self.functions:
            result.append(-f(*vector))
        return array(result, dtype='float')


if __name__ == '__main__':

    # f1 = lambda x, y: x ** 2 + y ** 2 / 4 - 1
    # f2 = lambda x, y: (x - 1) ** 2 + (y - 3) ** 2 - 25
    # jacobi_matrix = [
    #     [
    #         lambda x, y: 2 * x,
    #         lambda x, y: 0.5 * y
    #     ],
    #     [
    #         lambda x, y: 2 * (x - 1),
    #         lambda x, y: 2 * (y - 3)
    #     ]
    # ]

    f1 = lambda x, y: x ** 2 + y ** 2 - 1
    f2 = lambda x, y: y * sin(x)
    jacobi_matrix = [
        [
            lambda x, y: 2 * x,
            lambda x, y: 2 * y
        ],
        [
            lambda x, y: y * cos(x),
            lambda x, y: sin(x)
        ]
    ]

    functions = [f1, f2]
    test1 = Test(functions, jacobi_matrix, 0.0001, [1.0, -1.0])

    test = test1
    test.solve_system()
    test.print_result()
