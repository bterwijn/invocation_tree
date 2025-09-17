import random
import string

def get_name(i):
    name = ''
    while True:
        i, remainder = divmod(i, 26)
        name = string.ascii_lowercase[remainder] + name
        if i == 0:
            break
        i -= 1
    return name

def generate(n, max_edge, seed=0):
    random.seed(seed)
    nodes = [get_name(i) for i in range(n)]
    if len(nodes) > 2:
        nodes[1], nodes[-1] = nodes[-1], nodes[1]
    edges = []
    for node1 in nodes:
        nr_edges = random.randint(1, max_edge)
        for _ in range(nr_edges):
            node2 = random.choice(nodes)
            if node1 != node2:
                if node1 > node2:
                    node1 , node2 = node2, node1
                edge = (node1, node2)
                if edge not in edges:
                    edges.append(edge)
    return nodes, edges

if __name__ == '__main__':
    nodes, edges = generate(10, 3)
    print('nodes =', nodes)
    print('edges =', edges)