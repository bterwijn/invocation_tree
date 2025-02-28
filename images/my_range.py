import invocation_tree as invo_tree

class My_Iterator:

    def __init__(self, my_range):
        self.my_range = my_range
        self.value = self.my_range.start

    def __repr__(self):
        return f'My_Iterator value:{self.value}'

    def __next__(self):
        print('My_Iterator.__next__')
        prev = self.value
        self.value += self.my_range.step
        if prev < self.my_range.stop:
            return prev
        raise StopIteration

class My_Range:

    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step

    def __repr__(self):
        return f'My_Range start:{self.start} stop:{self.stop} step:{self.step}'
        
    def __iter__(self):
        print('My_Range.__iter__')
        return My_Iterator(self)

def main():
    my_range = My_Range(1, 4)
    for i in my_range:
        print(i)

tree = invo_tree.gif('my_range.png')
tree(main)

