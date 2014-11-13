# Copyright (c) 2014 https://github.com/maru/

import random

def test_ChoosePivotFirst(A, size, ChoosePivot):
    for t in xrange(1000):
        begin = int(random.random()*100000) % size
        end = 0
        while end < begin:
            end = int(random.random()*100000) % size
        res = ChoosePivot(A, begin, end)
        if begin != res:
            print "ERROR ", ChoosePivot, begin, end, "%d != %d" % (begin, res)


def test_ChoosePivotLast(A, size, ChoosePivot):
    for t in xrange(1000):
        begin = int(random.random()*100000) % size
        end = 0
        while end < begin:
            end = int(random.random()*100000) % size
        res = ChoosePivot(A, begin, end)
        if end - 1 != res:
            print "ERROR ", ChoosePivot, begin, end, "%d != %d" % (end - 1, res)

def test_ChoosePivotMedianOf3(A, size, ChoosePivot):
    for t in xrange(1000):
        begin = int(random.random()*100000) % size
        end = 0
        while end < begin:
            end = int(random.random()*100000) % size

        num_elem = end - begin
        middle = begin + num_elem/2 - 1
        if num_elem % 2 == 1:
          middle = begin + num_elem/2
        median = middle
        if (A[middle] < A[begin] and A[begin] < A[end-1]) or \
           (A[end-1]  < A[begin] and A[begin] < A[middle]):
            median = begin
        if (A[middle] < A[end-1] and A[end-1] < A[begin]) or \
           (A[begin]  < A[end-1] and A[end-1] < A[middle]):
            median = end-1

        res = ChoosePivot(A, begin, end)
        if median != res:
            print "ERROR ", ChoosePivot, begin, end, "%d != %d" % (median, res)


def ChoosePivotFirst(A, begin, end):
    return begin

def ChoosePivotLast(A, begin, end):
    return end - 1

def ChoosePivotMedianOf3(A, begin, end):
    index1 = ChoosePivotFirst(A, begin, end)
    index2 = ChoosePivotLast(A, begin, end)
    index3 = begin + (end - begin - 1)/2

    if (A[index2] < A[index1] and A[index1] < A[index3]) or \
       (A[index3] < A[index1] and A[index1] < A[index2]):
        return index1
    if (A[index1] < A[index2] and A[index2] < A[index3]) or \
       (A[index3] < A[index2] and A[index2] < A[index1]):
        return index2
    return index3

def QuickSort(A, ChoosePivot, begin, end):
    # Base case
    if end - begin <= 1:
        return 0

    # Get pivot, put it in first place of the current array A
    p = ChoosePivot(A, begin, end)
    pivot = A[p]
    A[p] = A[begin]
    A[begin] = pivot

    num_comparisons = end - begin - 1
    # Points to left-most element greater than the pivot
    j = begin + 1
    for i in xrange(begin + 1, end):
        if A[i] < pivot:
            if i != j:
              tmp = A[j]
              A[j] = A[i]
              A[i] = tmp
            j += 1

    # Move pivot to correct position
    if j - 1 > begin:
      A[begin] = A[j-1]
      A[j-1] = pivot

    # Do quicksort in both subarrays
    num_comparisons += QuickSort(A, ChoosePivot, begin, j-1)
    num_comparisons += QuickSort(A, ChoosePivot, j, end)
    return num_comparisons

if __name__ == "__main__":
    A = []
    with open('QuickSort.txt') as f:
        for l in f:
            A.append(int(l))

    # A = A[:1000]
    size = len(A)

    B = A[:]
    print QuickSort(B, ChoosePivotFirst, 0, size), 162085
    for i in xrange(1, size):
      if B[i-1] > B[i]:
          print 'ERROR 1'

    B = A[:]
    print QuickSort(B, ChoosePivotLast, 0, size), 164123
    for i in xrange(1, size):
      if B[i-1] > B[i]:
          print 'ERROR 2'

    B = A[:]
    print QuickSort(B, ChoosePivotMedianOf3, 0, size), '!= ', 142616
    for i in xrange(1, size):
      if B[i-1] > B[i]:
          print 'ERROR 3'

    test_ChoosePivotFirst(A, size, ChoosePivotFirst)
    test_ChoosePivotLast(A, size, ChoosePivotLast)
    test_ChoosePivotMedianOf3(A, size, ChoosePivotMedianOf3)
