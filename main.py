#Importaciones respectivas
from genericpath import exists
from tracemalloc import start
from node import *
from graph import *
import sys
# from pickle import FALSE
# from sympy import false
# import pandas as pd
# import networkx as nx
# from matplotlib import pyplot as plt


#Variables para usar luego
graph : Graph
newGraph : Graph
graphX1: Graph
nodesId = []
activities = []
start = ''
end = ''
num_nodes = 0
num_holg = 0


#Función para leer el archivo txt del proyecto
def read_file():
    
   #Variable de actividades 
    global activities
    #Se abre el TXT y se lee
    f = open("Archivo.txt", "r")
    #Se eliminan los \n con Splitline
    temp = f.read().splitlines()

    #Se recorre el documento leído
    for x in temp:
        #Se guardan las actividades -con sus datos id, descripción, duración, predecesores- 
        #Se separan los datos que se encuentran divididos por -
        activity = x.split('-') 
        activities.append(activity)
    #Se cierra el TXT
    f.close()
    #Retorna las actividades guardadas
    return activities


#Función para validar la información del TXT
def validate_txt(activities):

    #Variable para saber que el nodo Start no tiene predecesores
    start = ''

    #Para validar los ids repetidos se hace:

    #Se guardan los Ids de las actividades
    ids = [act[0] for act in activities]
    #Se hace una lista con todos los Ids que no estan duplicados
    ids_sin_dup = list(set(ids))
    #Si el tañano de la lista de los Ids es diferente al tamaño de la lista de los Ids sin duplicado
    if len(ids) != len(ids_sin_dup):
        #Eso quiere decir que hay IDs duplicados y eso no se permite, por lo que se lanza el siguiente mensaje
        print('No pueden existir Ids de las actividades duplicados.')
        return False

    #Para validar las duraciones de las actividades -que no puede tener letras y no puede ser 0- se tiene:
    
    #Se guardan las duraciones de las actividades que SOLO TENGAN como duración "0"
    durations_0 = [act[2] for act in activities if act[2] == 0]
    #Se guardan todas las duraciones de las actividades que están en el TXT
    durations =  [act[2] for act in activities]

    #Se recorren las duraciones
    for dur in durations:
        #Si una de las duraciones NO es un dígito
        if not dur.isdigit():
            #Se lanza el siguiente mensaje
            print('No pueden existir letras en las duraciones de las actividades.')
            return False
    #Si el tamaño de la lista donde solo se guardan las actividades de duración 0 es mayor a 0
    if len(durations_0) > 0:
        #Se lanza el siguiente mensaje
        print ('No pueden existir duraciones en las actividades igual a cero.')
        return False

    #Para validar si solo hay 1 nodo inicio, si los predecesores existen:
    
    #Se guardan todos los predecesores del TXT 
    predecessors = [act[3] for act in activities]
    #Variable que se usará para validar si hay más de dos nodos inicio
    num_starts = 0
    #Se recorren los predecesores
    for pred in predecessors:
        #Se separan los mismo porque en el TXT se encuntran separados por ","
        pred_sin_coma = pred.split(',')
        #Se recorren los predecesores guardaddos sin "," para ver si existen
        for id in pred_sin_coma:
            #Si el predecesor existe o uno de ellos tiene como predecesor vacío ""
            if id in ids or id == '':
                #No pasa nda
                #Si el predecesor es vacío
                if id == '':
                    #Se suma uno a la varibale para validar si hay más de dos nodos inicio
                    num_starts += 1
            else:
                #Si el predecesor no exite
                print('El id no está')
                return False
  
    #Para verificar si hay más de un nodo inicio o si NO existe
    #Si la varibale para validar si hay más de dos nodos inicio es mayor a 1 es que hay dos 
    if num_starts > 1:
        #Por ello se lanza el siguiente mensaje
        print('En su archivo hay más de una actividad inicio y eso no es posible.')
        return False
    #Si la varibale para validar si hay más de dos nodos inicio es mayor a 0, eso quiere decir que No hay nodo inicio
    elif num_starts == 0:
        #Por ello se lanza el siguiente mensaje
        print('No hay una actividad inicio.')
        return False

    return True


