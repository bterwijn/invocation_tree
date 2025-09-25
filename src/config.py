# Some useful invocation_tree configuration examples.
# Step through this file to see the effects.

def funC():
    x = 3

def funB():
    x = 2
    funC()

def funA():
    x = 1
    funB()
    
funA()

ivt_tree.hide_vars.add('funA.x')     # hide variable 'x' in funA
funA()

ivt_tree.hide_vars.add(r're:.*\.x')  # hide all variable 'x' with regex
funA()

ivt_tree.hide_calls.add('funB')      # hide function call
funA()

ivt_tree.ignore_calls.add('funB')    # ignore function call (including children)
funA()

lst = [1, 2, 3]
# change how type 'list' is shown in the tree:
ivt_tree.to_string[list] = lambda v : '|'.join(str(i) for i in v)
# there is a bug somewhere that introduces extra white spaces, I will look into that
lst.append(4)
