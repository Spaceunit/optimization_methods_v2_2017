import math
import matrix
import excel_transfer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab

from matplotlib.path import Path
import matplotlib.patches as patches

import sven_method

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
        self.sm = sven_method.SM()
        self.expression = expression.Expression("No name", "x**2")
        self.accuracy = 3
        self.sm.importparam(self.accuracy)
        self.result = {"xst": None, "fsxt" : None}
        self.raw_group = {}
        self.h = 0.00001
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
        self.epsilon = 10 ** (-self.accuracy)
        self.expression = expression.Expression("Parabola", "x**2")
        self.d_expression = expression.Expression("Line", "2*x")
        self.expression.range = [-10.0, 10.0]
        self.d_expression.range = self.expression.range
        self.expression.parameters["unimodal"] = True
        self.d_expression.parameters["unimodal"] = False
        self.x_start = -10.0
        self.result = {"xst": None, "fsxt" : None}
        self.h = 0.00001
        pass

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
        self.epsilon = 10 ** (-self.accuracy)

    def inputnewdata(self):
        self.expression.input_expr()
        self.expression.input_range()
        pass

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
        self.makedefault()
        self.sm.makedefault()
        self.sm.expression = self.expression.copy()
        self.sm.resolve()
        self.raw_group = self.sm.result
        self.dx = self.sm.d

        x_new = self.dsk(self.sm.find_min())

        self.paul(x_new)
        pass

    def dsk(self, raw):
        print(raw["xk"])
        print(raw["fxk"])
        print(self.dx)
        x_new = raw["xk"][1] + self.dx * (raw["fxk"][0] - raw["fxk"][2]) / (
        2 * (raw["fxk"][0] - 2 * raw["fxk"][1] + raw["fxk"][2]))
        print("x* = ", x_new)
        return x_new

    def paul(self, x_new):
        print("Begin Paul")
        # 0.2
        # 0.01
        self.dx = self.h
        self.epsilon = 0.00000000000001
        x1 = x_new
        x2 = x_new + self.dx
        f1 = self.expression.execute(x_new)
        f2 = self.expression.execute(x2)
        if f1 > f2:
            x3 = x_new + 2 * self.dx
        else:
            x3 = x_new - self.dx

        x = [x_new, x2, x3]
        f3 = self.expression.execute(min(x))

        a1 = (f2 - f1) / (x2 - x1)
        a2 = ((f3 - f1)/(x3 - x1) - (f2 - f1)/(x2 - x1))/ (x3 - x2)

        xst = 0.5 *(x1 + x2) - a1 / a2
        fs = self.expression.execute(xst)

        i = 0
        print("start sycle")
        while math.fabs(x2 - xst) < self.epsilon and math.fabs(f2 - fs) < self.epsilon and i < 100:
            x1 = xst
            f1 = self.expression.execute(x1)
            x2 = x1 + self.dx
            f2 = self.expression.execute(x2)
            if f1 > f2:
                x3 = x_new + 2 * self.dx
            else:
                x3 = x_new - self.dx
            x = [x_new, x2, x3]
            f3 = self.expression.execute(min(x))
            a1 = (f2 - f1) / (x2 - x1)
            a2 = ((f3 - f1) / (x3 - x1) - (f2 - f1) / (x2 - x1)) / (x3 - x2)
            xst = 0.5 * (x1 + x2) - a1 / (a2)
            fs = self.expression.execute(xst)
            print("i:", i)
            print("xst =", xst, "f(xst) =", fs)
            print("x2 =", x2, "f(x2) =", f2)
            print(math.fabs(x2 - xst), math.fabs(f2 - fs))
            i += 1
        self.result["xst"] = xst
        self.result["fsxt"] = fs
        print("xst =", xst, "f(xst) =", fs)
        pass

    def collect_result(self):
        pass

    def printresult_g(self):
        pass

    def printresult(self):
        print("xst =", self.result["xst"], "f(xst) =", self.result["fsxt"])