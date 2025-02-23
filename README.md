# Installation #
Install (or upgrade) `invocation_tree` using pip:
```
pip install --upgrade invocation_tree
```
Additionally [Graphviz](https://graphviz.org/download/) needs to be installed.

# Invocation Tree #
For program understanding and debugging, the [invocation_tree](https://pypi.org/project/invocation-tree/) package visualizes function invocations, that results from program execution, as tree. Each node represents a function call, and its color indicates its state: 

 - white: function currently being executed (top of call stack)
 - green: paused function that will execute later (on call stack)
 - red: function that has returned (removed from call stack)

For each function we show each local variable and indicate changes in value with **bold** and gray highligthing. An example:

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
    tree = invo_tree.blocking(filename="students.png")
	tree(main) # show invocation tree from main
```
![many_types.png](https://raw.githubusercontent.com/bterwijn/invocation_tree/main/images/students.gif)
