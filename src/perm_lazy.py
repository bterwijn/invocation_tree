def permutations(elements, perm, n):
    if n == 0:
        yield perm
    else:
        for element in elements:
            yield from permutations(elements, perm + element, n-1)

generator_function = permutations('LR', '', 3)
for perm in generator_function:
    print(perm)
