class Graph:

    def __init__(self):
        self.adj_list = {}

    def add_node(self, node):
        if node in self.adj_list:
            raise ValueError(f"This node {node} already exists")
        self.adj_list[node] = {'party': None}

    def add_party_to_a_node(self, node, party):
        if node not in self.adj_list:
            raise ValueError(f"This node {node} does not exist")
        self.adj_list[node]['party'] = party

    def add_edge(self, node1, node2, weight):
        if node1 not in self.adj_list or node2 not in self.adj_list:
            raise ValueError(f"Those nodes {node1} and {node2} are not in the list")
        if node1 == 'party' or node2 == 'party' or node1 == 'votes' or node2 == 'votes':
            raise ValueError("Node names 'party' and 'votes' are reserved and cannot be used for edges")
        if weight < 0:
            raise ValueError("The weight must be higher than zero")
        if 'edges' not in self.adj_list[node1]:
            self.adj_list[node1]['edges'] = {}
        if 'edges' not in self.adj_list[node2]:
            self.adj_list[node2]['edges'] = {}
        self.adj_list[node1]['edges'][node2] = weight
        self.adj_list[node2]['edges'][node1] = weight
    
    def filter_party(self, party):
        filtered_graph = Graph()

        for node, node_data in self.adj_list.items():
            if node_data['party'] == party:
                filtered_graph.add_node(node)
                filtered_graph.adj_list[node]['party'] = node_data['party']
                filtered_graph.adj_list[node]['votes'] = node_data.get('votes', 0)

        for node1, neighbors in self.adj_list.items():
            for node2, weight in neighbors.get('edges', {}).items():
                if self.adj_list[node1]['party'] == party and self.adj_list[node2]['party'] == party:
                    filtered_graph.add_edge(node1, node2, weight)

        return filtered_graph
    
    def get_edge_vote(self, node1, node2):
        if node2 not in self.adj_list[node1] or node1 not in self.adj_list:
            raise ValueError ("One of these nodes do not exist")
        return self.adj_list[node1][node2]
    
    def add_vote_to_a_node(self, node, vote):
        if node not in self.adj_list:
            raise ValueError(f"The node {node} hasn't been found")
        self.adj_list[node]["votes"] = vote

    def normalize_edges(self, filtered_graph):
        max_weight = float('-inf')
        
        for node1, neighbors in self.adj_list.items():
            for node2, weight in neighbors.get('edges', {}).items():
                if node1 != 'party' and node2 != 'party' and node1 != 'votes' and node2 != 'votes':
                    max_weight = max(max_weight, weight)
        
        for node1, neighbors in self.adj_list.items():
            for node2, weight in neighbors.get('edges', {}).items():
                if node1 != 'party' and node2 != 'party' and node1 != 'votes' and node2 != 'votes':
                    votes_node1 = self.adj_list[node1].get('votes', 0)
                    votes_node2 = self.adj_list[node2].get('votes', 0)
                
                    if votes_node1 > 0 and votes_node2 > 0:
                        normalized_weight = weight / max_weight
                        filtered_graph.add_edge(node1, node2, normalized_weight)

                            
    def threshold(self, threshold_value):
        filtered_graph = Graph()

        for node1, neighbors in self.adj_list.items():
            for node2, weight in neighbors.get('edges', {}).items():
                if weight >= threshold_value:
                    if node1 not in filtered_graph.adj_list:
                        filtered_graph.add_node(node1)
                        filtered_graph.adj_list[node1]['party'] = self.adj_list[node1]['party']
                        filtered_graph.adj_list[node1]['votes'] = self.adj_list[node1].get('votes', 0)

                    if node2 not in filtered_graph.adj_list:
                        filtered_graph.add_node(node2)
                        filtered_graph.adj_list[node2]['party'] = self.adj_list[node2]['party']
                        filtered_graph.adj_list[node2]['votes'] = self.adj_list[node2].get('votes', 0)

                    filtered_graph.add_edge(node1, node2, weight)

        return filtered_graph

        
    def __add__(self, other):
            if not isinstance(other, Graph):
                raise TypeError("Unsupported operand type(s) for +: 'Graph' and '{}'".format(type(other)))
            merged_graph = Graph()

            for node, node_data in self.adj_list.items():
                merged_graph.add_node(node)
                merged_graph.adj_list[node]['party'] = node_data['party']
                merged_graph.adj_list[node]['votes'] = node_data.get('votes', 0)

            for node1, neighbors in self.adj_list.items():
                for node2, weight in neighbors.get('edges', {}).items():
                    merged_graph.add_edge(node1, node2, weight)

            for node, node_data in other.adj_list.items():
                if node not in merged_graph.adj_list:
                    merged_graph.add_node(node)
                    merged_graph.adj_list[node]['party'] = node_data['party']
                    merged_graph.adj_list[node]['votes'] = node_data.get('votes', 0)

            for node1, neighbors in other.adj_list.items():
                for node2, weight in neighbors.get('edges', {}).items():
                    merged_graph.add_edge(node1, node2, weight)

            return merged_graph
        
    def __str__(self):
            for node, node_data in self.adj_list.items():
                result += f"{node} (Party: {node_data['party']}):\n"
                for neighbor, weight in node_data.get('edges', {}).items():
                    result += f"    -> {neighbor} (Weight: {weight:.2f})\n"
            return result
