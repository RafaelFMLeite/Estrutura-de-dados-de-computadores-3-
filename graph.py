class Graph:
    def __init__(self):
        self.adj_list = {}
        self.party = {}
        self.votes = {}

    
    def add_node(self, node, party, votes):
        if node not in self.adj_list:
            self.adj_list[node] = {}
            self.party[node] = party
            self.votes[node] = votes

    
    def add_edge(self, node1, node2, votes):
        if node1 in self.adj_list and node2 in self.adj_list:
            self.adj_list[node1][node2] = votes

    
    def filter(self, parties):
        filtered_graph = Graph()

        for node, party in self.party.items():
            if party in parties:
                filtered_graph.add_node(node, party, self.votes[node])
                for neighbor, votes in self.adj_list[node].items():
                    filtered_graph.add_edge(node, neighbor, votes)
        
        return filtered_graph
    
    
    def normalize_edges(self, filtered_graph):
        normalized_graph = Graph()

        for node1, neighbors in filtered_graph.adj_list.items():
            normalized_graph.add_node(node1, filtered_graph.party[node1], filtered_graph.votes[node1])
            for node2, votes in neighbors.items():
                min_votes_uv = min(filtered_graph.votes[node1], filtered_graph.votes[node2])
                normalized_weight = filtered_graph.adj_list[node1][node2] / min_votes_uv
                normalized_graph.add_edge(node1, node2, normalized_weight)

        return normalized_graph
    
    
    def threshold(self, normalized_graph ,threshold_value):
        thresholded_graph = Graph()

        for node1, neighbors in normalized_graph.adj_list.items():
            thresholded_graph.add_node(node1, normalized_graph.party[node1], normalized_graph.votes[node1])
            for node2, votes in neighbors.items():
                if votes >= threshold_value:
                    thresholded_graph.add_edge(node1, node2, votes)

        return thresholded_graph
    
    def invert_weights(self, threshold_graph):
        inverted_graph = Graph()

        for node1, neighbors in threshold_graph.adj_list.items():
            inverted_graph.add_node(node1, threshold_graph.party[node1], threshold_graph.votes[node1])
            for node2, votes in neighbors.items():
                    new_weight = 1 - threshold_graph.adj_list[node1][node2]
                    inverted_graph.add_edge(node1, node2, new_weight)

        return inverted_graph
