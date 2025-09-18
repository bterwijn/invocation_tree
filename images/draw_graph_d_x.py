import sys
import graph
import graphviz

def draw_graph(nodes, edges, filename='graph.png'):
    dot = graphviz.Graph(
        format='png',
    )
    for node in nodes:
        # Color specific nodes
        if node == 'a':
            dot.node(node, fillcolor='green', style='filled')
        elif node == 'b':
            dot.node(node, fillcolor='red', style='filled')
        elif node == 'd':
            dot.node(node, fillcolor='orange', style='filled')
        elif node == 'x':
            dot.node(node, fillcolor='gray', style='filled')
        else:
            dot.node(node)
    for edge in edges:
        dot.edge(edge[0], edge[1])
    dot.render(filename, cleanup=True)
    print('edges = ', edges)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python draw_graph.py <n> <max_edges> <output_file> <seed>")
        sys.exit(1)
    n = int(sys.argv[1])
    max_edges = int(sys.argv[2])
    output_file = sys.argv[3]
    seed = int(sys.argv[4])

    nodes, edges = graph.generate(n, max_edges, seed)
    draw_graph(nodes, edges, output_file)
