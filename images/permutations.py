import invocation_tree as ivt

def permutations(elements, perm, n):
    if n == 0:
        print(perm)
    else:
        for element in elements:
            permutations(elements, perm + element, n-1)

tree = ivt.gif('permutations.png')
result = tree(permutations, 'LR', '', 3)
