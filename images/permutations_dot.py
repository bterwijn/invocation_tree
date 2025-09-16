import sys

from graphviz import Digraph

def add_permute_nodes(dot, elements, perm, n, parent_id=None, node_id=[0]):
    if n < 0:
        return

    my_id = node_id[0]
    node_id[0] += 1
    dot.node(str(my_id), perm)

    
    if parent_id is not None:
        dot.edge(str(parent_id), str(my_id))
    
    for i, ch in enumerate(elements):
        add_permute_nodes(dot, elements, perm + ch, n-1, parent_id=my_id, node_id=node_id)

def make_permutation_tree(outfile, elements, n):
    dot = Digraph()
    dot.attr(rankdir='TB')  # top to bottom    
    add_permute_nodes(dot, elements, "", n)
    splits = outfile.split('.')
    dot.format = splits[-1]
    dot.render(filename=''.join(splits[:-1]), cleanup=True)
    print(f"Generated graph: {outfile}")

if __name__ == "__main__":
    make_permutation_tree(sys.argv[1], sys.argv[2], int(sys.argv[3]))
