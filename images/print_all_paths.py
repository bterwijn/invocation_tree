edges =  [('a', 'j'), ('f', 'j'), ('c', 'e'), ('b', 'd'), ('b', 'e'), ('f', 'g'), ('g', 'i'), ('h', 'i'), ('e', 'h'), ('a', 'i'), ('b', 'h'), ('b', 'f')]

def edges_to_steps(edges: list[tuple[str, str]]) -> dict[str,list[str]]:
    """ Returns a dict with for each node the nodes it is connected with. """ 
    steps = {}
    for n1, n2 in edges:
        if not n1 in steps:
            steps[n1] = []
        steps[n1].append(n2)
        if not n2 in steps:
            steps[n2] = []
        steps[n2].append(n1)
    return steps

def print_all_paths(steps, path, goal):
    current = path[-1]
    if current == goal:
        print(path)
    else:
        valid_steps = steps[current]
        for s in valid_steps:
            if s not in path:
                print_all_paths(steps, path+s, goal)

steps = edges_to_steps(edges)
print_all_paths(steps, 'a', 'b')
