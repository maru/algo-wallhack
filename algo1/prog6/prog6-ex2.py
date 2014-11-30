import heapq

class Heap(object):
  def __init__(self):
    self.h = []

  def push(self, item):
    heapq.heappush(self.h, item)

  def pop(self):
    item = heapq.heappop(self.h)
    return item

  def len(self):
    return len(self.h)

  def min(self):
    return self.h[0]

class HeapMin(Heap):
  pass


class HeapMax(Heap):
  def push(self, item):
    item = -item
    super(HeapMax, self).push(item)

  def pop(self):
    item = super(HeapMax, self).pop()
    return -item

  def max(self):
    return -super(HeapMax, self).min()


class MedianMaint(object):
  def __init__(self):
    self.hmax = HeapMax()
    self.hmin = HeapMin()
    self.min_item = -1
    self.max_item = -1
    self.min_len = 0
    self.max_len = 0

  def insert(self, item):
    if self.hmin.len() > 0 and item > self.hmin.min():
      self.hmin.push(item)
    else:
      self.hmax.push(item)
    if self.hmax.len() > self.hmin.len() + 1:
      item = self.hmax.pop()
      self.hmin.push(item)
    elif self.hmax.len() < self.hmin.len():
      item = self.hmin.pop()
      self.hmax.push(item)

  def get_median(self):
    return self.hmax.max()



def median_maintenance(filename):
  """Second exercise"""
  MOD = 10000
  median_sum = 0
  mm = MedianMaint()

  # Read file
  with open(filename) as f:
    for l in f:
      x = int(l.strip())
      mm.insert(x)
      median_sum += mm.get_median()

  print "2sum_range", filename, median_sum % MOD


if __name__ == "__main__":

  median_maintenance("test2-54.in")
  median_maintenance("test2-55.in")
  median_maintenance("test2-23.in")
  median_maintenance("test2-148.in")
  median_maintenance("Median.txt")
