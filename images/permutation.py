import invocation_tree

def permutations(data, perm, n):
    if n<=0:
        print(perm)
    else:
        for i in data:
            perm.append(i)
            permutations(data, perm, n-1)
            perm.pop()

invocation_tree = invocation_tree.Invocation_Tree()

invocation_tree.output_filename = 'permutation.png'
invocation_tree.output_count = 0
invocation_tree.block = False

invocation_tree(permutations, ['a','b','c'], [], 2)
