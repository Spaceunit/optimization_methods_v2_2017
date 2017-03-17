import math
import matrix
import excel_transfer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab

from resource import expression


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
            "image 1": 11,
            "image 2": 12,
            "mk2": 13
        }
        self.expression = expression.Expression("No name", "x**2")
        self.accuracy = 3
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
        self.expression.range = [-10.0, 10.0]
        self.expression.parameters["unimodal"] = True
        self.x_start = -9.0
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
        self.expression = str(input("enter expression ->"))
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
                self.printresult1()

            elif task == 13:
                self.resolve_with_grp()
        pass

    def print_raw_data(self):
        self.expression.show_expr()
        pass


    def resolve(self):
        i = 0
        ab = self.expression.range.copy()
        way = True
        print("Begin...")
        print("i =", i, "a =", ab[0], "b =", ab[1])
        while math.fabs(ab[1] - ab[0]) > self.epsilon:
            self.set_d(ab)
            x1 = self.findx1(ab)
            x2 = self.findx2(ab)

            y1 = self.expression.execute(x1)
            y2 = self.expression.execute(x2)

            if y1 < y2:
                if way == False:
                    ab[0] = x2
                    self.set_d(ab)
                    print("Overjump - change direction, go to B-point...")
                    way = True
                else:
                    ab[1] = x2
            else:
                if way == False:
                    ab[1] = x1
                    self.set_d(ab)
                    print("Overjump - change direction, go to A-point...")
                    way = True
                else:
                    ab[0] = x1
            i += 1
            print("i =", i, "a =", ab[0], "b =", ab[1], "d =", self.d)
        pass

    def resolve_with_grp(self):
        i = 0
        ab = self.expression.range.copy()
        way = True
        print("Begin...")
        print("i =", i, "a =", ab[0], "b =", ab[1])
        while math.fabs(ab[1] - ab[0]) > self.epsilon:
            self.set_d(ab)
            x1 = self.findx1(ab)
            x2 = self.findx2(ab)

            y1 = self.expression.execute(x1)
            y2 = self.expression.execute(x2)

            if y1 < y2:
                if way == False:
                    ab[0] = x2
                    self.set_d(ab)
                    print("Overjump - change direction, go to B-point...")
                    way = True
                else:
                    ab[1] = x2
            else:
                if way == False:
                    ab[1] = x1
                    self.set_d(ab)
                    print("Overjump - change direction, go to A-point...")
                    way = True
                else:
                    ab[0] = x1
            i += 1
            print("i =", i, "a =", ab[0], "b =", ab[1], "d =", self.d)
        pass

    def set_d(self, ab):
        self.d = math.fabs(ab[1] - ab[0]) / 4

    def findx1(self, ab):
        return (ab[1] + ab[0]) / 2 - self.d

    def findx2(self, ab):
        return (ab[1] + ab[0]) / 2 + self.d

    def printresult(self):
        pass

    def printresult1(self):
        pass