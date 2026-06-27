import string
import random

ivt_tree.hide_vars.add('depth_first_recursive.graph')

def create_graph(names, nr_edges):
    graph = {}
    names_set = set(names)
    for i in names:
        valid_edges = list(names_set - {i})
        graph[i] = ''.join([ e for e in random.sample(valid_edges, nr_edges)])
    return graph

def depth_first(graph, begin, end):
    path = [begin]
    all_paths = []
    
    def depth_first_recursive():
        current = path[-1]
        if current == end:
            all_paths.append(''.join(path)) # path to string
        else:
            for n in graph[current]:
                if n not in path:
                    path.append(n) # change path
                    depth_first_recursive()
                    path.pop()     # undo path change

    depth_first_recursive()
    return all_paths

nr_nodes = 5
nr_edges = 3
graph = create_graph(string.ascii_lowercase[:nr_nodes], nr_edges)
all_paths = depth_first(graph, 'a', 'b')
print(all_paths)
