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
        #self.expression = expression.Expression("No name", "x**2")

        self.expression = expression.Expression("Function", "(10*(x1-x2)**2+(x1-1)**2)**0.25")

        self.condition = expression.Expression("Linear Condition", "a*x1+b*x2+c <= 1")
        self.condition.parameters["a"] = 2.0
        self.condition.parameters["b"] = 1.0
        self.condition.parameters["c"] = 1.0

        self.accuracy = 3
        self.result = {"x1": [], "x2": [], "y": []}
        self.x_start = 10

        self.start_point = [3.0, 3.0]
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
        #self.expression = expression.Expression("Parabola", "x**2")
        self.expression.range = [-10.0, 10.0]
        self.expression.parameters["unimodal"] = True
        # self.x_start = -9.0
        self.result = {"x1": [], "x2": [], "x0": []}
        # 0.001
        self.d = 1.0
        pass

    def importparam(self, accuracy: int, main_expresson: expression.Expression, condition: expression.Expression):
        self.accuracy = accuracy
        self.expression = main_expresson.copy()
        self.condition = condition.copy()

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
        print("--------------")
        print("Sven Begin...")
        self.condition.show_expr()
        self.expression.show_expr()
        nv = [-self.condition.parameters["a"],self.condition.parameters["b"]]
        #nv = self.mul(nv, 1.0 / self.norm(nv))
        i = 0
        status = False
        f = {}
        f["xk"] = []
        xk = []
        fxk = []
        self.x_start = self.start_point.copy()
        f["x0"] = self.expression.execute_l(self.x_start)
        xk.append(self.x_start)
        fxk.append(f["x0"])
        print(self.d)
        # f["x0md"] = self.expression.execute_l(self.x_start - self.d)

        x_dif = self.dif(self.x_start, self.mul(nv, self.d))
        x_sum = self.sum(self.x_start, self.mul(nv, self.d))

        f["x0md"] = self.expression.execute_l(x_dif)

        # f["x0pd"] = self.expression.execute_l(self.x_start + self.d)

        f["x0pd"] = self.expression.execute_l(x_sum)

        if f["x0"] < f["x0md"] and f["x0"] > f["x0pd"]:
            print("<m")
            self.d = np.copysign(self.d, 1.0)
            fxk.append(f["x0pd"])
            xk.append(x_sum)
        elif f["x0"] < f["x0pd"] and f["x0"] > f["x0md"]:
            print("<p")
            self.d = np.copysign(self.d, -1.0)
            fxk.append(f["x0md"])
            xk.append(x_dif)
        elif f["x0"] <= f["x0md"] and f["x0"] <= f["x0pd"]:
            print(">=<")
            self.result["xk"] = [x_dif, self.x_start, x_sum]
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
            print(self.d)
            d = self.d
            while not status:
                if fxk[-1] < fxk[-2]:
                    print("fxk[-1] < fxk[-2]")
                    # x_next = xk[-1] + d
                    print(xk[-1])
                    x_next = self.sum(xk[-1], self.mul(nv, d))
                    print(x_next)
                    fxk.append(self.expression.execute_l(x_next))
                    xk.append(x_next)
                    d *= 2.0
                elif fxk[-1] > fxk[-2]:
                    print("fxk[-1] > fxk[-2]")
                    d /= 4.0
                    print(xk[-1])
                    print(d)
                    # x_next = xk[-1] - d
                    x_next = self.dif(xk[-1], self.mul(nv, d))
                    print(x_next)
                    xk.append(xk[-1].copy())
                    fxk.append(fxk[-1])
                    xk[-2] = x_next.copy()
                    fxk[-2] = self.expression.execute_l(x_next)
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
        self.result["x0"].append(x[1].copy())
        self.result["x1"].append(x[0].copy())
        self.result["x2"].append(x[2].copy())

        self.result["f0"].append(f[1])
        self.result["f1"].append(f[0])
        self.result["f2"].append(f[2])

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
            verts.append((self.result["xk"][i][0], self.result["xk"][i][1]))
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

# TWork = SM()
# TWork.dostaff()