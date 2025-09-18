edges =  [('a', 's'), ('i', 'z'), ('c', 'p'), ('d', 'p'), ('d', 'u'), ('b', 'e'), ('b', 'g'), ('f', 'p'), ('g', 'm'), ('h', 't'), ('h', 'y'), ('i', 'w'), ('i', 'j'), ('i', 'x'), ('k', 's'), ('k', 'l'), ('a', 'm'), ('n', 'u'), ('a', 'o'), ('a', 'v'), ('n', 'p'), ('a', 'q'), ('a', 'h'), ('p', 'r'), ('l', 's'), ('t', 'v'), ('u', 'y'), ('j', 'v'), ('a', 'j'), ('r', 'w'), ('r', 'u'), ('f', 'x'), ('x', 'y'), ('j', 'x'), ('d', 'j'), ('b', 'k'), ('b', 'x'), ('b', 'w')]

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

def print_all_paths(steps, path, goal, length, results):
    current = path[-1]
    length_path = len(path)
    if length_path >= length:
        if length_path == length and current == goal:
            if 'd' in path:
                results.append(path)
    else:
        valid_steps = steps[current]
        for s in valid_steps:
            if not s == 'x':
                print_all_paths(steps, path+s, goal, length, results)

steps = edges_to_steps(edges)
results = []
print_all_paths(steps, 'a', 'b', 10, results)
print('results:', results)
print(len(results))
