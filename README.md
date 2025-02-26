# Installation #
Install (or upgrade) `invocation_tree` using pip:
```
pip install --upgrade invocation_tree
```
Additionally [Graphviz](https://graphviz.org/download/) needs to be installed.

# Invocation Tree #
The [invocation_tree](https://pypi.org/project/invocation-tree/) package is designed to help with **program understanding and debugging** by visualizing the **tree of function invocations** that occur during program execution. Here’s an example of how it works:

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
![invocation tree](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/students.gif)

Each node in the tree represents a function call, and the node's color indicates its state:

 - White: The function is currently being executed (it is at the top of the call stack).
 - Green: The function is paused and will resume execution later (it is lower down on the call stack).
 - Red: The function has completed execution and returned (it has been removed from the call stack).

For every function, the package displays its **local variables** and **return value**. Changes to these values over time are highlighted using bold text and gray shading to make them easy to track.

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
print(result) # all permutations of going Left and Right of length 2
```
![permutations](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/permutations.gif)

## Hide Variables ##
In an educational context it can be useful to hide certian variables to avoid unnecessary complexity. This can for example be done with:

```python
tree = invo_tree.blocking()
tree.hide.add('permutations.elements')
tree.hide.add('permutations.element')
tree.hide.add('permutations.all_perms')
```
# Generators #
An invocation tree is also helpful to see how the order in which a pipeline of Iterables and generators gets evaluated.

```python
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
    pipeline = Source(start=1, stop=3) # Iterable, produces values: 1, 2
    pipeline = double(pipeline)        # generator, doubles values
    pipeline = (-i for i in pipeline)  # generator expression, makes negative
    pipeline = just_print(pipeline)    # generator, just prints values
    return sum(pipeline)               # sums the values

tree = invo_tree.blocking()
tree.to_string[types.GeneratorType] = lambda gen: 'generator' # short name
print('sum:', tree(main))
```
![generators](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/generator.gif)
Resulting in the output:

```
just print: -2
just print: -4
sum: -6
```

# Configuration #
These configuration settings are available for an `Invocation_Tree` objects:

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
  - HTML color name for active function 
- **tree.color_paused*** : string
  - HTML color name for paused functions
- **tree.color_returned***: string
  - HTML color name for returned functions
- **tree.hide** : set()
  - set of all variables names that are not shown in the tree
- **tree.to_string** : dict[str, fun]
  - mapping from type/name to a to_string() function for custom printing of values

For convenience we provide these functions to set common configurations:

- **invo_tree.blocking(filename)**, blocks on function call and return
- **invo_tree.blocking_each_change(filename)**, blocks on each change of value
- **invo_tree.debugger(filename)**, for use in debugger tool (open &lt;filename&gt; manually)
- **invo_tree.gif(filename)**, generates many output files on function call and return for gif creation
- **invo_tree.gif_each_change(filename)**, generates many output files on each change of value for gif creation

# Troubleshooting #
- Adobe Acrobat Reader [doesn't refresh a PDF file](https://superuser.com/questions/337011/windows-pdf-viewer-that-auto-refreshes-pdf-when-compiling-with-pdflatex) when it changes on disk and blocks updates which results in an `Could not open 'somefile.pdf' for writing : Permission denied` error. One solution is to install a PDF reader that does refresh ([Evince](https://www.fosshub.com/Evince.html), [Okular](https://okular.kde.org/), [SumatraPDF](https://www.sumatrapdfreader.org/), ...) and set it as the default PDF reader. Another solution is to save the tree to a different [Graphviz Output Format](https://graphviz.org/docs/outputs/).

## Memory_Graph Package ##
The [invocation_tree](https://pypi.org/project/invocation-tree/) package visualizes function calls at different moments in time. If instead you want a detailed visualization of your data at the current time, check out the [memory_graph](https://pypi.org/project/memory-graph/) package.

# Author #
Bas Terwijn

# Inspiration #
Inspired by [rcviz](https://github.com/carlsborg/rcviz).

# Supported by #
<img src="https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/uva.png" alt="University of Amsterdam" width="600">
