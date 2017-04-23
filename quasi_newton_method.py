# Quasi-Newton method
import math
import matrix
import excel_transfer
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import mlab

from matplotlib.path import Path
import matplotlib.patches as patches



from resource import expression


class QNM:
    def __init__(self):
        self.commands = {
            "commands": {
                "none": 0,
                "exit": 1,
                "test": 2,
                "clear": 3,
                "help": 4,
                "new": 5,
                "show slist": 6,
                "show scount": 7,
                "acc": 8,
                "mk": 9,
                "start": 10,
                "show result": 11,
                "image 1": 12,
                "image 2": 13
            },
            "description": {
                "none": "do nothing",
                "exit": "exit from module",
                "test": "do test stuff",
                "clear": "clear something",
                "help": "display helpfull information",
                "new": "enter new raw data",
                "show slist": "show raw data",
                "show scount": "show something",
                "acc": "set accuracy",
                "mk": "set default raw data",
                "start": "start calculation process",
                "show result": "show result",
                "image 1": "show 2D visualization",
                "image 2": "show 3D visualization"
            }
        }
        self.hg = matrix.Matrix([[0]], "Hessian matrix")
        self.hg.makedimatrix(2)
        self.ac = matrix.Matrix([[0]], "Correction matrix")
        self.expression = expression.Expression("No name", "x**2")
        self.accuracy = 3

        self.previous_s = matrix.Vector([0.0, 0.0], "previous Vector S")
        self.s = matrix.Vector([0.0, 0.0], "Vector S")
        self.previous_g = matrix.Vector([0.0, 0.0], "previous Gradient")
        self.g = matrix.Vector([0.0, 0.0], "Gradient")


        self.epsilon = [1, 1]
        self.mm = True
        self.msycle = 3
        self.cof = {"a": 1.0, "g": 2.0, "b": 0.5, "h": 0.001}
        self.result = {"i": [], "xk": [], "fx": [], "action": []}
        self.makedefault()



    def showCommands(self):
        print('')
        print("Commands...")
        print("---")
        for item in self.commands["commands"]:
            print(str(item) + ":")
            print("Number: " + str(self.commands["commands"][item]))
            print("Description: " + str(self.commands["description"][item]))
            print("---")

    def enterCommand(self):
        command = "0"
        print('')
        print("Enter command (help for Q&A)")
        while (command not in self.commands):
            command = input("->")
            if (command not in self.commands["commands"]):
                print("There is no such command")
            else:
                return self.commands["commands"][command]

    def showHelp(self):
        print('')
        print("Help v0.002")
        self.showCommands()

    def makedefault(self):
        self.epsilon[0] = 10 ** (-self.accuracy)
        self.epsilon[1] = self.epsilon[0]
        #self.expression = expression.Expression("Function", "4*(x1-2)**2+(x2-1)**2")
        #self.expression = expression.Expression("Function", "4*(x1-5)**2+(x2-6)**2")

        #self.expression = expression.Expression("Function", "3*x1**2+2*x1*x2+2*x2**2")

        self.expression = expression.Expression("Function", "2*x1**2+2*x1*x2+3*x2**2")

        self.expression.parameters["unimodal"] = True
        self.expression.parameters["global_min"] = [2.0, 1.0]
        #self.x_start = [[8.0, 9.0], [10.0, 11.0], [8.0, 11.0]]
        #self.x_start = [7.0, 6.0]
        self.x_start = [6.0, 4.0]
        self.cof = {"a": 1.0, "g": 2.0, "b": 0.5, "h": 0.001}
        self.result = {"i": [], "xk": [], "fx": [], "action": []}
        self.hg = matrix.Matrix([[0]], "Hessian matrix")
        self.hg.makedimatrix_f(2)
        self.ac.makedimatrix_f(len(self.x_start))

        self.previous_s = matrix.Vector([0.0 for _ in self.x_start], "previous Vector S")
        self.s = matrix.Vector([0.0 for _ in self.x_start], "Vector S")
        self.previous_g = matrix.Vector([0.0 for _ in self.x_start], "previous Gradient")
        self.g = matrix.Vector([0.0 for _ in self.x_start], "Gradient")


    def importparam(self, accuracy):
        self.accuracy = accuracy

    def setaccuracy(self):
        task = 0
        print('')
        print("Enter accuracy:")
        while (task != 1):
            self.accuracy = int(input("-> "))
            print("Input is correct? (enter - yes/n - no)")
            command = input("-> ")
            if (command != "n"):
                task = 1
            else:
                if self.accuracy < 0:
                    print("Please enter positive number!")
                    task = 0
        self.epsilon[0] = 10 ** (-self.accuracy)
        self.epsilon[1] = self.epsilon[0]

    def inputnewdata(self):
        self.expression.input_expr()
        self.expression.input_range()
        pass

    def dostaff(self):
        task = 0
        while (task != 1):
            print('')
            print("Quasi-Newton method")
            print('')
            task = self.enterCommand()
            if task == 2:
                pass
            elif task == 3:
                pass
            elif task == 4:
                self.showHelp()
            elif task == 5:
                self.inputnewdata()
            elif task == 6:
                self.print_raw_data()
            elif task == 8:
                self.setaccuracy()
            elif task == 9:
                self.makedefault()
            elif task == 10:
                self.resolve()
            elif task == 11:
                self.printresult()

            elif task == 12:
                self.printresult_g()
            elif task == 13:
                self.printresult_3d()
        pass

    def print_raw_data(self):
        self.expression.show_expr()
        pass

    def resolve(self):
        self.makedefault()
        k = 0
        x_w = self.x_start.copy()
        self.ac.makedimatrix_f(len(x_w))
        turn = True
        x_w = self.x_start.copy()
        hg = self.get_hessian_matrix(x_w)

        self.previous_s = matrix.Vector([0.0 for _ in self.x_start], "previous Vector S")
        self.s = matrix.Vector([0.0 for _ in self.x_start], "Vector S")

        self.g = matrix.Vector(self.get_gradient(x_w), "Gradient")
        self.previous_g = matrix.Vector(self.g.vector, "previous Gradient")
        print("Get lambda...")
        clambda = 1
        print("Get lambda ok")
        f_x_w = self.expression.execute_l(x_w)

        self.s.vector = self.mul(self.g.vector, -1.0)
        self.s.showvector()

        self.collect_data(k, x_w, f_x_w, "Initial point")

        k += 1
        print("step", k)
        print("-----------------------------")
        print("c_lambda", clambda)
        self.s.vector = self.mul(self.s.vector, clambda)

        self.s.showvector()
        x_w = self.sum(x_w, self.s.vector)
        self.previous_g.vector = self.g.vector.copy()
        self.g.vector = self.get_gradient(x_w)

        self.g.showvector()
        self.previous_g.showvector()

        f_x_w = self.expression.execute_l(x_w)
        self.ac.chel(0, 1, 1.0)
        self.ac.chel(1, 0, 1.0)
        self.ac.showmatrix()

        self.collect_data(k, x_w, f_x_w, "First special point")

        print("-----------------------------")

        while self.halting_check() and k < 60 and self.norm(self.s.vector) > 0.1:

            k += 1
            print("step", k)
            print("-----------------------------")
            self.set_correction_matrix(x_w)
            self.ac.showmatrix()

            name = self.s.name
            self.s = self.ac.matrixmv(self.g, 20)
            self.s.vector = self.mul(self.s.vector, -1.0)
            self.s.rename(name)
            self.s.showvector()

            clambda = self.get_lambda(x_w)
            print("c_lambda", clambda)
            self.s.vector = self.mul(self.s.vector, clambda)
            self.s.showvector()

            x_w = self.sum(x_w, self.s.vector)
            self.previous_g.vector = self.g.vector.copy()
            self.g.vector = self.get_gradient(x_w)

            self.g.showvector()
            self.previous_g.showvector()

            f_x_w = self.expression.execute_l(x_w)

            self.collect_data(k, x_w, f_x_w, "Next point")

            print("-----------------------------")

        self.printresult()

    def get_hessian_matrix(self, x_w):
        hg = matrix.Matrix([[0]], "Hessian matrix")
        hg.makedimatrix(2)
        #hg = matrix.copy()
        i = 0
        item = 0.0
        while i < hg.len[0]:
            j = 0
            while j < hg.len[1]:
                # warning!!! only for x1, x2!!!!
                item = self.expression.diff2_derivative_pi2_l(x_w, self.cof["h"], i, j)
                hg.chel(i, j, item)
                j += 1
            i += 1

        return hg

    def set_correction_matrix(self, x_w):
        print("Point", x_w)
        print("Previous point", self.result["xk"][-2])
        delta_x = matrix.Vector(self.dif(x_w, self.result["xk"][-2]), "Delta x")
        delta_grad = matrix.Vector(self.dif(self.g.vector, self.previous_g.vector), "Delta gradient")

        delta_x.showvector()
        delta_grad.showvector()

        matrix_1 = delta_x.vhm(delta_x, 20)
        try:
            cof = 1.0 / delta_x.hvm(delta_grad, 20)
        except ZeroDivisionError:
            cof = 1.0 / float('Inf')

        print("cof", cof)
        matrix_1.matrixmnum(cof, 20)
        matrix_1.rename("matrix 1")
        matrix_1.showmatrix()

        matrix_2 = delta_grad.vhm(delta_grad, 20)
        matrix_2 = self.ac.matrixm(matrix_2, 20)
        matrix_2 = matrix_2.matrixm(self.ac, 20)

        vector = self.ac.matrixmv(delta_grad, 20)

        try:
            cof = 1.0 / delta_x.hvm(vector, 20)
        except ZeroDivisionError:
            cof = 1.0 / float('Inf')

        matrix_2.matrixmnum(cof, 20)

        matrix_1.matrixsubtract(matrix_2, 20)

        name = self.ac.name
        self.ac = self.ac.matrixsum(matrix_1, 20)
        self.ac.rename(name)

    def get_lambda(self, x_w):
        hg = self.get_hessian_matrix(x_w)

        part_up = self.g.hvm(self.s, 20)
        part_down_temp = hg.matrixmv(self.s, 20)
        part_down = self.s.hvm(part_down_temp, 20)

        try:
            result = part_up / part_down
        except ZeroDivisionError:
            result = part_up / float('Inf')

        return -result

    #direction of fatest descent
    def get_dfd(self, x_w):
        dfd = self.get_gradient(x_w)
        try:
            dfd = self.mul(dfd, -1.0 / self.norm(dfd))
        except ZeroDivisionError:
            dfd = self.mul(dfd, -1.0 / float('Inf'))
        return dfd

    def get_gradient(self, x):
        result = []
        i = 0
        while i < len(x):
            result.append(self.expression.diff_derivative_pi2_l(x, self.cof["h"], i))
            i += 1
        return result

    def par_sort(self):
        pass

    @staticmethod
    def compare(x1, x2):
        ansver = False
        for i in range(len(x1)):
            for j in range(len(x1[0])):
                if x1[i][j] in x2:
                    ansver = True
        return ansver

    def halting_check(self):
        r = True
        if not r:
            r = False
            print("Halting check! - True")
        return r

    @staticmethod
    def norm(v):
        return math.sqrt(sum([math.pow(item, 2) for item in v]))

    @staticmethod
    def dif(v1, v2):
        return [v1[i] - v2[i] for i in range(len(v1))]

    @staticmethod
    def dif_part(v1, v2, part):
        r = v1.copy()
        r[part] -= v2[part]
        return r

    @staticmethod
    def sum(v1, v2):
        return [v1[i] + v2[i] for i in range(len(v1))]

    @staticmethod
    def sum_part(v1, v2, part):
        r = v1.copy()
        r[part] += v2[part]
        return r

    @staticmethod
    def mul(v1, c):
        r = v1.copy()
        for i in range(len(r)):
            r[i] *= c
        return r

    def collect_data(self, i, x, fx, action):
        self.result["i"].append(i)
        self.result["xk"].append(x.copy())
        self.result["fx"].append(fx)
        self.result["action"].append(action)

    def printresult_g(self):
        verts = []
        for i in range(len(self.result["xk"])):
            verts.append((self.result["xk"][i][0], self.result["xk"][i][1]))
        path = Path(verts)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        patch = patches.PathPatch(path, facecolor='none', lw=2)
        ax.add_patch(patch)

        xs, ys = zip(*verts)
        ax.plot(xs, ys, 'x--', lw=2, color='black', ms=10)

        plt.show()

    def printresult_3d(self):
        pass

    def printresult(self):
        print('')
        print("Result:")
        for i in range(len(self.result["i"])):
            print("#" + str(i) + ":")
            print("itteration:", self.result["i"][i])
            print("x:", self.result["xk"][i])
            print("f(x):", self.result["fx"][i])
            print("action:", self.result["action"][i])
            print("----------------------------------------")
        pass