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
import invocation_tree as ivt

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

tree = ivt.blocking()
print( tree(main) ) # show invocation tree starting at main
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
import invocation_tree as ivt
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
    tree = ivt.blocking()
    tree(main)
```
![students](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/students.gif)
```
['Ann', 'Coy']
```

## Blocking ##
The program blocks execution at every function call and return statement, printing the current location in the source code. Press the &lt;Enter&gt; key to continue execution. To block at every line of the program (like in a debugger tool) and only where a change of value occured, use instead:

```python
    tree = ivt.blocking_each_change()
```

# Debugger #
To visualize the invocation tree in a debugger tool, such as the integrated debugger in Visual Studio Code, use instead:

```python
    tree = ivt.debugger()
```

and open the 'tree.pdf' file manually.
![Visual Studio Code debugger](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/vscode.png)

# Recursion #
An invocation tree is particularly helpful to better understand recursion. A simple `factorial()` example:

```python
import invocation_tree as ivt

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

tree = ivt.blocking()
print( tree(factorial, 4) ) # show invocation tree of calling factorial(4)
```
![factorial](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/factorial.gif)
```
24
```

This `permutations()` example shows the depth-first nature of recursive execution:

```python
import invocation_tree as ivt

def permutations(elements, perm, n):
    if n==0:
        return [perm]
    all_perms = []
    for element in elements:
        all_perms.extend(permutations(elements, perm + element, n-1))
    return all_perms

tree = ivt.blocking()
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
tree = ivt.blocking()
tree.hide.add('permutations.elements')
tree.hide.add('permutations.element')
tree.hide.add('permutations.all_perms')
```

# Configuration #
These invocation_tree configurations are available for an `Invocation_Tree` objects:

```python
tree = ivt.Invocation_Tree()
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

- **ivt.blocking(filename)**, blocks on function call and return
- **ivt.blocking_each_change(filename)**, blocks on each change of value
- **ivt.debugger(filename)**, non-blocking for use in debugger tool (open &lt;filename&gt; manually)
- **ivt.gif(filename)**, generates many output files on function call and return for gif creation
- **ivt.gif_each_change(filename)**, generates many output files on each change of value for gif creation
- **ivt.non_blocking(filename)**, non-blocking on each function call and return

# Troubleshooting #
- Adobe Acrobat Reader [doesn't refresh a PDF file](https://superuser.com/questions/337011/windows-pdf-viewer-that-auto-refreshes-pdf-when-compiling-with-pdflatex) when it changes on disk and blocks updates which results in an `Could not open 'somefile.pdf' for writing : Permission denied` error. One solution is to install a PDF reader that does refresh ([Evince](https://www.fosshub.com/Evince.html), [Okular](https://okular.kde.org/), [SumatraPDF](https://www.sumatrapdfreader.org/), ...) and set it as the default PDF reader. Another solution is to save the tree to a different [Graphviz Output Format](https://graphviz.org/docs/outputs/).

## Memory_Graph Package ##
The [invocation_tree](https://pypi.org/project/invocation-tree/) package visualizes function calls at different moments in time. If instead you want a detailed visualization of your data at the current time, check out the [memory_graph](https://pypi.org/project/memory-graph/) package.
