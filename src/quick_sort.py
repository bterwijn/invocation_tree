
def quick_sort(values):
    if len(values) <= 1:
        return values
    pivot = values[0]
    smaller = [x for x in values if x  < pivot]
    equal   = [x for x in values if x == pivot]
    larger  = [x for x in values if x  > pivot]
    return quick_sort(smaller) + equal + quick_sort(larger)

values = [5, 3, 1, 4, 2, 8, 9, 7, 6]
print('unsorted values:',values)
values = quick_sort(values)
print('  sorted values:',values)
