from functools import reduce

nodes = lambda es: set(reduce(lambda acc, e: acc + list(e[0:2]), es, []))
sorted_edges = lambda es: sorted(es, key=lambda x: x[2])
is_cycle = lambda acc, e: set(e[0:2]).issubset(nodes(acc))
add_edge = lambda acc, e: acc + [e] if not is_cycle(acc, e) else acc
kruskal = lambda es: reduce(add_edge, sorted_edges(es), [])

# (node 1, node 2, cost)
edges = [(0,1,12),(0,2,34),(0,4,78),(1,3,55),(1,4,32),(2,3,61),(2,4,44),(3,4,93)]
print(kruskal(edges))
