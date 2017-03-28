import math
import matrix
import excel_transfer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab

from matplotlib.path import Path
import matplotlib.patches as patches

from resource import expression


class HJPS:
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
                "image 1": 12
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
                "image 1": "show visualization"
            }
        }
        self.expression = expression.Expression("No name", "x**2")
        self.accuracy = 3
        self.epsilon = [1, 1]
        self.mm = True
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
        self.expression = expression.Expression("Function", "(x1-2)**2+x2**2")
        self.expression.parameters["unimodal"] = True
        self.x_start = [4.0, 6.0]
        self.x_delta = [0.6, 0.8]
        self.result = {"i": [], "xk": [], "x_delta": [], "fx": [], "action": []}
        self.cross = []
        self.h = self.epsilon
        self.mm = True

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
            print("Hooke-Jeeves pattern search method")
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
        i = 0
        self.result["i"].append(i)
        self.result["xk"].append(self.x_start)
        self.result["x_delta"].append(self.x_delta)
        xk = self.result["xk"]
        fxk = self.result["fx"]
        dx = self.result["x_delta"]
        action = self.result["action"]
        action.append("Initial point")
        fxk.append(self.expression.execute_l(self.x_start))

        finest_point = self.find_finest_point(self.expression, xk[0], self.x_delta, self.mm)
        xw = [None, None]
        f_xw = None
        if finest_point != False:
            i += 1
            self.collect_data(i, finest_point, self.x_delta, self.expression.execute_l(finest_point), "make next point")
            #while self.halting_check(xk, self.expression, self.epsilon) and self.norm(self.x_delta) > self.epsilon[0]:
            while self.norm(self.x_delta) > self.epsilon[0]:
                xw = self.dif(self.mul(xk[-1], self.get_betta()), xk[-2])
                temp = self.find_finest_point(self.expression, xw, self.x_delta, self.mm)
                if temp != False:
                    xw = temp
                    f_xw = self.expression.execute_l(xw)
                    if f_xw < self.expression.execute_l(xk[-2]):
                        self.collect_data(i, xw, self.x_delta, f_xw, "make next point (NBP)")
                    else:
                        self.x_delta = self.mul(self.x_delta, self.get_alpha())
                        self.collect_data(i, xw, self.x_delta, f_xw, "decrease x-delta, go to PBP")
                else:
                    self.x_delta = self.mul(self.x_delta, self.get_alpha())
                    self.collect_data(i, xw, self.x_delta, f_xw, "decrease x-delta for x-work")
                i += 1
        self.printresult()

    @staticmethod
    def halting_check(harr, ex, eps):
        r = True
        if HJPS.norm(HJPS.dif(harr[-2], harr[-1])) / HJPS.norm(harr[-2]) <= eps[0] and math.fabs((ex.execute_l(harr[-2]) - ex.execute_l(harr[-1])) / ex.execute_l(harr[-2])) <= eps[1]:
            r = False
            print("Halting check! - True")
        return r

    @staticmethod
    def find_finest_point(ex, x, dx, mm):
        result = False
        cross = [
            HJPS.sum_part(x, dx, 0),
            HJPS.sum_part(x, dx, 1),
            HJPS.dif_part(x, dx, 0),
            HJPS.dif_part(x, dx, 1),
            HJPS.sum(x, dx),
            HJPS.dif(x, dx),
            [x[0] + dx[0], x[1] - dx[1]],
            [x[0] - dx[0], x[1] + dx[1]]
        ]

        f = []
        for i in range(len(cross)):
            f.append(ex.execute_l(cross[i]))
        if mm:
            result = min(f)
            if not result < ex.execute_l(x):
                result = False
            else:
                result = cross[f.index(result)]
        else:
            result = max(f)
            if not result > ex.execute_l(x):
                result = False
            else:
                result = cross[f.index(result)]

        return result

    def get_alpha(self):
        return 0.5

    def get_betta(self):
        return 2.0

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

    def collect_data(self, i, x, dx, fx, action):
        self.result["i"].append(i)
        self.result["xk"].append(x)
        self.result["fx"].append(fx)
        self.result["x_delta"].append(dx)
        self.result["action"].append(action)

    def printresult_g(self):
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
        print('')
        print("Result:")
        for i in range(len(self.result["i"])):
            print("#" + str(i) + ":")
            print("itteration:", self.result["i"][i])
            print("x:", self.result["xk"][i])
            print("f(x):", self.result["fx"][i])
            print("x-delta:", self.result["x_delta"][i])
            print("action:", self.result["action"][i])
            print("----------------------------------------")
        pass