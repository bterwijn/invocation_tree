import invocation_tree as invo_tree

def main():
    a = 12
    a = expression(a)
    return multiply(a, 6)
    
def expression(a):
    a = subtract(a, 7)
    return add(a, 2)
    
def subtract(a, b):
    return a - b

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

tree = invo_tree.gif('compute.png')
print( tree(main) )
