def inputmatrix(self):
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

class Expression:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        self.range = None
        self.local_min = None
        self.local_max = None

    def input_expr(self):
        ans = False
        command = ""
        print('')
        while not ans:
            self.range = list(map(float, input("Input range -> ").split()))
            print("Input is correct?[Y]-> ")
            command = input("-> ")
            if (command.lower() != "y" or command.lower() != "yes") and len(self.range) != 2:
                print("Try again and input \"yes\" or \"y\"")
            else:
                ans = True

    def input_expr(self):
        ans = False
        command = ""
        print('')
        while not ans:
            self.expression = str(input("enter expression -> "))
            print("Input is correct?[Y]-> ")
            command = input("-> ")
            if command.lower() != "y" or command.lower() != "yes":
                print("Try again and input \"yes\" or \"y\"")
            else:
                ans = True

    def set_range(self):

        pass

    def show_expr(self):
        pass

    def rename(self):
        pass

    def concatexp(self):
        pass