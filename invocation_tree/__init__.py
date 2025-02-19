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
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            result.append(f"<B>{str1[i1:i2]}</B>")
        elif tag == 'delete':
            result.append(f"--")
        elif tag == 'insert':
            result.append(f"<B>{str2[j1:j2]}</B>")
        elif tag == 'equal':
            result.append(str1[i1:i2])
    return ''.join(result)

class Tree_Node:

    def __init__(self, node_id, frame, return_value):
        self.node_id = node_id
        self.frame = frame
        self.return_value = return_value
        self.strings = {}

    def __repr__(self):
        return f'node_id:{self.node_id} frame:{self.frame} return_value:{self.return_value}'

class Invocation_Tree:

    def __init__(self, output_filename='invocation_tree.pdf', block=True, src_location=True, max_string_len=100, indent='   ',
                 color_paused = '#ccffcc', color_active = '#ffffff', color_returned = '#ffcccc', each_line=False, to_string=None):
        # --- config
        self.output_filename = output_filename
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
        # --- core
        self.stack = []
        self.node_id = 0
        self.node_id_to_table = {}
        self.edges = []
        
    def print_stack(self):
        for tree_node in self.stack:
            print(tree_node)

    def value_to_string(self, value, name):
        if id(value) in self.to_string:
            return self.to_string[id(value)](value)
        elif name in self.to_string:
            return self.to_string[name](value)
        elif type(value) in self.to_string:
            return self.to_string[type(value)](value)
        else:
            val_str = str(value)
            if len(val_str) > self.max_string_len:
                val_str = '...'+val_str[-self.max_string_len:]    
            return html.escape(val_str)

    def build_html_table(self, tree_node, active=False, returned=False):
        function_name = tree_node.frame.f_code.co_name
        local_vars = tree_node.frame.f_locals
        return_value = tree_node.return_value
        border = 1
        color = self.color_paused
        if active:
            color = self.color_active
            border = 3
        if returned:
            color = self.color_returned
        table = f'<\n<TABLE BORDER="{str(border)}" CELLBORDER="0" CELLSPACING="1" BGCOLOR="{color}">\n  <TR>'
        content = self.value_to_string(function_name, 'function_'+function_name)
        table += '<TD ALIGN="left">'+ content +'</TD>'
        tree_node.strings['__function_name__'] = content
        for var,val in local_vars.items():
            if not '__' in var:
                table += '</TR>\n  <TR>'
                content = self.indent + self.value_to_string(var, function_name+'_'+var) + ': ' + \
                                        self.value_to_string(val, function_name+'.'+var)
                table += '<TD ALIGN="left">'+ content  +'</TD>'
                tree_node.strings[var] = content
        if returned:
            table += '</TR>\n  <TR>'
            content = self.value_to_string(return_value, function_name+'.'+'return')
            table += '<TD ALIGN="left">'+ 'return ' + content +'</TD>'
            tree_node.strings['return'] = content
        table += '</TR>\n</TABLE>>'
        return table
            
    def update_node(self, tree_node, active=False, returned=False):
        table = self.build_html_table(tree_node, active, returned)
        self.node_id_to_table[str(tree_node.node_id)] = table
        
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
        
    def render_graph(self, frame, event):
        graphviz_graph_attr = {}
        graphviz_node_attr = {'shape':'plaintext'}
        graphviz_edge_attr = {}
        graph = Digraph(comment="recursion_graph",
                graph_attr=graphviz_graph_attr,
                node_attr=graphviz_node_attr,
                edge_attr=graphviz_edge_attr)
        for nid, table in self.node_id_to_table.items():
            graph.node(nid, label=table)
        for nid1, nid2 in self.edges:
            graph.edge(nid1, nid2)
        graph.render(outfile=self.get_output_filename(), cleanup=True)
        if self.block:
            if self.src_location:
                filename = frame.f_code.co_filename
                line_nr = frame.f_lineno
                print(f'{event.capitalize()} at {filename}:{line_nr}', end='. ')
            input('Press <Enter> to continue...')
            
    def trace_calls(self, frame, event, arg):
        #print('========= event:',event)
        if event == 'call':
            self.stack.append(Tree_Node(self.node_id, frame, None))
            self.node_id += 1
            #self.print_stack()
            if len(self.stack)>1:
                self.update_node(self.stack[-2])
                self.add_edge(self.stack[-2], self.stack[-1])
            self.update_node(self.stack[-1], active=True)
            self.render_graph(frame, event)
        elif event == 'return':
            self.stack[-1].return_value = arg
            #self.print_stack()
            self.update_node(self.stack[-1], returned=True)
            if len(self.stack)>1:
                self.update_node(self.stack[-2], active=True)
            self.stack.pop()
            self.render_graph(frame, event)
        elif event == 'line' and self.each_line:
            self.update_node(self.stack[-1], active=True)
            self.render_graph(frame, event)
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
