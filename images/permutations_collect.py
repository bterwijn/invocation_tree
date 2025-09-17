def permutations(elements, perm, n, results):
    if n == 0:
        results.append(perm)
    else:
        for element in elements:
            permutations(elements, perm + element, n-1, results)

results = []
permutations('LR', '', 3, results)
print(results)
