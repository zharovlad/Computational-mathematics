output_file_name = 'output.txt'

class Test:
    def __init__(self, interval_begin, interval_end, eps, step, f, d1, d2):

        # решение ищется на заданном отрезке [interval_begin, interval_end]
        self.interval_begin = interval_begin
        self.interval_end = interval_end

        # с точностью eps и шагом step
        self.eps = eps
        self.step = step

        # функция и 1-ая и 2-ая её производные
        self.f = f
        self.d1 = d1
        self.d2 = d2

        # в этом списке хранятся решения, на каком интервале они найдены, количество итераций, невязка
        self.solutions = []

    def find_solution(self):
        """ Решение нелинейного уравнения комбинированным методом """
        # помечаем границы первого интервала
        interval_begin = self.interval_begin
        interval_end = self.interval_begin + self.step

        # проверим решение в начале отрезка совпадающим с началом первого интервала
        if abs(self.f(interval_begin)) < self.eps:
            self.solutions.append(Solution(interval_begin, interval_begin, interval_end))

        # теперь исследуем каждый интервал
        while True:

            # если решение на границе, то добавляем его в список решений
            if abs(self.f(interval_end)) < self.eps:
                self.solutions.append(Solution(interval_end, interval_begin, interval_end))

            # если значение функций на границах интервала с разным знаком, значит на этом интервале есть решение
            elif self.f(interval_begin) * self.f(interval_end) < 0:
                self.find_solution_on_interval(interval_begin, interval_end)

            # изменяем интервал
            interval_begin = interval_end
            interval_end += self.step

            # чтобы не уйти за границу заданного отрезка, нужно подкорректировать интервал
            if interval_end > self.interval_end:
                interval_end = self.interval_end

            if interval_begin == interval_end:
                break
        return


    def find_solution_on_interval(self, interval_begin, interval_end):
        """ Поиск решения на отрезке """
        a = interval_begin
        b = interval_end
        i = 0
        while abs(a - b) > self.eps:
            if self.d2(a) * self.f(a) > 0.0:
                a = a - (self.f(a) / self.d1(a))
            else:
                a = a - self.f(a) * (a - b) / (self.f(a) - self.f(b))
            if self.d2(b) * self.f(b) > 0.0:
                b = b - self.f(b) / self.d1(b)
            else:
                b = b - self.f(b) * (b - a) / (self.f(b) - self.f(a))
            i += 1
        self.solutions.append(Solution((a + b) / 2, a, b, i, abs(a - (a + b) / 2)))

    def print_result(self):
        with open(output_file_name, 'w') as w:
            if len(self.solutions):
                strlen = 69

                w.write('Interval = [ %.1f ; %.1f ]\n' % (self.interval_begin, self.interval_end))
                w.write('Accuracy = %f\n' % self.eps)
                w.write('Step     = %f\n' % self.step)

                w.write('*' * strlen + '\n')
                w.write('* ' + 'Result'.center(12) + ' * ')
                w.write('Interval'.center(21) + ' * ')
                w.write('Iterations' + ' * ')
                w.write(' Discrepancy ' + ' *\n')
                w.write('*' * strlen + '\n')
                for each in self.solutions:
                    w.write('* %.10f * ' % each.value)
                    w.write(' [%.6f; %.6f] * ' % (each.interval[0], each.interval[1]))
                    w.write(str(each.iterations).center(10) + ' * ')
                    w.write(' %.10f *\n' % each.discrepancy)
                    w.write('*' * strlen + '\n')
            else:
                w.write('There are no solutions. Try to change step or interval.')



class Solution:
    def __init__(self, value, interval_begin, interval_end, iterations=0, discrepancy=0.0):
        self.value = value
        self.interval = (interval_begin, interval_end)
        self.iterations = iterations
        self.discrepancy = discrepancy


if __name__ == '__main__':
    # function = lambda x: 5 * x * x * x * x
    # dfunction1 = lambda x: 20 * x * x * x
    # dfunction2 = lambda x: 60 * x * x
    # test1 = Test(-50.0, 50.0, 0.0001, 0.3, function, dfunction1, dfunction2)

    function = lambda x: x * x * x - 7 * x * x + 10 * x
    dfunction1 = lambda x: 3 * x * x - 14 * x + 10
    dfunction2 = lambda x: 6 * x - 14
    test2 = Test(-10.0, 10.0, 0.001, 0.5, function, dfunction1, dfunction2)

    test = test2

    test.find_solution()
    test.print_result()
