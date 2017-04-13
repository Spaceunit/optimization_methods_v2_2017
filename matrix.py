import math
class Matrix:
    def __init__(self, matrix, name):
        self.name = name
        self.setmatrix(matrix)
        self.len = [len(self.matrix), len(self.matrix)]

    def copy(self):
        matrix = []
        for row in self.matrix:
            r = []
            for item in row:
                r.append(item)
                pass
            matrix.append(r)
        return Matrix(matrix, self.name + " copy")

    def setmatrix(self, matrix):
        self.matrix = []
        for row in matrix:
            r = []
            for item in row:
                r.append(item)
                pass
            self.matrix.append(r)

    def showmatrixold(self):
        print('')
        sh = self.copy()
        print(self.name)
        for row in self.matrix:
            print(row)
        print('')

    def showmatrix(self):
        print('')
        #sh = self.copy()
        matrix = self.matrix
        print(self.name)
        #for row in self.matrix:
            #print(row)
        s = [[str(e) for e in row] for row in matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))
        print('')

    def showmatrixaccuracy3(self):
        print('')
        #sh = self.copy()
        accuracy = 3
        matrix = self.matrix
        print(self.name)
        #for row in self.matrix:
            #print(row)
        s = [[str(round(e, accuracy)) for e in row] for row in matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))
        print('')

    def showmatrixaccuracy(self, accuracy):
        print('')
        #sh = self.copy()
        matrix = self.matrix
        print(self.name)
        #for row in self.matrix:
            #print(row)
        s = [[str(round(e, accuracy)) for e in row] for row in matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))
        print('')


    def appendrow(self, rowlen):
        self.matrix.append([0 for i in range(0, rowlen)])
        self.len[0] = len(self.matrix)
        self.len[1] = len(self.matrix[-1])

    def appenderow(self):
        self.matrix.append([])
        self.len[0] = len(self.matrix)
        self.len[1] = len(self.matrix[-1])

    def appendnrow(self, row):
        array = [item for item in row]
        self.matrix.append(array)
        self.len[0] = len(self.matrix)
        self.len[1] = len(self.matrix[-1])

    def append_column(self, column):
        array = [item for item in column]

        if self.len[0] < len(array):
            while self.len[0] < len(array):
                self.matrix.append([None])
                self.len[0] = len(self.matrix)

        for i in range(self.len[0]):
            self.matrix[i].append(array[i])

        self.len[0] = len(self.matrix)
        self.len[1] = len(self.matrix[-1])

    def chel(self, i, j, item):
        if (i >= 0 and j >= 0):
            if (i < self.len[0] and j < self.len[1]):
                self.matrix[i][j] = item
            else:
                print("change el: List assignment index out of range!")
        elif (i < 0 and j < 0):
            if (i >= -self.len[0] and j >= -self.len[1]):
                self.matrix[i][j] = item
            else:
                print("change el: List assignment index out of range!")
        else:
            print("change el: List assignment index out of range! (sign)")

    def getel(self, i, j):
        if (i >= 0 and j >= 0):
            if (i < self.len[0] and j < self.len[1]):
                return self.matrix[i][j]
            else:
                print("get el: List assignment index out of range!")
        elif (i < 0 and j < 0):
            if (i >= -self.len[0] and j >= -self.len[1]):
                return self.matrix[i][j]
            else:
                print("get el: List assignment index out of range!")
        else:
            print("get el: List assignment index out of range! (sign)")

    def appendel(self, i, item):
        if (i >= 0):
            if (i < self.len[0]):
                self.matrix[i].append(item)
            else:
                print("append el: List assignment index out of range!")
        elif (i < 0):
            if (i >= -self.len[0]):
                self.matrix[i].append(item)
            else:
                print("append el: List assignment index out of range!")
        else:
            print("append el: List assignment index out of range! (sign)")

    def delel(self,i,j):
        if (i >= 0 and j >= 0):
            if (i < self.len[0] and j < len(self.matrix[i])):
                return self.matrix[i].pop(j)
            else:
                print("del el: List assignment index out of range!")
        elif (i < 0 and j < 0):
            if (i >= -self.len[0] and j >= -len(self.matrix[i])):
                return self.matrix[i].pop(j + len(self.matrix[i]))
            else:
                print("del el: List assignment index out of range!")
        else:
            print("del el: List assignment index out of range! (sign)")

    def delrow(self,i):
        if (i >= 0):
            if (i < self.len[0]):
                row = self.matrix.pop(i)
                self.len[0] = len(self.matrix)
                return row
            else:
                print("del row: List assignment index out of range!")
        elif (i < 0):
            if (i >= -self.len[0]):
                row = self.matrix.pop(i + self.len[0])
                self.len[0] = len(self.matrix)
                return row
            else:
                print("del row: List assignment index out of range!")
        else:
            print("del row: List assignment index out of range! (sign)")

    def getrow(self,i):
        if (i >= 0):
            if (i < self.len[0]):
                row = Vector(self.matrix[i],"Row" + str(i) + "of " + self.name)
                return row
            else:
                print("get row: List assignment index out of range!")
        elif (i < 0):
            if (i >= -self.len[0]):
                row = Vector(self.matrix[i + self.len[0]], "Row" + str(i + self.len[0]) + "of " + self.name)
                return row
            else:
                print("get row: List assignment index out of range!")
        else:
            print("get row: List assignment index out of range! (sign)")

    def setrowm(self, i, row):
        if (i >= 0 and row.len == self.len[1]):
            if (i < self.len[0]):
                for j in range(0, self.len[1]):
                    self.matrix[i][j] = row.vector[j]
            else:
                print("set row: List assignment index out of range!")
        elif (i < 0 and row.len == self.len[1]):
            if (i >= -self.len[0]):
                for j in range(0, self.len[1]):
                    self.matrix[i + self.len[0]][j] = row.vector[j]
            else:
                print("set row: List assignment index out of range!")
        else:
            print("set row: List assignment index out of range! (sign)")

    def rowmnumber(self, i, num, accuracy):
        if (i >= 0):
            if (i < self.len[0]):
                for j in range(0, self.len[1]):
                    self.matrix[i][j] = round(self.matrix[i][j] * num, accuracy)
            else:
                print("rowmnumber: List assignment index out of range!")
        elif (i < 0):
            if (i >= -self.len[0]):
                for j in range(0, self.len[1]):
                    self.matrix[i + self.len[0]][j] = round(self.matrix[i + self.len[0]][j] * num, accuracy)
            else:
                print("rowmnumber: List assignment index out of range!")
        else:
            print("rowmnumber: List assignment index out of range! (sign)")

    def rowdnumber(self, i, num, accuracy):
        if (i >= 0):
            if (i < self.len[0]):
                for j in range(0, self.len[1]):
                    self.matrix[i][j] = round(self.matrix[i][j] / num, accuracy)
            else:
                print("rowdnumber: List assignment index out of range!")
        elif (i < 0):
            if (i >= -self.len[0]):
                for j in range(0, self.len[1]):
                    self.matrix[i + self.len[0]][j] = round(self.matrix[i + self.len[0]][j] / num, accuracy)
            else:
                print("rowdnumber: List assignment index out of range!")
        else:
            print("rowdnumber: List assignment index out of range! (sign)")

    def rowsubtract(self, i, i2, accuracy):
        if (i >= 0 and i2 >=0):
            if (i < self.len[0] and i2 < self.len[0]):
                for j in range(0, self.len[1]):
                    self.matrix[i][j] = round(self.matrix[i][j] - self.matrix[i2][j], accuracy)
            else:
                print("rowsubtract: List assignment index out of range!")
        elif (i < 0 and i2 < 0):
            if (i >= -self.len[0] and i2 >= -self.len[0]):
                for j in range(0, self.len[1]):
                    self.matrix[i + self.len[0]][j] = round(self.matrix[i + self.len[0]][j] - self.matrix[i2 + self.len[0]][j], accuracy)
            else:
                print("rowsubtract: List assignment index out of range!")
        else:
            print("rowsubtract: List assignment index out of range! (sign)")
        pass

    def rowsummarize(self, i, i2, accuracy):
        if (i >= 0 and i2 >= 0):
            if (i < self.len[0] and i2 < self.len[0]):
                for j in range(0, self.len[1]):
                    self.matrix[i][j] = round(self.matrix[i][j] + self.matrix[i2][j], accuracy)
            else:
                print("rowsubtract: List assignment index out of range!")
        elif (i < 0 and i2 < 0):
            if (i >= -self.len[0] and i2 >= -self.len[0]):
                for j in range(0, self.len[1]):
                    self.matrix[i + self.len[0]][j] = round(
                        self.matrix[i + self.len[0]][j] + self.matrix[i2 + self.len[0]][j], accuracy)
            else:
                print("rowsubtract: List assignment index out of range!")
        else:
            print("rowsubtract: List assignment index out of range! (sign)")
        pass


    def makezeromatrix(self, dim):
        if (dim > 0):
            self.matrix = [[0 for i in range(0, dim)] for i in range(0, dim)]
            self.len[0] = len(self.matrix)
            self.len[1] = len(self.matrix[0])
        else:
            print("Make zero-matrix: dim is < 0")

    def makedimatrix(self, dim):
        if (dim > 0):
            self.makezeromatrix(dim)
            for i in range(0, dim):
                self.matrix[i][i] = 1
            self.len[0] = len(self.matrix)
            self.len[1] = len(self.matrix[0])
        else:
            print("Make dimatrix: dim is < 0")

    def join(self, jm):
        for i in range(0, self.len[0]):
            for j in range(0, jm.len[1]):
                self.appendel(i, jm.getel(i, j))
        self.len[0] = len(self.matrix)
        self.len[1] = len(self.matrix[0])

    def copypart(self, param):
        # param = [i,j,sizei,sizej]
        result = []
        for i in range(param[0], param[2]):
            result.append([])
            for j in range(param[1], param[3]):
                result[-1].append(self.getel(i, j))
        return Matrix(result, "part copy")

    def reverseim(self):
        self.matrix = self.matrix[::-1]

    def rename(self, name):
        self.name = name

    def zerodown(self):
        for i in range(0,self.len[0]):
            pass
        self.matrix.append(self.matrix.pop(0))

    def transpose(self):
        if (self.len[0] == self.len[1]):
            for i in range(0, self.len[0]):
                for j in range(i, self.len[1]):
                    a = self.matrix[i][j]
                    self.matrix[i][j] = self.matrix[j][i]
                    self.matrix[j][i] = a
        elif (self.len[0] >= self.len[1]):
            for i in range(0, self.len[0]):
                if (i == self.len[1]):
                    pass
                for j in range(0, self.len[1]):
                    a = self.matrix[i][j]
                    self.matrix[i][j] = self.matrix[j][i]
                    self.matrix[j][i] = a
        pass

    def matrixm(self, B, accuracy):
        if (self.len[1] == B.len[0]):
            R = Matrix([], "Result")
            for n in range(0, self.len[0]):
                R.appendrow(B.len[1])
                for m in range(0, B.len[1]):
                    for i in range(0, self.len[1]):
                        sum = R.matrix[n][m]
                        R.matrix[n][m] += round(self.matrix[n][i] * B.matrix[i][m], accuracy)
                        #print("C[",n,m,"]+=","A[",n,i,"]*","B[",i,m,"]")
                        #print(R.matrix[n][m]," is sum of ", sum,"+", self.matrix[n][i],"*", B.matrix[i][m], " n: ", n," i: ", i, " i: ", i," m: ", m)
                        #R.showmatrix()
                #print("Row [",n,"] is done")
            return R
        else:
            print("Matrixm: error j != m")
            return 0

    def matrixmv(self, V, accuracy):
        if (self.len[0] == V.len):
            R = Vector([], "Result")
            R.makezero(self.len[0])
            for i in range(0, self.len[0]):
                for j in range(0, V.len):
                    R.vector[i] += round(self.matrix[i][j] * V.vector[j], accuracy)
            return R
        else:
            print("Matrixmv: error j != m")
            return 0

    def matrixsubtract(self, B, accuracy):
        if (self.len[0] == B.len[0] and self.len[1] == B.len[1]):
            R = self.copy()
            R.rename("Result")
            for i in range(0, self.len[0]):
                for j in range(0, B.len[1]):
                    #R.matrix[i][j] -= B.matrix[i][j]
                    R.matrix[i][j] = round(R.matrix[i][j] - B.matrix[i][j], accuracy)
                    #round(R.matrix[i][j], accuracy)
            return R
        else:
            print("Matrix subtract: error j != m")
            return 0

    def getcol(self,j):
        r = Vector([],"Column #" + str(j + 1) + "of " + self.name)
        for i in range(self.len[0]):
            r.appendel(self.getel(i, j))
        return r

    def getminor2(self, i, j, vh_r):
        minor = 0
        if vh_r != None:
            c = [i, j, i + 1 + vh_r[0], j + 1 + vh_r[1], i, j + 1 + vh_r[1], i + 1 + vh_r[0], j]
        else:
            c = [i, j, i + 1, j + 1, i, j + 1, i + 1, j]
        minor = self.getel(c[0], c[0]) * self.getel(c[1], c[1]) - (self.getel(c[0], c[1]) * self.getel(c[1], c[0]))
        return minor

