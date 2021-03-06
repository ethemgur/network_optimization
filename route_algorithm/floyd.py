import numpy as np
from math import inf
from time import time
import ujson


def timer(f):
  def inner(*args, **kwargs):
    start = time()
    rv = f(*args, **kwargs)
    end = time()
    print('\tEllapsed time is {} seconds'.format(round(end - start, 2)))
    return rv
  return inner


def get_path(pred, u, v, k, last=False):
  path = []
  node = pred[u][v][k]
  for i in range(k-1, 0, -1):
    path.append(node)
    node = pred[node][v][i]
    if last:
      print('Path', i)
      print([u] + path + [v])

  return [u] + path + [v]


@timer
def shortest_path(graph, k):
  print('Finding the shortest path')
  V = len(graph)

  sp = [[None] * V for _ in range(V)]
  pred = [[None] * V for _ in range(V)]

  for i in range(V):
    for j in range(V):
      sp[i][j] = [None] * (k + 1)
      pred[i][j] = [None] * (k + 1)

  for e in range(k + 1):
    for i in range(V):
      for j in range(V):
        sp[i][j][e] = inf

        if e == 0 and i == j:
          sp[i][j][e] = 0
        if e == 1 and graph[i][j] != inf:
          sp[i][j][e] = graph[i][j]

        if e > 1:
          for a in range(V):
            if graph[i][a] != inf and a not in [i, j] and sp[a][j][e - 1] != inf:
              new_path_score = graph[i][a] + sp[a][j][e - 1]
              if new_path_score < sp[i][j][e]:
#                 new_path = get_path(pred, a, j, e - 1)
#                 if len(new_path) == len(set(new_path)):
#                   sp[i][j][e] = new_path_score
#                   pred[i][j][e] = a
#                 else:
#                   new_path = get_path(pred, i, j, e - 1)
#                   if not a in new_path:
#                     sp[i][j][e] = new_path_score
#                     pred[i][j][e] = a
                pred_ij = pred[i][j][e]
                pred[i][j][e] = a
                new_path = get_path(pred, i, j, e)
                if len(new_path) == len(set(new_path)):
                  sp[i][j][e] = new_path_score
                  pred[i][j][e] = a
                else:
                  pred[i][j][e] = pred_ij


  return np.array(sp), pred


def test():
  inf = 10**8
  graph = [[inf, 4, inf, inf, inf, inf, inf, 8, inf],
          [4, inf, 8, inf, inf, inf, inf, 11, inf],
          [inf, 8, inf, 7, inf, 4, inf, inf, 2],
          [inf, inf, 7, inf, 9, 14, inf, inf, inf],
          [inf, inf, inf, 9, inf, 10, inf, inf, inf],
          [inf, inf, 4, 14, 10, inf, 2, inf, inf],
          [inf, inf, inf, inf, inf, 2, inf, 1, 6],
          [8, 11, inf, inf, inf, inf, 1, inf, 7],
          [inf, inf, 2, inf, inf, inf, 6, 7, inf]]

  u = 2
  v = 8
  k = 5

  sp, pred = shortest_path(graph, k)

  print('FROM {} TO {} IN {} STEPS'.format(u, v, k))
  print('Cost is', sp[u][v][k])
  print('Path is', ' => '.join([str(i) for i in get_path(pred, u, v, k)]))
