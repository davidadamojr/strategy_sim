
class ValueEngine:
    
    def __init__(self, graph, init_value):
        self.value_map = value_table = { node: init_value for (node, _) in graph.graph_dict.iteritems()}