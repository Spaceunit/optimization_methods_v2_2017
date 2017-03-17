class Expression:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        self.range = None
        self.local_min = None
        self.local_max = None
        self.parameters = {}

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

    def input_range(self):
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

    def show_expr(self):
        print("Expression name:", self.name)
        print("Expression:", self.expression)
        print("Range:", self.range)
        print("Local minimum:", self.local_min)
        print("Local maximum:", self.local_max)
        print("Parameters:", self.parameters)
        pass

    def execute(self, x):
        return eval(self.expression)

    def rename(self, name):
        self.name = name
        pass

    def concatexp(self):
        pass