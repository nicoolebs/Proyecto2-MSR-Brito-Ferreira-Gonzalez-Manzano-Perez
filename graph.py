from node import *
class Graph:

    def __init__(self):
        self.nodes_dict = {}
    
    def add_node(self, nodeId: int, nodeDescription: str, nodeDuration: float, pred:list):  
        new_node = Node(nodeId, nodeDescription, nodeDuration, pred)
        self.nodes_dict[nodeId] = new_node
        return new_node

    def add_edge(self, nodeFrom: int, nodeTo: int):
        self.nodes_dict[nodeFrom].set_sucesor(self.nodes_dict[nodeTo])
        self.nodes_dict[nodeTo].set_predecesor(self.nodes_dict[nodeFrom])

    def debug(self):
        print(self.nodes_dict)