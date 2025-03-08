import invocation_tree as ivt

def factorial(n):
    if n <= 1:
        return 1
    prev_result = factorial(n - 1)
    return n * prev_result

tree = ivt.gif('factorial.png')
tree(factorial, 4)
