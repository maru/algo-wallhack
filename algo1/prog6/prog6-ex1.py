def binsearch(A, N, val, ret_lo=True):
  lo = 0
  hi = N - 1
  while lo <= hi:
    mid = lo + (hi - lo)/2
    if A[mid] == val:
      return mid
    if A[mid] < val:
      lo = mid + 1
    else:
      hi = mid - 1
  if ret_lo:
    return lo
  return hi

def twosum_range(filename):
  """First exercise"""
  numbers = []
  count = 0
  min_num = 100000000000
  max_num = -100000000000
  computed = {}
  MIN_T = -10000
  MAX_T =  10000

  # Read file
  with open(filename) as f:
    for l in f:
      i = int(l.strip())
      numbers.append(i)
      min_num = min(min_num, i)
      max_num = max(max_num, i)

  numbers.sort()
  N = len(numbers)
  # print "##", numbers, N
  for i in xrange(N):
    x = numbers[i]
    # Find smallest value of range
    y0 = MIN_T - x
    j0 = binsearch(numbers, N, y0)
    j0 = max(j0, i+1)
    # assert 0 <= j0 and j0 <= N

    # Find largest value of range
    y1 = MAX_T - x
    j1 = binsearch(numbers, N, y1, False)
    j1 = min(j1 + 1, N)
    # assert 0 <= j1 and j1 <= N

    #print x, numbers[j0:j1], j0, j1
    # count t values
    for j in xrange(j0, j1):
      #print j
      # assert MIN_T <= x + numbers[j]
      # assert x + numbers[j] <= MAX_T
      t = x + numbers[j]
      computed[t] = True

  count = len(computed.keys())
  print "2sum_range", count


if __name__ == "__main__":

  twosum_range("test1-3.in")
  twosum_range("test1-5.in")
  twosum_range("test1-6.in")
  twosum_range("algo1-programming_prob-2sum.txt")
