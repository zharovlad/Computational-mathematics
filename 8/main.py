import math
from numpy import linspace
from matplotlib import pyplot as plt
from random import uniform

input_file_name = 'input.txt'
output_file_name = 'output.txt'

class Test():
    def __init__(self, x_left, x_right, f, d1, d2, d3, step):
        """ x_left, x_right - границы, f - функция, d - производные 1,2,3 порядка,
        дельта - шаг для вычисления значения функций и производных """

        self.x_left = x_left
        self.x_right = x_right
        self.f = f
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3

        # считаем x и y
        self.x_array = list(linspace(self.x_left, self.x_right, (self.x_right - self.x_left) / step + 1))
        # x с возмущениями delta
        self.x_array = [x + uniform(0, 0.01) for x in self.x_array]
        self.y_array = [f(x) for x in self.x_array]
        #self.y_array = [x + uniform(0, 0.001) for x in self.y_array]

        # считаем значения производных
        self.y_d1 = [d1(x) for x in self.x_array]
        self.y_d2 = [d2(x) for x in self.x_array]
        self.y_d3 = [d3(x) for x in self.x_array]

        # численное дифференцирование
        self.y_d1_L = self.get_first_derivative()
        self.y_d2_L = self.get_second_derivative()
        self.y_d3_L = self.get_third_derivative()

        self.printing()
        self.image_derivate()

    def get_first_derivative(self):
        h = self.x_array[1] - self.x_array[0]
        derivative = [math.nan]
        for i in range(1, len(self.x_array) - 1, 1):
            derivative.append((self.y_array[i + 1] - self.y_array[i - 1]) / (2 * h))
        derivative.append(math.nan)
        return derivative

    def get_second_derivative(self):
        h = self.x_array[1] - self.x_array[0]
        derivative = [math.nan]
        for i in range(1, len(self.x_array) - 1, 1):
            derivative.append((self.y_array[i - 1] - 2 * self.y_array[i] + self.y_array[i + 1]) / (h * h))
        derivative.append(math.nan)
        return derivative

    def get_third_derivative(self):
        h = self.x_array[1] - self.x_array[0]
        derivative = [math.nan, math.nan]
        for i in range(2, len(self.x_array) - 2, 1):
            derivative.append((self.y_array[i + 2] - 2 * self.y_array[i + 1] + 2 * self.y_array[i - 1] -
                               self.y_array[i - 2]) / (2 * h * h * h ))
        for i in range(2):
            derivative.append(math.nan)
        return derivative

    def image_derivate(self):
        fig, (d1, d2, d3) = plt.subplots(1, 3)

        d1.set_title('1 derivate')
        d1.plot(self.x_array, self.y_d1, label='derivate')
        d1.plot(self.x_array, self.y_d1_L, label='approximation')
        d1.legend()

        d2.set_title('2 derivate')
        d2.plot(self.x_array, self.y_d2, label='derivate')
        d2.plot(self.x_array, self.y_d2_L, label='approximation')
        d2.legend()

        d3.set_title('3 derivate')
        d3.plot(self.x_array, self.y_d3, label='derivate')
        d3.plot(self.x_array, self.y_d3_L, label='approximation')
        d3.legend()

        plt.show()

    def printing(self):
        with open(output_file_name, 'w') as w:
            for i in range(len(self.x_array)):
                w.write('%.10f' % self.x_array[i])
                w.write('   ')
                w.write('%.10f' % self.y_d1[i])
                w.write('   ')
                w.write('%.10f' % self.y_d1_L[i])
                w.write('   ')
                w.write('%.10f' % self.y_d2[i])
                w.write('   ')
                w.write('%.10f' % self.y_d2_L[i])
                w.write('   ')
                w.write('%.10f' % self.y_d3[i])
                w.write('   ')
                w.write('%.10f' % self.y_d3_L[i])
                w.write('\n')

if __name__ == '__main__':

    test1 = Test(-5.0, 5.0, math.exp, math.exp, math.exp, math.exp, 0.01)

    # test2 = Test(-5.0, 5.0,
    #              lambda x: x * x * x + 5 * x * x - 7 * x + 3,
    #              lambda x: 3 * x * x + 10 * x - 7,
    #              lambda x: 6 * x + 10,
    #              lambda x: 6,
    #              0.1)

    # test3 = Test(-5.0, 5.0,
    #              lambda x: x * x * x * x + 5 * x * x * x - 7 * x * x + 3 * x - 3,
    #              lambda x: 4 * x * x * x + 15 * x * x - 14 * x + 3,
    #              lambda x: 12 * x * x + 30 * x - 14,
    #              lambda x: 24 * x + 30,
    #              0.01)

    #test4 = Test(-2 * math.pi, 2 * math.pi, math.sin, math.cos, lambda x: -math.sin(x), lambda x: -math.cos(x), 0.01)


