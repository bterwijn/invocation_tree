import invocation_tree as ivt

def permutations(elements, perm, n):
    if n==0:
        return [perm]
    all_perms = []
    for element in elements:
        all_perms.extend(permutations(elements, perm + element, n-1))
    return all_perms

tree = ivt.gif('permutations.png')
result = tree(permutations, ['L','R'], '', 2)
print(result)
