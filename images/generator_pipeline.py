import invocation_tree as invo_tree

def subtract(pipeline):
    for a in pipeline:
        yield a - 3

def multiply(pipeline):
    for a in pipeline:
        yield a * 6
        
def main():
    pipeline = range(1,4)
    pipeline = subtract(pipeline)
    pipeline = (a + 9 for a in pipeline)
    pipeline = multiply(pipeline)
    return sum(pipeline)

tree = invo_tree.gif('generator_pipeline.png')
import types
tree.to_string[types.GeneratorType]  = lambda x: 'generator'      # short name for generators
tree.to_string[type(iter(range(0)))] = lambda x: 'range_iterator' # short name for range_iterator
print( tree(main) )
