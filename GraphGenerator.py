import random 

class Graph:
    def __init__(self, graph_dict):
        self.graph_dict = graph_dict
    
    # given a set of events in a previous node and the set of events in the current node
    # return the set of events that are in the current node but not in the previous node
    def get_new_events(self, previous_events, available_events):
        previous_events = set(previous_events)
        available_events = set(available_events)
        
        return list(available_events - previous_events)
    
    def get_num_nodes(self):
        return len(self.graph_dict.keys())
    
    def get_available_events(self, current_node):
        return self.graph_dict[current_node]
    
    def get_graph(self):
        return self.graph_dict
    
    

def select_neighbors(graph, node, node_choices, max_out_degree):
    while len(graph[node]) <= max_out_degree:
        neighbor = random.choice(node_choices)
        graph[node].add(neighbor)
    
    
def random_graph(num_nodes, terminals=10, loops=15, max_out_degree=3):
    graph = {}
    terminal_probability = float(terminals) / 100
    loop_probability = float(loops)/ 100

    # initialize nodes
    for i in range(num_nodes):
        graph[str(i)] = set([])

    # make straight line path through graph
    for node in graph:
        if int(node) < num_nodes - 1:
            graph[node].add(str(int(node)+1))
    
    all_nodes = sorted(graph.keys())
    
    for node in all_nodes:
        if node == "0":
            select_neighbors(graph, node, all_nodes[1:], max_out_degree)
            continue
            
        if random.random() < loop_probability:
            graph[node].add(node)
            select_neighbors(graph, node, all_nodes[1:], max_out_degree)
        elif random.random() < terminal_probability:
            graph[node].add(str(len(graph.keys())))
            graph[str(len(graph.keys()))] = set([])
            if len(graph[node]) == 1:
                complementary_node = random.choice(all_nodes[1:])
                graph[node].add(complementary_node)
            select_neighbors(graph, node, all_nodes[1:], max_out_degree)
        else:
            select_neighbors(graph, node, all_nodes[1:], max_out_degree)
    
    # convert graph dict values to lists instead of sets
    for node in graph:
        graph[node] = list(graph[node])
        
    return Graph(graph)