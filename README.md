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
import math 

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
    return my_round(average, 1)
    
def my_round(value, digits=0):
    shift = 10 ** digits
    return math.floor(value * shift + 0.5) / shift

def passing_students(avg):
    return [student 
        for student, average in avg.items() 
        if average >= 5.5]

if __name__ == '__main__':
    tree = invo_tree.blocking()
    tree(main) # show invocation tree starting at main
```
![invocation tree](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/students.gif)

Each node in the tree represents a function call, and node's color indicates its state:

 - White: The function is currently being executed (it is at the top of the call stack).
 - Green: The function is paused and will resume execution later (it is lower down on the call stack).
 - Red: The function has completed execution and returned (it has been removed from the call stack).

For every function, the package displays its **local variables** and **return value**. Changes to these values over time are highlighted using bold text and gray shading to make them easy to track.

The [invocation_tree](https://pypi.org/project/invocation-tree/) package visualizes function calls at different moments in time. If you want a more detailed visualization of your data at the current time, check out the [memory_graph](https://pypi.org/project/memory-graph/) package.

## Blocking ##
The program blocks execution at every function call and return statement, printing the current location in the source code. Press the &lt;Enter&gt; key to continue execution. To block at every line of the program (like in a debugger tool) where a change of value occured, use instead:

```python
    tree = invo_tree.blocking_each_line()
```

# Debugger #
To visualize the invocation tree in a debugger tool, such as the integrated debugger in Visual Studio Code, use instead:

```python
    tree = invo_tree.debugger()
```

and open the 'tree.pdf' file manually.
![Visual Studio Code debugger](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/vscode.png)

# Recursion #
An invocation tree is particularly useful to better understand recursion. A simple `factorial()` example:

```python
import invocation_tree as invo_tree

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

tree = invo_tree.blocking()
tree(factorial, 4) # show invocation tree of calling factorial(4)
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

## Hide variables ##
In an educational context it can be useful to hide certian variables to avoid unnecessary complexity. This can for example be done with:

```python
tree = invo_tree.blocking()
tree.hide.add('permutations.elements')
tree.hide.add('permutations.element')
tree.hide.add('permutations.all_perms')
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

- **invo_tree.blocking()**, for blocking on function call and return
- **invo_tree.blocking_each_line()**, for blocking on each line of the program
- **invo_tree.debugger()**, for use in debugger tool (open 'tree.pdf') manually
- **invo_tree.gif(filename)**, for generating many output files on function call and return for gif creation
- **invo_tree.gif_each_line(filename)**, for generating many output files on each line for gif creation

# Troubleshooting #

- Adobe Acrobat Reader [doesn't refresh a PDF file](https://superuser.com/questions/337011/windows-pdf-viewer-that-auto-refreshes-pdf-when-compiling-with-pdflatex) when it changes on disk and blocks updates which results in an `Could not open 'somefile.pdf' for writing : Permission denied` error. One solution is to install a PDF reader that does refresh ([Evince](https://www.fosshub.com/Evince.html), [Okular](https://okular.kde.org/), [SumatraPDF](https://www.sumatrapdfreader.org/), ...) and set it as the default PDF reader. Another solution is to save the tree to a different [Graphviz Output Format](https://graphviz.org/docs/outputs/).
