# The Matrix

*Submission to website*: November 21, 10pm

*Checkoff by LA/TA*: December 1, 10pm

This lab assumes you have Python 2.7 installed on your machine.
Please use the Chrome web browser.

**Note:** Please do **not** use an external library such as numpy.
The intent of the lab is for you to write the code yourself, not just
import a solution!

## Introduction

Trinity is really tired of doing her 18.06 homework: "I hate crunching
numbers!  Isn't that what computers are for?"  She has asked you to
create a Python module for 2-dimensional numeric matrices, which not
only includes support for the basic matrix data structure, but also
will let her solve systems of linear equations and compute the
inverse and determinant.

## The `Matrix` class

Please implement a "new-style" Python class called Matrix, which
supports the following methods.  Use the specified tests to verify
each method as you write it!  Note that implementing the `solve`,
`inverse` and `det` methods will take a bit work, but the other
methods should be straightforward.

**\_\_init\_\_**( *self, nrows, ncols* )
<span style="margin-left: 5em;"># tests 1-3</span>
<div style="margin-left:2em">
Initialize self to be a 2D *nrows-by-ncols* matrix where each element
is initialized to 0.  *nrows* and *ncols* should be saved as instance
variables, and it's recommended to use an instance variable of type
`list` to serve as storage for the matrix contents.

Raise `TypeError` if *nrows* or *ncols* are not integers.  Raise
`ValueError` if *nrows* or *ncols* are not greater than zero.

    >>> a = Matrix(2,-2)
    ValueError: matrix number of rows and columns must be positive
    >>> a = Matrix(2,'blue pill')
    TypeError: matrix number of rows and columns must be ints
</div>

**\_\_getitem\_\_**( *self, key* )
<span style="margin-left: 5em;"># tests 4-7</span>
<div style="margin-left:2em">
If *key* is a tuple with 2 integer values `(i,j)`, return the value of
the matrix element in row `i` and column `j`.  This will allow us to
use the standard notation `A[i,j]` to access matrix elements since
Python converts `A[i,j]` into `A.__getitem__((i,j))`.

Note that indices are 0-based, just like other indices in Python.

Raise `TypeError` if *key* is not a 2-element tuple or if the tuple
elements are not integers.  Raise `IndexError` if `i` is not in the
range `0` to `nrows-1` or if `j` is not in the range `0` to `ncols-1`.

    >>> a = Matrix(2,2)
    >>> a[0,0]
    0
    >>> a['keanu','reeves']
    TypeError: matrix indices must be integers
    >>> a[42]
    TypeError: matrix indices should be two values
    >>> a[0,3]
    IndexError: matrix index out of range
</div>

**\_\_setitem\_\_**( *self, key, v* )
<span style="margin-left: 5em;"># tests 8-10</span>
<div style="margin-left:2em">
If *key* is a tuple with 2 integer values `(i,j)`, set the value of
the matrix element in row `i` and column `j` to the value `v`.  Python
converts `A[i,j]=v` into `A.__setitem__((i,j),v)`.

Raise `TypeError` if *key* is not a 2-element tuple, if the tuple
elements are not integers, or if *v* is not numeric.  Note that you
can test if *v* is a number by using `isinstance(v,numbers.Number)`.
Raise `IndexError` if `i` is not in the range 0 to nrows-1 or if `j`
is not in the range 0 to ncols-1.

    >>> a = Matrix(2,2)
    >>> a[0,1] = 3
    >>> a[0,0], a[0,1], a[1,0], a[1,1]
    (0, 3, 0, 0)
    >>> a[0,3] = 42
    IndexError: matrix index out of range
    >>> a[0,0] = 'Morpheus'
    TypeError: matrix value must be numeric
</div>

**\_\_iter\_\_**( *self* )
<span style="margin-left: 5em;"># test 11</span>
<div style="margin-left:2em">
Return an iterator that visits each element of the matrix in the
following order: `[0,0]`, `[0,1]`, ..., `[0,ncols-1]`, `[1,0]`, ...,
`[nrows-1,ncols-1]`.  This allows a Matrix to behave like a sequence,
so, for example, `list(A)` will return the contents of matrix `A` as a
list.

Hint: see the bottom of Slide 11 in Handout #13.

    >>> a = Matrix(2,2)
    >>> a[0,0], a[1,0], a[0,1], a[1,1] = 1, 2, 3, 4
    >>> list(a)
    [1, 3, 2, 4]
</div>

