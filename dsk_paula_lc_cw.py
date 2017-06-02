import math
import matrix
import excel_transfer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab

from matplotlib.path import Path
import matplotlib.patches as patches

import sven_method_lc_cw

from resource import expression


class DSKP:
    def __init__(self):
        self.commands = {
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
            "image 1": 12
        }
        self.sm = sven_method_lc_cw.SM()
        self.expression = expression.Expression("Function", "(10*(x1-x2)**2+(x1-1)**2)**0.25")

        self.condition = expression.Expression("Linear Condition", "a*x1+b*x2+c <= 1")
        self.condition.parameters["a"] = 2.0
        self.condition.parameters["b"] = 1.0
        self.condition.parameters["c"] = 1.0
        self.nv = [-self.condition.parameters["a"], self.condition.parameters["b"]]
        self.start_point = [3.0, 5.0]
        self.accuracy = 20
        self.d_for_sven = 1.0
        self.accuracy = 3
        self.result = {"xst": [], "fsxt": [], "xn": [], "fxn": [], "i": []}
        self.raw_group = {}
        self.external_raw_group = None
        self.h = 0.1
        self.makedefault()



    def showCommands(self):
        print('')
        print("Commands...")
        for item in self.commands:
            print(str(item) + ": " + str(self.commands[item]))

    def enterCommand(self):
        command = "0"
        print('')
        print("Enter command (help for Q&A)")
        while (command not in self.commands):
            command = input("->")
            if (command not in self.commands):
                print("There is no such command")
            else:
                return self.commands[command]

    def showHelp(self):
        print('')
        print("Help v0.001")
        self.showCommands()


    def testfunc(self, x):
        y = 10 * x * math.log10(x) / math.log10(2.7) - (x**2) / 2
        return y


    def makedefault(self):
        #self.epsilon = 10 ** (-self.accuracy)
        self.sm.importparam(self.accuracy, self.expression, self.condition)

        self.x_start = self.start_point.copy()
        self.sm.start_point = self.start_point.copy()
        self.sm.d = self.d_for_sven
        self.epsilon = 10 ** (-self.accuracy)

        self.sm.resolve()

        self.epsilon = [self.epsilon, self.epsilon]
        self.expression.range = self.sm.find_min()
        # self.par_sort(self.expression.range["xk"], self.expression.range["fxk"])
        print("Error here")
        print(self.expression.range["xk"])
        self.x_start = self.start_point.copy()
        self.result = {"xst": [], "fsxt" : [], "xn" : [], "fxn" : [], "i": []}
        self.h = self.d_for_sven
        self.d_lambda = None
        pass

    def importparam(self, accuracy: int, main_expresson: expression.Expression, condition: expression.Expression, start_point: type([])):
        self.accuracy = accuracy
        self.expression = main_expresson.copy()
        self.condition = condition.copy()
        self.start_point = start_point.copy()

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
        self.epsilon = 10 ** (-self.accuracy)

    def inputdata(self, data_name, data_type):
        task = 0
        value = None
        input_type = int
        if data_type == "float":
            input_type = float
        elif data_type == "int":
            input_type = int
        else:
            print("Undefind type", data_type)
            task = 1
        if task == 0:
            print('')
            print("Enter ", data_name, ":")
            while (task != 1):
                value = input_type(input("-> "))
                print("Value", data_name, "is", value)
                print("Input is correct? (enter - yes/n - no)")
                command = input("-> ")
                if (command != "n"):
                    task = 1
            return value
        else:
            return None

    def inputnewdata(self):
        self.expression.input_expr()
        # self.expression.input_range()
        self.input_epsilon()
        self.x_start = self.inputdata("Start position", "float")
        self.h = self.inputdata("Step", "float")
        pass

    def input_epsilon(self):
        ans = False
        command = ""
        print('')
        while not ans:
            self.epsilon = list(map(float, input("Input epsilon1 and epsilon2 -> ").split()))
            print("Input is correct?[Y]-> ")
            command = input("-> ")
            if (command.lower() != "y" or command.lower() != "yes") and len(self.epsilon) != 2:
                print("Try again and input \"yes\" or \"y\"")
                ans = True
            else:
                ans = True

    def dostaff(self):
        task = 0
        while (task != 1):
            print('')
            print("DSK Paul`s method")
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
        pass

    def print_raw_data(self):
        self.expression.show_expr()
        pass


    def resolve(self):
        print("Begin DSK Paula method...")
        #self.expression.input_expr()
        #self.epsilon = self.inputdata("Epsilon", "float")
        #self.x_start = self.inputdata("Start position", "float")
        #self.d = self.inputdata("Step", "float")

        self.nv = [-self.condition.parameters["a"], self.condition.parameters["b"]]
        self.nv = self.mul(self.nv, 1.0 / self.norm(self.nv))

        self.sm.makedefault()
        self.sm.start_point = self.start_point.copy()
        # self.sm.d = self.d_for_sven
        if self.d_lambda == None:
            self.sm.d = self.d_for_sven
        else:
            self.sm.d = self.d_lambda
        self.sm.epsilon = self.epsilon[0]
        self.sm.expression = self.expression.copy()
        self.sm.resolve()
        if self.external_raw_group == None:
            self.raw_group = self.sm.result
        else:
            self.raw_group = self.external_raw_group
        self.dx = self.sm.d
        #if self.external_raw_group == None:
        print("Three points is", self.sm.find_min())
        x_new = self.dsk(self.sm.find_min())
        print("X_NEW (after DSK) is ", x_new)
        #else:
        #    print("Three points is", self.raw_group)
        #    x_new = self.dsk(self.raw_group)
        #    print("X_NEW is ", x_new)
        #x_new = []

        self.paul(x_new)
        pass

    def dsk(self, raw):
        #print(raw["xk"])
        #print(raw["fxk"])
        #print(self.dx)

        #x_new = raw["xk"][1] + self.dx * (raw["fxk"][0] - raw["fxk"][2]) / (
        #2 * (raw["fxk"][0] - 2 * raw["fxk"][1] + raw["fxk"][2]))

        try:
            part_1 = self.dx * (raw["fxk"][0] - raw["fxk"][2]) / (2 * (raw["fxk"][0] - 2 * raw["fxk"][1] + raw["fxk"][2]))
        except ZeroDivisionError:
            part_1 = float('Inf')

        x_new = self.sum(raw["xk"][1], self.mul(self.nv, part_1))

        #print("x* = ", x_new)
        return x_new

    def paul(self, x_new):
        print("Begin Paul")
        # 0.2
        # 0.01
        if self.d_lambda == None:
            self.dx = self.h
        else:
            self.dx = self.d_lambda
        #self.epsilon = 0.00000000000001
        x1 = x_new.copy()
        # x2 = x_new + self.dx
        x2 = self.sum(x_new, self.mul(self.nv, self.dx))
        f1 = self.expression.execute_l(x_new)
        f2 = self.expression.execute_l(x2)
        if f1 > f2:
            # x3 = x_new + 2 * self.dx
            x3 = self.sum(x_new, self.mul(self.nv, 2.0 * self.dx))
            print("x3 is", x3)
        else:
            # x3 = x_new - self.dx
            x3 = x2.copy()
            x2 = x1.copy()
            x1 = self.dif(x_new, self.mul(self.nv, self.dx))
            print("x3 is", x3)


        x = [x_new.copy(), x2.copy(), x3.copy()]

        print('')

        print("Group of x before sorting is", x)
        print([self.expression.execute_l(x[0]), self.expression.execute_l(x[1]), self.expression.execute_l(x[2])])

        self.par_sort(x, [self.expression.execute_l(x[0]), self.expression.execute_l(x[1]), self.expression.execute_l(x[2])])

        print("Group of x after sorting is", x)
        print([self.expression.execute_l(x[0]), self.expression.execute_l(x[1]), self.expression.execute_l(x[2])])

        f3 = self.expression.execute_l(x3)

        try:
            a1 = (f2 - f1) / self.distantion(x2, x1)
        except ZeroDivisionError:
            a1 = float('Inf')
        try:
            a2 = ((f3 - f1) / self.distantion(x3, x1) - (f2 - f1) / self.distantion(x2, x1)) / self.distantion(x3, x2)
        except ZeroDivisionError:
            a2 = float('Inf')

        # a1_a2 = a1 / a2
        try:
            a1_a2_1 = a1 / (2.0 * a2)
        except ZeroDivisionError:
            a1_a2_1 = float('inf')
        except OverflowError:
            a1_a2_1 = float('Inf')

        try:
            a1 = (f3 - f2) / self.distantion(x3, x2)
        except ZeroDivisionError:
            a1 = float('Inf')
        try:
            a2 = ((f3 - f1) / self.distantion(x3, x1) - (f3 - f2) / self.distantion(x3, x2)) / self.distantion(x2, x1)
        except ZeroDivisionError:
            a2 = float('Inf')

        # a1_a2 = a1 / a2
        try:
            a1_a2_2 = a1 / (2.0 * a2)
        except ZeroDivisionError:
            a1_a2_2 = float('inf')
        except OverflowError:
            a1_a2_2 = float('Inf')

        # xst = 0.5 *(x1 + x2) - a1 / a2

        xst_1 = self.mul(self.sum(x1, x2), 0.5)
        xst_1 = self.dif(xst_1, self.mul(self.nv, a1_a2_1))

        xst_2 = self.mul(self.sum(x2, x3), 0.5)
        xst_2 = self.dif(xst_2, self.mul(self.nv, a1_a2_2))

        fs_1 = self.expression.execute_l(xst_1)
        fs_2 = self.expression.execute_l(xst_2)

        print("fs_1 < fs_2", fs_1 < fs_2)
        if fs_1 < fs_2:
            xst = xst_1.copy()
        else:
            xst = xst_2.copy()

        fs = self.expression.execute_l(xst)
        i = 0
        x = [x1.copy(), x2.copy(), x3.copy()]
        f_x = [self.expression.execute_l(x1), self.expression.execute_l(x2),
               self.expression.execute_l(x3)]
        self.par_sort(x, f_x)
        xn = [x1.copy(), x2.copy(), x3.copy()]
        if self.distantion(xst, x1) < self.distantion(xst, x3):
            xn[2] = x2.copy()
            xn[1] = xst.copy()
            xn[0] = x1.copy()
        else:
            xn[0] = x2.copy()
            xn[1] = xst.copy()
            xn[2] = x3.copy()
        fxn = [self.expression.execute_l(xn[0]), self.expression.execute_l(xn[1]),
               self.expression.execute_l(xn[2])]

        self.collect_result(i, xn, xst.copy(), fxn, fs)

        #print("start sycle")
        while self.distantion(x[0], xst) > self.epsilon[0] and math.fabs(f_x[0] - fs) > self.epsilon[1] and i < 1000:
            #[x1.copy(), x2.copy(), x3.copy()]
            #x1 = xst.copy()
            #f1 = self.expression.execute_l(x1)
            #x2 = self.sum(x1, self.mul(self.nv, self.dx))
            # x2 = x1 + self.dx
            #f2 = self.expression.execute_l(x2)
            #if f1 > f2:
                # x3 = x_new + 2 * self.dx
            #    x3 = self.sum(x_new, self.mul(self.nv, 2.0 * self.dx))
            #else:
            #    # x3 = x_new - self.dx
            #    x3 = self.dif(x_new, self.mul(self.nv, self.dx))
            x = self.deepcopy(xn)
            self.par_sort(x, fxn.copy())
            #f3 = self.expression.execute_l(x3)
            x1 = xn[0].copy()
            x2 = xn[1].copy()
            x3 = xn[2].copy()
            try:
                # a1 = (f2 - f1) / (x2 - x1)
                a1 = (f2 - f1) / self.distantion(x2, x1)
            except ZeroDivisionError:
                a1 = float('Inf')
            part1 = self.distantion(x3, x1)
            part2 = self.distantion(x2, x1)
            part3 = self.distantion(x3, x2)
            try:
                part01 = (f3 - f1) / part1
            except ZeroDivisionError:
                part01 = float('Inf')

            try:
                part02 = (f2 - f1) / part2
            except ZeroDivisionError:
                part02 = float('Inf')

            try:
                a2 = (part01 - part02) / part3
            except ZeroDivisionError:
                a2 = float('Inf')

            #a2 = ((f3 - f1) / part1 - (f2 - f1) / part2) / part3
            # xst = 0.5 * (x1 + x2) - a1 / (a2)
            try:
                a1_a2_1 = a1 / (2.0 * a2)
            except ZeroDivisionError:
                a1_a2_1 = float('Inf')


            try:
                # a1 = (f2 - f1) / (x2 - x1)
                a1 = (f3 - f2) / self.distantion(x3, x2)
            except ZeroDivisionError:
                a1 = float('Inf')
            part1 = self.distantion(x3, x1)
            part2 = self.distantion(x3, x2)
            part3 = self.distantion(x2, x1)
            try:
                part01 = (f3 - f1) / part1
            except ZeroDivisionError:
                part01 = float('Inf')

            try:
                part02 = (f3 - f2) / part2
            except ZeroDivisionError:
                part02 = float('Inf')

            try:
                a2 = (part01 - part02) / part3
            except ZeroDivisionError:
                a2 = float('Inf')

            #a2 = ((f3 - f1) / part1 - (f2 - f1) / part2) / part3
            # xst = 0.5 * (x1 + x2) - a1 / (a2)
            try:
                a1_a2_2 = a1 / (2.0 * a2)
            except ZeroDivisionError:
                a1_a2_2 = float('Inf')

            xst_1 = self.mul(self.sum(x1, x2), 0.5)
            xst_1 = self.dif(xst_1, self.mul(self.nv, a1_a2_1))

            xst_2 = self.mul(self.sum(x2, x3), 0.5)
            xst_2 = self.dif(xst_2, self.mul(self.nv, a1_a2_2))

            fs_1 = self.expression.execute_l(xst_1)
            fs_2 = self.expression.execute_l(xst_2)

            print("fs_1 < fs_2", fs_1 < fs_2)
            if fs_1 < fs_2:
                xst = xst_1.copy()
            else:
                xst = xst_2.copy()

            fs = self.expression.execute_l(xst)
            #print("i:", i)
            #print("xst =", xst, "f(xst) =", fs)
            #print("x2 =", x2, "f(x2) =", f2)
            #print(math.fabs(x2 - xst), math.fabs(f2 - fs))
            i += 1
            x = [x1.copy(), x2.copy(), x3.copy()]
            f_x = [self.expression.execute_l(x1), self.expression.execute_l(x2),
                                 self.expression.execute_l(x3)]
            self.par_sort(x, f_x)
            xn = [x1.copy(), x2.copy(), x3.copy()]
            if self.distantion(xst, x1) < self.distantion(xst, x3):
                xn[2] = x2.copy()
                xn[1] = xst.copy()
                xn[0] = x1.copy()
            else:
                xn[0] = x2.copy()
                xn[1] = xst.copy()
                xn[2] = x3.copy()
            fxn = [self.expression.execute_l(xn[0]), self.expression.execute_l(xn[1]),
                   self.expression.execute_l(xn[2])]

            self.collect_result(i, xn, xst.copy(), fxn, fs)
        # self.result["xst"] = xst
        # self.result["fsxt"] = fs
        #print("xst =", xst, "f(xst) =", fs)
        pass

    @staticmethod
    def distantion(v1: type([]), v2: type([])):
        i = 0
        s = 0
        while i < len(v1):
            s += (v1[i] - v2[i]) ** 2.0
            i += 1
        return math.sqrt(s)

    @staticmethod
    def norm(v):
        return math.sqrt(sum([math.pow(item, 2) for item in v]))

    @staticmethod
    def dif(v1, v2):
        i = 0
        r = []
        while i < len(v1):
            r.append(v1[i] - v2[i])
            i += 1
        return r

    @staticmethod
    def dif_part(v1, v2, part):
        r = v1.copy()
        r[part] -= v2[part]
        return r

    @staticmethod
    def sum(v1, v2):
        i = 0
        r = []
        while i < len(v1):
            r.append(v1[i] + v2[i])
            i += 1
        return r

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

    @staticmethod
    def deepcopy(x):
        xn = [[] for _ in x]
        for i in range(len(x)):
            for j in range(len(x[i])):
                xn[i].append(x[i][j])
        return xn

    def par_sort(self, x, f):
        f_temp = f.copy()
        x_temp = self.deepcopy(x)
        f.sort()
        for i in range(len(x)):
            x[i] = x_temp[f_temp.index(f[i])]
            f_temp[f_temp.index(f[i])] = None

    def collect_result(self,i: int, xn: type([]), xst: type([]), f_n: type([]), f_xst: float):
        self.result["xn"].append(self.deepcopy(xn))
        self.result["fxn"].append(f_n.copy())
        self.result["xst"].append(xst.copy())
        self.result["fsxt"].append(f_xst)
        self.result["i"].append(i)
        pass

    def printresult_g(self):
        verts = []
        for i in range(len(self.result["xst"])):
            verts.append((self.result["xst"][i][0], self.result["xst"][i][1]))
        path = Path(verts)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        patch = patches.PathPatch(path, facecolor='none', lw=2)
        ax.add_patch(patch)

        xs, ys = zip(*verts)
        ax.plot(xs, ys, 'x--', lw=2, color='black', ms=10)

        plt.show()

    def printresult(self):
        print('')
        print("DSK Paula method")
        print("Result:")
        for i in range(len(self.result["i"])):
            print('')
            print("i:", i, ":")
            print("xst =", self.result["xst"][i], "f(xst) =", self.result["fsxt"][i])
            print("x1:", self.result["xn"][i][0], "f(x1):", self.result["fxn"][i][0])
            print("x2:", self.result["xn"][i][1], "f(x2):", self.result["fxn"][i][1])
            print("x3:", self.result["xn"][i][2], "f(x3):", self.result["fxn"][i][2])
        print("-----------------------")

# TWork = DSKP()
# TWork.dostaff()