# Installation #
Install (or upgrade) `invocation_tree` using pip:
```
pip install --upgrade invocation_tree
```
Additionally [Graphviz](https://graphviz.org/download/) needs to be installed.

# Highlights #
![permutations_vscode](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/permutations_vscode.gif)
Run a live demo in the 👉 [**Invocation Tree Web Debugger**](https://invocation-tree.com/#timestep=0.5&play) 👈 now, no installation required!

- shows the invocation tree (call tree) of a program **in real time**
- helps to **understand recursion** and its depth-first nature

# Topics #

[Iteration and Recursion](#iteration-and-recursion)

[Permutations](#permutations)

[Recursion Benefits](#recursion-benefits)

[Path Planning](#path-planning)

[Collecting Results](#collecting-results)

[Quick Sort](#quick-sort)

[Jugs Puzzle](#jugs-puzzle)

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


# Iteration and Recursion #

Repetion can be implemented with **iteration** and **recursion**. As an example we compute the factorial of 4.

``` python
import math

print(math.factorial(4))
```
```
24
```
The result is computed with repeated multiplication: `1 * 2 * 3 * 4 = 24`.

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

Or we can use recursion, a function that calls itself. Then we also need a **base case** as **stop condition** to prevent the function from calling itself indefinitely, like so:

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

This logic is evaluate as:
```
factorial(4) = 4 * factorial(3)
             = 4 * 3 * factorial(2)
             = 4 * 3 * 2 * factorial(1)
             = 4 * 3 * 2 * 1
             = 4 * 3 * 2
             = 4 * 6
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

to graph the function invocations. Run this program and press &lt;Enter&gt; to step through program execution.

![factorial](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/factorial.gif)

Or see it in the [Invocation Tree Web Debugger](https://www.invocation-tree.com/#codeurl=https://raw.githubusercontent.com/bterwijn/invocation_tree/refs/heads/main/src/factorial.py&play).

Each node in the invocation tree represents a function call, and the node's color indicates its state:

 - White: The function is currently being executed.
 - Green: The function is paused and will resume execution later.
 - Red: The function has completed execution and has returned.

For every function call, the package displays its **local variables** and **return value**. Changes to the values of these variables over time are highlighted using bold text and gray shading to make them easier to track.

With recursion we often use a divide and conquer strategy, spliting the problem in subproblems that are easier to solve. With factorial we split `factorial(4)` in a `4` and `factorial(3)` subproblem.

**exercise1:** Use recursions to compute the sum of all the values in a list (hint: split for example the list `[1, 2, 3, ...]` in head `1` and tail `[2, 3, ...]`).
```python
def sum(values):
    # <your recursive implementation>

print(sum([3, 7, 4, 9, 2]))  # 25
```

**exercise2:** Rewrite this iterative implementation of decimal to binary conversion to a recursive implementation.

```python
def binary(decimal):
    bin = []
    while decimal > 0:
        decimal, remainder = divmod(decimal, 2)
        bin = [remainder] + bin
    return bin

print( binary(22) )  # [1, 0, 1, 1, 0]
```

Checking that `[1, 0, 1, 1, 0]` is the correct binary repsentation for decimal 22:

|       | 2<sup>4</sup> | 2<sup>3</sup> | 2<sup>2</sup> | 2<sup>1</sup> | 2<sup>0</sup> |               |
|------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
| value |      16       |       8       |       4       |       2       |       1       |
| bits  |       1       |       0       |       1       |       1       |       0       |
| contrib |    +16      |       0       |      +4       |      +2       |       0       | =22


In some functional and logical programming languages (e.g. Haskell, Prolog) there are no loops so there only is recursion to implement repetition, but in Python we have a choice between recursion and iteration. Generally iteration is chosen in Python as it is often faster and many find it easier to understand. However, in some situations recursion comes with great benefits so it's important to master both ways.

# Permutations #

We can use recursion to compute all permutation of a number of elements with replacement (each element can be used any number of times). All permutations of length 3 of elements 'L' and 'R' can be made by moving down a tree for 3 steps and going **L**eft and **R**ight at each step:

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
tree(permutations, 'LR', '', 3)  # all permutations of L and R of length 3
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

# Recursion Benefits #

The benefit recursion brings is that it gives us more control over which permutations are generated. For example, if we don't want neighboring elements to be equal in all permutatations of 'A', 'B' and 'C' then we could simply write:

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
tree(permutations, 'ABC', '', 3)  # all permutations of A, B, C of length 3 without equal neigbors
```
This generates all permutation but without equal neighors like `AAB`:
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

With recursion we can stop neighbors from being equal early, in contrast to iteration, where we would have had to filter out a permutation with equal neighbors after it was fully generated, which could be much slower and would require a more complex program.

**exercise3:** Print all permutations with replacements of elements 'A', 'B', and 'C' of length 5 that are palindrome ('ABABA' is palindrome because if you read it backwards it's the same).

# Path Planning #

A graph is defined by nodes, which we name with letters, and edges that define the connections between nodes. For example edge `('a', 'j')` defines that there is a connection between node `a` and node `j`. In a bidirectional graph a connection betweeen two nodes can be used in both directions, from `a` to `j` and from `j` to `a`.

We define a bidirectional graph by a list of edges:
```
edges =  [('a', 'j'), ('f', 'j'), ('c', 'e'), ('b', 'd'), ('b', 'e'), ('f', 'g'),
          ('g', 'i'), ('h', 'i'), ('e', 'h'), ('a', 'i'), ('b', 'h'), ('b', 'f')]
```
that can be visualized as:

![graph_small](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/graph_small.png)

To print all the paths from `a` to `b` without going over the same node twice, we can use this recursive implementation:

```python
edges =  [('a', 'j'), ('f', 'j'), ('c', 'e'), ('b', 'd'), ('b', 'e'), ('f', 'g'),
          ('g', 'i'), ('h', 'i'), ('e', 'h'), ('a', 'i'), ('b', 'h'), ('b', 'f')]

def edges_to_connections(edges: list[tuple[str, str]]) -> dict[str,list[str]]:
    """ Returns a dict with for each node the nodes it is connected with. """
    connections = {}
    for n1, n2 in edges:
        if not n1 in connections:
            connections[n1] = []
        connections[n1].append(n2)
        if not n2 in connections:
            connections[n2] = []
        connections[n2].append(n1)
    return connections

def print_all_paths(connections, path, goal):
    current = path[-1]  # last node in path is the current node
    if current == goal:
        print(path)
    else:
        valid_connections = connections[current]  # get nodes connected to current
        for n in valid_connections:
            if n not in path:  # don't use same node twice
                print_all_paths(connections, path + n, goal)

connections = edges_to_connections(edges)
print_all_paths(connections, 'a', 'b')
```
```
ajfgiheb
ajfgihb
ajfb
aigfbaihb
aiheb
aihb
```
See it in the [Invocation Tree Web Debugger](https://www.invocation-tree.com/#codeurl=https://raw.githubusercontent.com/bterwijn/invocation_tree/refs/heads/main/src/print_paths_1.py&breakpoints=30&continues=1&timestep=0.5&play)

This would be much harder to implement with iteration and shows the power of recursion.

## Debug Prints ##

Adding temporarely debug print statements is in general a good technique to understand code, and is particularly helpful with recursion. Here we added a debug print statement when adding and removing a node from the path. As a result we can now in the output see how all paths are build step by step:

See it in the [Invocation Tree Web Debugger](https://www.invocation-tree.com/#codeurl=https://raw.githubusercontent.com/bterwijn/invocation_tree/refs/heads/main/src/print_paths_print_1.py&breakpoints=33&continues=1&timestep=0.2&play)

Add temporary debug prints wherever behavior isn’t clear. Experiment with what and how you print to maximize clarity.

**exercise4:** In this larger bidirectional graph, print all the paths of length 7 that connect node `a` to node `b` where going over the same node multiple times is allowed (`avjxbxb` is one such path, there are 114 such paths in total).

```python
edges =  [('a', 's'), ('i', 'z'), ('c', 'p'), ('d', 'p'), ('d', 'u'), ('b', 'e'), ('b', 'g'),
          ('f', 'p'), ('g', 'm'), ('h', 't'), ('h', 'y'), ('i', 'w'), ('i', 'j'), ('i', 'x'),
          ('k', 's'), ('k', 'l'), ('a', 'm'), ('n', 'u'), ('a', 'o'), ('a', 'v'), ('n', 'p'),
          ('a', 'q'), ('a', 'h'), ('p', 'r'), ('l', 's'), ('t', 'v'), ('u', 'y'), ('j', 'v'),
          ('a', 'j'), ('r', 'w'), ('r', 'u'), ('f', 'x'), ('x', 'y'), ('j', 'x'), ('d', 'j'),
          ('b', 'k'), ('b', 'x'), ('b', 'w')]
```
![graph_big.png)](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/graph_big.png)

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
<!-- ![permutations_return](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/permutations_return.gif) -->
See it in the [Invocation Tree Web Debugger](https://www.invocation-tree.com/#codeurl=https://raw.githubusercontent.com/bterwijn/invocation_tree/refs/heads/main/src/permutations_return.py&timestep=0.5&play)

However, sometimes it is easier to pass a list (or any other mutable container type) as an extra argument in the recursion to collect the results in. This is also faster because now just one list is used instead of each function call having to create its own `results` list.

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

<!-- ![permutations_collect](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/permutations_collect.gif) -->
See it in the [Invocation Tree Web Debugger](https://www.invocation-tree.com/#codeurl=https://raw.githubusercontent.com/bterwijn/invocation_tree/refs/heads/main/src/permutations_collect.py&timestep=0.5&play)

**exercise5:** Create a list with all paths of length 10 in the larger bidirectional graph that go from `a` to `b`, and that do go via `d` but do **not** go via `x` (`amajdjaskb` is one such path, there are 145 such paths in total).

Where is the best place in the code to test for `x` to make the program run fast?

```python
edges =  [('a', 's'), ('i', 'z'), ('c', 'p'), ('d', 'p'), ('d', 'u'), ('b', 'e'), ('b', 'g'),
          ('f', 'p'), ('g', 'm'), ('h', 't'), ('h', 'y'), ('i', 'w'), ('i', 'j'), ('i', 'x'),
          ('k', 's'), ('k', 'l'), ('a', 'm'), ('n', 'u'), ('a', 'o'), ('a', 'v'), ('n', 'p'),
          ('a', 'q'), ('a', 'h'), ('p', 'r'), ('l', 's'), ('t', 'v'), ('u', 'y'), ('j', 'v'),
          ('a', 'j'), ('r', 'w'), ('r', 'u'), ('f', 'x'), ('x', 'y'), ('j', 'x'), ('d', 'j'),
          ('b', 'k'), ('b', 'x'), ('b', 'w')]
```
![graph_big_d_x.png)](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/graph_big_d_x.png)

# Quick Sort #

Another nice example of divide-and-conquer is the recursive quicksort algorithm. It works by choosing a pivot element and dividing the list into elements smaller than the pivot and elements larger than the pivot. Each of these sublists is then quicksorted in the same way. When we get to the point a sublist has zero or one element, it is already sorted. When returning, these sorted sublists are then combined with the pivot to produce a larger sorted lists. Here we use the return value to get the sorted result.

```python
import invocation_tree as ivt

def quick_sort(values):
    if len(values) <= 1:
        return values
    pivot = values[0]  # choose arbitrarity the first as pivot
    smaller = [x for x in values if x  < pivot]
    equal   = [x for x in values if x == pivot]
    larger  = [x for x in values if x  > pivot]
    return quick_sort(smaller) + equal + quick_sort(larger)

values = [7, 4, 10, 11, 2, 6, 9, 1, 5, 3,  8, 12]
print('unsorted values:',values)
tree = ivt.blocking()
values = tree(quick_sort, values)
print('  sorted values:',values)
```
```
unsorted values: [7, 4, 10, 11, 2, 6, 9, 1, 5, 3, 8, 12]
  sorted values: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
```
<!-- ![quick_sort](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/quick_sort.gif) -->
See it in the [Invocation Tree Web Debugger](https://www.invocation-tree.com/#codeurl=https://raw.githubusercontent.com/bterwijn/invocation_tree/refs/heads/main/src/quick_sort.py&timestep=0.5&play)

**exercise6:** Rewrite this quick sort program so that we can pass in a list to collect the sorted result and we don't need to use a return value. This would make the program faster as it avoids having to use the `+` list concatenation operator that creates a new list each time we use it, whereas `+=` or `append()` only add to an existing list.

# Jugs Puzzle #

In the Jugs Puzzle we have a set of jugs of various capacities. Our goal is to get a jug with a certain amount of liquid in it. In each step we can take one of these actions:

- fill one jug until it is full
- empty one jug until it is empty
- pour from jug A to jug B until A is empty or B is full

![jugs.png](images/jugs.png)

In the first puzzle instance we have a jug with `3` liter capacity, a jug with `5` liter capacity, and our goal is to get to a jug with `4` liters in it. We already have a breadth-first algorithm that solves this puzzle:

- [jugs.py](https://raw.githubusercontent.com/bterwijn/invocation_tree/refs/heads/main/src/jugs.py)
- [jugs_bread_first.py](https://raw.githubusercontent.com/bterwijn/invocation_tree/refs/heads/main/src/jugs_breadth_first.py)

If we run this code we get a solution:
```
$ python jugs_breadth_first.py 4 3,5
Goal is to get a jug with 4 liters.
We start with jugs: 0/3 0/5
generation0:  [0/3 0/5]
0/3 0/5 (0, 3) -> 3/3 0/5
0/3 0/5 (1, 5) -> 0/3 5/5
generation1:  [3/3 0/5, 0/3 5/5]
3/3 0/5 (0, 1, 3) -> 0/3 3/5
3/3 0/5 (1, 5) -> 3/3 5/5
0/3 5/5 (1, 0, 3) -> 3/3 2/5
generation2:  [0/3 3/5, 3/3 5/5, 3/3 2/5]
0/3 3/5 (0, 3) -> 3/3 3/5
3/3 2/5 (0, -3) -> 0/3 2/5
generation3:  [3/3 3/5, 0/3 2/5]
3/3 3/5 (0, 1, 2) -> 1/3 5/5
0/3 2/5 (1, 0, 2) -> 2/3 0/5
generation4:  [1/3 5/5, 2/3 0/5]
1/3 5/5 (1, -5) -> 1/3 0/5
2/3 0/5 (1, 5) -> 2/3 5/5
generation5:  [1/3 0/5, 2/3 5/5]
1/3 0/5 (0, 1, 1) -> 0/3 1/5
2/3 5/5 (1, 0, 1) -> 3/3 4/5
=== solution:
0/3 0/5  -  Fill jug 1 with 5
0/3 5/5  -  Pour 3 from jug 1 to jug 0
3/3 2/5  -  Empty jug 0 with -3
0/3 2/5  -  Pour 2 from jug 1 to jug 0
2/3 0/5  -  Fill jug 1 with 5
2/3 5/5  -  Pour 1 from jug 1 to jug 0
3/3 4/5  -
```

Where:
- `0/3` represents a jug with `0` liter content and `3` liter capacity.
- `(0, 3)` represents the action of taking jug at index `0` and filling it with `3` liters
- `(0, 1, 2)` represents the action of pouring `2` liters from jug at index `0` to jug at index `1`

The breadth-first algorithm works and gives us the shortest path to a goal state, but to do that it uses a lot of memory to store each generation and all jugs states it has seen. Now we also want an algorithm that uses much less memory.

**exercise7:** Write a recursive solver for the Jugs Puzzle that uses less memory by searching for the solution in a depth-first manner.

- A solution may not have the same jugs state multiple times (this also avoids infinite loops).
- It is not necessary to find the shortest path to a goal state (like breadth-first does).

If you want to use the Invocation Tree Web Debugger, you can look at these [configuration examples](https://invocation-tree.com/#codeurl=https://raw.githubusercontent.com/bterwijn/invocation_tree/refs/heads/main/src/config.py) to keep the tree small and readable.

**solution exercise7:** First try it yourself, we give the [solution](https://www.invocation-tree.com/#codeurl=https://raw.githubusercontent.com/bterwijn/invocation_tree/refs/heads/main/src/jugs_depth_first.py&breakpoints=136&continues=1) here for comparison.

A harder more fun instance of this puzzle is with jugs with capacity 3, 5, 34 and 107 liter and the goal of getting to a jug with 51 liters.

```
$ python jugs_breadth_first.py 51 3,5,34,107
```

# Configuration #
The Invocation Tree Web Debugger gives examples of the [most important configurations](https://invocation-tree.com/#codeurl=https://raw.githubusercontent.com/bterwijn/invocation_tree/refs/heads/main/src/config.py).

## Hidding ##
It can be useful to hide certian variables or functions to avoid unnecessary complexity. This can be done with:

```python
tree = ivt.blocking()
tree.hide_vars.add('functionname.variablename')  # or:
tree.hide_vars.add('namespace.functionname.variablename')
```

Or hide certain function calls:

```python
tree = ivt.blocking()
tree.hide_calls.add('functionname')  # or:
tree.hide_calls.add('namespace.functionname')
```

Or ignore certain function calls so that all it's children are hidden too:

```python
tree = ivt.blocking()
tree.ignore_calls.add('namespace.functionname')
```

With the `re:` prefix we can use regular expresssions, for example:

```python
tree = ivt.blocking()
tree.ignore_calls.add(r're:namespace\..*')
```

ignores all function of `namespace`.

## Blocking ##

For convenience we provide these functions to set common configurations:

- **ivt.blocking(filename)**, blocks on function call and return
- **ivt.blocking_each_change(filename)**, blocks on each change of value
- **ivt.debugger(filename)**, non-blocking for use in debugger tool (open &lt;filename&gt; manually)
- **ivt.gif(filename)**, generates many output files on function call and return for gif creation
- **ivt.gif_each_change(filename)**, generates many output files on each change of value for gif creation
- **ivt.non_blocking(filename)**, non-blocking on each function call and return

To visualize the invocation tree in a debugger tool, such as the integrated debugger in Visual Studio Code, use:

```python
tree = ivt.debugger()
tree(som_function, arg1, arg2)
```
and open the 'tree.pdf' file in the local directory manually.
![Visual Studio Code debugger](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/vscode.png)


## Details ##
More detailed configurations can be set on an `Invocation_Tree` objects:

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
- **tree.to_string** : dict[str, fun]
  - mapping from type/name/id to a to_string() function for custom printing of values
- **tree.hide_vars** : set()
  - set of all variables names that are not shown in the tree
- **tree.hide_calls** : set()
  - set of all functions names that are not shown in the tree
- **tree.ignore_calls** : set()
  - set of all functions names that are not shown in the tree, including its children

# Troubleshooting #
- Adobe Acrobat Reader [doesn't refresh a PDF file](https://community.adobe.com/t5/acrobat-reader-discussions/reload-refresh-pdfs/td-p/9632292) when it changes on disk and blocks updates which results in an `Could not open 'tree.pdf' for writing : Permission denied` error. One solution is to install a PDF reader that does refresh ([SumatraPDF](https://www.sumatrapdfreader.org/), [Okular](https://okular.kde.org/),  ...) and set it as the default PDF reader. Another solution is to `render()` the graph to a different output format.

## Memory_Graph Package ##
The [invocation_tree](https://pypi.org/project/invocation-tree/) package visualizes function calls at different moments in time. If instead you want a detailed visualization of your data at the current time, check out the [memory_graph](https://pypi.org/project/memory-graph/) package.
