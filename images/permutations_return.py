def permutations(elements, perm, n):
    if n == 0:
        return [perm]
    else:
        results = []
        for element in elements:
            results += permutations(elements, perm + element, n-1)
        return results

print(permutations('LR', '', 3))
