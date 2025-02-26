import invocation_tree as invo_tree
import types

class Source:

    def __init__(self, stop, start=0, step=1):
        self.stop = stop
        self.step = step
        self.i = start

    def __repr__(self):
        return f'Source i:{self.i} step:{self.step} stop:{self.stop}'

    def __iter__(self):
        return self

    def __next__(self):
        prev = self.i
        self.i += self.step
        if prev < self.stop:
            return prev
        raise StopIteration()

def double(pipeline):
    for value in pipeline:
        yield value*2

def just_print(pipeline):
    for value in pipeline:
        print('just print:', value)
        yield value
        
def main():
    pipeline = Source(start=1, stop=3)
    pipeline = double(pipeline)
    pipeline = (-i for i in pipeline)
    pipeline = just_print(pipeline)
    return sum(pipeline)

tree = invo_tree.gif('generators.png')
tree.to_string[types.GeneratorType] = lambda gen: 'generator'
print('sum:', tree(main))
