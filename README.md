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

Each node in the tree represents a function call, and its color indicates its current state:

 - White: The function is currently being executed (it is at the top of the call stack).
 - Green: The function is paused and will resume execution later (it is lower on the call stack).
 - Red: The function has completed execution and returned (it has been removed from the call stack).

For every function, the package displays its **local variables** and **return value**. Changes to these values over time are highlighted using bold text and gray shading to make them easy to track.

## Blocking ##
The program blocks execution at every function call and return statement, printing the current location in the source code. Press the &lt;Enter&gt; key to continue execution. To block at every line of the program (like a debugger) where a change of value occured, use instead:

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
An invocation tree is particularly useful to better understand recursion. A simple factorial example:

```python
import invocation_tree as invo_tree

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

tree = invo_tree.blocking()
tree(factorial, 4) # calls factorial(4)
```
![factorial](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/factorial.gif)

This permutations examples shows the depth-first nature of recursive execution:

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
result = tree(permutations, ['L','R'], '', 3)
print(result)
```
![permutations](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/permutations.gif)
