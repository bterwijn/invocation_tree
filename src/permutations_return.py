import invocation_tree as ivt

def permutations(elements, perm, n):
    if n == 0:
        return [perm]
    else:
        results = []
        for element in elements:
            results += permutations(elements, perm + element, n-1)
        return results

tree = ivt.gif('permutations_return.png')
print(tree(permutations, 'LR', '', 3))
