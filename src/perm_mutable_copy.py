
def permutations(elements, perm, n):
    if n == 0:
        print(perm)
    else:
        for element in elements:
            permutations(elements, perm + [element], n-1)  # creates new list, SLOW!

permutations('LR', [], 3)
