
def random_graph(num_nodes, terminals=10, loops=15, max_out_degree=3):
    graph = {}

    # initialize nodes
    for i in range(num_nodes):
        graph[str(i)] = set([])

    # make straight line path through graph
    for node in graph:
        if int(node) < num_nodes - 1:
            graph[node].add(str(int(node)+1))

    print graph

random_graph(10)