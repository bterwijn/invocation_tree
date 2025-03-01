# Installation #
Install (or upgrade) `invocation_tree` using pip:
```
pip install --upgrade invocation_tree
```
Additionally [Graphviz](https://graphviz.org/download/) needs to be installed.

# Invocation Tree #
The [invocation_tree](https://pypi.org/project/invocation-tree/) package is designed to help with **program understanding and debugging** by visualizing the **tree of function invocations** that occur during program execution. Here’s a simple example of how it works, we start with `a = 1` and compute:

```
    (a - 3 + 9) * 6
```

```python
import invocation_tree as invo_tree

def main():
    a = 1
    a = expression(a)
    return multiply(a, 6)
    
def expression(a):
    a = subtract(a, 3)
    return add(a, 9)
    
def subtract(a, b):
    return a - b

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

tree = invo_tree.blocking()
print( tree(main) )
```
Running the program and pressing &lt;Enter&gt; a number of times results in:
![compute](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/compute.gif)
```
42
```
Each node in the tree represents a function call, and the node's color indicates its state:

 - White: The function is currently being executed (it is at the top of the call stack).
 - Green: The function is paused and will resume execution later (it is lower down on the call stack).
 - Red: The function has completed execution and returned (it has been removed from the call stack).

For every function, the package displays its **local variables** and **return value**. Changes to these values over time are highlighted using bold text and gray shading to make them easy to track.

# Chapters #

[Comprehensions](#Comprehensions)

[Debugger](#Debugger)

[Recursion](#Recursion)

[Lazy Evalution](#Lazy-Evalution)

[Configuration](#Configuration)

[Troubleshooting](#Troubleshooting)

# Author #
Bas Terwijn

# Inspiration #
Inspired by [rcviz](https://github.com/carlsborg/rcviz).

# Supported by #
<img src="https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/uva.png" alt="University of Amsterdam" width="600">

___
___

# Comprehensions #
In this more interesting example we compute which students pass a course by using list and dictionary comprehensions.

```python
import invocation_tree as invo_tree
from decimal import Decimal, ROUND_HALF_UP

def main():
    students = {'Ann':[7.5, 8.0], 
                'Bob':[4.5, 6.0], 
                'Coy':[7.5, 6.0]}
    averages = {student:compute_average(grades)
                for student, grades in students.items()}
    passing = passing_students(averages)
    print(passing)

def compute_average(grades):
    average = sum(grades)/len(grades)
    return half_up_round(average, 1)
    
def half_up_round(value, digits=0):
    """ High-precision half-up rounding of 'value' to a specified number of 'digits'. """
    return float(Decimal(str(value)).quantize(Decimal(f"1e-{digits}"),
                                              rounding=ROUND_HALF_UP))

def passing_students(averages):
    return [student 
        for student, average in averages.items() 
        if average >= 5.5]

if __name__ == '__main__':
    tree = invo_tree.blocking()
    tree(main) # show invocation tree starting at main
```
![students](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/students.gif)
```
['Ann', 'Coy']
```

## Blocking ##
The program blocks execution at every function call and return statement, printing the current location in the source code. Press the &lt;Enter&gt; key to continue execution. To block at every line of the program (like in a debugger tool) and only where a change of value occured, use instead:

```python
    tree = invo_tree.blocking_each_change()
```

# Debugger #
To visualize the invocation tree in a debugger tool, such as the integrated debugger in Visual Studio Code, use instead:

```python
    tree = invo_tree.debugger()
```

and open the 'tree.pdf' file manually.
![Visual Studio Code debugger](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/vscode.png)

# Recursion #
An invocation tree is particularly helpful to better understand recursion. A simple `factorial()` example:

```python
import invocation_tree as invo_tree

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

tree = invo_tree.blocking()
print( tree(factorial, 4) ) # show invocation tree of calling factorial(4)
```
![factorial](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/factorial.gif)
```
24
```

This `permutations()` example shows the depth-first nature of recursive execution:

```python
import invocation_tree as invo_tree

def permutations(elements, perm, n):
    if n==0:
        return [perm]
    all_perms = []
    for element in elements:
        all_perms.extend(permutations(elements, perm + element, n-1))
    return all_perms

tree = invo_tree.blocking()
result = tree(permutations, ['L','R'], '', 2)
print(result) # all permutations of going Left or Right of length 2
```
![permutations](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/permutations.gif)
```
['LL', 'LR', 'RL', 'RR']
```

## Hide Variables ##
In an educational context it can be useful to hide certian variables to avoid unnecessary complexity. This can for example be done with:

```python
tree = invo_tree.blocking()
tree.hide.add('permutations.elements')
tree.hide.add('permutations.element')
tree.hide.add('permutations.all_perms')
```

# Lazy Evalution
An invocation tree is helpful to understand how a pipeline of generators is lazily evaluated. But to understand generators and lazy evaluation we first have to understand the Iterator Protocol.

## Iterator Protocol ##
The [Iterator Protocol](https://docs.python.org/3/library/stdtypes.html#iterator-types) is implemented by many different types:

  `range`, `list`, `set`, `dict`, ...

which make these type iterable, meaning we can iterate over values of these types to get a sequence of values. It works by:

- first calling iter(iterable) to get an iterator
- then repeatedly calling next(iterator) to get each value
- the sequence ends when a StopIteration exceptions is raised

An example of iterable `range` and `list` in the Python interpreter looks like: 

<TABLE><TR><TD>

```
$ python
>>> iterator = iter(range(1,4))
>>> next(iterator)
1
>>> next(iterator)
2
>>> next(iterator)
3
>>> next(iterator)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

</TD><TD>

```
$ python
>>> iterator = iter([1,2,3])
>>> next(iterator)
1
>>> next(iterator)
2
>>> next(iterator)
3
>>> next(iterator)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

</TD></TR></TABLE>

It is the Iterator Protocol that allows a for-loop to read a sequence of values from an iterable:

```python
iterable = range(1,4)
for value in iterable:
    print(value)
```
```
1
2
3
```

and the same holds for many functions like `list()`, `sum()`,  `max()`, `min()`, ...

<TABLE><TR><TD>

```python
iterable = range(1,4)
print('list:', list(iterable))
```
```
list: [1, 2, 3]
```

</TD><TD>

```python
iterable = range(1,4)
print('sum:', sum(iterable))
```
```
sum: 6
```

</TD></TR></TABLE>

We can define our own `My_Range` and `My_Iterator` class to see the Iterator Protocol in action.
```python
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

tree = invo_tree.blocking()
tree(main)
```
![my_range.gif](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/my_range.gif)

```
My_Range.__iter__
My_Iterator.__next__
1
My_Iterator.__next__
2
My_Iterator.__next__
3
My_Iterator.__next__
```
As you can see a lot happens in `main()` to complete the for-loop:
- A 'my_range' object is created using its `My_Range.__init__` method. 
- The for-loop requests an iterator using 'iter(my_range)' resulting in a `My_Range.__iter__` method call.
- The for-loop keeps calling 'next(iterator)' to get the sequence of values resulting in `My_Iterator.__next__` calls.
- At the 4th call the sequence is ended with a `StopIteration` exception.

## Generator Functions ##
By using `yield` instead of `return` in a function, we can create a [generator](https://docs.python.org/3/reference/expressions.html#yield-expressions) that produces a sequence of values as an iterable.

```python
def my_generator():
    yield 1
    yield 2
    yield 3

def main():
    for i in my_generator():
        print(i)
    print('sum:', sum(my_generator()))

main()
```
```
1
2
3
sum: 6
```

The generator iterable can only be used once. Call the generator again when you need a new iterable:

```python
def my_generator():
    yield 1
    yield 2
    yield 3

def main():
    iterable = my_generator()
    print('sum:', sum(iterable)) # 6
    print('sum:', sum(iterable)) # 0, a used up generator doesn't give any values
    iterable = my_generator()
    print('sum:', sum(iterable)) # 6

main()
```

A generator is lazy, meaning that it will only produce its values if you request them via the Iterator Protocol. That means that if you print the generator it will just print '&lt;generator object ...&gt;'. To print its values you can for example use `list()` that uses the Iterator Protocol to request its values and converts them to a `list` that can be printed. But then you have used the generator so it no longer has values.

```python
def my_generator():
    yield 1
    yield 2
    yield 3

def main():
    my_gen = my_generator()
    print( my_gen )
    print( list(my_gen) ) # printing uses up the generator
    print( list(my_gen) ) # no more values available
    print( list(my_generator()) ) # new generator

main()
```
```
<generator object my_generator at 0x7fd965cf0ca0>
[1, 2, 3]
[]
[1, 2, 3]
```

By using invocation_tree we can see how the Iterator Protocol works on the generator.

```python
import invocation_tree as invo_tree

def my_generator():
    yield 1
    yield 2
    yield 3

def main():
    return list(my_generator())

tree = invo_tree.blocking()
print( tree(main) )
```
![generator_function.gif](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/generator_function.gif)
```
[1, 2, 3]
```
In `main()`:
- The 'list(my_generator())' call requests an iterator from the generator. 
- It keep calling next() on it to read the sequence resulting in `my_generator()` calls.
- When called `my_generator()` yields a value, and then pauses and saves its state, allowing it to continue from where it left off when called again.
- At the 4th call `my_generator()` returns None and automatically raises a StopIteration exception that signals the end of the sequence and makes `list()` return its result.

## Generator Expressions ##
Another way to create a generator is with a [generator expression](https://docs.python.org/3/reference/expressions.html#generator-expressions) that looks like a list comprehension except that it uses the '(' and ')' parentheses instead of the '[' and ']' brackets. A generator expression reads from an iterable and produces a generator iterable:

```python
import invocation_tree as invo_tree

def main():
    my_generator = (i*10 for i in range(1,4)) # generator expression
    return list(my_generator)

tree = invo_tree.blocking()
import types
tree.to_string[types.GeneratorType]  = lambda x: 'generator' # short name for generators
tree.to_string[type(iter(range(0)))] = lambda x: 'iterator'  # short name for iterator
print( tree(main) )
```
![generator_expression.gif](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/generator_expression.gif)
```
[10, 20, 30]
```
## Generator Pipeline ##
The key advantage of Python generators is their ability to create a **pipeline of computations**, where each generator handles a specific part of the process. Values are processed one at a time and flow through the pipeline lazily, meaning computations are performed only when needed. This eliminates the need to store the entire dataset in memory, such as in a list, making generators highly memory-efficient. Because the computation is split into modular steps, it’s easy to add, remove, or modify generators in the pipeline. This combination of flexibility, low memory usage, and on-demand processing makes generators ideal for handling large datasets or continuous data streams.

```python
import invocation_tree as invo_tree

def subtract(pipeline):
    for a in pipeline:
        yield a - 3

def multiply(pipeline):
    for a in pipeline:
        yield a * 6

def my_sum(pipeline):
    total = 0
    for i in pipeline:
        total += i
    return total # return not yield, so not lazy
        
def main():
    pipeline = range(1,4)
    pipeline = subtract(pipeline)
    pipeline = (a + 9 for a in pipeline)
    pipeline = multiply(pipeline)
    return my_sum(pipeline)

tree = invo_tree.blocking()
import types
tree.to_string[types.GeneratorType]  = lambda x: 'generator' # short name for generators
tree.to_string[type(iter(range(0)))] = lambda x: 'iterator'  # short name for iterator
print( tree(main) )
```
![generator_pipeline.gif](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/generator_pipeline.gif)
```
144
```
Note that the generators are lazy but the `sum()` function is not, and that is what is pulling the values through the pipeline one at the time.

## Itertools ##
The pythonic (or idiomatic) way of programming in Python is not to use raw for-loops but to use iterables, generators and [itertools](https://docs.python.org/3/library/itertools.html) functions instead. See for a short introduction:

[![Idiomatic Python: The `itertools` Module](https://img.youtube.com/vi/guEDsBshGfI/maxresdefault.jpg)](https://www.youtube.com/watch?v=guEDsBshGfI)

Whenever you write a for-loop, finish it and make it work correctly, but afterwards see of if you can rewrite it with generators and itertools functions. Then in time you will find you can think in terms of generators and itertools from the start. This can make your code shorter, more expressive, easier to change, use less memory, faster, and generally more correct.

# Configuration #
These invocation_tree configurations are available for an `Invocation_Tree` objects:

```python
tree = invo_tree.Invocation_Tree()
```

- **tree.filename** : str  
  - filename to save the tree to, defaults to 'tree.pdf'
- **tree.show** : bool
  - if `True` the default application is open to view 'tree.filename'
- **tree.block** :  bool
  - if `True` program execution is blocked after the tree is saved
- **tree.src_loc** : bool
  - if `True` the source location is printed when blocking
- **tree.each_line** : bool
  - if `True` each line of the program is stepped through
- **tree.max_string_len** : int
  - the maximum string length, only the end is shown of longer strings 
- **tree.gifcount** : int
  - if `>=0` the out filename is numbered for animated gif making
- **tree.indent** : string
  - the string used for identing the local variables
- **tree.color_active** : string
  - HTML color for active function 
- **tree.color_paused*** : string
  - HTML color for paused functions
- **tree.color_returned***: string
  - HTML color for returned functions
- **tree.hide** : set()
  - set of all variables names that are not shown in the tree
- **tree.to_string** : dict[str, fun]
  - mapping from type/name to a to_string() function for custom printing of values

For convenience we provide these functions to set common configurations:

- **invo_tree.blocking(filename)**, blocks on function call and return
- **invo_tree.blocking_each_change(filename)**, blocks on each change of value
- **invo_tree.debugger(filename)**, non-blocking for use in debugger tool (open &lt;filename&gt; manually)
- **invo_tree.gif(filename)**, generates many output files on function call and return for gif creation
- **invo_tree.gif_each_change(filename)**, generates many output files on each change of value for gif creation
- **invo_tree.non_blocking(filename)**, non-blocking on each function call and return

# Troubleshooting #
- Adobe Acrobat Reader [doesn't refresh a PDF file](https://superuser.com/questions/337011/windows-pdf-viewer-that-auto-refreshes-pdf-when-compiling-with-pdflatex) when it changes on disk and blocks updates which results in an `Could not open 'somefile.pdf' for writing : Permission denied` error. One solution is to install a PDF reader that does refresh ([Evince](https://www.fosshub.com/Evince.html), [Okular](https://okular.kde.org/), [SumatraPDF](https://www.sumatrapdfreader.org/), ...) and set it as the default PDF reader. Another solution is to save the tree to a different [Graphviz Output Format](https://graphviz.org/docs/outputs/).

## Memory_Graph Package ##
The [invocation_tree](https://pypi.org/project/invocation-tree/) package visualizes function calls at different moments in time. If instead you want a detailed visualization of your data at the current time, check out the [memory_graph](https://pypi.org/project/memory-graph/) package.
