import math
import matrix
import excel_transfer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab

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
        self.x_start = {"x1": 0, "x2": 0}
        self.x_delta = {"x1": 0, "x2": 0}
        self.result = {"i": [], "xk": [], "x_delta": [], "fx": []}
        self.epsilon = [1, 1]
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
        self.x_start = {"x1": 4.0, "x2": 6.0}
        self.x_delta = {"x1": 0.6, "x2": 0.8}
        self.result = {"i": [], "xk": [], "x_delta": [], "fx": []}
        self.h = self.epsilon

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
        self.h = self.epsilon

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
        xw = {"x1": 1, "x2": 1}
        xp = {"x1": 1, "x2": 1}
        xn = {"x1": 1, "x2": 1}
        i = 0
        chalt = False
        x = self.x_start
        dx = self.x_delta
        print('-')
        print(dx)
        self.collect_result(i, x, dx, self.expression.execute_d(x))
        print(self.result["x_delta"][-1])

        xw = x.copy()
        fp = self.expression.execute_d(x)
        print("Before choose point")
        xw = self.choose_point(x, dx, True)
        xw.pop("__builtins__", None)
        print(xw)
        fw = self.expression.execute_d(xw)
        print("After choose point")

        xn = x.copy()
        xp = x.copy()
        print("Before first while fw >fp?", fw > fp)
        while fw > fp and not chalt:
            dx = self.mul(dx, self.get_alpha())
            if self.norm(dx) > self.epsilon[0]:
                xw = self.choose_point(x, dx, True)
                fw = self.expression.execute_d(xw)
            else:
                chalt = True

        xn = xw.copy()
        xp = x.copy()
        fn = fw

        if not chalt:
            i += 1
            self.collect_result(i, xn, dx, fn)
            while not self.halting_check() and not chalt:
                print("i", i)
                #fp = fw
                xp.pop("__builtins__", None)
                xn.pop("__builtins__", None)
                xw.pop("__builtins__", None)

                print("xp: ", xp)
                print("fp: ", fp)

                print("xn: ", xn)
                print("fn: ", fn)

                print("Before 2TB - BT, xw:", xw)
                xw = self.mul(xn, 2.0)
                xw = self.dif(xw, xp)
                print("After 2TB - BT, xw:", xw)
                #xw = self.choose_point(self.dif(self.mul(xn, self.get_betta()), xn), dx, True)
                xw = self.choose_point(xw, dx, True)
                xw.pop("__builtins__", None)
                print("xw: ", xw)

                fw = self.expression.execute_d(xw)
                print("fw", fw)

                print("dx", dx)

                print("Before second while fw >fp?", fw > fp)
                if fw > fp and not chalt:
                    wx = xp.copy()
                    dx = self.mul(dx, self.get_alpha())
                    print("dx", dx)

                    if self.norm(dx) > self.epsilon[0]:
                        print("xp: ", xp)
                        xw.pop("__builtins__", None)
                        print("Before choose, xw:", xw)
                        xw = self.choose_point(xp, dx, True)
                        xw.pop("__builtins__", None)
                        print("After choose, xw:", xw)
                        fw = self.expression.execute_d(xw)
                    else:
                        chalt = True
                    xw.pop("__builtins__", None)

                fn = fw
                print("Are chalt false?", chalt)
                print("After second while fn < fp?", fn < fp)
                if fn < fp and not chalt:
                    fp = fn
                    xp = xn.copy()
                    xp.pop("__builtins__", None)
                    xn = xw.copy()
                    xn.pop("__builtins__", None)
                elif fn >= fp and not chalt:
                    dx = self.mul(dx, self.get_alpha())
                    xw = self.choose_point(xp, dx, True)
                    xw.pop("__builtins__", None)
                    fw = self.expression.execute_d(xw)

                    while fw > fp and not chalt:
                        dx = self.mul(dx, self.get_alpha())
                        if self.norm(dx) > self.epsilon[0]:
                            xw = self.choose_point(xp, dx, True)
                            xw.pop("__builtins__", None)
                            fw = self.expression.execute_d(xw)
                        else:
                            chalt = True

                    if fn < fp and not chalt:
                        xp = xn.copy()
                        xp.pop("__builtins__", None)
                        xn = xw.copy()
                        xn.pop("__builtins__", None)
                        fp = fn

                i += 1
                self.collect_result(i, xn, dx, fn)
                pass
        else:
            pass
        self.printresult()
        pass

    def halting_check(self):
        ansver = False
        if self.norm(self.dif(self.result["xk"][-2], self.result["xk"][-1])) / self.norm(self.result["xk"][-2]) <= \
                self.epsilon[0] and math.fabs((self.expression.execute_d(
                self.result["xk"][-2]) - self.expression.execute_d(self.result["xk"][-1])) / self.expression.execute_d(
                self.result["xk"][-2])) <= self.epsilon[1]:
            ansver = True
            print("Halting check! - True")
        else:
            ansver = False
        return ansver

    def get_alpha(self):
        return 0.5

    def get_betta(self):
        return 2.0

    def choose_point(self, x, dx, m):
        #print('')
        #print("Choose point---")
        argument_x = [
            self.sum(x, dx),
            self.dif_part(self.sum_part(x, dx, "x1"), dx, "x2"),
            self.sum_part(self.dif_part(x, dx, "x1"), dx, "x2"),
            self.dif(x, dx)
        ]
        #print(argument_x)
        f = [self.expression.execute_d(xw) for xw in argument_x]
        #print(f)
        if m:
            r = argument_x[f.index(min(f))]
        else:
            r = argument_x[f.index(max(f))]
        #print("--end--")
        return r

    def norm(self, v):
        s = 0.0
        v = v.copy()
        v.pop("__builtins__", None)
        for item in v:
            s += math.pow(v[item], 2)
        return math.sqrt(s)

    def dif(self, v1, v2):
        d = v1.copy()
        d.pop("__builtins__", None)
        for item in d:
            d[item] = v1[item] - v2[item]
        return d

    def dif_part(self, v1, v2, part):
        d = v1.copy()
        d.pop("__builtins__", None)
        d[part] = v1[part] - v2[part]
        return d

    def sum(self, v1, v2):
        s = v1.copy()
        s.pop("__builtins__", None)
        for item in s:
            s[item] = v1[item] + v2[item]
        return s

    def sum_part(self, v1, v2, part):
        d = v1.copy()
        d.pop("__builtins__", None)
        d[part] = v1[part] + v2[part]
        return d

    def mul(self, v1, betta):
        v1 = v1.copy()
        v1.pop("__builtins__", None)
        for item in v1:
            v1[item] *= betta
        return v1

    def collect_result(self, i, x, dx, f):
        x = x.copy()
        x.pop("__builtins__", None)
        dx = dx.copy()
        dx.pop("__builtins__", None)
        self.result["i"].append(i)
        self.result["xk"].append(x)
        self.result["x_delta"].append(dx)
        self.result["fx"].append(f)

    def printresult_g(self):
        pass

    def printresult(self):
        print("Result:")
        for i in range(len(self.result["i"])):
            print('')
            print("i:", self.result["i"][i])
            self.result["xk"][i].pop("__builtins__", None)
            print("x:", self.result["xk"][i])
            self.result["x_delta"][i].pop("__builtins__", None)
            print("dx:", self.result["x_delta"][i])
            print("f:", self.result["fx"][i])
        pass
        print("Result:")