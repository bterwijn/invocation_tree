def permutations(elems, perm, n):
    if n == 0:
        print(perm)
    else:
        for element in elems:
            if len(perm) == 0 or not perm[-1] == element:
                permutations(elems, perm + element, n-1)  

permutations('ABC', '', 3)
