# This file is part of invocation_tree.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

from graphviz import Digraph
import html
import sys
import inspect
import difflib 

__version__ = "0.0.1"
__author__ = 'Bas Terwijn'

def highlight_diff(str1, str2):
    matcher = difflib.SequenceMatcher(None, str1, str2)
    result = []
    is_highlighted = False
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace' and j1+1<j2:
            result.append(f'<B>{str2[j1:j2]}&#8203;</B>&#8203;')
            is_highlighted = True
        elif tag == 'delete' and i1+1<i2:
            result.append(f'<FONT COLOR="#aaaaaa"><I>{str1[i1:i2]}&#8203;</I></FONT>&#8203;')
            is_highlighted = True
        elif tag == 'insert' and j1+1<j2:
            result.append(f'<B>{str2[j1:j2]}&#8203;</B>&#8203;')
            is_highlighted = True
        elif tag == 'equal':
            result.append(str2[j1:j2])
    diff = ''.join(result)
    return diff, is_highlighted

def get_class_function(frame):
    class_name = ''
    if 'self' in frame.f_locals:
        class_name = frame.f_locals['self'].__class__.__name__ + '.'
    function_name = class_name+frame.f_code.co_name
    return function_name

def filter_variables(var, val):
    if callable(val):
        return False
    if isinstance(val, (type, type(object), type(__import__('os')))):
        return False
    if var.startswith('__'):
        return False
    return True

class Tree_Node:

    def __init__(self, node_id, frame, return_value):
        self.node_id = node_id
        self.frame = frame
        self.return_value = return_value
        self.is_retured = False
        self.strings = {}

    def __repr__(self):
        return f'node_id:{self.node_id} frame:{self.frame} return_value:{self.return_value}'

