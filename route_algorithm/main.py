import numpy as np
import json
from math import inf
from ahp import ahp
from floyd import shortest_path, get_path
from time import time


def timer(f):
  def inner(*args, **kwargs):
    start = time()
    rv = f(*args, **kwargs)
    end = time()
    print('Ellapsed time is {} seconds'.format(round(end - start, 2)))
    return rv
  return inner


def get_score_params(data, place1, place2, prefs):
  distance = data['places'][place1]['neighbours'][place2][0] / 10000
  rating = data['places'][place1]['rating']
  comment = data['places'][place1]['rating_count'] / 45000
  rating2 = data['places'][place2]['rating']
  comment2 = data['places'][place2]['rating_count'] / 45000
  category = len(set(data['places'][place1]['category']).intersection(prefs)) / 2
  category2 = len(set(data['places'][place2]['category']).intersection(prefs)) / 2

  return (distance, 4 - (rating + comment + rating2 + comment2), 2 - (category + category2))


def get_score(data, place1, place2, weights, prefs):
  score_params = get_score_params(data, place1, place2, prefs)
  score = sum([x * score_params[i] for i, x in enumerate(weights)])
  return score


def init_graph(data, weights, prefs):
  V = len(data['places'])
  graph = [[inf]*V for _ in range(V)]
  places = list(data['places'].keys())
  for i in places:
    for j in data['places'][i]['neighbours']:
      try:
        int(j)
      except:
        graph[places.index(i)][places.index(j)] = get_score(data, i, j, weights, prefs)

  return graph


@timer
def main():
  with open('data/istanbul-graph.json', 'rb') as f:
    data = json.load(f)

  V = len(data['places'])
  K = 6
  weights = ahp([[1, 1/5, 1/11],
                [5, 1, 1/5],
                [11, 5, 1]])

  graph = init_graph(data, weights, {'museum'})
  sp, pred = shortest_path(graph, K)
  sp_index = np.unravel_index(np.argmin(sp[:, :, K]), sp.shape[:2])
  places = list(data['places'].keys())
  path_ids = [places[i] for i in get_path(pred, sp_index[0], sp_index[1], K)]
  path_names = [data['places'][i]['name'] for i in path_ids]
  print(' => '.join(path_names))


main()
