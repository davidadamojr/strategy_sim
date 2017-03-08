import json
import random
import math
from FrequencyEngine import FrequencyEngine
from ValueEngine import ValueEngine
from GraphGenerator import random_graph

def explore(graph, strategy):
    total_events = graph.get_num_nodes() - 1
    
    testcases = set([])

    selection_strategy = SELECTION_STRATEGIES[strategy]
    covered_events = set([])
    covered_count = 0
    test_case_count = 0
    while covered_count < total_events:
        testcase = []
        last_event = "0"
        available_events = ["0"]
        while available_events:
            home_event = last_event + "/home"
            if (random.random() < 0.05):
                selected_event = home_event
            else:
                selected_event = selection_strategy(available_events)

            if selected_event not in covered_events and selected_event != home_event:
                covered_count = covered_count + 1
                covered_events.add(selected_event)
            testcase.append(selected_event)

            if selected_event == home_event:
                break

            last_event = selected_event
            available_events = graph.get_available_events(selected_event)

        testcase = tuple(testcase)
        if testcase not in testcases:
            testcases.add(testcase)
            test_case_count = test_case_count + 1

    return testcases

def random_selection(available_events):
    return random.choice(available_events)

def min_frequency_selection(available_events):
    return frequency_engine.min_frequency_selection(available_events)
    
def linear_weighted_selection(available_events):
    return frequency_engine.weighted_selection(available_events, FrequencyEngine.LINEAR)

def sigmoid_weighted_selection(available_events):
    return frequency_engine.weighted_selection(available_events, FrequencyEngine.SIGMOID)

def sigmoid_min_weighted_selection(available_events):
    return frequency_engine.sigmoid_min_weighted_selection(available_events)

def check_all_nodes_reachable(graph):
    def depth_first_search(start_node, target):
        node_stack = [start_node]
        visited = set([])
        while node_stack:
            current_node = node_stack.pop()
            visited.add(current_node)
            if current_node == target:
                # print "Reached target node: {}".format(target)
                return True

            for neighbor in graph[current_node]:
                if neighbor not in visited:
                    node_stack.append(neighbor)

        print "Could not reach target node: {}".format(target)
        return False


    for node in sorted(graph.keys()):
        found = depth_first_search("0", node)
        if not found:
            return False
    
    return True

SELECTION_STRATEGIES = {
    'random' : random_selection,
    'min_frequency' : min_frequency_selection,
    'linear_weighted' : linear_weighted_selection,
    'sigmoid_weighted' : sigmoid_weighted_selection,
    'sigmoid_min_weighted' : sigmoid_min_weighted_selection
}

if __name__ == "__main__":
    import numpy
    
    raw_data = {}
    init_value = 1.0

    experiment_strategies = ["random", "min_frequency", "linear_weighted", "sigmoid_weighted", "sigmoid_min_weighted"]
    
    n = 100
    
    trials = 0
    while trials < n:
        loops = random.randrange(1, 100)
        max_out_degree = random.randrange(2, 50)
        terminals = random.randrange(10, 100)
        graph = random_graph(random.randrange(500, 1000), terminals=terminals, loops=loops, max_out_degree=max_out_degree)
        frequency_engine = FrequencyEngine(graph)
        # value_engine = ValueEngine(graph, init_value)
        if check_all_nodes_reachable(graph.get_graph()):
            print "Trial {} with {} nodes, {}% possibility of loops, {} max out degree and {}% possibility of terminals".format(trials, graph.get_num_nodes(), loops, max_out_degree, terminals)
            for strategy in experiment_strategies:
                testsuite_length = len(explore(graph, strategy))
                if strategy in raw_data:
                    raw_data[strategy].append(testsuite_length)
                else:
                    raw_data[strategy] = [testsuite_length]
            
            trials = trials + 1
        else:
            print "Bad graph."

    print "\nAverage test suite length"
    print "========================="
    for exp_strategy, data in raw_data.iteritems():
        print "{} : {}".format(exp_strategy, numpy.mean(data))
        
    print "\nMedian test suite length"
    print "========================"
    for exp_strategy, data in raw_data.iteritems():
        print "{} : {}".format(exp_strategy, numpy.median(data))
        
    print "\nStandard deviation"
    print "=================="
    for exp_strategy, data in raw_data.iteritems():
        print "{} : {}".format(exp_strategy, numpy.std(data))

    # check_all_nodes_reachable(graph)

#     graph_file.close()