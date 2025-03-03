import invocation_tree as invo_tree

def subtract(pipeline):
    return [a - 3 for a in pipeline]

def multiply(pipeline):
    return [a * 6 for a in pipeline]

def my_sum(pipeline):
    total = 0
    for i in pipeline:
        total += i
    return total # return not yield, so not lazy
        
def main():
    pipeline = range(1,4)
    pipeline = subtract(pipeline)
    pipeline = [a + 9 for a in pipeline]
    pipeline = multiply(pipeline)
    return my_sum(pipeline)

tree = invo_tree.gif('eager_pipeline.png')
print( tree(main) )
