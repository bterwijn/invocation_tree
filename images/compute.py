import invocation_tree as ivt

def main():
    a = 1
    a = expression(a)
    return multiply(a, 6)
    
def expression(a):
    a = subtract(a, 3)
    return add(a, 9)
    
def subtract(a, b):
    return a - b

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

tree = ivt.gif('compute.png')
print( tree(main) )
