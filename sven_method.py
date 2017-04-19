import math
import matrix
import excel_transfer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab

from matplotlib.path import Path
import matplotlib.patches as patches

from resource import expression


class SM:
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
            "image 1": 12,
            "start -g": 13
        }
        self.expression = expression.Expression("No name", "x**2")
        self.accuracy = 3
        self.result = {"x1": [], "x2": [], "y": []}
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
        self.result = {"x1": [], "x2": [], "x0": []}
        self.d = 0.001
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
        #self.expression.input_range()
        self.epsilon = self.inputdata("Epsilon", "float")
        self.x_start = self.inputdata("Start position", "float")
        self.d = self.inputdata("Step", "float")
        pass

    def dostaff(self):
        task = 0
        while (task != 1):
            print('')
            print("Sven's method")
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
                self.printresult_graph()

            elif task == 13:
                pass
        pass

    def print_raw_data(self):
        self.expression.show_expr()
        pass


    def resolve(self):
        print("Sven Begin...")
        i = 0
        status = False
        f = {}
        f["xk"] = []
        xk = []
        fxk = []
        f["x0"] = self.expression.execute(self.x_start)
        xk.append(self.x_start)
        fxk.append(f["x0"])
        f["x0md"] = self.expression.execute(self.x_start - self.d)
        f["x0pd"] = self.expression.execute(self.x_start + self.d)

        if f["x0"] < f["x0md"]:
            #print("<m")
            self.d = np.copysign(self.d, 1.0)
            fxk.append(f["x0pd"])
            xk.append(self.x_start + self.d)
        elif f["x0"] < f["x0pd"]:
            #print("<p")
            self.d = np.copysign(self.d, -1.0)
            fxk.append(f["x0md"])
            xk.append(self.x_start + self.d)
        elif f["x0"] >= f["x0md"] and f["x0"] <= f["x0pd"]:
            #print(">=<")
            self.result["xk"] = [self.x_start - self.d, self.x_start, self.x_start + self.d]
            self.result["fxk"] = [f["x0md"], fxk[0], f["x0pd"]]
            status = True
        else:
            print("WTF")
            self.result = None
            status = True

        #print("x:", xk[-2], "f(x):", fxk[-2])
        #print("x:", xk[-1], "f(x):", fxk[-1])

        if not status:
            x_next = None
            d = self.d
            while not status:
                if fxk[-1] < fxk[-2]:
                    x_next = xk[-1] + d
                    fxk.append(self.expression.execute(x_next))
                    xk.append(x_next)
                    d *= 2
                elif fxk[-1] > fxk[-2]:
                    #print("fxk[-1] > fxk[-2]")
                    d /= 4
                    x_next = xk[-1] - d
                    xk.append(xk[-1])
                    fxk.append(fxk[-1])
                    xk[-2] = x_next
                    fxk[-2] = self.expression.execute(x_next)
                    #print("x:", xk[-3], "f(x):", fxk[-3])
                    #print("x:", xk[-2], "f(x):", fxk[-2])
                    #print("x:", xk[-1], "f(x):", fxk[-1])
                    status = True
                elif fxk[-1] >= fxk[-2] and fxk[-2] <= fxk[-3]:
                    #print("fxk[-1] >= fxk[-2] and fxk[-2] <= fxk[-3]")
                    status = True
                else:
                    print("WTF")
            self.result["xk"] = xk
            self.result["fxk"] = fxk
            self.d = d

    def collect_final_result(self, x, f):
        self.result["x0"].append(x[1])
        self.result["x1"].append(x[0])
        self.result["x2"].append(x[2])

        self.result["f0"].append(f[1])
        self.result["f1"].append(f[0])
        self.result["f2"].append(f[2])

    def set_d(self, ab):
        self.d = math.fabs(ab[1] - ab[0]) / 4

    def find_f1(self, ab):
        return (ab[1] + ab[0]) / 2 - self.d

    def find_f2(self, ab):
        return (ab[1] + ab[0]) / 2 + self.d

    def find_min(self):
        array = {"xk": [None, None, None], "fxk": [None, None, None]}
        pos = self.result["fxk"].index(min(self.result["fxk"]))

        array["xk"][1] = self.result["xk"][pos]
        array["xk"][0] = self.result["xk"][pos - 1]
        array["xk"][2] = self.result["xk"][pos + 1]

        array["fxk"][1] = self.result["fxk"][pos]
        array["fxk"][0] = self.result["fxk"][pos - 1]
        array["fxk"][2] = self.result["fxk"][pos + 1]
        return array

    def printresult_graph(self):
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
        print("Sven method")
        for i in range(len(self.result["xk"])):
            print("i:", i, "x:", self.result["xk"][i], "f(x):", self.result["fxk"][i])
        pass