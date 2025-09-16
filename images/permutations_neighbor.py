import invocation_tree as ivt

def permutations(elems, perm, n):
    if n == 0:
        print(perm)
    else:
        for element in elems:
            if len(perm) == 0 or not perm[-1] == element:  # test neighbor
                permutations(elems, perm + element, n-1)  

tree = ivt.gif('permutations_neighbor.png')
tree(permutations, 'ABC', '', 3)  # permutations of A, B, C of length 3
