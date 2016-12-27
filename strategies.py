import json
import random
import math

# def get_all_events(graph):
#     all_events = set([])
#     for node in graph:
#         all_events.add(node)
#
#     # assert len(all_events) == 24
#     return all_events


def initialize_frequencies(graph):
    frequency_table = { node:0 for (node, _) in graph.iteritems()}
    return frequency_table


def initialize_values(graph):
    value_table = { node: 1.0 for (node, _) in graph.iteritems()}
    return value_table


def explore(graph, strategy):
    total_events = len(graph.keys()) - 1
    # print "Total number of events to cover: " + str(total_events)
    testcases = set([])

    frequency_table = initialize_frequencies(graph)
    value_table = initialize_values(graph)

    selection_strategy = SELECTION_STRATEGIES[strategy]
    covered_events = set([])
    covered_count = 0
    testcasecount = 0
    while covered_count < total_events:
    # while testcasecount < 15:
        testcase = []
        last_event = "0"
        available_events = graph["0"]
        while available_events:
            home_event = last_event + "/home"
            if (random.random() < 0.05):
                selected_event = home_event
            else:
                selected_event = selection_strategy(graph, available_events, frequency_table, value_table)
                # frequency_table[selected_event] = frequency_table[selected_event] + 1

            if selected_event not in covered_events and selected_event != home_event:
                covered_count = covered_count + 1
                covered_events.add(selected_event)
            testcase.append(selected_event)

            if selected_event == home_event:
                break

            last_event = selected_event
            available_events = graph[selected_event]

        testcase = tuple(testcase)
        if testcase not in testcases:
            # print testcase
            testcases.add(tuple(testcase))
            testcasecount = testcasecount + 1

    return testcases


def sigmoid_value_update(selected_event):
    pass

def random_selection(graph, available_events, frequency_table, value_table):
    return random.choice(available_events)


def rand_min_selection(graph, available_events, frequency_table, value_table):
    min_frequency = float("inf")
    candidates = []
    for event in available_events:
        event_frequency = frequency_table[event]
        if event_frequency < min_frequency:
            min_frequency = event_frequency
            candidates[:] = []
            candidates.append(event)
        elif event_frequency == min_frequency:
            candidates.append(event)

    selected_event = random.choice(candidates)
    frequency_table[selected_event] = frequency_table[selected_event] + 1

    return selected_event

def max_sigmoid_selection_max(ui_graph, available_events, frequency_table, value_table):
    max_value = 0
    candidates = []
    for event in available_events:
        event_value = value_table[event]
        if event_value > max_value:
            max_value = event_value
            candidates = []
            candidates.append(event)
        elif event_value == max_value:
            candidates.append(event)

    selected_event = random.choice(candidates)
    frequency_table[selected_event] = frequency_table[selected_event] + 1

    # update selected event value
    if not graph[selected_event]:
        value_table[selected_event] = 0
    else:
        next_events = ui_graph[selected_event]
        max_next = max(value_table[event] for event in next_events)
        event_frequency = frequency_table[selected_event]
        # try:
        value = 1.0 / (1 + math.exp(math.log(event_frequency)))
        # except:
        # value = float('inf')
        value_table[selected_event] = value

    return selected_event

def sigmoid_adjusted_midpoint(ui_graph, available_events, frequency_table, value_table):
    max_value = 0
    candidates = []
    for event in available_events:
        event_value = value_table[event]
        if event_value > max_value:
            max_value = event_value
            candidates = []
            candidates.append(event)
        elif event_value == max_value:
            candidates.append(event)

    selected_event = random.choice(candidates)
    frequency_table[selected_event] = frequency_table[selected_event] + 1

    # update selected event value
    if not graph[selected_event]:
        value_table[selected_event] = 0
    else:
        next_events = ui_graph[selected_event]
        event_frequency = frequency_table[selected_event]
        # try:
        value = 1.0 / (1 + math.exp(math.log(event_frequency) - math.log(len(next_events))))
        # except:
        # value = float('inf')
        value_table[selected_event] = value

    return selected_event


def sigmoid_adjusted_midpoint_and_nextdiscount(ui_graph, available_events, frequency_table, value_table):
    max_value = 0
    candidates = []
    for event in available_events:
        event_value = value_table[event]
        if event_value > max_value:
            max_value = event_value
            candidates = []
            candidates.append(event)
        elif event_value == max_value:
            candidates.append(event)

    selected_event = random.choice(candidates)
    frequency_table[selected_event] = frequency_table[selected_event] + 1

    # update selected event value
    if not graph[selected_event]:
        value_table[selected_event] = 0
    else:
        next_events = ui_graph[selected_event]

        max_pair = (0, None)
        candidates = []
        for event in next_events:
            event_value = value_table[event]
            if event_value > max_pair[0]:
                max_pair = (event_value, event)
                candidates[:] = []
                candidates.append(max_pair)
            elif event_value == max_pair[0]:
                pair = (event_value, event)
                candidates.append(pair)
        max_pair = random.choice(candidates)

        event_frequency = frequency_table[selected_event]
        # try:
        value = 1.0 / (1 + math.exp(math.log(event_frequency) - math.log(len(next_events))))
        # except:
        # value = float('inf')
        max_next_freq = frequency_table[max_pair[1]]
        max_next_value = value_table[max_pair[1]]
        discount_factor = 1.0 / (1 + math.exp(math.log(max_next_freq+2)))
        value_table[selected_event] = value + (discount_factor * max_next_value)

    return selected_event


