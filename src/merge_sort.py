import random

def heap_sort(values):
    def heapify(values, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and values[left] > values[largest]:
            largest = left

        if right < n and values[right] > values[largest]:
            largest = right

        if largest != i:
            values[i], values[largest] = values[largest], values[i]
            heapify(values, n, largest)

    n = len(values)
    for i in range(n // 2 - 1, -1, -1):
        heapify(values, n, i)
    for i in range(n - 1, 0, -1):
        values[i], values[0] = values[0], values[i]
        heapify(values, i, 0)
    return values

n = 10
values = list(range(n))
random.shuffle(values)
print('unsorted values:',values)
values = heap_sort(values)
print('  sorted values:',values)