**fill**( *self, v* )
<span style="margin-left: 5em;"># tests 12-16</span>
<div style="margin-left:2em">
If *v* is `None`, simply return.

If *v* is a number, set each matrix element to the specified value.

If *v* is a list of length `nrows*ncols`, use the numbers from the
list to set the values of matrix elements in the in the following
order: `[0,0]`, `[0,1]`, ..., `[0,ncols-1]`, `[1,0]`, ...,
`[nrows-1,ncols-1]`.

You should now modify the **\_\_init\_\_** method to have an optional
third argument `fill` with a default value of `None`.
**\_\_init\_\_** should call `self.fill()` with the specified fill
value.

Raise `TypeError` if *v* is not a number or a list of numbers.  Raise
`ValueError` if *v* is a list but doesn't have `nrows*ncols` elements.

    >>> a = Matrix(2,2)
    >>> a.fill(5)
    >>> list(a)
    [5, 5, 5, 5]
    >>> a.fill([5,6,7,8])
    >>> list(a)
    [5, 6, 7, 8]
    >>> a.fill('Agent Smith')
    TypeError: matrix fill value not number or list
    >>> a.fill([-1,-2,-3])
    ValueError: matrix fill value has incorrect number of elements
    >>> b = Matrix(2,1,[3.14, 2.78])
    >>> list(b)
    [3.14, 2.78]
</div>

**\_\_repr\_\_**( *self* )
<span style="margin-left: 5em;"># test 17</span>
<div style="margin-left:2em">
Return a string that can be used to reconstruct the Matrix from
scratch.  This string is what's printed when the Python interpreter
needs to print a Matrix value.

    >>> a = Matrix(2,2,[1,2,3,4])
    >>> a
    Matrix(2,2,[1, 2, 3, 4])
</div>

**I**( *n* )
<span style="margin-left: 5em;"># test 18</span>
<div style="margin-left:2em">
This is a static class method that should return a newly created
*n*-by-*n* identity matrix, i.e., a matrix whose diagonal elements are
1 and all other elements are 0.

    >>> Matrix.I(3)
    Matrix(3,3,[1, 0, 0, 0, 1, 0, 0, 0, 1])
</div>

**shape**
<span style="margin-left: 5em;"># test 19</span>
<div style="margin-left:2em">
This should be a property of the Matrix class -- see slides 5 and 6 of
Lecture 8.  Returns a 2-element tuple with the values of `nrows` and
`ncols`.

    >>> Matrix(23,4).shape
    (23, 4)
</div>

**copy**( *self* )
<span style="margin-left: 5em;"># test 20</span>
<div style="margin-left:2em">
Return a newly created matrix that has the same shape and contents.

    >>> a = Matrix(2,2,[1,2,3,4])
    >>> b = a.copy()
    >>> b[1,0] = 17
    >>> a
    Matrix(2,2,[1, 2, 3, 4])
    >>> b
    Matrix(2,2,[1, 2, 17, 4])
</div>

##Operations on matrices

**\_\_mul\_\_**( *self, other* )
<span style="margin-left: 5em;"># tests 21-24</span>
<div style="margin-left:2em">
Return a newly created matrix that's the result of the matrix
multiplication of *self* with the matrix *other*.  Multiplying an
*n-by-m* matrix by a *m-by-p* matrix results in a *n-by-p* matrix.

Raise `TypeError` if *other* is not a Matrix.  Raise `ValueError` if
the number of rows in *other* is not equal to the number of columns in
*self*.

    >>> a = Matrix(3,2,[1,2,3,4,5,6])
    >>> a*Matrix.I(2)
    Matrix(3,2,[1, 2, 3, 4, 5, 6])
    >>> b = Matrix(2,1,[7,8])
    >>> a*b
    Matrix(3,1,[23, 53, 83])
    >>> b*a
    ValueError: matrix dot argument has incorrect number of rows
</div>

**transpose**( *self* )
<span style="margin-left: 5em;"># tests 25-26</span>
<div style="margin-left:2em">
Return a newly created matrix that's the tranpose of *s*.  If *self*
is an *n-by-m* matrix, its tranpose is an *m-by-n* matrix.  Element
`[i,j]` in the transpose is equal to element `[j,i]` of *self*.

    >>> a = Matrix(3,2,[1,2,3,4,5,6])
    >>> a.transpose()
    Matrix(2,3,[1, 3, 5, 2, 4, 6])
</div>

