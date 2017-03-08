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

    def dostaff(self):
        task = 0
        while (task != 1):
            print('')
            print("Golden section search")
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
        pass

    def resolve(self):
        pass

    def printresult(self):
        pass

    def printresult1(self):
        pass
    # 13