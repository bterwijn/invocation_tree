import call_tree

def permutations(all_permutations, data, perm, n):
    if n<=0:
        print(perm)
        all_permutations.append(perm.copy())
    else:
        for i in data:
            perm.append(i)
            permutations(all_permutations, data, perm, n-1)
            perm.pop()

call_tree = call_tree.Call_Tree(each_line=True)
all_permutations = []

call_tree.to_string[list] = lambda x : f'my_list:{x}'
call_tree.to_string[id(all_permutations)] = lambda x : f'perms:{x}'
call_tree.to_string['permutations.return'] = lambda x : f'return:{x}'
call_tree.to_string['permutations.n'] = lambda x : f'{x} this is n'

#call_tree(permutations, ['a','b','c'], [], 2)
call_tree(permutations, all_permutations, ['a','b','c'], [], 2)
print('all_permutations:', all_permutations)
