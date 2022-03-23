#Importaciones respectivas
from node import *

#Clase Grafo
class Graph:

    def __init__(self):
        #Lista de nodos del grafo
        self.nodes_dict = {}
    
    #Función para agregar nodos. Cada uno con su ID, descripción, duración y predecesores
    def add_node(self, nodeId: int, nodeDescription: str, nodeDuration: float, pred:list):  
        new_node = Node(nodeId, nodeDescription, nodeDuration, pred)
        self.nodes_dict[nodeId] = new_node
        return new_node

    #Función para agregar aristas. Los respectivo sucesores y predecesores de cada uno
    def add_edge(self, nodeFrom: int, nodeTo: int):
        self.nodes_dict[nodeFrom].set_sucesor(self.nodes_dict[nodeTo])
        self.nodes_dict[nodeTo].set_predecesor(self.nodes_dict[nodeFrom])

    def debug(self):
        print(self.nodes_dict)