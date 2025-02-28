import invocation_tree as invo_tree

def my_generator():
    yield 1
    yield 2
    yield 3

def main():
    return list(my_generator())

tree = invo_tree.gif('generator_function.png')
print( tree(main) )
