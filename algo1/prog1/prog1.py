# Copyright (c) 2014 https://github.com/maru/

def Merge(A, size1, size2, begin, end):
    B = A[begin : begin+size1]
    C = A[begin+size1 :end]

    num_inv = 0
    j = 0
    k = 0
    for i in xrange(begin, end):
        if j < size1 and (k >= size2 or B[j] <= C[k]):
            A[i] = B[j]
            j += 1
        else:
            A[i] = C[k]
            k += 1
            if j < size1:
                num_inv += size1 - j
    return num_inv

def CountInversions(A, size, begin, end):
    if size == 1:
        return 0

    num_inv = 0
    size1 = size/2
    size2 = size - size1

    num_inv += CountInversions(A, size1, begin, begin+size1)
    num_inv += CountInversions(A, size2, begin+size1, end)
    num_inv += Merge(A, size1, size2, begin, end)
    return num_inv

if __name__ == '__main__':

    # Programming Question 1
    A = []
    with open('IntegerArray.txt') as f:
        for l in f:
            A.append(int(l))
    size = len(A)
    print CountInversions(A, size, 0, size)

    print "TEST CASE - 1",
    A = [1,3,5,2,4,6]
    size = len(A)
    print (CountInversions(A, size, 0, size) == 3)

    print "TEST CASE - 2",
    A = [1,5,3,2,4]
    size = len(A)
    print (CountInversions(A, size, 0, size) == 4)

    print "TEST CASE - 3",
    A = [5,4,3,2,1]
    size = len(A)
    print (CountInversions(A, size, 0, size) == 10)

    print "TEST CASE - 4",
    A = [1,6,3,2,4,5]
    size = len(A)
    print (CountInversions(A, size, 0, size) == 5)

    print "Test Case - #1 - 15 numbers",
    A = [ 9, 12, 3, 1, 6, 8, 2, 5, 14, 13, 11, 7, 10, 4, 0 ]
    size = len(A)
    print (CountInversions(A, size, 0, size) == 56)

    print "Test Case - #2 - 50 numbers",
    A = [ 37, 7, 2, 14, 35, 47, 10, 24, 44, 17, 34, 11, 16, 48, 1, 39, 6, 33, 43, 26, 40, 4, 28, 5, 38, 41, 42, 12, 13, 21, 29, 18, 3, 19, 0  , 32, 46, 27, 31, 25, 15, 36, 20, 8, 9, 49, 22, 23, 30, 45 ]
    size = len(A)
    print (CountInversions(A, size, 0, size) == 590)

    print "Test Case - #3 - 100 numbers",
    A = [ 4, 80, 70, 23, 9, 60, 68, 27, 66, 78, 12, 40, 52, 53, 44, 8, 49, 28, 18, 46, 21, 39, 51, 7, 87, 99, 69, 62, 84, 6, 79, 67, 14, 98, 83, 0, 96, 5, 82, 10, 26, 48, 3, 2, 15, 92, 11, 55, 63, 97, 43, 45, 81, 42, 95, 20, 25, 74, 24, 72, 91, 35, 86, 19, 75, 58, 71, 47, 76, 59, 64, 93, 17, 50, 56, 94, 90, 89, 32, 37, 34, 65, 1, 73, 41, 36, 57, 77, 30, 22, 13, 29, 38, 16, 88, 61, 31, 85, 33, 54 ]
    size = len(A)
    print (CountInversions(A, size, 0, size) == 2372)
