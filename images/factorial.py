import invocation_tree as ivt

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

tree = ivt.gif('factorial.png')
tree(factorial, 4)
