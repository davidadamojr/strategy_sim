import math 
import random

class FrequencyEngine:
    
    LINEAR = "linear"
    SIGMOID = "sigmoid"
    
    def __init__(self, graph):
        self.freq_map = { node:0 for (node, _) in graph.graph_dict.iteritems()}
        
    def get_frequency(self, event):
        return self.freq_map[event]
    
    def min_frequency_selection(self, available_events):
        min_frequency = float('inf')
        candidates = []
        for event in available_events:
            event_frequency = self.get_frequency(event)
            if event_frequency < min_frequency:
                candidates[:] = []
                candidates.append(event)
                min_frequency = event_frequency
            elif event_frequency == min_frequency:
                candidates.append(event)
        
        selected_event = random.choice(candidates)
        self.freq_map[selected_event] += 1
        
        return selected_event
    
    def weighted_selection(self, available_events, weight_type):
        # get total weight
        weight_dict = {}
        total_weight = 0.0
        for event in available_events:
            event_frequency = self.freq_map[event]
            if weight_type == FrequencyEngine.LINEAR:
                event_weight = 1.0 / (1 + event_frequency)
            elif weight_type == FrequencyEngine.SIGMOID:
                event_weight = 1.0 / math.exp(math.log(event_frequency + 0.1))
            weight_dict[event] = event_weight 
            
            total_weight = total_weight + event_weight
        
        expected_weight = random.random() * total_weight
        weight_sum = 0.0
        selected_event = available_events[0]
        for event in available_events:
            weight_sum = weight_sum + weight_dict[event]
            if weight_sum >= expected_weight:
                self.freq_map[event] += 1
                return event
        
        self.freq_map[selected_event] += 1
        return selected_event 
    
    def sigmoid_min_weighted_selection(self, available_events):
        candidates = []
        for event in available_events:
            if self.freq_map[event] == 0:
                candidates.append(event)
        
        if candidates:
            selected_event = random.choice(candidates)
            self.freq_map[selected_event] += 1
            return selected_event
        
        return self.weighted_selection(available_events, FrequencyEngine.SIGMOID)
                
            
    
    