def sigmoid_adjusted_midpoint_and_valuediscount(ui_graph, available_events, frequency_table, value_table):
    max_value = 0
    candidates = []
    for event in available_events:
        event_value = value_table[event]
        if event_value > max_value:
            max_value = event_value
            candidates = []
            candidates.append(event)
        elif event_value == max_value:
            candidates.append(event)

    selected_event = random.choice(candidates)
    frequency_table[selected_event] = frequency_table[selected_event] + 1

    # update selected event value
    if not graph[selected_event]:
        value_table[selected_event] = 0
    else:
        next_events = ui_graph[selected_event]
        event_frequency = frequency_table[selected_event]
        # try:
        value = 1.0 / (1 + math.exp(math.log(event_frequency) - math.log(len(next_events))))
        # except:
        # value = float('inf')
        max_next_value = max(value_table[event] for event in next_events)
        value_table[selected_event] = value + (value * max_next_value)

    return selected_event


def calculate_state_value(ui_graph, next_state_events, frequency_table, value_table):
    state_value = 0.0
    for event in next_state_events:
        event_frequency = frequency_table[event]
        event_sigmoid = 1.0 / (1 + math.exp(math.log(event_frequency+1)))
        state_value = state_value + event_sigmoid

    state_value = float(state_value) / len(next_state_events)

    return state_value

def full_value_selection(ui_graph, available_events, frequency_table, value_table):
    max_value = 0
    candidates = []
    for event in available_events:
        event_value = value_table[event]
        if event_value > max_value:
            max_value = event_value
            candidates = []
            candidates.append(event)
        elif event_value == max_value:
            candidates.append(event)

    selected_event = random.choice(candidates)
    frequency_table[selected_event] = frequency_table[selected_event] + 1

    # update selected event value
    if not graph[selected_event]:
        value_table[selected_event] = 0
    else:
        next_events = ui_graph[selected_event]

        max_pair = (0, None)
        candidates = []
        for event in next_events:
            event_value = value_table[event]
            if event_value > max_pair[0]:
                max_pair = (event_value, event)
                candidates[:] = []
                candidates.append(max_pair)
            elif event_value == max_pair[0]:
                pair = (event_value, event)
                candidates.append(pair)
        max_pair = random.choice(candidates)

        event_frequency = frequency_table[selected_event]
        # try:
        value = 1.0 / (1 + math.exp(math.log(event_frequency) - math.log(len(next_events))))
        # except:
        # value = float('inf')
        max_next_freq = frequency_table[max_pair[1]]
        max_next_value = value_table[max_pair[1]]
        discount_factor = 1.0 / (1 + math.exp(math.log(max_next_freq+2)))
        state_value = calculate_state_value(ui_graph, next_events, frequency_table, value_table)
        value_table[selected_event] = state_value + value + (discount_factor * max_next_value)

    return selected_event


def sigmoid_mid_selection(ui_graph, available_events):
    pass


def learned_rand_selection(ui_graph, available_events, frequency_table, value_table):
    non_zero_events = [event for event in available_events if value_table[event] > 0]
    selected_event = random.choice(non_zero_events)

    if not ui_graph[selected_event]:
        value_table[selected_event] = 0

    return selected_event


def weighted_selection(weight_table):
    pass


def check_all_nodes_reachable(graph):
    def depth_first_search(start_node, target):
        node_stack = [start_node]
        visited = set([])
        while node_stack:
            current_node = node_stack.pop()
            visited.add(current_node)
            if current_node == target:
                return "Found target node: {}".format(target)

            for neighbor in graph[current_node]:
                if neighbor not in visited:
                    node_stack.append(neighbor)

        return "Could not find target node: {}".format(target)


    for node in sorted(graph.keys()):
        print depth_first_search("0", node)

SELECTION_STRATEGIES = {
    'random' : random_selection,
    'min_frequency' : rand_min_selection,
    'max_sigmoid_max' : max_sigmoid_selection_max,
    'sigmoid_mid' : sigmoid_mid_selection,
    'learned_rand' : learned_rand_selection,
    'sigmoid_adjusted_midpoint' : sigmoid_adjusted_midpoint,
    'sigmoid_adjusted_midpoint_and_nextdiscount' : sigmoid_adjusted_midpoint_and_nextdiscount,
    'sigmoid_adjusted_midpoint_and_valuediscount' : sigmoid_adjusted_midpoint_and_valuediscount,
    'full_value_selection' : full_value_selection
}

if __name__ == "__main__":
    graph_file = open("loaned_graph_2.json", 'r')
    graph = json.load(graph_file)

    # print len(explore(graph, "max_sigmoid_average"))
    # print len(explore(graph, "max_sigmoid_max"))

    report = {}

    experiment_strategies = ["random", "min_frequency", "learned_rand", "max_sigmoid_max", "sigmoid_adjusted_midpoint", "sigmoid_adjusted_midpoint_and_nextdiscount",
                             "sigmoid_adjusted_midpoint_and_valuediscount", "full_value_selection"]
    for strategy in experiment_strategies:
        print "Testing strategy: {}".format(strategy)
        test_length_sum = 0
        n = 2000
        for _ in range(0, n):
            test_length_sum = test_length_sum + len(explore(graph, strategy))

        report[strategy] = float(test_length_sum) / n

    for exp_strategy, average_length in report.iteritems():
        print "{} : {}".format(exp_strategy, average_length)

    # check_all_nodes_reachable(graph)

    graph_file.close()