import invocation_tree as ivt

def quick_sort(values):
    if len(values) <= 1:
        return values
    pivot = values[0]
    smaller = [x for x in values if x  < pivot]
    equal   = [x for x in values if x == pivot]
    larger  = [x for x in values if x  > pivot]
    return quick_sort(smaller) + equal + quick_sort(larger)

values = [7, 4, 2, 6, 1, 5, 3, 9, 10, 8, 7, 11]
print('unsorted values:',values)
tree = ivt.gif('quick_sort.png')
values = tree(quick_sort, values)
print('  sorted values:',values)
