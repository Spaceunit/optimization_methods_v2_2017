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
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection



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
        self.result = {"i": [], "xk": [], "fx": [], "action": []}
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
        # a = 4 b = 2 c = 1
        # self.expression = expression.Expression("Function", "4*(x1-3)**2+(x2-2)**2")
        # self.expression = expression.Expression("Function", "4*(x1-2)**2+(x2-1)**2")
        # self.expression = expression.Expression("Function", "4*(x1-5)**2+(x2-6)**2")
        # self.expression.parameters["global_min"] = [5.0, 6.0]

        # self.expression = expression.Expression("Function", "(10*(x1-x2)**2+(x1-1)**2)**0.25")
        self.expression = expression.Expression("Function", "(10*(x1-x2)**2+(x1-1)**2)**0.25")
        self.expression.parameters["global_min"] = [1.0, 1.0]

        self.expression.parameters["unimodal"] = True
        # self.expression.parameters["global_min"] = [5.0, 6.0]
        # self.x_start = [[8.0, 9.0], [10.0, 11.0], [8.0, 11.0]]
        # self.x_start = [[5.0, 4.0], [7.0, 6.0], [5.0, 6.0]]
        # self.x_start = [[6.0, 5.0], [8.0, 7.0], [6.0, 7.0]]
        # self.x_start = [[6.0, 4.0], [8.0, 7.0], [6.0, 7.0]]


        # self.x_start = [[600.0, 400.0], [-800.0, 700.0], [600.0, 700.0]]


        # self.x_start = [[-1.2, -1.2], [0.0, 1.2], [1.2, -1.2]]


        self.x_start = [[-1.2, -1.2], [0.0, 1.2], [-1.2, 1.2]]

        # self.x_start = [[-1.2, -1.2], [-1.2, 1.2], [1.2, 1.2], [1.2, -1.2]]

        # self.x_start = [[-5.0, -5.0], [-5.0, -4.0], [-4.0, -4.0], [-4.0, -5.0]]
        # self.x_start = [[-5.0, -5.0], [-5.0, -4.0], [-4.0, -4.0], [-4.0, -5.0]]

        self.msycle = len(self.x_start)

        # self.x_start = [[-0.023444155834422054 - 3, 1.203772072451931], [0.0, 1.203772072451931 + 3], [0.023444155834422054 + 3, 1.203772072451931]]

        self.cof = {"a": 1.0, "g": 2.0, "b": 0.5}
        self.result = {"i": [], "xk": [], "fx": [], "action": []}


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
                self.print_boundary()
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
        flag = False
        exp_r = self.expression
        x_w = self.deepcopy(self.x_start)
        center = [0 for _ in range(len(x_w[0]))]
        f_arr = [exp_r.execute_l(x) for x in x_w]
        h_temp = [0 for _ in range(len(x_w[0]))]
        cycling = [0 for _ in range(len(x_w))]
        print(x_w)
        self.par_sort(x_w, f_arr, cycling)
        print(x_w)
        self.collect_data(k, x_w, f_arr, "initial simplex")
        while self.halting_check(f_arr, center) and k <= 600:
            k += 1
            print('')
            print("----------")
            print("Index", k)
            i = 1
            #for i in range(len(x_w) - 1):
            #    center = self.sum(center, x_w[i])
            center = x_w[0].copy()
            while i < (len(x_w) - 1):
                center = self.sum(center, x_w[i])
                i += 1
            #center = self.sum(x_w[0], x_w[1])
            center = self.mul(center, 1.0 / float(len(x_w) - 1))
            h_temp = self.reflection(center, x_w)
            print("center is", center)
            print("h_temp is", h_temp)
            f_h_temp = exp_r.execute_l(h_temp)
            print("fcenter is", f_h_temp)
            if flag:
                self.reduction(x_w)
                i = 0
                while i < len(x_w):
                    f_arr[i] = exp_r.execute_l(x_w[i])
                    i += 1
                flag = False
                self.collect_data(k, x_w, f_arr, "reduction for cycling of min")
            elif f_h_temp <= f_arr[0]:
                h_temp_new = self.expansion(center, h_temp, x_w)
                f_h_temp_new = exp_r.execute_l(h_temp_new)
                if f_h_temp_new < f_arr[0]:
                    x_w[-1] = h_temp_new.copy()
                    f_arr[-1] = f_h_temp_new
                    self.collect_data(k, x_w, f_arr, "expansion")
                else:
                    x_w[-1] = h_temp.copy()
                    f_arr[-1] = f_h_temp
                    self.collect_data(k, x_w, f_arr, "reflection")
            elif f_h_temp >= f_arr[-2] and f_h_temp < f_arr[-1]:
                h_temp_new = self.compression(center, h_temp, x_w)
                x_w[-1] = h_temp_new
                f_arr[-1] = exp_r.execute_l(h_temp_new)
                self.collect_data(k, x_w, f_arr, "compression")
            else:
                self.reduction(x_w)
                i = 0
                while i < len(x_w):
                    f_arr[i] = exp_r.execute_l(x_w[i])
                    i += 1
                self.collect_data(k, x_w, f_arr, "reduction")
            self.par_sort(x_w, f_arr, cycling)
            cycling_test = self.find_cycling(x_w, self.result["xk"][-1], cycling, self.msycle)
            if cycling_test != None:
                print("-------------------")
                print("Cycling on step", k)
                action_type = self.analyse_cycling(cycling_test, f_arr, self.result["fx"][-1])
                if action_type == 0:
                    x_temp = x_w[-1]
                    x_w[-1] = x_w[-2]
                    x_w[-2] = x_temp
                    f_temp = f_arr[-1]
                    f_arr[-1] = f_arr[-2]
                    f_arr[-2] = f_temp
                    cycling[-1] = 0
                elif action_type == 1:
                    x_temp = x_w[0]
                    x_w[0] = x_w[1]
                    x_w[1] = x_temp
                    f_temp = f_arr[0]
                    f_arr[0] = f_arr[1]
                    f_arr[1] = f_temp
                    flag = True
                    cycling[0] = 0
                elif action_type == 2:
                    pass
                else:
                    print("WTF")

            #self.collect_data(k, x_w, f_arr, "default iterration")
            #k += 1
        self.printresult()

    def reduction(self, x_w):
        i = 1
        while i < len(x_w):
            x_w[i] = self.dif(x_w[i], x_w[0])
            x_w[i] = self.mul(x_w[i], 0.5)
            x_w[i] = self.sum(x_w[i], x_w[0])
            i += 1

    def expansion(self, center, h_temp, x_w):
        h_temp = self.dif(h_temp, center)
        h_temp = self.mul(h_temp, self.cof["g"])
        h_temp = self.sum(h_temp, center)
        return h_temp

    def compression(self, center, h_temp, x_w):
        h_temp = self.dif(x_w[-1], center)
        h_temp = self.mul(h_temp, self.cof["b"])
        h_temp = self.sum(h_temp, center)
        return h_temp

    def reflection(self, center, x_w):
        h_temp = self.dif(center, x_w[-1])
        h_temp = self.mul(h_temp, self.cof["a"])
        h_temp = self.sum(h_temp, center)
        return h_temp

    def par_sort(self, x, f, cycling):
        f_temp = f.copy()
        x_temp = self.deepcopy(x)
        cycling_temp = cycling.copy()
        index = [i for i in range(len(x))]
        f.sort()
        for i in range(len(x)):
            x[i] = x_temp[f_temp.index(f[i])]
            cycling[i] = cycling_temp[f_temp.index(f[i])]
            f_temp[f_temp.index(f[i])] = None

    @staticmethod
    def analyse_cycling(i_cycling, f_x, f_xp):
        answer = None
        if max(f_x) == max(f_xp):
            answer = 0
        elif i_cycling == f_x.index(min(f_x)):
            answer = 1
        else:
            answer = 2
        return answer


    @staticmethod
    def find_cycling(x, xp, cycling, m_cycling):
        answer = None
        if NMM.compare(x, xp):
            i = 0
            while i < len(x):
                if x[i] in xp[i]:
                    cycling[i] += 1
                if cycling[i] > m_cycling:
                    answer = i
                i += 1
        return answer

    @staticmethod
    def compare0(x1, x2):
        ansver = False
        for i in range(len(x1)):
            for j in range(len(x1[0])):
                if x1[i][j] in x2:
                    ansver = True
        return ansver

    @staticmethod
    def compare(x1, x2):
        ansver = False
        for i in range(len(x1)):
            if x1[i] in x2:
                ansver = True
        return ansver

    def halting_check(self, f_arr, center):
        r = True
        f_center = self.expression.execute_l(center)
        if math.sqrt(math.pow(sum([item - f_center for item in f_arr]), 2.0) / float(len(f_arr))) <= self.epsilon[0]:
            r = False
            print("Halting check! - True")
        return r

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
        xn = [[]for _ in x]
        for i in range(len(x)):
            for j in range(len(x[i])):
                xn[i].append(x[i][j])
        return xn

    def collect_data(self, i, x, fx, action):
        self.result["i"].append(i)
        self.result["xk"].append(self.deepcopy(x))
        self.result["fx"].append(fx.copy())
        self.result["action"].append(action)

    def get_contour_line(self, a, step):
        cl_path_up = []
        cl_path_down = []
        boundary = self.get_boundary_for_cl(a)
        boundary.sort()
        x1 = boundary[0]

        while x1 < boundary[1]:
            pair = self.cl_expression_x2(x1, a)
            cl_path_down.append([x1, pair[0]])
            cl_path_up.append([x1, pair[1]])
            x1 += step

        pair = self.cl_expression_x2(boundary[1], a)
        cl_path_down.append([boundary[1], pair[0]])
        cl_path_up.append([boundary[1], pair[1]])

        cl_path_down.reverse()

        cl_path_down.pop(-1)
        cl_path_down.pop(0)

        return cl_path_up + cl_path_down

        pass

    def cl_expression_x2(self, x1, a):
        part_root = (0.1 *(a**4 - (x1 - 1)**2))**0.5
        x2_up = x1 + part_root
        x2_down = x1 - part_root
        return [x2_down, x2_up]



    def get_boundary_for_cl(self, a):
        return [1.0 - math.pow(a, 2.0), 1.0 + math.pow(a, 2.0)]

    def printresult_g(self):
        fig, ax = plt.subplots()
        patches = []
        N = 3
        for i in range(len(self.result["i"])):
            for j in range(N):
                polygon = Polygon(np.array(self.result["xk"][i]), True)
            patches.append(polygon)

        p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)

        colors = 100 * np.random.rand(len(patches))
        p.set_array(np.array(colors))

        ax.add_collection(p)
        # Set x ticks
        #plt.xticks(np.linspace(-10, 10, 10, endpoint=True))

        # Set y ticks
        #plt.yticks(np.linspace(-10, 10, 10, endpoint=True))
        plt.show()
        pass

    def printresult_3d(self):
        pass

    def print_boundary(self):
        a = 2.0
        cl_x = []
        cl_y = []
        cl = self.get_contour_line(a, 0.1)
        print(cl)

        i = 0
        while i < len(cl):
            cl_x.append(cl[i][0])
            cl_y.append(cl[i][1])
            i += 1
        print(cl_x)
        print(cl_y)
        #cl_x.sort()
        #cl_y.sort()
        #x = np.array(cl_x)
        #y = np.array(cl_y)
        delta = 0.055
        radius = 10
        sector = self.expression.parameters["global_min"].copy()
        sector = [sector[0] - math.copysign(radius, sector[0]), sector[1] + math.copysign(radius, sector[1])]
        x = np.arange(sector[0], sector[1], delta)
        y = np.arange(sector[0], sector[1], delta)

        X, Y = np.meshgrid(x, y)

        #Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
        #Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)

        #Z = 10.0 * (Z2 - Z1)
        # "(10*(x1-x2)**2+(x1-1)**2)**0.25"
        #Z = 10.0 * ((X - Y)**2 + (X - 1)**2)**0.25

        Z = self.expression.execute_l([X, Y])

        print(Z)

        #
        fig, ax = plt.subplots()
        center = []
        m_patches = []
        verts = []
        N = len(self.x_start)
        for i in range(len(self.result["i"])):
            polygon = Polygon(np.array(self.result["xk"][i]), True)
            # count center...
            j = 1
            center = self.result["xk"][i][0].copy()
            while j < N:
                center = self.sum(center, self.result["xk"][i][j])
                j += 1
            center = self.mul(center, 1.0 / float(N))
            # print("Center is", center)
            verts.append((center[0], center[1]))
            ax.text(center[0], center[1], "#"+str(self.result["i"][i])+" ", color="black", fontsize="10", verticalalignment='bottom', horizontalalignment='right')
            # ...
            m_patches.append(polygon)

        path = Path(verts)
        patch = patches.PathPatch(path, facecolor='none', lw=0.5)
        ax.add_patch(patch)
        xs, ys = zip(*verts)
        plt.plot(xs, ys, "x--", lw=1.5, color='black', ms=10)
        p = PatchCollection(m_patches, cmap=matplotlib.cm.jet, alpha=0.4, lw=1.0)

        colors = 100 * np.random.rand(len(m_patches))
        p.set_array(np.array(colors))

        ax.add_collection(p)


        #

        #plt.figure()
        #CS = plt.contour(X, Y, Z,
        #                 colors='k'  # negative contours will be dashed by default
        #                 )
        #plt.clabel(CS, fontsize=9, inline=1)
        #plt.title('Single color - negative contours dashed')

        #plt.figure()
        CS = plt.contour(X, Y, Z)
        plt.clabel(CS, inline=1, fontsize=10)
        plt.title("Path of simplex with "+str(N)+" vertexes")

        plt.show()
        pass

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