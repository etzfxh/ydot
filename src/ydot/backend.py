#!/usr/bin/env python3

SINGLE_INDENT = 4 * ' '

GRAPH = '''\
{typ} {name} {{
{config}
{nodes}
{subgraphs}
{edges}
}}'''

SUBGRAPH = '''
{indent}subgraph {name} {{
{config}
{nodes}
{subgraphs}
{edges}
{indent}}}'''

NODE = '''
{indent}node [{config}]
{indent}{name} [label="{label}"]'''

EDGE = '''
{indent}edge [{config}]
{indent}{name} [label="{label}"]'''


def dict_to_str(the_dict, separator, level):
    line_template = (level * SINGLE_INDENT) + '{key}="{value}"'
    return separator.join([
        line_template.format(key=key, value=value)
        for key, value in sorted(the_dict.items())])

def compile_graph(graph):
    for key in ['typ', 'name', 'config', 'nodes', 'subgraphs', 'edges']:
        assert key in graph, 'Error: No %s in the graph.' % key
    code = GRAPH.format(
        typ=graph['typ'],
        name=graph['name'],
        config=dict_to_str(graph['config'], '\n', level=1),
        nodes='\n'.join([
            compile_node(node, level=1) for node in graph['nodes']]),
        subgraphs='\n'.join([
            compile_subgraph(subgraph, level=1)
            for subgraph in graph['subgraphs']]),
        edges='\n'.join([
            compile_edge(edge, level=1) for edge in graph['edges']]))
    return code

def compile_node(node, level):
    [(name, body)] = node.items()
    for key in ['config', 'label']:
        assert key in body, 'Error: No %s in the node "%s".' % (key, name)
    code = NODE.format(
        config=dict_to_str(body['config'], ' ', level=0),
        name=name,
        label=body['label'],
        indent=level * SINGLE_INDENT)
    return code

def compile_edge(edge, level):
    [(name, body)] = edge.items()
    for key in ['config', 'label']:
        assert key in body, 'Error: No %s in the edge "%s".' % (key, name)
    code = EDGE.format(
        config=dict_to_str(body['config'], ' ', level=0),
        name=name,
        label=body['label'],
        indent=level * SINGLE_INDENT)
    return code

def compile_subgraph(subgraph, level):
    [(name, body)] = subgraph.items()
    for key in ['config', 'nodes', 'subgraphs', 'edges']:
        assert key in body, 'Error: No %s in the subgraph "%s".' % (key, name)
    code = SUBGRAPH.format(
        indent=level * SINGLE_INDENT,
        name=name,
        config=dict_to_str(body['config'], '\n', level=level+1),
        nodes='\n'.join([
            compile_node(node, level=level+1) for node in body['nodes']]),
        subgraphs='\n'.join([
            compile_subgraph(subsubgraph, level=level+1)
            for subsubgraph in body['subgraphs']]),
        edges='\n'.join([
            compile_edge(edge, level=level+1) for edge in body['edges']]))
    return code

def test_backend():
    graph = dict(
        typ='digraph',
        name='test',
        config=dict(
            rankdir='TD',
            nodesep='1',
            fontname='acme',
            fontsize=28,
            splines='ortho',
            penwidth=2,
            newrank='true',
            compound='true'),
        nodes=[
            {'fizz_buzz': dict(
                label='3 FIZZ BUZZ',
                config=dict(
                    fontname='acme',
                    fontsize=24,
                    fillcolor='white',
                    style='filled,rounded',
                    shape='box',
                    fixedsize='true',
                    width=3,
                    height=1,
                    labelloc='b'))}],
        subgraphs=[
            {'cluster_1': dict(
                config=dict(
                    label='\nBRRRRT',
                    labelloc='t',
                    margin=40,
                    style='filled',
                    fillcolor='lightgrey',
                    clusterrank='none',
                    ranksep='1 equally',
                    color='white'),
                subgraphs=[],
                nodes=[
                    {'foo_bar': dict(
                        label='1 FOO BAR',
                        config=dict(
                            fontname='acme',
                            fontsize=24,
                            fillcolor='white',
                            style='filled,rounded',
                            shape='box',
                            fixedsize='true',
                            width=3,
                            height=1,
                            labelloc='m'))
                    }, {
                    'baz': dict(
                        label='2 BAZ',
                        config=dict(
                            fontname='acme',
                            fontsize=24,
                            fillcolor='white',
                            style='filled,rounded',
                            shape='box',
                            fixedsize='true',
                            width=3,
                            height=1,
                            labelloc='t'))
                    }],
                edges=[
                    {'foobar -> baz': dict(
                        label='',
                        config={})}])
            }
        ],
        edges=[
            {'baz -> fizz_buzz': dict(
                label='',
                config={})}],
    )
    print(compile_graph(graph))


if __name__ == '__main__':
    test_backend()
