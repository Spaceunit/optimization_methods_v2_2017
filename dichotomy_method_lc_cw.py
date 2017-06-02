import math
import matrix
import excel_transfer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab

from resource import expression

import sven_method_lc_cw


class DM:
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
        self.expression = expression.Expression("Function", "(10*(x1-x2)**2+(x1-1)**2)**0.25")

        self.condition = expression.Expression("Linear Condition", "a*x1+b*x2+c <= 1")
        self.condition.parameters["a"] = 2.0
        self.condition.parameters["b"] = 1.0
        self.condition.parameters["c"] = 1.0
        self.nv = [-self.condition.parameters["a"], self.condition.parameters["b"]]
        self.accuracy = 10
        self.d_for_sven = 1.0
        self.result = {"x1": [], "x2": [], "y": [], "fxk": []}
        self.way = True
        self.sm = sven_method_lc_cw.SM()
        #self.sm.importparam(self.accuracy, self.expression, self.condition)
        self.start_point = [3.0, 5.0]
        #self.makedefault()



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
        self.sm.importparam(self.accuracy, self.expression, self.condition)

        self.x_start = self.start_point.copy()
        self.sm.start_point = self.start_point.copy()
        self.epsilon = 10 ** (-self.accuracy)

        self.sm.d = self.d_for_sven
        self.sm.resolve()
        self.expression.range = self.sm.find_min()
        print("Not sorted xk")
        print(self.expression.range["xk"])
        print(self.expression.range["fxk"])
        self.par_sort(self.expression.range["xk"], self.expression.range["fxk"])
        print("Sorted xk")
        print(self.expression.range["xk"])
        print(self.expression.range["fxk"])
        self.expression.range["xk"].pop(0)
        self.expression.range["fxk"].pop(0)
        self.expression.parameters["unimodal"] = True
        self.result = {"x1": [], "x2": [], "i": [], "fxk": []}
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
            pass

    def inputnewdata(self):
        self.expression.input_expr()
        self.expression.input_range()
        self.epsilon = self.inputdata("Epsilon", "float")
        pass

    def dostaff(self):
        task = 0
        while (task != 1):
            print('')
            print("Dichotomy method")
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
        self.makedefault()
        self.nv = [-self.condition.parameters["a"], self.condition.parameters["b"]]
        self.nv = self.mul(self.nv, 1.0 / self.norm(self.nv))
        i = 0
        print("Error 2")
        print(self.expression.range["xk"])
        ab = self.deepcopy(self.expression.range["xk"])
        f_ab = []
        k = 0
        while k < len(ab):
            f_ab.append(self.expression.execute_l(ab[k]))
            k += 1
        #self.par_sort(ab, f_ab)
        print(ab)
        way = True

        self.collect_result(i, ab, f_ab[0], f_ab[1])
        print('-----------------------')
        print("Begin Dichotomy method")
        self.expression.show_expr()
        # print("i =", i, "a =", ab[0], "b =", ab[1])
        while self.distantion(ab[0], ab[1]) > self.epsilon:
            self.set_d(ab)
            x1 = self.findx1(ab)
            x2 = self.findx2(ab)

            y1 = self.expression.execute_l(x1)
            y2 = self.expression.execute_l(x2)

            print(i)
            print(x1, x2)
            print(y1, y2)

            if y1 < y2:
                if way == False:
                    ab[0] = x2.copy()
                    self.set_d(ab)
                    #print("Overjump - change direction, go to B-point...")
                    way = True
                else:
                    ab[1] = x2.copy()
            else:
                if way == False:
                    ab[1] = x1.copy()
                    self.set_d(ab)
                    #print("Overjump - change direction, go to A-point...")
                    way = True
                else:
                    ab[0] = x1.copy()
            i += 1
            self.collect_result(i, ab, y1, y2)
            #print("i =", i, "a =", ab[0], "b =", ab[1], "d =", self.d)


    def collect_result(self, i, ab, y1, y2):
        self.result["x1"].append(ab[0].copy())
        self.result["x2"].append(ab[1].copy())
        self.result["fxk"].append([y1, y2])
        self.result["i"].append(i)

    def set_d(self, ab):
        self.d = self.distantion(ab[0], ab[1]) / 4.0

    def findx1(self, ab):
        x = self.sum(ab[1], ab[0])
        x = self.mul(x, 0.5)
        x = self.dif(x, self.mul(self.nv, self.d))
        return x

    def findx2(self, ab):
        x = self.sum(ab[1], ab[0])
        x = self.mul(x, 0.5)
        x = self.sum(x, self.mul(self.nv, self.d))
        return x

    @staticmethod
    def distantion(v1: type([]), v2: type([])):
        i = 0
        s = 0
        while i < len(v1):
            s += (v1[i] - v2[i])**2.0
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

    def printresult_g(self):
        y = np.arange(0.0, float(self.result["i"][-1]), 1.0)
        x1 = [item[0] for item in self.result["fxk"]]
        x2 = [item[1] for item in self.result["fxk"]]
        #y = np.arange(0.0, 5.0, 0.1)
        fig = plt.figure(1)
        dm = fig.add_subplot(111)
        dm.hlines(y, x1, x2, lw=2)
        plt.show()

    def printresult(self):
        print("Result:")
        for i in range(len(self.result["i"])):
            print('')
            print("i:", i, ":")
            print("x1:", self.result["x1"][i])
            print("x2:", self.result["x2"][i])
            print("fx:", self.result["fxk"][i])
        pass

    pass

# TWork = DM()
# TWork.dostaff()