class Vector:
    def __init__(self, vector, name):
        self.name = name
        self.setvector(vector)
        self.len = len(self.vector)

    def rename(self, name):
        self.name = name

    def setvector(self, vector):
        self.vector = []
        for item in range(0, len(vector)):
            self.vector.append(vector[item])
        self.len = len(self.vector)

    def makezero(self,size):
        self.vector = []
        for i in range(0,size):
            self.vector.append(0)
        self.len = len(self.vector)

    def makeivector(self,size):
        self.vector = []
        for i in range(0, size):
            self.vector.append(1)
        self.len = len(self.vector)

    def copy(self):
        return Vector(self.vector, self.name + " copy")

    def reverse(self):
        self.vector = self.vector[::-1]

    def getel(self, i):
        if (i >= 0):
            if (i < self.len):
                return self.vector[i]
            else:
                print("get el: List assignment index out of range!")
        elif (i < 0):
            if (i >= -self.len):
                return self.vector[i]
            else:
                print("get el: List assignment index out of range!")
        else:
            print("get el: List assignment index out of range! (sign)")

    def chel(self, i, item):
        if (i >= 0):
            if (i < self.len):
                self.vector[i] = item
            else:
                print("change el: List assignment index out of range!")
        elif (i < 0):
            if (i >= -self.len):
                self.vector[i] = item
            else:
                print("change el: List assignment index out of range!")
        else:
            print("change el: List assignment index out of range! (sign)")

    def appendel(self, item):
        self.vector.append(item)
        self.len = len(self.vector)

    def showvector(self):
        print('')
        # sh = self.copy()
        vector = self.vector
        print(self.name)
        # for row in self.matrix:
        # print(row)
        #s = [[str(e) for e in row] for row in vector]
        s = [str(row) for row in vector]
        print('\n'.join(s))
        print('')

    def rowsubtract(self, B, accuracy):
        if (self.len == B.len):
            R = self.copy()
            R.rename("Result")
            for i in range(0, B.len):
                #R.vector[i] -= B.vector[i]
                R.vector[i] = round(R.vector[i] - B.vector[i], accuracy)
                #round(R.vector[i], accuracy)
            return R
        else:
            print("Row subtract: error i != n")
            return False

    def rowsummarize(self, B, accuracy):
        if (self.len == B.len):
            R = self.copy()
            R.rename("Result")
            for i in range(0, B.len):
                #R.vector[i] += B.vector[i]
                R.vector[i] = round(R.vector[i] + B.vector[i], accuracy)
                #round(R.vector[i], accuracy)
            return R
        else:
            print("Row subtract: error i != n")
            return False

    def compare(self, B, accuracy):
        c = True
        if (self.len == B.len):
            for i in range(0, self.len):
                if (math.fabs(round(self.vector[i], accuracy) - round(B.vector[i], accuracy)) >= round(1 / (10**accuracy), accuracy)):
                    c = False
                    break
            return c
        else:
            print("Row subtract: error i != n")
            return False

    def mnumber(self, num, accuracy):
        for i in range(0, self.len):
            self.vector[i] = round(self.vector[i] * num, accuracy)

    # horizontal vector by vertical vector
    def hvm(self, v, accuracy):
        i = 0
        summ = 0
        while i < self.len:
            summ += round(self.vector[i] * v.vector[i], accuracy)
        return summ

    def dnumber(self, num, accuracy):
        for i in range(0, self.len):
            self.vector[i] = round(self.vector[i] / num, accuracy)

    def tomatrix(self, accuracy):
        m = Matrix([], self.name)
        for i in range(0, self.len):
            m.matrix.append([round(self.vector[i], accuracy)])
        m.len[0] = len(m.matrix)
        m.len[1] = 1
        return m