import math
import matrix
import excel_transfer
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import mlab

from matplotlib.path import Path
import matplotlib.patches as patches



from resource import expression


class NMM:
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
                "image 1": 12,
                "image 2": 13
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
                "image 1": "show 2D visualization",
                "image 2": "show 3D visualization"
            }
        }
        self.expression = expression.Expression("No name", "x**2")
        self.accuracy = 3
        self.epsilon = [1, 1]
        self.mm = True
        self.msycle = 3
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
        self.expression = expression.Expression("Function", "4*(x1-2)**2+(x2-1)**2")
        self.expression.parameters["unimodal"] = True
        self.x_start = [[5.0, 4.0], [7.0, 6.0], [5.0, 6.0]]
        self.x_delta = [[5.0, 4.0], [7.0, 6.0], [5.0, 6.0]]
        self.result = {"i": [], "xk": [], "fx": [], "action": []}
        self.cross = []
        self.h = self.epsilon
        self.msycle = 3
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
            print("Nelder–Mead method")
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
            elif task == 13:
                self.printresult_3d()
        pass

    def print_raw_data(self):
        self.expression.show_expr()
        pass

    def resolve(self):
        self.makedefault()
        k = 0
        sycle = [0,0,0]
        x_mod = self.deepcopy(self.x_start)
        while k <= 30:
            f = []
            x = NMM.deepcopy(x_mod)
            for i in range(len(x)):
                f.append(self.expression.execute_l(x[i]))

            self.collect_data(k, x, f, "initial simplex")

            xmax = x[f.index(max(f))].copy()
            xmin = x[f.index(min(f))].copy()
            xmed= [0.0, 0.0]
            for item in x:
                index = x.index(item)
                if index != x.index(xmax) and index != x.index(xmin):
                    xmed = item.copy()
            xhalf = self.mul(self.sum(xmin, xmed), 0.5)

            xtest = self.sum(self.mul(self.dif(xhalf, xmax), 2.0), xmax)
            f_xtest = self.expression.execute_l(xtest)
            if f_xtest < f[x.index(xmed)] and f_xtest > f[x.index(xmin)]:
                xnew = self.sum(self.mul(self.dif(xhalf, xmax), 2.0), xmax)
            elif (f_xtest < max(f) and f_xtest > f[x.index(xmed)]):
                xnew = self.sum(self.mul(self.dif(xhalf, xmax), 0.5), xmax)
            else:
                xnew = self.sum(self.mul(self.dif(xhalf, xmax), 0.5), xmax)

            x_mod = [xnew.copy(), xmed.copy(), xmin.copy()]

            if self.compare(x, x_mod):
                for item in x_mod:
                    if item in x:
                        sycle[x_mod.index(item)] += 1

                for item in sycle:
                    if item >= self.msycle:
                        center = item.copy()
                        x_ch = []
                        for item1 in x_mod:
                            index = x.index(item1)
                            if index != x_mod.index(center):
                                x_ch.append(item1.copy())

                        arr = self.reduction(center, x_ch[0], x_ch[1])
                        x_mod = [center, x_ch[0], x_ch[1]]
                        f = []
                        for i in range(len(x_mod)):
                            f.append(self.expression.execute_l(x_mod[i]))
                        self.collect_data(k, x_mod, f, "do reduction")
                        sycle = [0, 0, 0]
                        break
                    else:
                        self.collect_data(k, x_mod, f, "make new simplex")
            else:
                self.collect_data(k, x_mod, f, "make new simplex")
            #x = self.deepcopy(x_mod)
            k += 1
            print(k)
        self.printresult()

    @staticmethod
    def reduction(center, x1, x2):
        half_x1 = NMM.mul(NMM.sum(x1, center), 0.5)
        half_x2 = NMM.mul(NMM.sum(x2, center), 0.5)
        return [half_x1, half_x2]

    @staticmethod
    def compare(x1, x2):
        ansver = False
        for i in range(len(x1)):
            for j in range(len(x1[0])):
                if x1[i][j] in x2:
                    ansver = True
        return ansver

    @staticmethod
    def halting_check(harr, ex, eps):
        r = True
        if True:
            r = False
            print("Halting check! - True")
        return r

    @staticmethod
    def find_finest_simplex(ex, x, dx, mm):
        result = False
        simplex = [

        ]

        f = []
        for i in range(len(simplex)):
            f.append(ex.execute_l(simplex[i]))
        if mm:
            result = min(f)
            if not result < ex.execute_l(x):
                result = False
            else:
                result = simplex[f.index(result)]
        else:
            result = max(f)
            if not result > ex.execute_l(x):
                result = False
            else:
                result = simplex[f.index(result)]

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

    @staticmethod
    def deepcopy(x):
        xn = [[], [], []]
        for i in range(len(x)):
            for j in range(len(x[i])):
                xn[i].append(x[i][j])
        return xn

    def collect_data(self, i, x, fx, action):
        self.result["i"].append(i)
        self.result["xk"].append(x)
        self.result["fx"].append(fx)
        self.result["action"].append(action)

    def printresult_g0(self):
        verts = []
        for i in range(len(self.result["xk"])):
            if not ("decrease x-delta" in self.result["action"][i]):
                verts.append((self.result["xk"][i][0], self.result["xk"][i][1]))
        print("Points count:", len(verts))
        path = Path(verts)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        patch = patches.PathPatch(path, facecolor='none', lw=2)
        ax.add_patch(patch)

        xs, ys = zip(*verts)
        ax.plot(xs, ys, 'x--', lw=2, color='black', ms=10)

        plt.show()

    def printresult_g(self):
        verts = []
        for i in range(len(self.result["xk"])):
        #    if not ("decrease x-delta" in self.result["action"][i]):
            verts.append((self.result["xk"][i][0], self.result["xk"][i][1]))
        print("Points count:", len(verts))
        path = Path(verts)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        patch = patches.PathPatch(path, facecolor='none', lw=2)
        ax.add_patch(patch)

        xs, ys = zip(*verts)
        ax.plot(xs, ys, 'x--', lw=2, color='black', ms=10)

        plt.show()

    def printresult_3d(self):
        verts = [[], [], []]
        for i in range(len(self.result["xk"])):
            if not ("decrease x-delta" in self.result["action"][i]):
                verts[0].append(self.result["xk"][i][0])
                verts[1].append(self.result["xk"][i][1])
                verts[2].append(self.result["fx"][i])
        print("Points count:", len(verts[0]))


        fig = plt.figure()
        ax = fig.gca(projection='3d')

        # Make data.
        X = np.arange(-5, 5, 0.25)

        Y = np.arange(-5, 5, 0.25)

        X, Y = np.meshgrid(X, Y)
        #R = np.sqrt(X ** 2 + Y ** 2)
        Z = np.array([self.expression.execute_l([X[i], Y[i]]) for i in range(len(X))])

        # Plot the surface.
        surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)

        #X = np.array(verts[0])
        #Y = np.array(verts[1])
        #Z = np.array([self.expression.execute_l([verts[0][i], verts[1][i]]) for i in range(len(verts[2]))])

        #surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
        #                       linewidth=0, antialiased=False)

        # Customize the z axis.
        ax.set_zlim(-1.01, 1.01)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.show()

    def printresult(self):
        print('')
        print("Result:")
        for i in range(len(self.result["i"])):
            print("#" + str(i) + ":")
            print("itteration:", self.result["i"][i])
            print("x:", self.result["xk"][i])
            print("f(x):", self.result["fx"][i])
            print("action:", self.result["action"][i])
            print("----------------------------------------")
        pass