#Función para crear el grafo a partir de la información del txt
def create():
    #Varibales
    global graph 
    graph = Graph()
    global nodesId
    global activities
    nodesId = []
    global start
    global end
    auxiliaryArray = []
    global num_nodes

    #Se recorre las actividades para agregarlas al grafo
    for activity in activities:
        #Se guardan separados los predecesores sin ","
        predecessors = activity[3].split(',')

        if predecessors[0] == '':
            start = activity[0]

        nodesId.append(activity[0])

        for pred in predecessors:
            if pred not in nodesId and pred != '':
                print('Error, no existe el nodo ' + pred + 'en el grafo, revise que el archivo TXT esté ingresando los nodos en orden')
            
        graph.add_node(activity[0], activity[1], float(activity[2]), predecessors)
        num_nodes += 1
    
    for i in nodesId:
        for j in graph.nodes_dict[i].pred:
            if j not in auxiliaryArray:
                auxiliaryArray.append(j)

    setAll = set(nodesId)
    setPred = set(auxiliaryArray)
    setLast = (setAll - setPred) 
    end = list(setLast)[0]
    
    return graph


def cpm(graphVal: Graph):

    alterNodesId:list = []
    arrayQueue:list = []
    graphX: Graph = graphVal
    global num_holg

    for node in nodesId:
        alterNodesId.append(node)

    #Forward pass

    alterNodesId.pop(0)

    graphX.nodes_dict[start].ef += graphX.nodes_dict[start].duration
    
    for i in alterNodesId:

            if graphX.nodes_dict[i].pred[0] == start:
                arrayQueue.append(graphX.nodes_dict[i].id)

    while len(arrayQueue) !=0:

        predNodes:list = []
        actual = arrayQueue.pop()

        if True:

            predNodes = graphX.nodes_dict[actual].pred
            valid = True

            for k in predNodes:

                if graphX.nodes_dict[k].ef == 0:
                    valid = False
                    break

            if valid:

                maxEF = 0
                for n in predNodes:
                    if graphX.nodes_dict[n].ef > maxEF:
                        maxEF = graphX.nodes_dict[n].ef

                graphX.nodes_dict[actual].es = maxEF
                graphX.nodes_dict[actual].ef = graphX.nodes_dict[actual].es + graphX.nodes_dict[actual].duration

                for l in alterNodesId:
                    if actual in graphX.nodes_dict[l].pred:
                        arrayQueue.append(l)

    # for i in nodesId:
        # print(f'Nodo: {i}, ES: {graphX.nodes_dict[i].es}, EF: {graphX.nodes_dict[i].ef}')
   

    #Backward pass

    firstList = graphX.nodes_dict[end].pred

    graphX.nodes_dict[end].lf = graphX.nodes_dict[end].ef
    graphX.nodes_dict[end].ls = graphX.nodes_dict[end].lf - graphX.nodes_dict[end].duration

    indexA = alterNodesId.index(end)
    alterNodesId.pop(indexA)

    for j in firstList:
        arrayQueue.append(j)
        index = alterNodesId.index(j)
        alterNodesId.pop(index)

    while len(arrayQueue) != 0:

        predNodes:list = []
        sucNodes:list = []
        actual = arrayQueue.pop(0)

        if actual in firstList:

            maxEfbP = 0
            for i in firstList:
                if graphX.nodes_dict[i].ef > maxEfbP:
                    maxEfbP = graphX.nodes_dict[i].ef

            graphX.nodes_dict[actual].lf = maxEfbP
            graphX.nodes_dict[actual].ls = maxEfbP - graphX.nodes_dict[actual].duration

            for i in graphX.nodes_dict[actual].pred:
                if i not in arrayQueue:
                    arrayQueue.append(i)

        else:

            for i in nodesId:
                if actual in graphX.nodes_dict[i].pred:
                    sucNodes.append(i)

            valid = True

            for j in sucNodes:
                if graphX.nodes_dict[j].ls == 0:
                    valid = False
                    break
            
            if valid:

                minLS = 99999999999999999

                for i in sucNodes:
                    if graphX.nodes_dict[i].ls < minLS:
                        minLS = graphX.nodes_dict[i].ls

                graphX.nodes_dict[actual].lf = minLS
                graphX.nodes_dict[actual].ls = graphX.nodes_dict[actual].lf - graphX.nodes_dict[actual].duration

                for j in graphX.nodes_dict[actual].pred:
                    if j != 0 and j not in arrayQueue:
                        arrayQueue.append(j)

    # for i in nodesId:
    #     print(f'Nodo: {i}, LS: {graphX.nodes_dict[i].ls}, LF: {graphX.nodes_dict[i].lf}')

    #Calcular holguras

    for i in nodesId:
        holg = graphX.nodes_dict[i].ls - graphX.nodes_dict[i].es
        if holg != 0:
            graphX.nodes_dict[i].holgura = holg
        else: 
            num_holg += 1

    nodosHolguraId = []

    for m in nodesId:
        if graphX.nodes_dict[m].holgura != 0:
            nodosHolguraId.append(m)

    #CPM
    path = []
    startList = []
    inicio = ""
    final = ""

    path.append(start)
    for i in nodesId:   
        if i != start:
            if graphX.nodes_dict[i].pred[0] == start:
                startList.append(i)

    auxiliaryArray: list = []

    for i in alterNodesId:
        for j in graphX.nodes_dict[i].pred:
            if j not in auxiliaryArray:
                auxiliaryArray.append(j)

    actualId = ""
    loop = True 

    for i in startList:
            if graphX.nodes_dict[i].holgura == 0:
                actualId = i
                inicio = i

    while loop:
        sucChoose = []
        path.append(actualId)

        for i in nodesId:
            if actualId in graphX.nodes_dict[i].pred:
                sucChoose.append(i)

        if len(sucChoose)!=0:
            for i in sucChoose:
                if graphX.nodes_dict[i].holgura == 0:
                    actualId = i
        else:            
            final = actualId
            loop = False

    pathStr = ""
    totalDuration = graphX.nodes_dict[end].lf
    for i in path:
        if i != path[len(path)-1]:
            pathStr += i+" ==> "
        else:
            pathStr += i
    
    if num_holg == num_nodes:
        print(f'En este proyecto todas las activides son críticas')
        print(f'Una posible ruta crítica puede ser la siguiente')
        
    print(f'CPM: {pathStr}')
    print(f'TIEMPO DE DURACION DEL CP: {totalDuration}')
    print(f'INICIAL: { graphX.nodes_dict[start].description }')
    print(f'FINAL: { graphX.nodes_dict[end].description }')
    print("\n")

    if num_holg != num_nodes:
        print("Nodos con holgura")
        for n in nodosHolguraId:
            print(f"Nodo: {n}, Holgura: {graph.nodes_dict[n].holgura}")
    
    # #CPM

    # global graphX1 
    # graphX1 = graphX

    # fromList = []
    # toList = []

    # for i in nodesId:
    #     for j in graphX.nodes_dict[i].pred:
    #         fromList.append(j)
    #         toList.append(i)
    # df = pd.DataFrame({
    # 'from': fromList,
    # 'to': toList
    # })
    
    # G = nx.convert_matrix.from_pandas_edgelist(df, 'from', 'to')
    # red_edges = []


    # for i in range(len(path)):
    #     if i != 0:
    #         auxTup = (path[i-1],path[i])
    #         red_edges.append(auxTup)
    # black_edges = [edge for edge in G.edges() if edge not in red_edges]
    # edgesList = []
    # colorList = []
    # for i in red_edges:
    #     edgesList.append(i)
    #     colorList.append('red')
    # for i in black_edges:
    #     edgesList.append(i)
    #     colorList.append('black')
    

    # values = [('green' if node == 'inicio' or node == "final"  else ('blue')) for node in G.nodes()]
    # # nx.draw(G,  arrows=True, with_labels=True, node_size = 1000, node_color = values)
    # nx.drawing.nx_pylab.draw_networkx (G,  arrows=True, with_labels=True, edgelist=edgesList, edge_color=colorList, node_size = 1000, node_color = values)

    # # nx.drawing.nx_pylab.draw_networkx (G,  arrows=True, with_labels=True, edgelist=black_edges,)
    # plt.show()


