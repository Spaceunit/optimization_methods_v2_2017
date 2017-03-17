import math
import matrix
import excel_transfer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab

# Not ready yet!
class DSKP:
    def __init__(self):
        self.epsilon = 0.001
        self.N = 600
        self.xmin = None
        self.ymin = None
        self.ea = None
        self.ab = [0, 100]
        self.intervals = [0.4, 0.8, 1.6]
        self.raw_data = {}
        self.result_data = {}
        self.dx = 0.1
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
        self.accuracy = 3
        self.expression = "x**2 + 6/x"


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


    #remake
    def inputnewdata0(self):
        task = 0
        self.am = matrix.Matrix([], "Initial matrix")
        while (task != 1):
            print('')
            print("Enter matrix dimension:")
            while (task != 1):
                num = int(input("-> "))
                print("Input is correct? (enter - yes/n - no)")
                command = input("-> ")
                if (command != "n"):
                    self.am = self.inputmatrix(num)
                    # self.dv = self.inputvector()
                    task = 1
            task = 0
            self.am.rename("Initial matrix")
            self.um = self.am.copy()
            self.um.rename("U-matrix")
            self.am.showmatrix()
            print("Our matrix with accuracy: 3")
            self.am.showmatrixaccuracy3()
            # self.dv.showvector()
            print("Matrix is correct? (enter - yes/n - no)")
            command = input("-> ")
            if (command != "n"):
                task = 1

    def makedefault0(self):
        print("Setting up data for task#15")
        self.raw_data = {'a': 1.77, 'b': 2.17, 'c': 1.38, 'd': 0.89, 'x0': 3.39, 'y0': 2.13, 't0': 15, 't1': 45}
        #self.raw_data = {'a': 1.89, 'b': 2.25, 'c': 1.49, 'd': 1.05, 'x0': 3.55, 'y0': 2.35, 't0': 18, 't1': 48}
        self.accuracy = 3
        self.print_raw_data()
        print("Accuracy of calculations:",(10**(-self.accuracy)))
        pass

    def makedefault(self):
        self.accuracy = 2
        #self.epsilon = 10 ** (-self.accuracy)
        self.epsilon = 0.01
        #self.expression = "10 * x * math.log10(x) / math.log10(2.7) - (x**2) / 2"
        #self.expression = "(x-12)**2"
        #self.expression = "x**2 + 6/x"
        self.expression = "x**2 - 6/x"
        self.ab = [0.1, 3.0]
        self.x = 0.1
        self.dx = 0.1
        pass

    def makedefault2(self):
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
        pass

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

    #def inputnewdata(self):
    #    for value in ['a', 'b', 'c', 'd', 'x0', 'y0', 't0', 't1']:
    #        self.raw_data[value] = self.inputdata(value, 'float')

    def inputnewdata(self):
        self.expression = str(input("enter expression ->"))
        pass

    def inputmatrix(self, num):
        print('')
        i = 0
        task = 0
        nm = matrix.Matrix([], "new matrix")
        while (i < num):
            print("Enter matrix row (use spaces)")
            print("Row ", i + 1)
            while (task != 1):
                row = list(map(float, input("-> ").split()))
                print("Input is correct? (enter - yes/n - no)")
                command = input("-> ")
                if (command != "n" and len(row) == num):
                    task = 1
                    nm.appendnrow(row)
                elif (len(row) != num):
                    print('')
                    print("Incorrect input: count of items.")
            task = 0
            i += 1
        return nm

    #@staticmethod
    def execute_expression(self, function, x):
        return eval(function)

    def dostaff(self):
        task = 0
        while (task != 1):
            print('')
            print("DSK Paul`s method")
            print('')
            task = self.enterCommand()
            if (task == 2):
                pass
            elif (task == 3):
                pass
            elif (task == 4):
                self.showHelp()
            elif (task == 5):
                self.inputnewdata()
                pass
            elif (task == 6):
                self.print_raw_data()
                pass
            elif (task == 8):
                self.setaccuracy()
                pass
            elif (task == 9):
                self.makedefault()
                pass
            elif (task == 10):
                self.resolve_main()
                pass
            elif (task == 11):
                self.printresult()

            elif (task == 12):
                self.printresult1()
            elif (task == 13):
                self.makedefault2()
        pass

    def print_raw_data(self):
        pass

    def resolve_sven(self):
        i = 1
        self.intervals = []
        self.set_h()
        print(self.expression)
        f1 = self.count_f(self.x)
        print("x1 =", self.x, "f(x1) =", f1, "h =", self.h)
        x_temp = self.x + self.h
        f2 = self.count_f(x_temp)
        print("x2 =", x_temp, "f(x2) =", f2, "h =", self.h)
        if f1 < f2:
            self.h = -self.h
            self.x = self.x + self.h
            f2 = self.count_f(self.x)
        else:
            self.x = x_temp

        print("--------------------------------------------")
        print("i =", i, "x =", self.x, "f(x1) =", f1, "h =", self.h)
        print("Important")
        print("i =", i, "x =", self.x, "f(x2) =", f2, "h =", self.h)

        while f2 < f1:
            x_temp = self.x
            self.h *= 2
            f1 = self.count_f(x_temp)
            self.x += self.h
            f2 = self.count_f(self.x)
            #print("i =", i, "x =", self.x, "h =", self.h)
            print("--------------------------------------------")
            print("i =", i, "x =", self.x, "f(x1) =", f1, "h =", self.h)
            print("Important")
            print("i =", i, "x =", self.x, "f(x2) =", f2, "h =", self.h)
            if f2 < f1:
                self.intervals.append(self.x)
            i += 1

        print(self.intervals)
        pass

    def set_h(self):
        self.h = self.dx

    def count_f(self, x):
        return self.execute_expression(self.expression, x)

    def resolve_dsk(self):
        self.func = []
        for i in range(3):
            self.func.append(self.count_f(self.intervals[i]))
        print(self.func)
        self.xnew = self.intervals[1] + self.dx * (self.func[0] - self.func[2]) /(2*(self.func[0] - 2 * self.func[1] + self.func[2]))
        #self.x = self.xnew
        print("x* = ", self.xnew)
        pass

    def resolve_paul(self):
        # 0.2
        # 0.01
        x1 = self.xnew
        x2 = self.xnew + self.dx
        f1 = self.count_f(self.xnew)
        f2 = self.count_f(x2)
        if f1 > f2:
            x3 = self.xnew + 2 * self.dx
        else:
            x3 = self.xnew - self.dx

        x = [self.xnew, x2, x3]
        f3 = self.count_f(min(x))
        a1 = (f2 - f1) / (x2 - x1)
        a2 = ((f3 - f1)/(x3 - x1) - (f2 - f1)/(x2 - x1))/ (x3 - x2)
        xst = 0.5 *(x1 + x2) - a1 / a2
        fs = self.count_f(xst)
        while math.fabs(x2 - xst) < self.epsilon and math.fabs(f2 - fs) < self.epsilon:
            f1 = self.count_f(x1)
            x2 = x1 + self.dx
            f2 = self.count_f(x2)
            if f1 > f2:
                x3 = self.xnew + 2 * self.dx
            else:
                x3 = self.xnew - self.dx

            f3 = self.count_f(min(x))
            a1 = (f2 - f1) / (x2 - x1)
            a2 = ((f3 - f1) / (x3 - x1) - (f2 - f1) / (x2 - x1)) / (x3 - x2)
            xst = 0.5 * (x1 + x2) - a1 / a2
            fs = self.count_f(xst)
        print("xst =", xst, "f(xst) =", fs)
        pass

    def resolve_main(self):
        self.resolve_sven()
        self.resolve_dsk()
        self.resolve_paul()
        pass

    #def count_f(self, x):
    #    self.execute_expression(self.expression, x)


    def set_d(self):
        self.d = math.fabs(self.ab[1] - self.ab[0]) / 4

    def findx1(self):
        return (self.ab[1] + self.ab[0]) / 2 - self.d

    def findx2(self):
        return (self.ab[1] + self.ab[0]) / 2 + self.d

    def printresult(self):
        pass

    def printresult1(self):
        pass

    #xn = x2 + dx * (f1 - f3) /(2*(f1 - 2f2 + f3))
    #[0.4, 0.8, 1.6]