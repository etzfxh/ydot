#!/usr/bin/env python3

import os
import sys
import yaml

from frontend import parse_graph, parse_style
from backend import compile_graph


USAGE = '''
Usage:
$ ydot PATH
'''


def get_path_graph():
    current_working_directory = os.getcwd()
    try:
        fname_graph = sys.argv[1]
    except IndexError:
        print(USAGE)
        sys.exit()
    path_graph = os.path.join(current_working_directory, fname_graph)
    return path_graph

def get_path_style():
    current_working_directory = os.getcwd()
    default_style_directory = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'style')
    fname_style = 'style.yaml'
    path_style_custom = os.path.join(current_working_directory, fname_style)
    path_style_default = os.path.join(default_style_directory, fname_style)
    if os.path.isfile(path_style_custom):
        return path_style_custom
    if os.path.isfile(path_style_default):
        return path_style_default
    raise FileNotFoundError('Error: No style file found.')

def load_yaml(path):
    with open(path) as f:
        the_yaml = yaml.safe_load(f)
    return the_yaml

def load_graph(path):
    return load_yaml(path)

def load_style(path):
    style = load_yaml(path)
    for key in ['graph_base', 'node_base', 'edge_base']:
        assert key in style, 'Error: No %s in the style file.' % key
    return style

def ydot():
    graph_raw = load_graph(get_path_graph())
    style = parse_style(load_style(get_path_style()))
    graph = parse_graph(graph_raw, style)
    dot = compile_graph(graph)
    print(dot)


if __name__ == '__main__':
    ydot()
