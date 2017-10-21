## Lab 9: The Matrix
## Name: Michael Ortega
## Hours Spent: 8

# to test for a number use isinstance(x,numbers.Number)
import numbers

# a 2D numeric matrix
class Matrix(object):
    def __init__(self,nrows,ncols,fill=None):
        """ build nrows-by-ncols matrix, initial contents 0"""

        if not(isinstance(nrows, int) and isinstance(ncols, int)):
            raise TypeError
        if nrows <= 0 or ncols <= 0:
            raise ValueError

        self.rows = nrows
        self.cols = ncols
        self.mat = [[0 for c in xrange(ncols)] for r in xrange(nrows)]
        self.fill_value = fill

        self.fill(fill)

            



        

    def __getitem__(self,key):
        """ support A[r,c] """

        if not (isinstance(key,tuple) and len(key) == 2 and
            isinstance(key[0],int) and isinstance(key[1],int)): 
            
            raise TypeError

        if not ( 0<= key[0] < self.rows and 0 <= key[1] < self.cols ):
            raise IndexError

        return self.mat[key[0]][key[1]]

    def __setitem__(self,key,v):
        """ support A[r,c] = v """
        if not (isinstance(key,tuple) and len(key) == 2 and
            isinstance(key[0],int) and isinstance(key[1],int) and isinstance(v,numbers.Number)): 
            
            raise TypeError

        if not ( 0<= key[0] < self.rows and 0 <= key[1] < self.cols ):
            raise IndexError

        self.mat[key[0]][key[1]] = v


    def __iter__(self):
        """ iterate over contents: makes list(matrix) work! """
        return iter([element for row in self.mat for element in row])

    def get_row(self, row_index):
        return self.mat[row_index]

    def fill(self,value):
        """ fill matrix from a number or list of numbers """
        if value:

            if isinstance(value, numbers.Number):
                for row in xrange(self.rows):
                    for col in xrange(self.cols):
                        self.mat[row][col] = value
            elif isinstance(value,list):
                if len(value) == self.rows*self.cols:
                    for row in xrange(self.rows):
                        for col in xrange(self.cols):
                            self.mat[row][col] = value[col + row*self.cols]
                else:
                    raise ValueError
            else:
                raise TypeError


        return

    def width(self):
        return self.cols
    def height(self):
        return self.rows

    def __repr__(self):
        """ return string representation """
        return 'Matrix({},{},{})'.format(self.rows, self.cols, self.fill_value)
    def __str__(self):
        result = ""
        for row in self.mat:
            for elem in row:
                result += " \t"+ str(elem)
            result += "\n"
        return result

    @staticmethod
    def I(n):
        """ static method to construct nxn identity matrix """
        return Matrix(n, n, [1 if row==col else 0 for col in xrange(n) for row in xrange(n) ])

    def _shape(self):
        """ return dimensions of matrix as (nrows,ncols) """
        return (self.rows, self.cols)
    shape = property(_shape)

    def copy(self):
        """ return new matrix which is a copy of self """
        return Matrix(self.rows,self.cols, list(self))

    def __mul__(self,m):
        """ returns new matrix which is the matrix product of self and m """
        if isinstance(m, Matrix):
            if self.cols == m.height():
                
                result = [0 for c in xrange(m.width()*self.rows) ]

                # iterate through rows of self
                for r in xrange(self.rows):
                    # iterate through columns of other
                    for c in xrange(m.width()):

                        # iterate through rows of other  
                        for k in xrange(m.height()):
                            result[c+r*m.width()] += self.mat[r][k] * m[k,c]


                return Matrix(self.rows, m.width(), result)
            else:
                raise ValueError
        else:
            raise TypeError

    def transpose(self):
        """ return new matrix which is the transpose of self """
        result = Matrix(self.cols,self.rows)
        
        for i in xrange(result.height()):
            for j in xrange(result.width()):
                result[i,j] = self.mat[j][i]

        
        return Matrix(self.cols,self.rows,list(result))



    def solve(self,b):
        """ return new matrix x such that self*x = b """

        # create augmented matrix containing both self and b
        result = []
        for row_index, row in enumerate(self.mat):
            result.extend(row)
            result.extend(b.get_row(row_index))

        
        A = Matrix(self.rows, self.cols+b.width(), result)

        


        n = A.height()
        m = A.width()


        for i in xrange(n):

            # find largest element in column
            max_pivot = abs(A[i,i])
            max_row = i

            for k in xrange(i+1, n):
                if abs(A[k,i]) > max_pivot:
                    max_pivot = abs(A[k,i])
                    max_row = k

            # check if matrix is singular
            if max_pivot == 0:
                raise ValueError

            # swap max row with current row
            for k in xrange(i,m):
                A[max_row,k], A[i,k] = A[i,k], A[max_row,k]
            
            # make all elements below current pivot zero
            for k in xrange(i+1, n):
                const = -float(A[k,i]) / A[i,i]
                for j in xrange(i,m):
                    A[k,j] += const * A[i,j]


        # solve using back substitution

        for i in xrange(n-1, -1, -1):

            # divide row by pivot
            current_pivot = A[i,i]
            for k in xrange(i, m):
                A[i, k] /= float(current_pivot)

            # make all elements above current pivot zero
            for k in xrange(i-1 , -1, -1):
                const = -float(A[k,i]) / A[i,i]
                for j in xrange(i, m):
                    A[k,j] += const * A[i,j]
        

        # return matrix where values of matrix come from last columns of A
        result = []
        
        for i in xrange(A.height()):
            result.extend(A.get_row(i)[self.width():A.width()])
        

        return Matrix(b.height(), b.width(), result)



    def inverse(self):
        """ return new matrix which is the inverse of self """
        return self.solve( Matrix.I(self.width()) )


        
    def det(self):
        """ compute determinant """
        A = Matrix(self.rows, self.cols, list(self))
        n = self.rows
        nswaps = 0
        for i in xrange(n):

            # find largest element in column
            max_pivot = abs(A[i,i])
            max_row = i

            for k in xrange(i+1, n):
                if abs(A[k,i]) > max_pivot:
                    max_pivot = abs(A[k,i])
                    max_row = k

            # check if any rows were swapped
            if max_row != i:
                nswaps += 1


            # check if matrix is singular
            if max_pivot == 0:
                raise ValueError

            # swap max row with current row
            for k in xrange(i,n):
                A[max_row,k], A[i,k] = A[i,k], A[max_row,k]
            
            # make all elements below current pivot zero
            for k in xrange(i+1, n):
                const = -float(A[k,i]) / A[i,i]
                for j in xrange(i,n):
                    A[k,j] += const * A[i,j]


        # get product of diagonals
        diags = [A[i,i] for i in xrange(n)]
        product = 1
        for elem in diags:
            product *= elem

        return (-1)**nswaps * product









