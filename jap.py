import math
import matrix
import excel_transfer
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab


class JAP:
    def __init__(self):
        self.a = matrix.Matrix([[0]], "Initial matrix")
        self.raw_data = {}
        self.result_data = {}
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
        self.accuracy = 3
        #self.print_raw_data()
        print("Accuracy of calculations:", (10 ** (-self.accuracy)))
        self.a = matrix.Matrix([[9, 2, 7, 8],
                                [6, 4, 3, 7],
                                [5, 8, 1, 8],
                                [7, 6, 9, 4]],
                                "Cost matrix")
        self.inm = self.a.copy()
        self.inm.rename("Initial matrix")
        self.mask = matrix.Matrix([[0]], "Mask matrix")
        self.mask.makezeromatrix(self.a.len[0])

        self.c_cover = matrix.Vector([], "Column cover")
        self.r_cover = matrix.Vector([], "Row cocer")

        self.c_cover.makezero(self.a.len[0])
        self.r_cover.makezero(self.a.len[0])

        self.path_row_0 = None
        self.path_col_0 = None

        self.a.showmatrix()
        self.mask.showmatrix()

        #self.a.rename("Cost matrix")
        pass

    def makedefault2(self):
        self.accuracy = 3
        #self.print_raw_data()
        print("Accuracy of calculations:", (10 ** (-self.accuracy)))
        self.a = matrix.Matrix([[1, 2, 3],
                                [2, 4, 6],
                                [3, 6, 9]],
                                "Cost matrix")
        self.inm = self.a.copy()
        self.inm.rename("Initial matrix")

        self.mask = matrix.Matrix([[0]], "Mask matrix")
        self.mask.makezeromatrix(self.a.len[0])

        self.c_cover = matrix.Vector([], "Column cover")
        self.r_cover = matrix.Vector([], "Row cocer")

        self.c_cover.makezero(self.a.len[0])
        self.r_cover.makezero(self.a.len[0])

        self.path_row_0 = None
        self.path_col_0 = None

        self.a.showmatrix()
        self.mask.showmatrix()

        #self.a.rename("Cost matrix")
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
        task = 0
        self.a = matrix.Matrix([], "Initial matrix")
        while (task != 1):
            print('')
            print("Enter matrix dimension:")
            while (task != 1):
                num = int(input("-> "))
                print("Input is correct? (enter - yes/n - no)")
                command = input("-> ")
                if (command != "n"):
                    self.a = self.inputmatrix(num)
                    task = 1
            task = 0
            self.a.rename("Initial matrix")
            self.a.showmatrix()
            print("Matrix is correct? (enter - yes/n - no)")
            command = input("-> ")
            if (command != "n"):
                task = 1

        self.inm = self.a.copy()
        self.inm.rename("Initial matrix")

        self.mask = matrix.Matrix([[0]], "Mask matrix")
        self.mask.makezeromatrix(self.a.len[0])

        self.c_cover = matrix.Vector([], "Column cover")
        self.r_cover = matrix.Vector([], "Row cocer")

        self.c_cover.makezero(self.a.len[0])
        self.r_cover.makezero(self.a.len[0])

        self.path_row_0 = None
        self.path_col_0 = None

        self.a.showmatrix()
        self.mask.showmatrix()

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

    def dostaff(self):
        task = 0
        while (task != 1):
            print('')
            print("Job Assignment Problem")
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
                self.resolve()
                pass
            elif (task == 11):
                self.printresult()

            elif (task == 12):
                self.printresult1()
            elif (task == 13):
                self.makedefault2()
        pass

    def print_raw_data(self):
        self.a.showmatrix()
        pass

    def resolve(self):
        self.done = False
        self.step = 1
        self.step_history = 1
        while(not self.done):
            self.a.showmatrix()
            self.mask.showmatrix()
            if self.step == 1:
                self.step_one()
                pass
            elif self.step == 2:
                self.step_two()
                pass
            elif self.step == 3:
                self.step_three()
                pass
            elif self.step == 4:
                self.step_four()
                pass
            elif self.step == 5:
                self.step_five()
                pass
            elif self.step == 6:
                self.step_six()
                pass
            elif self.step == 7:
                self.step_seven()
                pass
            self.step_history += 1
            print(self.step_history)
            print("")
            self.r_cover.showvector()
            self.c_cover.showvector()
        pass

    def step_one(self):
        print("step 1")
        min_in_row = None
        r = 0
        while r < self.a.len[0]:
            min_in_row = self.a.getel(r, 0)
            c = 0
            while c < self.a.len[1]:
                if self.a.getel(r, c) < min_in_row:
                    min_in_row = self.a.getel(r, c)
                c += 1
            c = 0
            while c < self.a.len[1]:
                self.a.chel(r, c, self.a.getel(r, c) - min_in_row)
                c += 1
            r += 1
        self.step = 2
        pass

    def step_two(self):
        print("step 2")
        r = 0
        while r < self.a.len[0]:
            c = 0
            while c < self.a.len[1]:
                if self.a.getel(r, c) == 0 and self.r_cover.getel(r) == 0 and self.c_cover.getel(c) == 0:
                    self.mask.chel(r, c, 1)
                    self.r_cover.chel(r, 1)
                    self.c_cover.chel(c, 1)
                c += 1
            r += 1
        r = 0
        while r < self.a.len[0]:
            self.r_cover.chel(r, 0)
            r += 1
        c = 0
        while c < self.a.len[1]:
            self.c_cover.chel(c, 0)
            c += 1
        self.step = 3
        pass

    def step_three(self):
        print("step 3")
        colcount = 0
        r = 0
        while r < self.a.len[0]:
            c = 0
            while c < self.a.len[1]:
                if self.mask.getel(r, c) == 1:
                    self.c_cover.chel(c, 1)
                c += 1
            r += 1
        colcount = 0
        c = 0
        while c < self.a.len[1]:
            if self.c_cover.getel(c) == 1:
                colcount += 1
            c += 1
        if colcount >= self.a.len[1] or colcount >= self.a.len[0]:
            self.step = 7
        else:
            self.step = 4
        pass

    def step_four(self):
        print("step 4")
        self.row = -1
        self.col = -1
        done = False
        while not done:
            self.find_zero()
            if self.row == -1:
                done = True
                self.step = 6
            else:
                self.mask.chel(self.row, self.col, 2)
                if self.star_in_row(self.row):
                    self.find_star_in_row(self.row)
                    self.r_cover.chel(self.row, 1)
                    self.c_cover.chel(self.col, 0)
                else:
                    done = True
                    self.step = 5
                    self.path_row_0 = self.row
                    self.path_col_0 = self.col

        pass

    def step_five(self):
        print("step 5")
        done = False
        r = -1
        c = -1
        self.path_count = 1
        #self.path = [[self.path_row_0], [self.path_col_0]]
        self.path = [[0,0] for _ in range(61)]
        print("part 5 subpart 2")
        self.path[self.path_count - 1][0] = self.path_row_0
        self.path[self.path_count - 1][1] = self.path_col_0
        print("part 5 subpart 3")
        while not done:
            r = self.find_start_in_col(self.path[self.path_count - 1][1])
            print("Before if > -1")
            if r > -1:
                self.path_count += 1
                self.path[self.path_count - 1][0] = r
                self.path[self.path_count - 1][1] = self.path[self.path_count - 2][1]
            else:
                done = True
            print("After if > -1")
            if not done:
                print("Find value")
                value = self.find_prime_in_row(self.path[self.path_count - 1][0])
                print("Value is", value)
                if value == None:
                    print("Before continue")
                    continue
                else:
                    c = value
                    print("c is", c)
                self.path_count += 1
                self.path[self.path_count - 1][0] = self.path[self.path_count - 2][0]
                self.path[self.path_count - 1][1] = c
        print("Before 3")
        self.augment_path()
        print("Before 2")
        self.clear_covers()
        print("Before 1")
        self.erase_pripes()
        self.step = 3
        pass

    def step_six(self):
        print("step 6")
        minval = 5000
        minval = self.find_smallest(minval)
        r = 0
        while r < self.a.len[0]:
            c = 0
            while c < self.a.len[1]:
                if self.r_cover.getel(r) == 1:
                    #self.a.chel(r, c, self.mask.getel(r, c) + minval)
                    self.a.matrix[r][c] += minval
                if self.c_cover.getel(c) == 0:
                    #self.a.chel(r, c, self.mask.getel(r, c) - minval)
                    self.a.matrix[r][c] -= minval
                c += 1
            r += 1
        self.step = 4
        pass

    def step_seven(self):
        print("---------Run Complete----------")
        result = 0
        r = 0
        while r < self.a.len[0]:
            c = 0
            while c < self.a.len[1]:
                if self.mask.getel(r, c) == 1:
                    result += self.inm.getel(r, c)
                c += 1
            r += 1
        print("Minimum of cost: ", result)
        self.done = True

    def find_zero(self):
        r = 0
        c = None
        done = False
        self.row = -1
        self.col = -1
        while not done:
            c = 0
            done_1 = True
            while done_1:
                if self.a.getel(r, c) == 0 and self.r_cover.getel(r) == 0 and self.c_cover.getel(c) == 0:
                    self.row = r
                    self.col = c
                    done = True
                c += 1
                if c >= self.a.len[1] or done:
                    done_1 = False
            r += 1
            if r >= self.a.len[0]:
                done = True
        pass

    def star_in_row(self, row):
        tmp = False
        c = 0
        while c < self.a.len[1]:
            if self.mask.getel(row, c) == 1:
                tmp = True
            c += 1
        return tmp

    def find_star_in_row(self, row):
        self.col = -1
        c = 0
        while c < self.a.len[1]:
            if self.mask.getel(row, c) == 1:
                self.col = c
            c += 1
        print("find_start_in_row is done")
        pass

    def find_start_in_col(self, c):
        r = -1
        i = 0
        while i < self.a.len[0]:
            if self.mask.getel(i, c) == 1:
                r = i
            i += 1
        return r

    def find_prime_in_row(self, r):
        c = None
        j = 0
        while j < self.a.len[1]:
            if self.mask.getel(r, j) == 2:
                c = j
            j += 1
        return c

    def augment_path(self):
        p = 0
        while p < self.path_count:
            if self.mask.getel(self.path[p][0], self.path[p][1]) == 1:
                self.mask.chel(self.path[p][0], self.path[p][1], 0)
            else:
                self.mask.chel(self.path[p][0], self.path[p][1], 1)
            p += 1
    def clear_covers(self):
        r = 0
        while r < self.a.len[0]:
            self.r_cover.chel(r, 0)
            r += 1
        c = 0
        while c < self.a.len[1]:
            self.c_cover.chel(c, 0)
            c += 1

    def erase_pripes(self):
        r = 0
        while r < self.a.len[0]:
            c = 0
            while c < self.a.len[1]:
                if self.mask.getel(r, c) == 2:
                    self.mask.chel(r, c, 0)
                c += 1
            r += 1

    def find_smallest(self, minval):
        r = 0
        while r < self.a.len[0]:
            c = 0
            while c < self.a.len[1]:
                if self.r_cover.getel(r) == 0 and self.c_cover.getel(c) == 0:
                    if minval > self.a.getel(r, c):
                        minval = self.a.getel(r, c)
                c += 1
            r += 1
        return minval

    def printresult(self):
        self.a.showmatrix()
        self.mask.showmatrix()
        pass

    def printresult1(self):
        pass
    # 13