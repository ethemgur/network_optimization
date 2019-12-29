import numpy as np
import json
from math import inf
from ahp import ahp
from floyd import shortest_path, get_path, timer


def get_score_params(data, place1, place2, prefs):
  distance = data[place1]['neighbours'][place2][0] / 10000
  rating, comment, category = 0, 0, 0
  for i in [place1, place2]:
    rating += data[place1]['rating'] / 5 / 2
    comment += data[place1]['rating_count'] / 45000 / 2
    category += len(set(data[place1]['category']).intersection(prefs)) / 2

  return (distance, - (rating * comment), - category)


def get_score(data, place1, place2, weights, prefs):
  score_params = get_score_params(data, place1, place2, prefs)
  score = sum([x * score_params[i] for i, x in enumerate(weights)])
  return score + 100


@timer
def init_graph(data, weights, prefs):
  print('Initializing the graph')
  V = len(data)
  graph = [[inf]*V for _ in range(V)]
  places = list(data.keys())
  for i in places:
    for j in data[i]['neighbours']:
      graph[places.index(i)][places.index(j)] = get_score(data, i, j, weights, prefs)

  return graph


def path_handler(data, sp, pred):
  sp_index = np.unravel_index(np.argmin(sp[:, :, -1]), sp.shape[:2])
  places = list(data.keys())
  path_ids = [places[i] for i in get_path(pred, sp_index[0], sp_index[1], sp.shape[2]-1)]
  path_names = [data[i]['name'] for i in path_ids]
  return path_ids, path_names


@timer
def main():
  print('Model is in progress')
  with open('graph.json', 'rb') as f:
    data = json.load(f)

  K = 6
  ahp_weights = ahp([[1, 1/5, 1/11],
                [5, 1, 1/5],
                [11, 5, 1]])

  graph = init_graph(data, ahp_weights, {'museum'})
  sp, pred = shortest_path(graph, K)
  path_ids, path_names = path_handler(data, sp, pred)
  print(' => '.join(path_names))


main()
