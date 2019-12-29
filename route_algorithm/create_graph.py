import json

def main():
  with open('data/istanbul-graph.json', 'rb') as f:
    data = json.load(f)

  for i in data['places']:
    del data['places'][i]['reviews']
    del data['places'][i]['opening_hours']

    neighbours = list(data['places'][i]['neighbours'].keys()).copy()

    for j in neighbours:
      try:
        int(j)
        del data['places'][i]['neighbours'][j]
        print(j, 'is deleted')
      except:
        pass

  with open('graph.json', 'w') as f:
    json.dump(data['places'], f, indent=2)


main()
