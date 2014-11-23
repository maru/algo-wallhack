from collections import defaultdict, Counter
import sys

DEBUG = False

def log(*arg):
  """
  Logging function for debugging.
  """
  if not DEBUG:
    return

  # print "DEBUG:",
  for i in range(len(arg)):
    print arg[i],
  print

class Stack(object):
  def __init__(self):
    self.s = []
    self.size = 0

  def __str__(self):
    return self.s.__str__()

  def push(self, e):
    self.s.append(e)
    self.size += 1

  def pop(self):
    if self.empty():
      return None
    self.size -= 1
    return self.s.pop()

  def top(self):
    if self.empty():
      return None
    return self.s[self.size-1]

  def empty(self):
    return self.size == 0

"""
Graph class
"""
class Graph(object):
  def __init__(self):
    self.edges = defaultdict(list)
    self.vertices = set()

  def add_vertex(self, v):
    """
    Add vertex to graph.
    """
    self.vertices.add(v)

  def add_edge(self, s, t):
    """
    Add edge to graph.
    """
    self.edges[s].append(t)

  def get_edges(self, v):
    """
    Get edges coming from vertex v.
    """
    return self.edges[v]

  def sort_edges(self):
    """
    Sort neighbor vertices in edges.
    """
    for v in self.vertices:
      self.edges[v].sort()

  def get_reverse(self):
    """
    Get graph with all arcs reversed.
    """
    graph = Graph()
    for v in self.vertices:
      graph.add_vertex(v)
      for w in self.edges[v]:
        graph.add_vertex(w)
        graph.add_edge(w, v)
    return graph

"""
Strongly Connected Components class
"""
class SCC(object):

  def __init__(self):
    self.init()

  def init(self):
    """
    Initialize common structures.
    """
    self.curr_time = 0
    self.curr_leader = 0
    self.leader = {}
    self.explored = {}
    self.fin_time = []

  def DFS_loop(self, graph, vertices):
    """
    DFS start function.
    """
    log("vertices", vertices)
    num_v = len(vertices)
    self.init()

    for v in vertices:
      if v in self.explored and self.explored[v]:
        continue
      log("+ DFS_loop", v)
      self.curr_leader = v
      self.DFS(graph, v)
      log("  explored", self.explored)
      log("  leader", self.leader)
      log("  fin_time", self.fin_time)


  def DFS_it(self, graph, v):
    """
    DFS recursive function.
    Uses a stack to avoid maximum recursion depth exceeded.
    """
    stack = Stack()
    stack.push(v)
    finished = Stack()
    while not stack.empty():
      v = stack.top()
      if not v in self.explored or not self.explored[v]:
        log(" - DFS", v) #, stack)
        self.explored[v] = True
        self.leader[v] = self.curr_leader
        edges = graph.get_edges(v)[:]
        log("   edges:", edges)
        edges.reverse()
        for w in edges:
          if w in self.explored and self.explored[w]:
            continue
          stack.push(w)
        finished.push(v)
      else:
        if v == finished.top():
          self.fin_time.append(finished.pop())
        stack.pop()

  def DFS_rec(self, graph, v):
    """
    DFS recursive function.
    """
    log(" - DFS", v)
    self.explored[v] = True
    self.leader[v] = self.curr_leader
    edges = graph.get_edges(v)
    log("   edges:", edges)
    for w in edges:
      if w in self.explored and self.explored[w]:
        continue
      self.DFS(graph, w)
    self.fin_time.append(v)

  def SCC(self, graph):
    """
    Main function to obtain the strongly connected components of a graph.
    """
    g_rev = graph.get_reverse()
    log("graph.edges", graph.edges.items())
    log("g_rev.edges", g_rev.edges.items())

    log("")
    # Computer magical ordering of nodes
    vertices = list(g_rev.vertices)
    vertices.reverse()
    self.DFS_loop(g_rev, vertices)

    log("")
    # Discover the SCCs one by one
    vertices = self.fin_time
    vertices.reverse()
    self.DFS_loop(graph, vertices)

    # Get SCCs
    self.get_SCCs()

  def get_SCCs(self):
    """
    """
    self.scc_counter = Counter()
    for _, v in self.leader.items():
      self.scc_counter[v] += 1

  def most_common(self):
    """
    Gets the size of the biggest strongly connected components, in decreasing order.
    """
    return self.scc_counter.most_common()


def sol_format(values, n):
    """
    Formats the size of the n biggest SCCs using the format "A,B,C".
    If the number of values is less than n, then the value 0 is used.
    """
    res = [0]*n
    # Get first n values
    for i in range(min(len(values), n)):
      res[i] = values[i][1]

    # Format to string
    s = str(res[0])
    for i in range(1, n):
      s = s  + ",%d" % (res[i])
    return s

if __name__ == "__main__":

  filename = "SCC.txt"
  if len(sys.argv) > 1:
    filename = sys.argv[1]

  graph = Graph()
  with open(filename) as f:
    for l in f:
      v, w = l.split()
      v, w = int(v, 10), int(w, 10)
      graph.add_vertex(v)
      graph.add_vertex(w)
      graph.add_edge(v, w)

  graph.sort_edges()
  scc = SCC()
  # use iterative DFS
  scc.DFS = scc.DFS_it
  # calculate SCCs
  scc.SCC(graph)
  print sol_format(scc.most_common(), 5)
