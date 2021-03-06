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
import dsk_paula_v2
import chords_method
import bolzano_bisection_method
import hooke_jeeves_pattern_search
import nelder_mead_method
import gradient_descent
import partan_gradient_descent
import second_derivative_method_nm
import powell_method_conjugate_directions_p
import powell_method_conjugate_directions_m
import powell_method_conjugate_directions_3
import powell_method_conjugate_directions
import fletcher_reeves_conjugate_gradient_method
import quasi_newton_method
import conjugate_direction_method

import nelder_mead_method_cw
import nelder_mead_method_cw_fix
import nelder_mead_method_cw_ds


class Work:
    def __init__(self):
        self.accuracy = 3
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
                "jap": 10,
                "gss": 11,
                "dm": 12,
                "nm": 13,
                "sm": 14,
                "bsm": 15,
                "dskp": 16,
                "cm": 17,
                "bbsm": 18,
                "hjps": 19,
                "nmm": 20,
                "gdm": 21,
                "pgdm": 22,
                "sdmnm": 23,
                "pmcd": 24,
                "pmcdp": 25,
                "pmcd3": 26,
                "frcgm": 27,
                "qnm": 28,
                "cdm": 29,
                "cw": 30,
                "pe": 31
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
                "jap": "Job Assignment Problem",
                "gss": "Hooke-Jeeves pattern search method",
                "dm": "Dichotomy method",
                "nm": "Newton's method",
                "sm": "Sven's method",
                "bsm": "Bisection method",
                "dskp": "DSK Paul`s method",
                "cm": "Chords method",
                "bbsm": "Bolzano-bisection method",
                "hjps": "Hooke-Jeeves pattern search method",
                "nmm": "Nelder–Mead method",
                "gdm": "Gradient descent method",
                "pgdm": "Partan gradient descent method",
                "sdmnm": "Second derivative method: Newton`s method",
                "pmcd": "The Powell method of conjugate directions",
                "pmcdp": "The Powell method of conjugate directions (p)",
                "pmcd3": "The Powell method of conjugate directions (p)",
                "frcgm": "The Fletcher-Reeves conjugate gradient method",
                "qnm": "Quasi-Newton method",
                "cdm": "Conjugate gradient method",
                "cw": "Course work",
                "pe": "python excel 2010"
            }
        }
        pass

    def enterCommand(self):
        command = "0"
        print('')
        print("Enter command (help for Q&A)")
        while command not in self.commands["commands"]:
            command = input("->")
            if command not in self.commands["commands"]:
                print("There is no such command")
            else:
                return self.commands["commands"][command]

    def showCommands(self):
        print('')
        print("Commands...")
        print("---")
        for item in self.commands["commands"]:
            print(str(item) + ":")
            print("Number: " + str(self.commands["commands"][item]))
            print("Description: " + str(self.commands["description"][item]))
            print("---")

    def showHelp(self):
        print('')
        print("Help v0.002")
        print("Author of this program: Oleksiy Polshchak")
        self.showCommands()

    def dostaff(self):
        task = 0
        while (task != 1):
            print('')
            print("Optimization methods v2 2017")
            print('')
            task = self.enterCommand()
            if task == 2:
                self.dostaff()
            elif task == 3:
                pass
            elif task == 4:
                self.showHelp()
            elif task == 5:
                self.inputnewdata()
                pass
            elif task == 6:
                self.a.showmatrix()
                pass
            elif task == 8:
                self.setaccuracy()
                pass
            elif task == 9:
                self.makedafault()
            elif task == 10:
                Task = jap.JAP()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 11:
                Task = golden_section_search.GSS()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 12:
                Task = dichotomy_method.DM()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 13:
                Task = newtons_method.NM()
                Task.importparam(self.accuracy)
                Task.dostaff()
            elif task == 14:
                Task = sven_method.SM()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 15:
                Task = bisection_method.BSM()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 16:
                Task = dsk_paula_v2.DSKP()
                Task.importparam(self.accuracy)
                Task.dostaff()
            elif task == 17:
                Task = chords_method.CM()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 18:
                Task = bolzano_bisection_method.BBSM()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 19:
                Task = hooke_jeeves_pattern_search.HJPS()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 20:
                Task = nelder_mead_method.NMM()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 21:
                Task = gradient_descent.GDM()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 22:
                Task = partan_gradient_descent.PGDM()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 23:
                Task = second_derivative_method_nm.SDMNM()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 24:
                Task = powell_method_conjugate_directions.PMCD()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 25:
                Task = powell_method_conjugate_directions_p.PMCD()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 26:
                Task = powell_method_conjugate_directions_3.PMCD3()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 27:
                Task = fletcher_reeves_conjugate_gradient_method.FRCGM()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 28:
                Task = quasi_newton_method.QNM()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 29:
                Task = conjugate_direction_method.CDM()
                Task.importparam(self.accuracy)
                Task.dostaff()
                pass
            elif task == 30:
                Task = nelder_mead_method_cw_ds.NMM()
                Task.importparam(self.accuracy)
                Task.dostaff()
            elif task == 31:
                Task = excel_transfer.Excel()
                Task.importparam()
                Task.dostaff()
        pass


    def inputnewdata(self):
        task = 0
        self.a = matrix.Matrix([], "Initial matrix")
        while task != 1:
            print('')
            print("Enter matrix dimension:")
            while task != 1:
                num = int(input("-> "))
                print("Input is correct? (enter - yes/n - no)")
                command = input("-> ")
                if command != "n":
                    self.a = self.inputmatrix(num)
                    task = 1
            task = 0
            self.a.rename("Initial matrix")
            self.a.showmatrix()
            print("Matrix is correct? (enter - yes/n - no)")
            command = input("-> ")
            if command != "n":
                task = 1

    def inputmatrix(self, num):
        print('')
        i = 0
        task = 0
        nm = matrix.Matrix([], "new matrix")
        while i < num:
            print("Enter matrix row (use spaces)")
            print("Row ", i + 1)
            while task != 1:
                row = list(map(float, input("-> ").split()))
                print("Input is correct? (enter - yes/n - no)")
                command = input("-> ")
                if command != "n" and len(row) == num:
                    task = 1
                    nm.appendnrow(row)
                elif len(row) != num:
                    print('')
                    print("Incorrect input: count of items.")
            task = 0
            i += 1
        return nm

    def setaccuracy(self):
        task = 0
        print('')
        print("Enter accuracy:")
        while task != 1:
            self.accuracy = int(input("-> "))
            print("Input is correct? (enter - yes/n - no)")
            command = input("-> ")
            if command != "n":
                task = 1
        pass

    def makedafault(self):
        self.exeldata = excel_transfer.Excel()
        self.a = self.exeldata.transferlist('square')
        self.accuracy = 3


Some = Work()
Some.dostaff()
