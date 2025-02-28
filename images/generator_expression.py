import invocation_tree as invo_tree

def main():
    my_generator = (i*10 for i in range(1,4)) # generator expression
    return list(my_generator)

tree = invo_tree.gif('generator_expression.png')
import types
tree.to_string[types.GeneratorType]  = lambda x: 'generator'      # short name for generators
tree.to_string[type(iter(range(0)))] = lambda x: 'range_iterator' # short name for range_iterator
print( tree(main) )
