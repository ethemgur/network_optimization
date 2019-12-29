from pulp import *
import json


TIME_LIMIT = 500
pref = {'landmark', 'historic'}

def read_json():
  with open('data/istanbul-graph.json', 'r') as f:
    graph = json.load(f)

  return graph['places']


def satisfaction(graph_el):
  return 1 if len(set(graph_el['category']).intersection(pref)) > 0 else 0

def lp(graph):

  model = LpProblem('Route', LpMaximize)
  locations = [i for i in graph.keys()]
  order = list(range(6))
  place = LpVariable.dicts('Place', [(i,k) for i in locations for k in order], cat=LpBinary)
  edge = LpVariable.dicts('Edge', [(i,j) for i in locations for j in graph[i]['neighbours'].keys()], cat=LpBinary)

  model += lpSum(place[i, k] * (0*graph[i]['rating']*graph[i]['rating_count']/90000 + 0.8*satisfaction(graph[i])/2) for i in locations for k in order)

  for k in order:
    model += lpSum(place[i, k] for i in locations) <= 1

  for i in locations:
    model += lpSum(place[i, k] for k in order) <= 1

  model += lpSum(edge[i,j] * graph[i]['neighbours'][j][1]/60 for i in locations for j in graph[i]['neighbours']) + lpSum(place[i,k] * graph[i]['duration'] for i in locations for k in order) <= TIME_LIMIT

  for i in locations:
    for j in graph[i]['neighbours'].keys():
      model += -0.5 + 0.5 * (lpSum(place[i, k] + place[i, k+1] for k in order[:-1]))  <= edge[i, j]

  model.solve()
  print(LpStatus[model.status])

  trip = []
  for i in locations:
    for k in order:
      if place[i, k].varValue != 0:
        trip.append((place[i, k].varValue, k, graph[i]['name'], i))

  trip = sorted(trip, key=lambda x: x[1])
  print('Trip: ')
  for i in trip:
    print(i)
    print(graph[i[3]]['category'])


lp(read_json())
