# ydot

`ydot` compiles a `yaml` format to [`dot`](https://www.graphviz.org/doc/info/lang.html),
the graph desciption language employed by [graphviz](https://graphviz.org).

All graphs that can be described in plain `dot` shall be describable in the
`ydot` format, but with a more productive interface.


## Why?

- Cleaner code
    - Less redundancy
    - More overview
    - Fewer braces
- [Faster development](https://en.wikipedia.org/wiki/Notation_for_differentiation#Newton's_notation)
    - Rapid prototyping
    - Tight iteration loop
    - Central configuration


## How?

- Separate graph description from style declaration (optionally in separate files)
- Separate source code flow from graph structure
- Inheritance (via prototypes) for Nodes, Edges, Subgraphs, and entire Graphs
- Sane label formatting


## Example:

```yaml
# petersen_graph.yaml
petersen_graph:
    nodes:
        - a
        - b
        - c
        - d
        - e
    edges:
        - 'a -- b'
        - 'b -- c'
        - 'c -- d'
        - 'd -- e'
        - 'e -- a'

# style.yaml
graph_base:
    typ: graph
    config:
        nodesep: '1'

node_base:
    config: 
        shape: 'circle'
        fixedsize: 'true'
        height: '2'
        width: '7'
        penwidth: '2'
        style: 'filled'
        fillcolor: '#ffffff'
        color: '#000000'
        fontname: 'acme'
        fontsize: '28'

edge_base:
    config: 
        penwidth: '2'
        arrowsize: '1.5'
        color: 'black'

# Makefile
.PHONY: all
all: petersen_graph.pdf petersen_graph.svg

%.pdf: %.yaml style.yaml
    bash -ic "ydot $< > $<.dot && cat $<.dot | dot -Tpdf:cairo -o $@"

%.svg: %.yaml style.yaml
    bash -ic "ydot $< > $<.dot && cat $<.dot | dot -Tsvg:cairo -o $@"
```


## Get started

```bash
sudo apt update
sudo apt -y install graphviz
sudo apt -y install python3-pip
pip3 install -r requirements.txt --user
```
