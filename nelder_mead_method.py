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


class NMM:
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
        self.expression = expression.Expression("No name", "x**2")
        self.accuracy = 3
        self.epsilon = [1, 1]
        self.mm = True
        self.msycle = 3
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
        self.expression = expression.Expression("Function", "4*(x1-5)**2+(x2-6)**2")
        self.expression.parameters["unimodal"] = True
        self.expression.parameters["global_min"] = [5.0, 6.0]
        self.x_start = [[8.0, 9.0], [10.0, 11.0], [8.0, 11.0]]
        self.cof = {"a": 1.0, "g": 2.0, "b": 0.5}


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
            print("Nelder–Mead method")
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
        exp_r = self.expression
        f_arr = [exp_r.execute_l(x) for x in self.x_start]
        x_w = self.deepcopy(self.x_start)
        center = [0 for _ in range(len(x_w[0]))]
        h_temp = [0 for _ in range(len(x_w[0]))]

        self.par_sort(x_w, f_arr)
        while self.halting_check():
            for i in range(len(x_w) - 1):
                center = self.sum(center, x_w[i])
            center = self.mul(center, 1.0 / float(len(x_w) - 1))
            h_temp = self.reflection(center, x_w)
            f_h_temp = exp_r.execute_l(h_temp)
            if f_h_temp <= f_arr[0]:
                h_temp_new = self.stretching(center, h_temp, x_w)
                f_h_temp_new = exp_r.execute_l(h_temp_new)
                if f_h_temp_new < f_arr[0]:
                    x_w[-1] = h_temp_new.copy()
                else:
                    x_w[-1] = h_temp.copy()
            elif f_h_temp > f_arr[-2] and f_h_temp < f_arr[-1]:
                h_temp_new = self.compression(center, h_temp, x_w)
                x_w[-1] = h_temp_new
            else:
                i = 1
                while i < len(x_w)
                    x_w[i] = self.mul(x_w[i], 0.5)
                    i += 1
        pass

    def stretching(self, center, h_temp, x_w):
        h_temp = self.dif(h_temp, center)
        h_temp = self.mul(h_temp, self.cof["g"])
        h_temp = self.sum(h_temp, center)
        return h_temp

    def compression(self, center, h_temp, x_w):
        h_temp = self.dif(h_temp, center)
        h_temp = self.mul(h_temp, self.cof["b"])
        h_temp = self.sum(h_temp, center)
        return h_temp

    def reflection(self, center, x_w):
        h_temp = self.dif(center, x_w[-1])
        h_temp = self.mul(h_temp, self.cof["a"])
        h_temp = self.sum(h_temp, center)
        return h_temp

    @staticmethod
    def par_sort(x, f):
        f_temp = f.copy()
        x_temp = x.copy()
        index = [i for i in range(len(x))]
        f.sort()
        for i in range(len(x)):
            x[i] = x_temp[f_temp.index(f[i])]




    @staticmethod
    def reduction(center, x1, x2):
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
        if 1 / float(len(self.x_start)):
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

    @staticmethod
    def deepcopy(x):
        xn = [[], [], []]
        for i in range(len(x)):
            for j in range(len(x[i])):
                xn[i].append(x[i][j])
        return xn

    def collect_data(self, i, x, fx, action):
        self.result["i"].append(i)
        self.result["xk"].append(x)
        self.result["fx"].append(fx)
        self.result["action"].append(action)

    def printresult_g(self):
        pass

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