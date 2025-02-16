import invoke_tree

def permutations(all_permutations, data, perm, n):
    if n<=0:
        print(perm)
        all_permutations.append(perm.copy())
    else:
        for i in data:
            perm.append(i)
            permutations(all_permutations, data, perm, n-1)
            perm.pop()

invoke_tree = invoke_tree.Invoke_Tree(each_line=True)
all_permutations = []

invoke_tree.to_string[list] = lambda x : f'my_list:{x}'
invoke_tree.to_string[id(all_permutations)] = lambda x : f'perms:{x}'
invoke_tree.to_string['permutations.return'] = lambda x : f'return:{x}'
invoke_tree.to_string['permutations.n'] = lambda x : f'{x} this is n'

#invoke_tree(permutations, ['a','b','c'], [], 2)
invoke_tree(permutations, all_permutations, ['a','b','c'], [], 2)
print('all_permutations:', all_permutations)
