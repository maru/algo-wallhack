from collections import defaultdict, Counter
import sys

DEBUG = True

def log(*arg):
  """
  Logging function for debugging.
  """
  if not DEBUG:
    return

  for i in range(len(arg)):
    print arg[i],
  print

"""
Graph class
"""
class Graph(object):
  def __init__(self):
    self.edges = defaultdict(list)
    self.vertices = set()

  def __str__(self):
    return self.vertices.__str__() + "\n" + self.edges.__str__()

  def add_vertex(self, v):
    """
    Add vertex to graph.
    """
    self.vertices.add(v)

  def add_edge(self, s, t, length):
    """
    Add edge to graph.
    """
    self.edges[s].append((t, length))

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

class ShortestPath(object):
  def __init__(self, graph):
    self.graph = graph
    self.max_distance = 1000000
    self.get_shortest_path = self.dijkstra

  def get_shortest_paths(self, src, to_list):
    d = []
    for dst in to_list:
      d.append(self.get_shortest_path(src, dst))
    return d

  def dijkstra(self, src, dst):
    d_cost = { src: 0, dst: self.max_distance }
    vertices = set()
    vertices.add(src)
    while dst not in vertices:
      min_cost = self.max_distance
      min_w = 0
      for v in vertices:
        for w, length in self.graph.get_edges(v):
          if w in vertices:
            continue
          c = d_cost[v] + length
          if min_cost > c:
            min_cost = c
            min_w = w
      if min_w == 0:
        print "NOT FOUND %d -> %d" % (src, dst)
        break
      vertices.add(min_w)
      d_cost[min_w] = min_cost

    return d_cost[dst]


def load_graph(filename):
  """
  Read from file and load graph.
  """
  graph = Graph()
  with open(filename) as f:
    for l in f:
      values = l.split()
      v = int(values[0])
      graph.add_vertex(v)
      for val in values[1:]:
        w, l = val.split(",")
        w, l = int(w, 10), int(l, 10)
        graph.add_vertex(w)
        graph.add_edge(v, w, l)
  graph.sort_edges()
  return graph

def print_fmt(sol):
  """
  Print solution using required format.
  """
  s = str(sol[0])
  for i in sol[1:]:
    s += ",%d" % (i)
  print s

if __name__ == "__main__":

  filename = "dijkstraData.txt"
  if len(sys.argv) > 1:
    filename = sys.argv[1]

  graph = load_graph(filename)
  sp = ShortestPath(graph)
  sp.get_shortest_path = sp.dijkstra
  sol = sp.get_shortest_paths(1, [7,37,59,82,99,115,133,165,188,197])
  print_fmt(sol)
