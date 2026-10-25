import random

def merge_sort(values):
    
    def merge(values1, values2):
        values = []
        i1, i2 = 0, 0
        while not (i1==len(values1) and i2==len(values2)):
            if i1 == len(values1):
                values.extend(values2[i2:])
                i2 = len(values2)
            elif i2 == len(values2):
                values.extend(values1[i1:])
                i1 = len(values1)
            else:
                if values1[i1] <= values2[i2]:
                    values.append(values1[i1])
                    i1 += 1
                else:
                    values.append(values2[i2])
                    i2 += 1
        return values 

    if (len(values)<=1):  # stop condition
        return values
    values1, values2 = values[:len(values)//2], values[len(values)//2:]
    return merge(merge_sort(values1), merge_sort(values2))

n = 10
values = [random.randrange(n*2) for i in range(n)]
print('values       :', values)
values_sorted = merge_sort(values)
print('values_sorted:', values_sorted)
