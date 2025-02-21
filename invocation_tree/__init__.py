# This file is part of invocation_tree.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

from graphviz import Digraph
import html
import sys
#import inspect
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

    def __init__(self, output_filename='invocation_tree.pdf', show=True, block=True, src_location=True, max_string_len=100, indent='   ',
                 color_paused = '#ccffcc', color_active = '#ffffff', color_returned = '#ffcccc', each_line=False, 
                 to_string=None, hidden=None):
        # --- config
        self.output_filename = output_filename
        self.show = show
        self.output_count = -1
        self.block = block
        self.src_location = src_location
        self.max_string_len = max_string_len
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
        
    def print_stack(self):
        for tree_node in self.stack:
            print(tree_node)

    def value_to_string(self, key, value, use_repr=False):
        if id(value) in self.to_string:
            val_str = self.to_string[id(value)](value)
        elif key in self.to_string:
            val_str = self.to_string[key](value)
        elif type(value) in self.to_string:
            val_str = self.to_string[type(value)](value)
        else:
            val_str = repr(value) if use_repr else str(value)
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
            if len(content.strip())>0: # graphviz error on empty <B></B> tag
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
        function_name = tree_node.frame.f_code.co_name
        local_vars = tree_node.frame.f_locals
        return_value = tree_node.return_value
        border = 1
        color = self.color_paused
        if active:
            color = self.color_active
            border = 3
        if is_returned:
            color = self.color_returned
        table = f'<\n<TABLE BORDER="{str(border)}" CELLBORDER="0" CELLSPACING="1" BGCOLOR="{color}">\n  <TR>'
        hightlighted_content = self.get_hightlighted_content(tree_node, '__function_name__', function_name, use_old_content)
        table += '<TD ALIGN="left">'+ hightlighted_content +'</TD>'
        for var,val in local_vars.items():
            var_name = function_name+'..'+var
            val_name = function_name+'.'+var
            if not '__' in var and not val_name in self.hidden:
                table += '</TR>\n  <TR>'
                hightlighted_var = self.get_hightlighted_content(tree_node, var_name, var, use_old_content)
                hightlighted_val = self.get_hightlighted_content(tree_node, val_name, val, use_old_content, use_repr=True)
                hightlighted_content = self.indent + hightlighted_var + ': ' + hightlighted_val
                table += '<TD ALIGN="left">'+ hightlighted_content  +'</TD>'
        if is_returned:
            return_name = function_name+'.return'
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
        if self.output_count >= 0:
            splits = self.output_filename.split('.')
            if len(splits)>1:
                splits[-2]+=str(self.output_count)
                self.output_count += 1
                return '.'.join(splits)
        return self.output_filename
        
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
                if self.show:
                    graph.view()
                else:
                    graph.render(outfile=self.get_output_filename(), cleanup=False)
                if self.src_location:
                    filename = frame.f_code.co_filename
                    line_nr = frame.f_lineno
                    print(f'{event.capitalize()} at {filename}:{line_nr}', end='. ')
                    input('Press <Enter> to continue...')
        else:
            if self.show:
                graph.view()
            else:
                graph.render(outfile=self.get_output_filename(), cleanup=False)
        self.is_highlighted = False
        self.update_nodes_log_prev = self.update_nodes_log
        self.update_nodes_log = {}

    def trace_calls(self, frame, event, arg):
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
    
    def __call__(self, fun, *args, **kwargs):
        sys.settrace(self.trace_calls)
        try:
            result = fun(*args, **kwargs)
        except Exception as e:
            raise
        finally:
            sys.settrace(None)
        return result
