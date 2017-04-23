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
        self.epsilon = [0.0001, 0.0001]
        self.expression = expression.Expression("Parabola", "x**2 - 2*x")
        self.d_expression = expression.Expression("Line", "2*x")
        self.expression.range = [2.0, 3.0]
        self.d_expression.range = self.expression.range
        self.expression.parameters["unimodal"] = True
        self.d_expression.parameters["unimodal"] = False
        self.x_start = 2.2
        self.result = {"xst": None, "fsxt" : None}
        self.h = 0.00001
        self.d_lambda = None
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

        self.sm.makedefault()
        self.sm.x_start = self.x_start
        if self.d_lambda == None:
            self.sm.d = self.h
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
        print("X_NEW is ", x_new)
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
        x_new = raw["xk"][1] + self.dx * (raw["fxk"][0] - raw["fxk"][2]) / (
        2 * (raw["fxk"][0] - 2 * raw["fxk"][1] + raw["fxk"][2]))
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
        #print("start sycle")
        while math.fabs(x2 - xst) < self.epsilon[1] and math.fabs(f2 - fs) < self.epsilon[0] and i < 100:
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
            try:
                a1 = (f2 - f1) / (x2 - x1)
            except ZeroDivisionError:
                a1 = (f2 - f1) / float('Inf')
            part1 = (x3 - x1)
            part2 = (x2 - x1)
            part3 = (x3 - x2)
            try:
                part01 = (f3 - f1) / part1
            except ZeroDivisionError:
                part01 = (f3 - f1) / float('Inf')

            try:
                part02 = (f2 - f1) / part2
            except ZeroDivisionError:
                part02 = (f2 - f1) / float('Inf')

            try:
                a2 = (part01 - part02) / part3
            except ZeroDivisionError:
                a2 = (part01 - part02) / float('Inf')

            #a2 = ((f3 - f1) / part1 - (f2 - f1) / part2) / part3
            xst = 0.5 * (x1 + x2) - a1 / (a2)
            fs = self.expression.execute(xst)
            #print("i:", i)
            #print("xst =", xst, "f(xst) =", fs)
            #print("x2 =", x2, "f(x2) =", f2)
            #print(math.fabs(x2 - xst), math.fabs(f2 - fs))
            i += 1
        self.result["xst"] = xst
        self.result["fsxt"] = fs
        #print("xst =", xst, "f(xst) =", fs)
        pass

    def collect_result(self):
        pass

    def printresult_g(self):
        pass

    def printresult(self):
        print("DSK Paula method")
        print("xst =", self.result["xst"], "f(xst) =", self.result["fsxt"])