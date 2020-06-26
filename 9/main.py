from numpy import linspace
output_file_name = 'output.txt'

class Test:
    def __init__(self, f, x_min, x_max, step):
        self.f = f
        self.x_min = x_min
        self.x_max = x_max
        self.h = step
        self.x = list(linspace(x_min, x_max, (x_max - x_min) / step + 1))

    # краткое описание всех методов находится в отчете

    def middle_rectangle(self):
        """ Считает приблизительное значение определенного интеграла методом средних прямоугольников """
        result = 0.0
        for i in range(len(self.x) - 1):
            result += self.f(self.x[i] + self.h / 2) * self.h
        return result

    def left_rectangle(self):
        """ Считает приблизительное значение определенного интеграла методом левых прямоугольников """
        result = 0.0
        for i in range(len(self.x) - 1):
            result += self.f(self.x[i]) * self.h
        return result

    def right_rectangle(self):
        """ Считает приблизительное значение определенного интеграла методом правых прямоугольников """
        result = 0.0
        for i in range(1, len(self.x), 1):
            result += self.f(self.x[i]) * self.h
        return result

    def trapezoid(self):
        """ Считает приблизительное значение определенного интеграла методом трапеции """
        result = 0.0
        for i in range(len(self.x) - 1):
            result += (self.f(self.x[i]) + self.f(self.x[i + 1])) * self.h / 2.0
        return result

    def simpson(self):
        """ Считает приблизительное значение определенного интеграла методом Симпсона """
        result = 0.0
        #for i in range(1, len(self.x) - 1, 2):
        #    result += (self.h / 3) * (self.f(self.x[i - 1]) + 4 * self.f(self.x[i]) + self.f(self.x[i + 1]))
        for i in range(len(self.x) - 1):
           result += (self.h / 6) * (self.f(self.x[i]) + 4 * self.f(self.x[i] + self.h / 2) + self.f(self.x[i + 1]))
        return result

class Auto(Test):
    def __init__(self, f, x_min, x_max, eps):
        Test.__init__(self, f, x_min, x_max, 1.0)
        self.eps = eps

    def auto_rec(self):
        """ Определяет шаг автоматически для метода прямоугольников, для заданной точности """
        stack = []
        amount_of_intervals = 0
        for x in self.x:
            stack.append(x)
        result = 0
        while len(stack) != 1:
            element1 = stack.pop(0)
            element3 = stack[0]
            step = element3 - element1
            element2 = element1 + step / 2

            # площадь целого интеграла
            I = self.f(element2) * step

            # площадь двух половинок
            small_I = self.f(element1 + (step / 4)) * (step / 2) + \
                             self.f(element2 + (step / 4)) * (step / 2)

            if abs(I - small_I) <= (self.eps * step) / self.x_max - self.x_min:
                result += I
                amount_of_intervals += 1
            else:
                stack.insert(0, element2)
                stack.insert(0, element1)

        return result, amount_of_intervals

    def auto_trapezoid(self):
        """ Определяет шаг автоматически для метода трапеций, для заданной точности """
        stack = []
        amount_of_intervals = 0
        for x in self.x:
            stack.append(x)
        result = 0
        while len(stack) != 1:
            # result += (self.f(self.x[i]) + self.f(self.x[i + 1])) * self.h / 2.0
            element1 = stack.pop(0)
            element3 = stack[0]
            step = element3 - element1
            element2 = element1 + step / 2

            # площадь целого интеграла
            I = (self.f(element1) + self.f(element3)) * step / 2

            # площадь двух половинок
            small_I = (self.f(element1) + self.f(element2)) * step / 4 + \
                             (self.f(element3) + self.f(element2)) * step / 4

            if abs(I - small_I) <= (self.eps * step) / self.x_max - self.x_min:
                result += I
                amount_of_intervals += 1
            else:
                stack.insert(0, element2)
                stack.insert(0, element1)

        return result, amount_of_intervals

    def auto_simpson(self):
        """ Определяет шаг автоматически для метода Симпсона, для заданной точности """
        stack = []
        amount_of_intervals = 0
        for x in self.x:
            stack.append(x)
        result = 0
        while len(stack) != 1:
            # result += (self.h / 6) * (self.f(self.x[i]) + 4 * self.f(self.x[i] + self.h / 2) + self.f(self.x[i + 1]))
            element1 = stack.pop(0)
            element3 = stack[0]
            step = element3 - element1
            element2 = element1 + step / 2

            # площадь целого интеграла
            I = (step / 6) * (self.f(element1) + 4 * self.f(element2) + self.f(element3))

            step15 = element2 - element1
            element15 = element1 + step15 / 2

            step25 = element3 - element2
            element25 = element2 + step25 / 2

            # площадь двух половинок
            small_I = (step15 / 6) * (self.f(element1) + 4 * self.f(element15) + self.f(element2)) + \
                             (step25 / 6) * (self.f(element2) + 4 * self.f(element25) + self.f(element3))

            if abs(I - small_I) <= (self.eps * step) / self.x_max - self.x_min:
                result += I
                amount_of_intervals += 1
            else:
                stack.insert(0, element2)
                stack.insert(0, element1)

        return result, amount_of_intervals


if __name__ == '__main__':
    test1 = Test(lambda x: x * x * x * x + 4 * x * x * x, 0, 3, 0.001)
    test2 = Test(lambda x: 3 * x * x, 0, 2, 0.1)
    auto = Auto(lambda x: 3 * x * x, 0, 2, 0.00001)
    with open(output_file_name, 'w') as w:
        test = test2
        w.write('step ' + str(test.h) + '\n')
        w.write('left_rectangle ' + str(test.left_rectangle()) + '\n')
        w.write('right_rectangle ' + str(test.right_rectangle()) + '\n')
        w.write('middle_rectangle ' + str(test.middle_rectangle()) + '\n')
        w.write('trapezoid ' + str(test.trapezoid()) + '\n')
        w.write('Simpson ' + str(test.simpson()) + '\n')

        res, am = auto.auto_rec()
        w.write('\n')
        w.write('accuracy ' + str(auto.eps) + '\n')
        w.write('middle_rectangle ' + str(res) + '\n')
        w.write('amount of steps ' + str(am) + '\n')

        res, am = auto.auto_trapezoid()
        w.write('\n')
        w.write('trapezoid ' + str(res) + '\n')
        w.write('amount of steps ' + str(am) + '\n')

        res, am = auto.auto_simpson()
        w.write('\n')
        w.write('Simpson ' + str(res) + '\n')
        w.write('amount of steps ' + str(am) + '\n')



