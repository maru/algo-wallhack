import sys
import random

DEBUG = False
def log(*msg):
  if not DEBUG:
    return
  for s in msg:
    print s,
  print

def remove_vertex(vertices, u):
  log("remove vertex %d" % (u))
  assert vertices.count(u) > 0
  vertices.remove(u)

def add_vertex(vertices, u):
  log("append vertex %d" % (u))
  vertices.append(u)

def pick_edge(edges):
  num_edges = len(edges)
  i = random.SystemRandom().randint(0, num_edges-1)
  assert num_edges > i
  return edges[i]

def remove_edge(edges, edge):
  log("remove edge (%d, %d)" % (edge))
  assert edges.count(edge) > 0
  edges.remove(edge)

def remove_neighbor(neighbors, edges, u, v):
  while neighbors[u].count(v) > 0:
    log("remove self loop (%d, %d)" % (u, v))
    neighbors[u].remove(v)

  edge = (min(u, v), max(u, v))
  while edges.count(edge) > 0:
    remove_edge(edges, edge)

def remove_self_loops(neighbors, edges, u, v):
  remove_neighbor(neighbors, edges, u, v)
  remove_neighbor(neighbors, edges, v, u)

def modify_neighbors(neighbors, edges, u, newid):
  assert neighbors.has_key(u)
  for neigh in neighbors[u]:
    # Remove neighbor
    assert neighbors[neigh].count(u) > 0
    neighbors[neigh].remove(u)
    # Remove edge
    edge = (min(u, neigh), max(u, neigh))
    assert edge[0] < edge[1]
    log("change edge (%d, %d)" % edge, "-> (%d, %d)" % (neigh, newid))
    assert edges.count(edge) > 0
    edges.remove(edge)
    assert neigh < newid
    edges.append((neigh, newid))

def merge_neighbors(neighbors, newid, u, v):
  assert neighbors.has_key(u) > 0
  assert neighbors.has_key(v) > 0
  neighbors[newid] = neighbors[u] + neighbors[v]
  assert len(neighbors[newid]) == len(neighbors[u]) + len(neighbors[v])
  log("new vertex:", neighbors[newid])
  # Create links
  for neigh in neighbors[newid]:
    neighbors[neigh].append(newid)

def remove_neighbors(neighbors, u):
  assert neighbors.has_key(u)
  neighbors.pop(u)

def RandomContraction(neighbors, vertices, edges, newid):

  num_vertices = len(vertices)

  while num_vertices > 2:
    log("edges", edges)
    log("vertices", vertices)
    log("neighbors", neighbors)
    log("------------------------------------")
    # pick edge (u,v) at random
    edge = pick_edge(edges)
    remove_edge(edges, edge)
    u, v = edge

    # merge u and v into a single vertex
    remove_vertex(vertices, u)
    remove_vertex(vertices, v)
    add_vertex(vertices, newid)
    num_vertices -= 1

    # remove self-loops
    log("u:", u, neighbors[u])
    log("v:", v, neighbors[v])
    remove_self_loops(neighbors, edges, u, v)

    # rearrange edges
    modify_neighbors(neighbors, edges, u, newid)
    modify_neighbors(neighbors, edges, v, newid)
    merge_neighbors(neighbors, newid, u, v)

    # Remove neighbors
    remove_neighbors(neighbors, u)
    remove_neighbors(neighbors, v)

    newid += 1

    log()

  log("edges", edges)
  log("vertices", vertices)
  minCuts = len(edges)
  return minCuts

def do_test(neighbors, vertices, edges, newid, num_tests):

  bestSol = len(edges)
  solutions = {}
  for i in xrange(num_tests):
    n = {}
    for k in neighbors:
      n[k] = neighbors[k][:]
    v = vertices[:]
    e = edges[:]
    nid = newid
    minCuts = RandomContraction(n, v, e, nid)

    if minCuts < bestSol:
      print "min:", minCuts
      bestSol = minCuts

    solutions[minCuts] = solutions.setdefault(minCuts, 0) + 1

  # Stats
  print
  for i in xrange(len(edges)):
    if solutions.has_key(i):
      print i, solutions[i]
  print

  print "Solution:", bestSol


if __name__ == "__main__":

  if len(sys.argv) == 1:
    filename = 'kargerMinCut.txt'
  else:
    filename = sys.argv[1]

  # Read nodes and adjacency lists
  neighbors = {}
  vertices = []
  edges = []
  newid = 0
  with open(filename) as f:
    for l in f:
      line = l.strip().split()
      id = int(line[0])
      newid = max(id+1, newid)
      # Save vertex
      vertices.append(id)
      # Init adjacency list
      neighbors[id] = []
      for neigh in line[1:]:
        neigh = int(neigh)
        # Add node to adjacency list
        neighbors[id].append(neigh)
        # Save edge
        if id < neigh:
          edges.append((id, neigh))

  do_test(neighbors, vertices, edges, newid, 50000)

