import math
import matrix
import excel_transfer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab

from matplotlib.path import Path
import matplotlib.patches as patches

from resource import expression


class GSS:
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
        self.result = {"xk": []}
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
        self.result = {"xk": [], "fxk": []}
        self.h = 0.1
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
        self.expression.input_expr()
        self.expression.input_range()
        pass

    def dostaff(self):
        task = 0
        while (task != 1):
            print('')
            print("Golden section search")
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
        ab = self.expression.range.copy()
        i = 0
        xk = []
        fxk = []
        self.result["xk"] = []
        self.result["fxk"] = []
        self.t = self.get_t()
        self.er = (ab[1] - ab[0]) / (2 * math.pow(self.t, self.N))
        x1 = self.findx1(ab)
        x2 = self.findx2(ab)

        f1 = self.expression.execute(x1)
        f2 = self.expression.execute(x2)
        m = 1
        while math.fabs(ab[1] - ab[0]) > self.epsilon:
            if f1 < f2:
                ab[1] = x2
                x2 = x1
                f2 = f1
                x1 = self.findx1(ab)
                f1 = self.expression.execute(x1)
                print("i=", m, "; x1=", x1, "; x2=", x2, "; f1=", f1, "; f2=", f2, ";")
            else:
                ab[0] = x1
                x1 = x2
                f1 = f2
                x2 = self.findx2(ab)
                f2 = self.expression.execute(x2)
                print("i=", m, "; x1=", x1, "; x2=", x2, "; f1=", f1, "; f2=", f2, ";")
            i += 1
        if f1 < f2:
            ab[1] = x2
        else:
            ab[0] = x1
            self.xmin = (ab[1] + ab[0]) / 2
            self.ymin = self.expression.execute(self.xmin)
            self.ea = (ab[1] - ab[0]) / 2
        print(self.xmin, self.ymin, self.er, self.ea)
        pass

    def findx1(self, ab):
        return ab[1] - (ab[1] - ab[0]) / self.t

    def findx2(self, ab):
        return ab[0] + (ab[1] - ab[0]) / self.t

    def get_t(self):
        return (1 + math.sqrt(5)) / 2


    def collect_result(self):
        pass

    def set_d(self, ab):
        self.d = math.fabs(ab[1] - ab[0]) / 4

    def printresult_g(self):
        verts = []
        for i in range(len(self.result["xk"])):
            verts.append((self.result["xk"][i], self.result["fxk"][i]))
        path = Path(verts)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        patch = patches.PathPatch(path, facecolor='none', lw=2)
        ax.add_patch(patch)

        xs, ys = zip(*verts)
        ax.plot(xs, ys, 'x--', lw=2, color='black', ms=10)

        plt.show()

    def printresult(self):
        print(self.x)