def main():
    
    read_file()

    valid = validate_txt(activities)

    if valid:
        
        graph = create()

        print("Su grafo se encuentra creado. Indique qué desea realizar: ")

        cpm(graph)
    
    else: 

        print('Txt malo')


    #     print("1. Verificar ruta critica.")
        # print("4. Solicitar información de actividad en el grafo")

        

    #     elif opcion == "8":
    #         fromList = []
    #         toList = []

    #         for i in nodesId:
    #             for j in graph.nodes_dict[i].pred:
    #                 fromList.append(j)
    #                 toList.append(i)
    #         df = pd.DataFrame({
    #         'from': fromList,
    #         'to': toList
    #         })
            
    #         G = nx.convert_matrix.from_pandas_edgelist(df, 'from', 'to')


    #         values = [('green' if node == 'inicio' or node == "final"  else ('blue')) for node in G.nodes()]
    #         # nx.draw(G,  arrows=True, with_labels=True, node_size = 1000, node_color = values)
    #         nx.drawing.nx_pylab.draw_networkx (G,  arrows=True, with_labels=True, node_size = 1000, node_color = values)

    #         # nx.drawing.nx_pylab.draw_networkx (G,  arrows=True, with_labels=True, edgelist=black_edges,)
    #         plt.show()




main()
