import numpy as np
import json
from math import inf
from ahp import ahp
from floyd import shortest_path, get_path, timer
import config


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
  V = len(data['places'])
  graph = [[inf]*V for _ in range(V)]
  places = data['places']
  places_keys = list(places.keys())
  for i in places_keys:
    for j in places[i]['neighbours']:
      if j in places_keys:
        graph[places_keys.index(i)][places_keys.index(j)] = get_score(places, i, j, weights, prefs)

  print(len(graph))
  return graph


def path_handler(places, sp, pred):
  sp_index = np.unravel_index(np.argmin(sp[:, :, -1]), sp.shape[:2])
  places_keys = list(places.keys())
  path_ids = [places_keys[i] for i in get_path(pred, sp_index[0], sp_index[1], sp.shape[2]-1, True)]
  path_obj = [places[i] for i in path_ids]
  return path_obj


def select_meal_points(path, prefs, current_time=540): #current_time gunun kacinci dakikasi, saat 9:00
  meal_points = [(0,0)]
  last_meal = 0
  for meal in prefs:
    for i in range(meal_points[-1][0], len(path)):
      if last_meal + 270 < current_time and config.MEAL_TIMES[meal][1] > current_time > config.MEAL_TIMES[meal][0]:
        meal_points.append((i, path[i], meal))
        last_meal = current_time
        current_time += config.MEAL_DURATION
        break
      current_time += path[i]['duration']
  del meal_points[0]
  return meal_points


def get_meal_nodes(restaurants, meal_points, path_obj):
  neighbours_list = []
  for i in meal_points:
    if i[2] == 0:
      places = [path_obj[i[0]]['id'], path_obj[i[0]]['id']]
      neighbours = set(path_obj[i[0]]['neighbours'])
    else:
      places = [path_obj[i[0]]['id'], path_obj[i[0]-1]['id']]
      neighbours = set(path_obj[i[0]]['neighbours']).intersection(set(path_obj[i[0]-1]['neighbours']))

    neighbours_list.append((places, [restaurants[r] for r in neighbours if r in restaurants]))
  return neighbours_list


def select_restaurant(neighbours_list, restaurants, weights, prefs):
  final_rest = []
  for places, neighbours in neighbours_list:
    best_rest = {}
    best_score = inf
    for r in neighbours:
      score = 0
      for p in places:
        score += get_score(restaurants, r['id'], p, weights, prefs)
      if score < best_score:
        best_score = score
        best_rest = r
    final_rest.append(best_rest)
  return final_rest


def merge_path(restaurants, meal_points, path):
  for i, x in enumerate(meal_points):
    path.insert(x[0] + i, restaurants[i])
  return path


@timer
def main(pref, K):
  print('Model is in progress')
  with open('istanbul-graph.json', 'rb') as f:
    data = json.load(f)

  K -= 1
  ahp_weights = ahp([[1, 3, 1/3],
                    [1/3, 1, 1/9],
                    [3, 9, 1]])

  graph = init_graph(data, ahp_weights, set(pref))
  sp, pred = shortest_path(graph, K)
  path_obj = path_handler(data['places'], sp, pred)
  meal_points = select_meal_points(path_obj, [0, 1, 2])
  meal_nodes = get_meal_nodes(data['restaurants'], meal_points, path_obj)
  selected_restaurants = (select_restaurant(meal_nodes, data['restaurants'], ahp_weights, set(['turkish'])))
  path_obj = merge_path(selected_restaurants, meal_points, path_obj)
  print(' => '.join([i['name'] for i in path_obj]))
  return path_obj

def get_place_route(pref, K):
  print('Model is in progress')
  with open('istanbul-graph.json', 'rb') as f:
    data = json.load(f)

  K -= 1
  ahp_weights = ahp([[1, 3, 1/3],
                    [1/3, 1, 1/9],
                    [3, 9, 1]])

  graph = init_graph(data, ahp_weights, set(pref))
  sp, pred = shortest_path(graph, K)
  path_obj = path_handler(data['places'], sp, pred)

  print(' => '.join([i['name'] for i in path_obj]))
  return path_obj

# Category: {'park', 'art', 'museum', 'landmark', 'amusement', 'shopping', 'sea_side', 'historic', 'sightseeing'}
# main(['park'], 6)
