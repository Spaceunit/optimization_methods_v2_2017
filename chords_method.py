import math
import matrix
import excel_transfer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab

from resource import expression


class CM:
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
        self.expression = expression.Expression("No name", "x**2")
        self.accuracy = 3
        self.result = {"length": [], "middle": [], "x1": [], "x2": [], "i": []}
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
        self.expression = expression.Expression("Parabola", "(x-3)**3")
        self.expression.range = [1.0, 10.0]
        self.expression.parameters["unimodal"] = False
        self.x_start = 9.0
        self.result = {"length": [], "middle": [], "x1": [], "x2": [], "i": []}
        self.h = self.epsilon * 10

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
            print("Chords method")
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
        print('')
        print("Begin")
        i = 1
        ab = self.expression.range.copy()
        d = self.h
        int_part = None

        int_part = math.modf(
            self.expression.diff_derivative(ab[1], d) - self.expression.diff_derivative(ab[0], d))
        middle = ab[1] - (self.expression.diff_derivative(ab[1], d) * (ab[1] - ab[0])) / int_part[1]
        fm = self.expression.execute(middle)

        print("function in middle:", middle)
        print("derivative:", math.fabs(self.expression.diff_derivative(middle, d)))
        while math.fabs(self.expression.diff_derivative(middle, d)) > self.epsilon and fm != 0:
            ab[0] = middle
            int_part = math.modf(
                self.expression.diff_derivative(ab[1], d) - self.expression.diff_derivative(ab[0], d))
            middle = ab[1] - (self.expression.diff_derivative(ab[1], d) * (ab[1] - ab[0])) / int_part[1]
            print("i:", i)
            print("middle =", middle)
            print("length =", d)
            print("Xa =", ab[0], "Xb =", ab[1])
            self.collect_result(d, middle, i, ab)
            #middle = ab[0] + d
            i += 1
        pass


    def collect_result(self, d, middle, i, ab):
        self.result["length"].append(d)
        self.result["middle"].append(middle)
        self.result["x1"].append(ab[0])
        self.result["x2"].append(ab[1])
        self.result["i"].append(i)

    def set_d(self):
        self.d = math.fabs(self.ab[1] - self.ab[0]) / 4

    def findx1(self):
        return (self.ab[1] + self.ab[0]) / 2 - self.d

    def findx2(self):
        return (self.ab[1] + self.ab[0]) / 2 + self.d

    def printresult_g(self):
        y = np.arange(0.0, float(self.result["i"][-1]), 1.0)
        # y = np.arange(0.0, 5.0, 0.1)
        fig = plt.figure(1)
        dm = fig.add_subplot(111)
        dm.hlines(y, self.result["x1"], self.result["x2"], lw=2)
        plt.show()
        pass

    def printresult(self):
        print("Result:")
        for i in range(len(self.result["i"])):
            print('')
            print("i:", self.result["i"][i])
            print("middle =", self.result["middle"][i])
            print("length =", self.result["length"][i])
            print("Xa =", self.result["x1"][0], "Xb =", self.result["x1"][1])
        pass

    pass