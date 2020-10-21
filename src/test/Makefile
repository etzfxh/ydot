.PHONY: all
all: test_minimum_viable_graph_file.pdf # test_empty_graph_file.pdf

%.pdf: %.yaml
	python3 ../ydot/ydot.py $^ > $^.dot && cat $^.dot | dot -Tpdf:cairo -o $@
