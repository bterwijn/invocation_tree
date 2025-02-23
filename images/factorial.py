import invocation_tree as invo_tree

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

tree = invo_tree.gif('factorial.png')
tree(factorial, 4)
