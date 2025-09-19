edges =  [('a', 'j'), ('f', 'j'), ('c', 'e'), ('b', 'd'), ('b', 'e'), ('f', 'g'), 
          ('g', 'i'), ('h', 'i'), ('e', 'h'), ('a', 'i'), ('b', 'h'), ('b', 'f')]

# hide variable with long value
ivt_tree.hide_vars.add('print_all_paths.connections')

def edges_to_connections(edges: list[tuple[str, str]]) -> dict[str,list[str]]:
    """ Returns a dict with for each node the nodes it is connected with. """ 
    connections = {}
    for n1, n2 in edges:
        if not n1 in connections:
            connections[n1] = []
        connections[n1].append(n2)
        if not n2 in connections:
            connections[n2] = []
        connections[n2].append(n1)
    return connections

def print_all_paths(connections, path, goal):
    current = path[-1]
    if current == goal:
        print(path)
    else:
        valid_connections = connections[current]  
        for n in valid_connections:
            if n not in path:
                new_path = path + n
                print(f'--- add   :{n}  {new_path}')
                print_all_paths(connections, new_path, goal)
                print(f'--- remove:{n}  {path}')

connections = edges_to_connections(edges)
print_all_paths(connections, 'a', 'b')
