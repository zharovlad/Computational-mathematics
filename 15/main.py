from math import sin, pi, exp
from numpy import linspace
import matplotlib.pyplot as plt
amount_of_dots = 5000  # для построения графика, если нужно построить бОльший интервал -> увеличить


class FiniteDifferenceMethod:

    def __init__(self, A=lambda x: 0.0, B=lambda x: -2 / (x ** 3 + x ** 2), C=lambda x: 0.0, a=1.0, b=2.0, F1=0.0,
                 D1=1.0, E1=-1.0, F2=1.0, D2=2.0, E2=1.0, u=lambda x: 1 + 1 / x, amount_of_steps=25):
        self.A = A
        self.B = B
        self.C = C
        self.a = a
        self.b = b
        self.F1 = F1
        self.D1 = D1
        self.E1 = E1
        self.F2 = F2
        self.D2 = D2
        self.E2 = E2
        self.u = u
        self.amount_of_steps = amount_of_steps

        self.h = (b - a) / (amount_of_steps - 1)
        self.u1_norm = []
        self.u2_norm = []
        self.steps = list(linspace(0.001, 0.35, 50))

    def first_approx(_, h=None, steps=None):
        if not h:
            h = _.h
            steps = _.amount_of_steps - 1
        a = [0.0]
        b = [_.D1 -_.F1 * h]
        c = [_.D1]
        d = [_.E1 * h]
        x = _.a
        for i in range(1, steps, 1):
            x += h
            a.append(1 - _.A(x) * h / 2)
            b.append(2 - _.B(x) * h ** 2)
            c.append(1 + _.A(x) * h / 2)
            d.append(_.C(x) * h ** 2)
        a.append(-_.D2)
        b.append(-_.F2 * h - _.D2)
        c.append(0.0)
        d.append(_.E2 * h)
        y = FiniteDifferenceMethod.solve_system(a, b, c, d)
        return y

    def second_approx(_, h=None, steps=None):
        if not h:
            h = _.h
            steps = _.amount_of_steps - 1
        a = [0.0]
        b = [-_.F1 * h + _.D1 + _.D1 * (_.A(_.a) - _.B(_.a) * h) * h / 2]
        c = [_.A(_.a) * _.D1 * h / 2 + _.D1]
        d = [_.E1 * h + _.C(_.a) * _.D1 * h ** 2 / 2]
        x = _.a
        for i in range(1, steps, 1):
            x += h
            a.append(1 - _.A(x) * h / 2)
            b.append(2 - _.B(x) * h ** 2)
            c.append(1 + _.A(x) * h / 2)
            d.append(_.C(x) * h ** 2)
        a.append(_.A(_.b) * _.D2 * h / 2 - _.D2)
        b.append(-_.F2 * h - _.D2 + _.D2 * (_.A(_.b) - _.B(_.b) * h) * h / 2)
        c.append(0.0)
        d.append(_.E2 * h + _.C(_.b) * _.D2 * h ** 2 / 2)
        y = FiniteDifferenceMethod.solve_system(a, b, c, d)
        return y

    @staticmethod
    def solve_system(a, b, c, d):
        """ Метод прогонки """
        alpha = [0]
        beta = [0]
        for i in range(0, len(d) - 1):
            alpha.append(c[i] / (b[i] - a[i] * alpha[i]))
            beta.append((a[i] * beta[i] - d[i]) / (b[i] - a[i] * alpha[i]))

        y = [0 for _ in range(len(d))]
        y[-1] = (a[-1] * beta[-1] - d[-1]) / (b[-1] - a[-1] * alpha[-1])
        for i in range(len(y) - 2, -1, -1):
            y[i] = alpha[i + 1] * y[i + 1] + beta[i + 1]

        return y

    def recount_C_norm(self):
        for step in self.steps:
            amount_of_steps = int((self.b - self.a) / step - 1)
            x = list(linspace(self.a, self.b, amount_of_steps))
            y = [self.u(xi) for xi in x]
            y1 = self.first_approx(step, amount_of_steps)
            y2 = self.second_approx(step, amount_of_steps)
            self.u1_norm.append(max([abs(y[i] - y1[i]) for i in range(len(y))]))
            self.u2_norm.append(max([abs(y[i] - y2[i]) for i in range(len(y))]))


def image_graphics(x, u, u1, u2, test):
    fig, ax = plt.subplots()
    plt.grid(True)
    ax.plot(x, u, label='u')
    ax.plot(x, u1, label='u first approx')
    ax.plot(x, u2, label='u second approx')

    plt.title('amount of steps = ' + str(test.amount_of_steps))
    plt.legend()
    plt.show()

    # fig, ax = plt.subplots()
    # plt.grid(True)
    # ax.plot(test.steps, test.u1_norm, label='u first approx')
    # ax.plot(test.steps, test.u2_norm, label='u second approx')
    # plt.legend()
    # plt.show()


if __name__ == '__main__':
    test = FiniteDifferenceMethod(amount_of_steps=500)

    x = list(linspace(test.a, test.b, test.amount_of_steps))
    y = [test.u(xi) for xi in x]
    y1 = test.first_approx()
    y2 = test.second_approx()
    test.recount_C_norm()

    image_graphics(x, y, y1, y2, test)
