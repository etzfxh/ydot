#!/usr/bin/env python3

from copy import deepcopy
import sys


def extend(d1, d2):
    '''
    For given dicts d1, d2, return a new dict d3 with the following properties:
    - d3 contains all keys that are in d1 or d2.
    - d3 contains a key named 'config', irrespecitve of whether or not this
        key is in d1 or d2. If 'config' is neither in d1 nor d2, then
        d3['config'] = {}. If 'config' is in d1 or d2, we assume its respective
        value is a dict.
    - Keys that are exclusively either in d1 or d2, keep their d1 or d2 values
        in d3 (including possibly the key 'config').
    - For each key k that is both in d1 and d2:
        - If k is not 'config', then d3[k] = d2[k]
        - If k is 'config', then the dict d3[k] is a copy of the dict d1[k],
            updated with all items from the dict d2[k].
    '''
    d3 = deepcopy(d1)
    for k, v in d2.items():
        if k != 'config':
            d3[k] = v
    if not 'config' in d1:
        d3['config'] = {}
    if 'config' in d2:
        for k, v in d2['config'].items():
            d3['config'][k] = v
    return d3

class Constructor(object):
    '''
    The motivation for this class is that any single constructor can be used
    only when all constructors have been created.
    '''
    def __init__(self, extendable):
        self.extendable = extendable

    def construct(self, extension, constructors):
        if not 'extends' in self.extendable:
            return extend(self.extendable, extension)
        parent_name = self.extendable['extends']
        return extend(
            constructors[parent_name].construct(
                self.extendable, constructors),
            extension)

def instantiate(extendable, constructors):
    if 'extends' in extendable:
        parent_name = extendable['extends']
        try:
            constructor = constructors[parent_name]
        except KeyError:
            print(
                'Error: No constructor defined for %s' % parent_name,
                file=sys.stderr)
            raise
        # @TODO: Maybe leave key 'extends' in, and ignore it downstream.
        instance = {
            k: v
            for k, v in constructor.construct(extendable, constructors).items()
            if k != 'extends'}
    else:
        instance = extendable
    if not 'config' in instance:
        instance['config'] = {}
    return instance

def parse_style(style_raw):
    style = {
        extendable_name: Constructor(extendable)
        for extendable_name, extendable in style_raw.items()}
    return style

def parse_node(node_raw, style):
    if isinstance(node_raw, str):
        name = node_raw
        body = {}
    else:
        [(name, body)] = node_raw.items()
    if not 'extends' in body:
        body['extends'] = 'node_base'
    body = instantiate(body, style)
    if not 'label' in body:
        body['label'] = name
    return {name: body}

def parse_edge(edge_raw, style):
    if isinstance(edge_raw, str):
        name = edge_raw
        body = {}
    else:
        [(name, body)] = edge_raw.items()
    if not 'extends' in body:
        body['extends'] = 'edge_base'
    body = instantiate(body, style)
    if not 'label' in body:
        body['label'] = ''
    return {name: body}

def parse_subgraph(subgraph_raw, style):
    [(name, body)] = subgraph_raw.items()
    body = instantiate(body, style)
    try:
        nodes_raw = body['nodes']
    except KeyError:
        print('Error: Each subgraph must have nodes.', file=sys.stderr)
        raise
    body['nodes'] = [parse_node(n, style) for n in nodes_raw]
    if 'edges' in body:
        body['edges'] = [
            parse_edge(e, style) for e in body['edges']]
    if 'subgraphs' in body:
        body['subgraphs'] = [
            parse_subgraph(s, style) for s in body['subgraphs']]
    else:
        body['subgraphs'] = []
    return {name: body}

def parse_graph(graph_raw, style):
    [(graph_name, graph_raw_body)] = graph_raw.items()
    if not 'extends' in graph_raw_body:
        graph_raw_body['extends'] = 'graph_base'
    graph = instantiate(graph_raw_body, style)
    if not 'typ' in graph:
        graph['typ'] = 'digraph'
    graph['name'] = graph_name
    # Expand the raw nodes.
    try:
        nodes_raw = graph_raw_body['nodes']
    except KeyError:
        print('Error: Each graph must have nodes.', file=sys.stderr)
        raise
    graph['nodes'] = [parse_node(n, style) for n in nodes_raw]
    # Expand the raw edges if there are any.
    if 'edges' in graph_raw_body:
        graph['edges'] = [
            parse_edge(e, style) for e in graph_raw_body['edges']]
    else:
        graph['edges'] = []
    # Expand the raw subgraphs if there are any.
    if 'subgraphs' in graph_raw_body:
        graph['subgraphs'] = [
            parse_subgraph(s, style) for s in graph_raw_body['subgraphs']]
    else:
        graph['subgraphs'] = []
    return graph

def test_frontend():
    import os
    from pprint import pprint
    import yaml
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, 'test', 'workflow.yaml')) as f:
        graph_raw = yaml.safe_load(f)
    with open(os.path.join(root, 'style', 'style.yaml')) as f:
        style = yaml.safe_load(f)
    graph = parse_graph(graph_raw, parse_style(style))
    pprint(graph)


if __name__ == '__main__':
    test_frontend()