class Invocation_Tree:

    def __init__(self, 
                 filename='tree.pdf', 
                 show=True, 
                 block=True, 
                 src_loc=True, 
                 each_line=False, 
                 outcount=-1,
                 max_string_len=150, 
                 indent='   ', 
                 color_paused = '#ccffcc', 
                 color_active = '#ffffff', 
                 color_returned = '#ffcccc', 
                 to_string=None, 
                 hidden=None):
        # --- config
        self.filename = filename
        self.prev_filename = None
        self.show = show
        self.block = block
        self.src_loc = src_loc
        self.max_string_len = max_string_len
        self.outcount = outcount
        self.indent = indent
        self.color_paused = color_paused
        self.color_active = color_active
        self.color_returned = color_returned
        self.each_line = each_line
        self.to_string = {}
        if not to_string is None:
            self.to_string = to_string
        self.hidden = set()
        if not hidden is None:
            self.hidden = hidden
        # --- core
        self.stack = []
        self.node_id = 0
        self.node_id_to_table = {}
        self.edges = []
        self.update_nodes_log = {}
        self.update_nodes_log_prev = {}
        self.is_highlighted = False
        self.ignore_calls = {'Invocation_Tree.__exit__', 'Invocation_Tree.stop_trace'}

    def __repr__(self):
        return f'Invocation_Tree(filename={repr(self.filename)}, show={self.show}, block={self.block}, each_line={self.each_line}, outcount={self.outcount})'

    def __enter__(self):
        frameInfo = inspect.stack()[1]
        self.stack.append(Tree_Node(self.node_id, frameInfo.frame, None))
        self.node_id += 1
        self.update_node_and_log(self.stack[-1], active=True)
        self.output_graph(frameInfo.frame, 'begin')
        sys.settrace(self.trace_calls)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_trace()
        self.update_node_and_log(self.stack[-1], active=True)
        self.stack.pop()
        frameInfo = inspect.stack()[1]
        self.output_graph(frameInfo.frame, 'end')

    def stop_trace(self):
        sys.settrace(None)

    def print_stack(self):
        for tree_node in self.stack:
            print(tree_node)

    def value_to_string(self, key, value, use_repr=False):
        try:
            if id(value) in self.to_string:
                val_str = self.to_string[id(value)](value)
            elif key in self.to_string:
                val_str = self.to_string[key](value)
            elif type(value) in self.to_string:
                val_str = self.to_string[type(value)](value)
            else:
                val_str = repr(value) if use_repr else str(value)
        except Exception as e:
            return '<I>not-string-convertable</I>'
        if len(val_str) > self.max_string_len:
            val_str = '...'+val_str[-self.max_string_len:]
        return html.escape(val_str)

    def get_hightlighted_content(self, tree_node, key, value, use_old_content=False, use_repr=False):
        if use_old_content:
            return tree_node.strings[key]
        is_highlighted = False
        content = self.value_to_string(key, value, use_repr=use_repr)
        if key in tree_node.strings:
            use_old_content = tree_node.strings[key]
            hightlighted_content, is_highlighted = highlight_diff(use_old_content, content)
        else:
            if len(content.strip())>0: # fixes graphviz error on empty <B></B> tag
                hightlighted_content = '<B>'+content+'</B>' 
                is_highlighted = True
            else:
                hightlighted_content = content
        tree_node.strings[key] = content
        self.is_highlighted |= is_highlighted
        return hightlighted_content
    
    def build_html_table(self, tree_node, active=False, is_returned=None, use_old_content=False):
        if is_returned is None:
            is_returned = tree_node.is_returned
        else:
            tree_node.is_returned = is_returned
        return_value = tree_node.return_value
        border = 1
        color = self.color_paused
        if active:
            color = self.color_active
            border = 3
        if is_returned:
            color = self.color_returned
        table = f'<\n<TABLE BORDER="{str(border)}" CELLBORDER="0" CELLSPACING="0" BGCOLOR="{color}">\n  <TR>'
        class_fun_name = get_class_function(tree_node.frame)
        local_vars = tree_node.frame.f_locals
        hightlighted_content = self.get_hightlighted_content(tree_node, class_fun_name, class_fun_name, use_old_content)
        table += '<TD ALIGN="left">'+ '➤'+ hightlighted_content +'</TD>'
        for var,val in local_vars.items():
            var_name = class_fun_name+'..'+var
            val_name = class_fun_name+'.'+var
            if filter_variables(var,val) and not val_name in self.hidden:
                table += '</TR>\n  <TR>'
                hightlighted_var = self.get_hightlighted_content(tree_node, var_name, var, use_old_content)
                hightlighted_val = self.get_hightlighted_content(tree_node, val_name, val, use_old_content, use_repr=True)
                hightlighted_content = self.indent + hightlighted_var + ': ' + hightlighted_val
                table += '<TD ALIGN="left">'+ hightlighted_content  +'</TD>'
        if is_returned:
            return_name = class_fun_name+'.return'
            if not return_name in self.hidden:
                table += '</TR>\n  <TR>'
                hightlighted_content = self.get_hightlighted_content(tree_node, return_name, return_value, use_old_content, use_repr=True)
                table += '<TD ALIGN="left">'+ 'return ' + hightlighted_content +'</TD>'
        table += '</TR>\n</TABLE>>'
        return table

    def update_node(self, tree_node, active=False, returned=None, use_old_content=False):
        table = self.build_html_table(tree_node, active, returned, use_old_content=use_old_content)
        self.node_id_to_table[str(tree_node.node_id)] = table
        
    def update_node_and_log(self, tree_node, active=False, returned=False):
        self.update_node(tree_node, active, returned)
        self.update_nodes_log[id(tree_node)] = tree_node

    def add_edge(self, tree_node1, tree_node2):
        self.edges.append((str(tree_node1.node_id), str(tree_node2.node_id)))

    def get_output_filename(self):
        if self.outcount >= 0:
            splits = self.filename.split('.')
            if len(splits)>1:
                splits[-2]+=str(self.outcount)
                self.outcount += 1
                return '.'.join(splits)
        return self.filename
        
    def render_graph(self, graph):
        view = (self.filename!=self.prev_filename) and self.show
        graph.render(outfile=self.get_output_filename(), cleanup=False, view=view)
        self.prev_filename = self.filename

    def output_graph(self, frame, event):
        for idn, node in {(k, v) for k, v in self.update_nodes_log_prev.items() 
                        if k not in self.update_nodes_log}:
            self.update_node(node, use_old_content=True) # TODO
        graphviz_graph_attr = {}
        graphviz_node_attr = {'shape':'plaintext'}
        graphviz_edge_attr = {}
        graph = Digraph('invocation_tree',
                graph_attr=graphviz_graph_attr,
                node_attr=graphviz_node_attr,
                edge_attr=graphviz_edge_attr)
        for nid, table in self.node_id_to_table.items():
            graph.node(nid, label=table)
        for nid1, nid2 in self.edges:
            graph.edge(nid1, nid2)
        if self.block:
            if self.is_highlighted:
                self.render_graph(graph)
                if self.src_loc:
                    filename = frame.f_code.co_filename
                    line_nr = frame.f_lineno
                    print(f'{event.capitalize()} at {filename}:{line_nr}', end='. ')
                    input('Press <Enter> to continue...')
        else:
            self.render_graph(graph)
        self.is_highlighted = False
        self.update_nodes_log_prev = self.update_nodes_log
        self.update_nodes_log = {}

    def trace_calls(self, frame, event, arg):
        class_fun_name = get_class_function(frame)
        if not class_fun_name in self.ignore_calls:
            if event == 'call':
                self.stack.append(Tree_Node(self.node_id, frame, None))
                self.node_id += 1
                if len(self.stack)>1:
                    self.update_node_and_log(self.stack[-2])
                    self.add_edge(self.stack[-2], self.stack[-1])
                self.update_node_and_log(self.stack[-1], active=True)
                self.output_graph(frame, event)
            elif event == 'return':
                self.stack[-1].return_value = arg
                self.update_node_and_log(self.stack[-1], returned=True)
                if len(self.stack)>1:
                    self.update_node_and_log(self.stack[-2], active=True)
                self.stack.pop()
                self.output_graph(frame, event)
            elif event == 'line' and self.each_line:
                self.update_node_and_log(self.stack[-1], active=True)
                self.output_graph(frame, event)
        return self.trace_calls

def blocking():
    return Invocation_Tree()

def blocking_each_line():
    return Invocation_Tree(each_line=True)

def debugger():
    return Invocation_Tree(show=False, block=False, each_line=True)

def gif():
    return Invocation_Tree(filename='tree.png', show=False, block=False, outcount=0)
