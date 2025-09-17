this page is under constructions, there may be inconsistencies or things missing

# Installation #
Install (or upgrade) `invocation_tree` using pip:
```
pip install --upgrade invocation_tree
```
Additionally [Graphviz](https://graphviz.org/download/) needs to be installed.

# Highlights #

```python
def permutations(elements, perm, n):
    if n == 0:
        print(perm)
    else:
        for element in elements:
            permutations(elements, perm + element, n-1)

permutations('LR', '', 3)
```
![permutations](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/permutations.gif)
Run a live demo in the 👉 [**Invocation Tree Web Debugger**](https://invocation-tree.com/#timestep=1.0&play) 👈 now, no installation required!

- shows the invocation tree (call tree) of a program **in real time**
- helps to **understand recursion** and its depth-first nature

# Chapters #

[Recursion and Iteration](#recursion-and-iteration)

[Permutations](#permutations)

[Permutations Benefits](#recursion-benefits)

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


# Recursion and Iteration #

Repetion can be implemented with recursion and iteration. Lets first look at simply computing the factorial of 4.

``` python
import math

print(math.factorial(4))
```
```
24
```
The result is `1 * 2 * 3 * 4 = 24`.

To implement our own factorial function we can use iteration, a for-loop or while-loop, like so:

```python
def factorial(n):
    result = 1
    for i in range(1, n+1):
        result *= i
    return result

print(factorial(4))
```
```
24
```

or we can use recursion, a function that calls itself. Then we also need a stop condition to prevent the function from calling itself indefinitely, like so:

```python
def factorial(n):
    if n <= 1:  # stop condition
        return 1
    return n * factorial(n - 1)  # function calling itself
print(factorial(4))
```
```
24
```

We can evaluate this as:
```
factorial(4) = 4 * factorial(3)
             = 4 * 3 * factorial(2)
             = 4 * 3 * 2 * factorial(1)
             = 4 * 3 * 2 * 1
             = 24
```

To better understand what is going on when we run the program we can use invocation_tree:

```python
import invocation_tree as ivt

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

tree = ivt.blocking()  # block and wait for <Enter> key press
tree(factorial, 4)     # call function 'factorial' with argument '4' 
```

to graph the function invocations. Press &lt;Enter&gt; to walk through each step of the repetition until the stop condition is met.

![factorial](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/factorial.gif)

Or see it in the [Invocation Tree Web Debugger](https://www.invocation-tree.com/#codeurl=https://raw.githubusercontent.com/bterwijn/invocation_tree/refs/heads/main/src/factorial.py).

Each node in the invocation tree represents a function call, and the node's color indicates its state:

 - White: The function is currently being executed.
 - Green: The function is paused and will resume execution later.
 - Red: The function has completed execution and has returned.

For every function call, the package displays its **local variables** and **return value**. Changes to the values of these variables over time are highlighted using bold text and gray shading to make them easier to track.

With recursion we often use a divide and conquer strategy, spliting the problem in subproblems that are easier to solve. With factorial we split `factorial(4)` in a `4` and `factorial(3)` subproblem.

**exerise1:** Use recursions to compute the sum of all the values in a list (hint: split for example the list `[1,2,3,...]` in head `1` and tail `[2,3,...]`).
```python
def sum(values):
    # <your recursive implementation>

print(sum([3,7,4,9,2]))  # 25
```

**exerise2:** Rewrite this iterative implementation of a decimal to binary conversion to a recursive implementation.

```python
def binary(decimal):
    bin = []
    while decimal > 0:
        decimal, remainder = divmod(decimal, 2)
        bin = [remainder] + bin
    return bin

print( binary(22) )  # [1, 0, 1, 1, 0]
```

In some functional and logical programming languages (e.g. Haskell, Prolog) there are not loops so there is only recursion to implement repetition, but in Python we have a choice between recursion and iteration. Generally iteration is chosen in Python as it is often faster and many find it easier to understand. However, in some situation recursion comes with great benefits so it's important to master both ways.

# Permutations #

We can use recursion to compute all permutation of a number of elements with replacement (each element can be used any number of times). All permutations of length 3 of elements 'L' and 'R' can be made by moving down a tree for 3 steps and going Left and Right at each step:

![perms_LR3](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/perms_LR3.png)

This can be implemented recursively like:

```python
import invocation_tree as ivt

def permutations(elements, perm, n):
    if n == 0:       # stop condition, check if all steps are used up
        print(perm)
    else:
        for element in elements:                         # for each element
            permutations(elements, perm + element, n-1)  #   add it and do next step

tree = ivt.blocking()
tree(permutations, 'LR', '', 3)  # permutations of L and R of length 3
```
```
LLL
LLR
LRL
LRR
RLL
RLR
RRL
RRR
```
![permutations](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/permutations.gif)
Or see it in the [Invocation Tree Web Debugger](https://invocation-tree.com/#timestep=1.0&play)

The visualization shows the depth-first nature of recursion. In each step the first elements is chosen first, and quickly the bottom of the tree is reached. Then the permutation is printed, the function returns, one step back is made, and the next element is chosen. When each element had it's turn the function returns and another step back is made. This pattern repeats until all permutations are printed.

We can also iterate over all permutations with replacement using the `product()` function of `iterools` to get the same result:

```python
import itertools as it

for perm in it.product('LR', repeat = 3):
    print(perm)
```

# Recursion Benefit #

The benefit recursion brings is that it gives more control over which permutations are generated. For example, if we don't want neighboring elements to be equal in all permutatations of 'A', 'B' and 'C' then we could simply write:

```python
import invocation_tree as ivt

def permutations(elems, perm, n):
    if n == 0:
        print(perm)
    else:
        for element in elems:
            if len(perm) == 0 or not perm[-1] == element:  # test neighbor
                permutations(elems, perm + element, n-1)  

tree = ivt.blocking()
tree(permutations, 'ABC', '', 3)  # permutations of A, B, C of length 3
```
```
ABA
ABC
ACA
ACB
BAB
BAC
BCA
BCB
CAB
CAC
CBA
CBC
```
![permutations](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/permutations_neighbor.gif)
Or see it in the [Invocation Tree Web Debugger](https://www.invocation-tree.com/#codeurl=https://raw.githubusercontent.com/bterwijn/invocation_tree/refs/heads/main/src/permutations_neighbor.py)

This stops neighbors from being equal early, in contrast to iteration, where we would have had to filter permutation with equal neighbors out after the fact which could be much slower.

**exercise3:** Print all permutations with replacements of elements 'A', 'B', and 'C' of length 5 that are palindrome ('ABABA' is palindrome because if you read it backwards it's the same).

# Path Planning #

A graph is defined by nodes which we name with letters, and edges which define the connections between nodes. For example edge `('a', 'j')` defines tat there is a connection between node `a` and node `j`. In a bidirectional graph a connection betweeen two nodes can be used in both directions, from `a` to `j` and from `j` to `a`.

We define a bidirectional graph by a list of edges:
```
edges =  [('a', 'j'), ('f', 'j'), ('c', 'e'), ('b', 'd'), ('b', 'e'), ('f', 'g'), ('g', 'i'), ('h', 'i'), ('e', 'h'), ('a', 'i'), ('b', 'h'), ('b', 'f')]
```
that can be visualized as:

![permutations](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/graph_small.png)

To print all the paths from `a` to `b` without going over the same node twice, we can use this recursive implementation:

```python
edges =  [('a', 'j'), ('f', 'j'), ('c', 'e'), ('b', 'd'), ('b', 'e'), ('f', 'g'), ('g', 'i'), ('h', 'i'), ('e', 'h'), ('a', 'i'), ('b', 'h'), ('b', 'f')]

def edges_to_steps(edges: list[tuple[str, str]]) -> dict[str,list[str]]:
    """ Returns a dict with for each node the nodes it is connected with. """ 
    steps = {}
    for n1, n2 in edges:
        if not n1 in steps:
            steps[n1] = []
        steps[n1].append(n2)
        if not n2 in steps:
            steps[n2] = []
        steps[n2].append(n1)
    return steps

def print_all_paths(steps, path, goal):
    current = path[-1]
    if current == goal:
        print(path)
    else:
        valid_steps = steps[current]
        for s in valid_steps:
            if s not in path:  # don't use twice
                print_all_paths(steps, path+s, goal)

steps = edges_to_steps(edges)
print_all_paths(steps, 'a', 'b')
```
```
ajfgiheb
ajfgihb
ajfb
aigfb
aiheb
aihb
```
This would be much harder to implement with iteration and shows the power of recursion.

**exercise4:** In this larger bidirectional graph, print all the paths of length 7 that connect node `a` to node `b` where going over the same node multiple times is allowed (`avjxbxb` is one such path, there are 114 such paths in total).

```python
edges =  [('a', 's'), ('i', 'z'), ('c', 'p'), ('d', 'p'), ('d', 'u'), ('b', 'e'), ('b', 'g'), ('f', 'p'), ('g', 'm'), ('h', 't'), ('h', 'y'), ('i', 'w'), ('i', 'j'), ('i', 'x'), ('k', 's'), ('k', 'l'), ('a', 'm'), ('n', 'u'), ('a', 'o'), ('a', 'v'), ('n', 'p'), ('a', 'q'), ('a', 'h'), ('p', 'r'), ('l', 's'), ('t', 'v'), ('u', 'y'), ('j', 'v'), ('a', 'j'), ('r', 'w'), ('r', 'u'), ('f', 'x'), ('x', 'y'), ('j', 'x'), ('d', 'j'), ('b', 'k'), ('b', 'x'), ('b', 'w')]
```
![permutations](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/graph_big.png)

# Collecting Results #

If instead of printing we want to collect each result in a list for later use, we can use the return value of our recursive function, like in this example for our earlier permutation problem.

```python
import invocation_tree as ivt

def permutations(elements, perm, n):
    if n == 0:
        return [perm]
    else:
        results = []
        for element in elements:
            results += permutations(elements, perm + element, n-1)
        return results

tree = ivt.blocking()
print(tree(permutations, 'LR', '', 3))
```
```
['LLL', 'LLR', 'LRL', 'LRR', 'RLL', 'RLR', 'RRL', 'RRR']
```
![permutations_return](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/permutations_return.gif)
Or see it in the [Invocation Tree Web Debugger](https://www.invocation-tree.com/#codeurl=https://raw.githubusercontent.com/bterwijn/invocation_tree/refs/heads/main/src/permutations_return.py)

But often it is easier to pass a list (or other mutable container type) as an extra argument in the recursion to collect the results in. This can also be faster as it avoids many list copies as a result of the '+=' list concatenation.

```python
import invocation_tree as ivt

def permutations(elements, perm, n, results):
    if n == 0:
        results.append(perm)
    else:
        for element in elements:
            permutations(elements, perm + element, n-1, results)

tree = ivt.blocking()
results = []
tree(permutations, 'LR', '', 3, results)
print(results)
```
```
['LLL', 'LLR', 'LRL', 'LRR', 'RLL', 'RLR', 'RRL', 'RRR']
```

![permutations_collect](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/permutations_collect.gif)
Or see it in the [Invocation Tree Web Debugger](https://www.invocation-tree.com/#codeurl=https://raw.githubusercontent.com/bterwijn/invocation_tree/refs/heads/main/src/permutations_collect.py)


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



## Hidding ##
It can be useful to hide certian variables or functions to avoid unnecessary complexity. This can for example be done with:

```python
tree = ivt.blocking()
tree.hide_vars.add('permutations.elements')
tree.hide_vars.add('permutations.element')
tree.hide_vars.add('permutations.all_perms')
```

Or hide certain function calls:

```python
tree = ivt.blocking()
tree.hide_calls.add('namespace.functionname')
```

Or ignore certain function calls so that all it's children are hidden too:

```python
tree = ivt.blocking()
tree.ignore_calls.add('namespace.functionname')
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
- Adobe Acrobat Reader [doesn't refresh a PDF file](https://community.adobe.com/t5/acrobat-reader-discussions/reload-refresh-pdfs/td-p/9632292) when it changes on disk and blocks updates which results in an `Could not open 'somefile.pdf' for writing : Permission denied` error. One solution is to install a PDF reader that does refresh ([SumatraPDF](https://www.sumatrapdfreader.org/), [Okular](https://okular.kde.org/),  ...) and set it as the default PDF reader. Another solution is to `render()` the graph to a different output format and to open it manually.

## Memory_Graph Package ##
The [invocation_tree](https://pypi.org/project/invocation-tree/) package visualizes function calls at different moments in time. If instead you want a detailed visualization of your data at the current time, check out the [memory_graph](https://pypi.org/project/memory-graph/) package.
