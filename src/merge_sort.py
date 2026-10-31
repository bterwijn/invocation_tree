import random

def merge_sort(values):
    
    def merge(values1, values2):
        """ Merge and return sorted lists 'values1' and 'values2'. """
        values = []
        i1, i2 = 0, 0
        while True:
            if i1 == len(values1):           # finished with values1
                values.extend(values2[i2:])  # so add remainder values2
                break
            elif i2 == len(values2):         # finished with values2
                values.extend(values1[i1:])  # so add remainder values1
                break
            else:
                if values1[i1] <= values2[i2]:  # find next smallest value
                    values.append(values1[i1])
                    i1 += 1
                else:
                    values.append(values2[i2])
                    i2 += 1
        return values 

    if len(values) <= 1:  # stop condition
        return values
    half = len(values)//2
    values1, values2 = values[:half], values[half:]  # split in two halfs
    return merge(merge_sort(values1), merge_sort(values2))

n = 10
values = [random.randrange(n*2) for i in range(n)]
print('values       :', values)
values_sorted = merge_sort(values)
print('values_sorted:', values_sorted)
