# Gradient descent
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


# methods...
import sven_method
import dsk_paula_v2
import golden_section_search
import dichotomy_method



from resource import expression


class PMCD:
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
        self.expression = expression.Expression("No name", "x**2")
        self.r_expression = expression.Expression("No name", "x**2")
        self.accuracy = 3
        self.epsilon = [1, 1]
        self.mm = True
        self.msycle = 3
        self.cof = {"a": 1.0, "g": 2.0, "b": 0.5, "h": 0.001}
        self.result = {"i": [], "xk": [], "fx": [], "action": []}
        self.makedefault()

        # prepare methods

        self.sm = sven_method.SM()
        self.sm.importparam(self.accuracy)

        self.dsk = dsk_paula_v2.DSKP()
        self.dsk.importparam(self.accuracy)

        self.gsm = golden_section_search.GSS()
        self.gsm.importparam(self.accuracy)

        self.dichom = dichotomy_method.DM()
        self.importparam(self.accuracy)

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
        self.expression = expression.Expression("Function", "(x1-15)**2-x1*x2+3*x2**2")
        self.r_expression = self.expression.copy()

        self.expression.parameters["unimodal"] = True
        self.expression.parameters["global_min"] = [2.0, 1.0]
        #self.x_start = [[8.0, 9.0], [10.0, 11.0], [8.0, 11.0]]
        #self.x_start = [7.0, 6.0]
        self.x_start = [-23.5, -23.5]
        self.cof = {"a": 1.0, "g": 2.0, "b": 0.5, "h": 0.001}
        self.result = {"i": [], "xk": [], "fx": [], "action": []}
        self.hg = matrix.Matrix([[0]], "Hessian matrix")
        self.hg.makedimatrix(2)


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
            print("The Powell method of conjugate directions")
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
        x_w = [self.x_start[0], self.x_start[1]]
        f_x_w = self.expression.execute_l(x_w)
        gradient = matrix.Vector(self.get_gradient(x_w), "Gradient")
        s1 = matrix.Vector([1.0, 0.0], "Vector S(1)")
        s2 = matrix.Vector([0.0, 1.0], "Vector S(2)")

        # It will be soon...
        s3 = matrix.Vector([1.0, 1.0], "Vector S(3)")
        self.collect_data(k, x_w, f_x_w, "Initial point")
        k += 1

        interval = self.sven_method(x_w, s2)

        print(interval)

        c_lambda = self.dichotomy_method(interval)
        c_lambda = -c_lambda
        s2_temp = s2.copy()
        s2_temp.rename(s2.name)
        s2_temp.vector = self.mul(s2_temp.vector, c_lambda)
        x_w = self.sum(x_w, s2_temp.vector)
        f_x_w = self.expression.execute_l(x_w)
        self.collect_data(k, x_w, f_x_w, "Next point by Dichotomy method")
        k += 1
        print(c_lambda)

        interval = self.sven_method(x_w, s1)
        c_lambda = self.golden_section_search_method(interval)
        c_lambda = -c_lambda
        s1_temp = s1.copy()
        s1_temp.rename(s1.name)
        s1_temp.vector = self.mul(s1_temp.vector, c_lambda)
        x_w = self.sum(x_w, s1_temp.vector)
        f_x_w = self.expression.execute_l(x_w)
        self.collect_data(k, x_w, f_x_w, "Next point by Sven method")
        k += 1
        print(c_lambda)

        c_lambda = self.dsk_paula()
        c_lambda = -c_lambda
        s2_temp = s2.copy()
        s2_temp.rename(s2.name)
        s2_temp.vector = self.mul(s2_temp.vector, c_lambda)
        x_w = self.sum(x_w, s2_temp.vector)
        f_x_w = self.expression.execute_l(x_w)
        self.collect_data(k, x_w, f_x_w, "Next point by DSK Paula method")
        k += 1
        print(c_lambda)

        x_w = self.quad_step(x_w, s3)
        f_x_w = self.expression.execute_l(x_w)
        self.collect_data(k, x_w, f_x_w, "Next point by Quad step")
        k += 1

        while self.halting_check() and k < 60 and self.norm(gradient.vector) > 0.1:
            k += 1
        self.printresult()

    def quad_step(self, x_w, s):
        stat = True
        start = 0.0
        c_lambda = []
        # S = matrix.Vector([0.0, 1.0], "Vector S(1)")
        s.vector = self.dif(x_w, self.result["xk"][-3])
        #d_lambda = 0.1 * self.norm(x_w) / self.norm(s.vector)

        self.r_expression.replace_arg([
            "("+str(x_w[0])+"+"+str(s.vector[0])+"*x"+")",
            "("+str(x_w[1])+"+"+str(s.vector[1])+"*x"+")"
        ])

        interval = self.sven_method(x_w, s)

        c_lambda = self.dichotomy_method(interval)
        c_lambda = -c_lambda
        print(c_lambda)
        s_temp = s.copy()
        s_temp.rename(s.name)
        s_temp.vector = self.mul(s_temp.vector, c_lambda)
        x_w = self.sum(x_w, s_temp.vector)

        return x_w

    def sven_method(self, x_w, S):
        stat = True
        start = 0.0
        c_lambda = []
        #S = matrix.Vector([0.0, 1.0], "Vector S(1)")
        d_lambda = 0.1 * self.norm(x_w) / self.norm(S.vector)
        if S.vector[0] == 0.0:
            # S(2)
            self.r_expression.replace_arg([x_w[0], None])
            start = x_w[1]
            pass
        elif S.vector[1] == 0.0:
            # S(1)
            self.r_expression.replace_arg([None, x_w[1]])
            start = x_w[0]
            pass
        elif S.name == "Vector S(3)":
            start = x_w[0]
        else:
            print("Wrong Vector S([1, 2])")
            stat = False
        if stat:
            self.sm.makedefault()
            self.r_expression.show_expr()
            self.sm.expression = self.r_expression.copy()
            self.sm.x_start = start
            self.sm.expression.show_expr()
            self.sm.resolve()
            raw_group = self.sm.find_min()
            c_lambda.append(raw_group["xk"][0])
            c_lambda.append(raw_group["xk"][1])
            pass
        else:
            c_lambda = None
        return c_lambda

    def dsk_paula(self):
        c_lambda = None
        if True:
            self.dsk.makedefault()
            self.dsk.expression = self.r_expression.copy()
            self.dsk.epsilon = self.epsilon.copy()
            self.dsk.resolve()
            c_lambda = self.dsk.result["xst"]
        else:
            print("Error in DSK Paula method: Interval = None (must be list)")

        return c_lambda
        pass

    def golden_section_search_method(self, interval):
        c_lambda = None
        if interval != None:
            self.gsm.makedefault()
            self.gsm.expression = self.r_expression.copy()
            self.gsm.expression.range = interval.copy()
            self.gsm.epsilon = self.epsilon[0]
            self.gsm.resolve()
            c_lambda = (self.gsm.result["a"][-1] + self.gsm.result["b"][-1]) / 2.0
        else:
            print("Error in golden section method: Interval = None (must be list)")

        return c_lambda
        pass

    def dichotomy_method(self, interval):
        c_lambda = None
        if interval != None:
            self.dichom.makedefault()
            self.dichom.expression = self.r_expression.copy()
            self.dichom.expression.range = interval.copy()
            self.dichom.epsilon = self.epsilon[0]
            self.dichom.resolve()
            c_lambda = (self.dichom.result["x1"][-1] + self.dichom.result["x2"][-1]) / 2.0
        else:
            print("Error in dichotomy method: Interval = None (must be list)")

        return c_lambda

    def conjugate_directions(self):
        #x(k) = x(k-1) + lambda(k)S(2)
        pass

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

    def get_lambda(self, x_w):
        hg = self.get_hessian_matrix(x_w)
        #gradient = self.get_gradient(x_w)
        #dfd = self.get_dfd(x_w)

        gradient = matrix.Vector(self.get_gradient(x_w), "Gradient")
        dfd = matrix.Vector(self.get_dfd(x_w), "DFD")

        part_up = gradient.hvm(dfd, 20)
        part_down_temp = hg.matrixmv(dfd, 20)
        part_down = dfd.hvm(part_down_temp, 20)

        try:
            result = part_up / part_down
        except ZeroDivisionError:
            result = float('Inf')

        return result

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