**solve**( *self, b* )
<span style="margin-left: 5em;"># tests 27-30</span>
<div style="margin-left:2em">
Return a newly created matrix *x* that satisfies *self* * *x* =
*b*.  When *self* is an *n-by-n* square matrix and *b* is an *n-by-1*
column vector, the `solve` method can be used to solve a system of
linear equations in *n* variables.

Here are the steps needed when *self* is *n-by-n* and *b* is *n-by-m*:

  1. Create a temporary *n-by-(n+m)* augmented matrix `A = [ self | b
  ]`.  The contents of columns 0 through *n-1* of `A` are the contents
  of matrix *self*, and the contents of columns *n* through *n+m-1*
  are the contents of matrix *b*.

  2. Use Gaussian elimination with row pivoting to convert A to [ row
  echelon form](https://en.wikipedia.org/wiki/Row_echelon_form).  See
  [Gaussian Elimination
  Pseudocode](https://en.wikipedia.org/wiki/Gaussian_elimination#Pseudocode).
  This step may discover that `A` is singular, in which case a
  `ValueError` should be raised.  Don't forget that division
  operations should be using floating-point division!

  3. Use backward substitution to convert the result of step 2 to [
  reduced row echelon
  form](https://en.wikipedia.org/wiki/Row_echelon_form).  See the
  "Example of the algorithm" section of [Gaussian
  Elimination](https://en.wikipedia.org/wiki/Gaussian_elimination).

  4. *x* can be found in columns *n* through *n+m-1* of the result of step 3.

Raise `TypeError` if *b* is not a Matrix.  Raise `ValueError` if
*self* is not a square matrix or if the number of rows in *b* is not
equal to the number of columns in *self*.  Raise `ValueError` if
*self* is singular.

    >>> a = Matrix(3,3,[1,1,1,4,3,-1,3,5,3])
    >>> b = Matrix(3,1,[1,6,4])
    >>> x = a.solve(b)
    >>> x
    Matrix(3,1,[1.0, 0.5, -0.5])
    >>> a*x    # result should be equal to b
    Matrix(3,1,[1.0, 6.0, 4.0])
    >>> c = Matrix(3,3,[1,1,1,2,2,2,3,3,3])
    >>> c.solve(b)
    ValueError: matrix is singular
</div>

**inverse**( *self* )
<span style="margin-left: 5em;"># tests 31-32</span>
<div style="margin-left:2em">
Return a newly created matrix that's the inverse of *self*. If *self*
is an *n-by-n* matrix, its inverse is easily computed as
`self.solve(Matrix.I(n))`.  See the "Computing the inverse of a
matrix" section of
[Gaussian elimination applications](https://en.wikipedia.org/wiki/Gaussian_elimination#Applications).

    >>> a = Matrix(3,3,[2,-1,0,-1,2,-1,0,-1,2])
    >>> ainv = a.inverse()
    >>> ainv
    Matrix(3,3,[0.75, 0.5, 0.24999999999999997,
    0.5, 1.0, 0.49999999999999994,
    0.24999999999999997, 0.49999999999999994, 0.7499999999999999])
    >>> # The small differences from the expected answer
    >>> # [0.75, 0.5, 0.25, 0.5, 1.0, 0.5, 0.25, 0.5, 0.75]
    >>> # are due to the vagaries of floating-point arithmetic!
    >>> a * ainv   # result should be the identity matrix
    Matrix(3,3,[1.0, 0.0, 0.0,
    2.7755575615628914e-17, 1.0, 0.0,
    -5.551115123125783e-17, -1.1102230246251565e-16, 0.9999999999999998])
    >>> # again floating-point issues makes the answer slightly
    >>> # different from I(3)
</div>

**det**( *self* )
<span style="margin-left: 5em;"># test 33</span>
<div style="margin-left:2em">
Return the determinant of the square matrix *self*.

See the "Computing determinants" section of [Gaussian elimination
applications](https://en.wikipedia.org/wiki/Gaussian_elimination#Applications).
Basically you want to copy steps 1 and 2 from `solve`, keeping track
of `nswaps`, the number of row swaps performed while pivoting.  The
determinant will be the product of (-1)<sup>nswaps</sup> and the *n*
diagonal elements from columns 0 through *n-1* of the augmented matrix
in row echelon form.

    >>> d = Matrix(3,3,[-2,2,-3,-1,1,3,2,0,-1])
    >>> d.det()
    18.0
    >>> d.transpose().det()   # result should be same as d.det()
    18.0
    >>> d.inverse().det()     # result should be 1/d.det()
    0.055555555555555566
</div>
