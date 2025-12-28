
def permutations(elements, perm, n):
    if n == 0:
        print(perm)
    else:
        for element in elements:
            perm.append(element)  # do action that mutates list, FAST!
            permutations(elements, perm, n-1)
            perm.pop()            # undo action
            
permutations('LR', [], 3)
