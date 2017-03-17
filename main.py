import openpyxl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab


from resource import matrix
from resource import excel_transfer

import jap
import golden_section_search
import dichotomy_method
import newtons_method
import sven_method
import bisection_method
import dsk_paula


class Work:
    def __init__(self):
        self.a = matrix.Matrix([[0]],"Initial matrix")
        self.accuracy = 3
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
            "jap": 10,
            "gss": 11,
            "dm": 12,
            "nm": 13,
            "sm": 14,
            "bsm": 15,
            "dskp": 16

        }
        pass

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

    def showCommands(self):
        print('')
        print("Commands...")
        for item in self.commands:
            print(str(item) + ": " + str(self.commands[item]))

    def showHelp(self):
        print('')
        print("Help v0.001")
        print("Author of this program: Sir Oleksiy Polshchak")
        self.showCommands()

    def dostaff(self):
        task = 0
        while (task != 1):
            print('')
            print("Optimization methods v2 2017")
            print('')
            task = self.enterCommand()
            if (task == 2):
                self.dostaff()
            elif (task == 3):
                pass
            elif (task == 4):
                self.showHelp()
            elif (task == 5):
                self.inputnewdata()
                pass
            elif (task == 6):
                self.a.showmatrix()
                pass
            elif (task == 8):
                self.setaccuracy()
                pass
            elif (task == 9):
                self.makedafault()
            elif (task == 10):
                Task = jap.JAP()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif (task == 11):
                Task = golden_section_search.GSS()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif (task == 12):
                Task = dichotomy_method.DM()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif (task == 13):
                Task = newtons_method.NM()
                Task.importparam(self.accuracy)
                Task.dostaff()
            elif (task == 14):
                Task = sven_method.SM()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif (task == 15):
                Task = bisection_method.BSM()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif (task == 16):
                Task = dsk_paula.DSKP()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
        pass


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
        pass

    def makedafault(self):
        self.exeldata = excel_transfer.Excel()
        self.a = self.exeldata.transferlist('square')
        self.accuracy = 3


Some = Work()
Some.dostaff()
