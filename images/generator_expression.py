import invocation_tree as invo_tree
import types

def main():
    my_generator = (i*10 for i in range(1,4)) # generator expression
    result = list(my_generator)
    print('result:', result)

tree = invo_tree.gif('generator_expression.png')
tree.to_string[type(iter(range(0)))] = lambda x: 'range_iterator' # short name for range_iterator
tree.to_string[types.GeneratorType]  = lambda x: 'generator'      # short name for generators
tree(main)
