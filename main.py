#Importaciones respectivas
from genericpath import exists
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
                print('El id está')
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
    global inicio

    #Se recorre las actividades para agregarlas al grafo
    for activity in activities:
        #Se guardan separados los predecesores sin ","
        predecessors = activity[3].split(',')

        #Falta guardar el inicio y validar que No puede tener como predecesores de un nodo al nodo inicio y a otro nodo

        graph.add_node(activity[0], activity[1], float(activity[2]), predecessors)
        nodesId.append("inicio")

   
 
    #         pre = input("Ingrese los ids de sus predecesores separados por comas: ")
    #         while "inicio" in pre.split(",") and len(pre.split(",")) > 1:
    #             pre = input("No puede tener como predecesores de un nodo al nodo inicio y a otro nodo. Ingrese los ids de sus predecesores separados por comas: ")
    #         pre = pre.split(",") 
    #         #pres = []
    #         #for p in pre:
    #         #    pres.append(int(p))
            
    #         valid = True
    #         while valid:
    #             a = True
    #             for p in pre:
    #                 if p not in nodesId not in nodesId:
    #                     a = False
    #                     break
    #             if a == False:
    #                 pre = input(f"No existe un nodo {p} en el grafo. Ingrese los ids de sus predecesores separados por comas: ")
    #                 pre = pre.split(",")
    #                 #pres = []   
    #                 #for p in pre:
    #                 #    pres.append(int(p))
    #             else:
    #                 valid = False

    #         graph.add_node(id, descripcion, duracion, pre)
            
            
    #         nodesId.append(id)
    #         print("Esta listo su grafo?: ")
    #         print ("1. Si")
    #         print ("2. No")
    #         caso =["1","2"]
    #         loop = input("Ingrese 1 o 2 segun corresponda: ")
    #         while loop not in caso:
    #             loop = input("Ingrese 1 o 2 segun corresponda: ")
    # auxiliaryArray: list = []

    # for i in nodesId:
    #     for j in graph.nodes_dict[i].pred:
    #         if j not in auxiliaryArray:
    #             auxiliaryArray.append(j)
    # setAll = set(nodesId)
    # setPred = set(auxiliaryArray)
    # setLast = (setAll - setPred) 
    # end = list(setLast)
    # descripcionFin = str(input("Ingrese la descripcion de la actividad final: "))
    # while descripcionFin.isspace() or not descripcionFin:
    #     descripcionFin = str(input("Ingrese la descripcion de la actividad final no vacia: "))
    # graph.add_node("final", descripcionFin, 0, end)
    # nodesId.append("final")
    # return graph




def cpm(graphVal: Graph):
    alterNodesId:list = []
    arrayQueue:list = []
    graphX: Graph = graphVal
    for i in nodesId:
        graph.add_node(i, graphVal.nodes_dict[i].description, graphVal.nodes_dict[i].duration, graphVal.nodes_dict[i].pred)
    for node in nodesId:
        alterNodesId.append(node)
    #forward
    alterNodesId.pop(0)
    
    for i in alterNodesId:
            if graphX.nodes_dict[i].pred[0] == "inicio":
                arrayQueue.append(graphX.nodes_dict[i].id)
    while len(arrayQueue) !=0:
        predNodes:list = []
        actual = arrayQueue.pop()
        if graphX.nodes_dict[actual].pred[0] == "inicio":
            graphX.nodes_dict[actual].ef += graphX.nodes_dict[actual].duration
            for j in alterNodesId:
                if actual in graphX.nodes_dict[j].pred:
                    arrayQueue.append(j)
        else:
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
                graphX.nodes_dict[actual].ef = maxEF +graphX.nodes_dict[actual].duration
                for l in alterNodesId:
                    if actual in graphX.nodes_dict[l].pred:
                        arrayQueue.append(l)

    for i in nodesId:
        print(f'Nodo: {i}, ES: {graphX.nodes_dict[i].es}, EF: {graphX.nodes_dict[i].ef}')
    #forward

    #alterNodesId = nodesId
    #alterNodesId.pop(0)

    #backward
    # auxiliaryArray: list = []
    # for i in alterNodesId:
    #     for j in graphX.nodes_dict[i].pred:
    #         if j not in auxiliaryArray:
    #             auxiliaryArray.append(j)
    # setAll = set(alterNodesId)
    # setPred = set(auxiliaryArray)
    # setLast = (setAll - setPred) 
    firstList = graphX.nodes_dict["final"].pred
    graphX.nodes_dict["final"].lf = graphX.nodes_dict["final"].ef
    graphX.nodes_dict["final"].ls = graphX.nodes_dict["final"].lf - graphX.nodes_dict["final"].duration
    indexA = alterNodesId.index("final")
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
                maxLS = sys.maxsize
                for i in sucNodes:
                    if graphX.nodes_dict[i].ls < maxLS:
                        maxLS = graphX.nodes_dict[i].ls
                graphX.nodes_dict[actual].lf = maxLS
                graphX.nodes_dict[actual].ls = maxLS - graphX.nodes_dict[actual].duration
                for j in graphX.nodes_dict[actual].pred:
                    if j != 0 and j not in arrayQueue:
                        arrayQueue.append(j)
    for i in nodesId:
        print(f'Nodo: {i}, LS: {graphX.nodes_dict[i].ls}, LF: {graphX.nodes_dict[i].lf}')


    #backward

    #holguras
    for i in nodesId:
        sum = graphX.nodes_dict[i].ls - graphX.nodes_dict[i].es
        if sum != 0:
                graphX.nodes_dict[i].holgura = sum

    print("\n")
    nodosHolguraId = []
    for m in nodesId:
        if graph.nodes_dict[m].holgura != 0:
            nodosHolguraId.append(m)

    #holguras

    #CPM
    path = []
    start = []
    inicio = ""
    end = []
    final = ""

    path.append("inicio")
    for i in nodesId:   
        if i != "inicio":
            if graphX.nodes_dict[i].pred[0] == "inicio":
                start.append(i)
    auxiliaryArray: list = []

    for i in alterNodesId:
        for j in graphX.nodes_dict[i].pred:
            if j not in auxiliaryArray:
                auxiliaryArray.append(j)
    setAll = set(alterNodesId)
    setPred = set(auxiliaryArray)
    setLast = (setAll - setPred) 
    end = list(setLast)

    actualId = ""
    loop = True 
    for i in start:
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
    totalDuration = graphX.nodes_dict["final"].es
    for i in path:
        if i != path[len(path)-1]:
            pathStr += i+" ==> "
        else:
            pathStr += i
    
    print(f'CPM: {pathStr}')
    print(f'TIEMPO DE DURACION DEL CP: {totalDuration}')
    print(f'INICIAL: { graphX.nodes_dict["inicio"].description }')
    print(f'FINAL: { graphX.nodes_dict["final"].description }')
    print("\n")
    print("Nodos con holgura")
    for n in nodosHolguraId:
        print(f"Nodo: {n}, Holgura: {graph.nodes_dict[n].holgura}")

    
    #CPM

    global graphX1 
    graphX1 = graphX

    fromList = []
    toList = []

    for i in nodesId:
        for j in graphX.nodes_dict[i].pred:
            fromList.append(j)
            toList.append(i)
    df = pd.DataFrame({
    'from': fromList,
    'to': toList
    })
    
    G = nx.convert_matrix.from_pandas_edgelist(df, 'from', 'to')
    red_edges = []


    for i in range(len(path)):
        if i != 0:
            auxTup = (path[i-1],path[i])
            red_edges.append(auxTup)
    black_edges = [edge for edge in G.edges() if edge not in red_edges]
    edgesList = []
    colorList = []
    for i in red_edges:
        edgesList.append(i)
        colorList.append('red')
    for i in black_edges:
        edgesList.append(i)
        colorList.append('black')
    

    values = [('green' if node == 'inicio' or node == "final"  else ('blue')) for node in G.nodes()]
    # nx.draw(G,  arrows=True, with_labels=True, node_size = 1000, node_color = values)
    nx.drawing.nx_pylab.draw_networkx (G,  arrows=True, with_labels=True, edgelist=edgesList, edge_color=colorList, node_size = 1000, node_color = values)

    # nx.drawing.nx_pylab.draw_networkx (G,  arrows=True, with_labels=True, edgelist=black_edges,)
    plt.show()

    









def main():
    opciones = ["1","2","3","4","5","6","7","8"]
    opciones2 = ["1","2","3","4","5","6","7","8","9"]
    print("\n")
    print("Bienvenido. En vista de que es su primera vez accediendo al programa, debera armar un grafo con las actividades.")
    print("\n")
    graph = create()

    read_file()

    valid = validate_txt(activities)

    if valid:
        
        create()
    
    else: 

        print('Txt malo')

    #print("Su grafo se encuentra creado. Indique qué desea realizar: ")
    # opcion = "1"
    # while opcion in opciones:
    #     print("\n")
    #     print("Su grafo se encuentra creado. Indique que desea realizar: ")
    #     print("\n")
    #     print("Menu")
    #     print("1. Verificar ruta critica.")
    #     print("4. Solicitar descripcion de actividad en el grafo")
    #     print("7. Borrar el grafo existente y crear uno nuevo")

        
    #     opcion = (input("Ingrese 1,2,3,4,5,6,7,8 u 9 segun corresponda: "))
    #     while opcion not in opciones2:
    #         opcion = (input("Ingrese 1,2,3,4,5,6,7,8 u 9 segun corresponda: "))
        
    #     print("\n")
    
    #     if opcion == "1":
    #         cpm(graph)
    #     elif opcion == "2":
    #         loop = "2"

    #         while loop == "2":
    #                 id = input("Ingrese el id de la actividad: ")
    #                 while id in nodesId or id.isspace() or not id:
    #                     id = input("Existe una actividad con el ID indicado o es vacio. Indique otro id: ")
    #                 descripcion = str(input("Ingrese la descripcion de la actividad: "))
    #                 while descripcion.isspace() or not descripcion:
    #                     descripcion = str(input("Ingrese la descripcion de la actividad no vacia: "))
    #                 duracion = input("Ingrese la duracion de la actividad: ")
    #                 boo = check_user_input(duracion)
    #                 while boo == False:
    #                     duracion = input("Ingrese la duracion de la actividad: ")
    #                     if duracion == '':
    #                         duracion = 's'
    #                     boo = check_user_input(duracion)
    #                 duracion = float(duracion)      
    #                 pre = input("Ingrese los ids de sus predecesores separados por comas. Si quiere añadir de predecesor al inicio ingrese 'inicio': ")
    #                 while "inicio" in pre.split(",") and len(pre.split(",")) > 1:
    #                     pre = input("No puede tener como predecesores de un nodo al nodo inicio y a otro nodo. Ingrese los ids de sus predecesores separados por comas: ")
    #                 pre = pre.split(",") 
                    
    #                 valid = True
    #                 while valid:
    #                     a = True
    #                     for p in pre:
    #                         if p not in nodesId not in nodesId:
    #                             a = False
    #                             break
    #                     if a == False:
    #                         pre = input(f"No existe un nodo {p} en el grafo. Ingrese los ids de sus predecesores separados por comas: ")
    #                         pre = pre.split(",")
    #                     else:
    #                         valid = False

    #                 while "final" in pre:
    #                     pre = input("No puede tener como predecesores de un nodo al nodo final. Ingrese los ids de sus predecesores separados por comas: ")
    #                     pre = pre.split(",")

    #                 graph.add_node(id, descripcion, duracion, pre)
    #                 nodesId.append(id)
    #                 print("Está listo su grafo?: ")
    #                 print ("1. Si")
    #                 print ("2. No")
    #                 caso =["1","2"]
    #                 loop = input("Ingrese 1 o 2 segun corresponda: ")
    #                 while loop not in caso:
    #                     loop = input("Ingrese 1 o 2 segun corresponda: ")

    #         auxiliaryArray = []
    #         alterNodesNow = []
    #         for i in nodesId:
    #             alterNodesNow.append(i)
    #         alterNodesNow.pop(0)
    #         ind = alterNodesNow.index("final")
    #         alterNodesNow.pop(ind)
    #         for i in alterNodesNow:
    #             for j in graph.nodes_dict[i].pred:
    #                 if j not in auxiliaryArray:
    #                     auxiliaryArray.append(j)
    #         setAll = set(alterNodesNow)
    #         setPred = set(auxiliaryArray)
    #         setLast = (setAll - setPred) 
    #         end = list(setLast)
    #         graph.nodes_dict["final"].pred = end
    #         inde = nodesId.index("final")
    #         nodesId.pop(inde)
    #         nodesId.append("final")


    #     elif opcion == "3":
    #         verificar = input("Indique el ID del nodo que desea verificar se encuentra dentro del grafo: ")
    #         while verificar not in nodesId or verificar == "inicio":
    #             print("El ID indicado no se encuentra en el grafo o es 0.")
    #         else:
    #             print("El ID indicado se encuentra en el grafo.")


    #     elif opcion == "4":
    #         verificar = input("Indique el ID del nodo que desea verificar su descripcion: ")
    #         while verificar not in nodesId or verificar == "inicio":
    #             print("El ID indicado no se encuentra en el grafo o es inicio.")
    #             verificar = input("Indique el ID del nodo que desea verificar su descripcion: ")
    #         else:
    #             print("Descripcion: ")
    #             print(graph.nodes_dict[verificar].description)
    #             print("Duracion: ")
    #             print(graph.nodes_dict[verificar].duration)
        
    #     elif opcion == "5":
    #         verificar = input("Indique el ID del nodo que desea alterar su descripcion: ")
    #         while verificar not in nodesId :
    #             print("El ID indicado no se encuentra en el grafo.")
    #             verificar = input("Indique el ID del nodo que desea verificar su descripcion: ")
    #         else:
    #             print("Descripcion anterior: ")
    #             print(graph.nodes_dict[verificar].description)
    #             descripcionN = input("Ingrese la nueva descripcion: ")
    #             while descripcionN.isspace() or not descripcionN:
    #                 descripcionN = input("Ingrese la nueva descripcion no vacia: ")
    #             graph.nodes_dict[verificar].set_description(descripcionN)
        
    #     elif opcion == "6":
    #         verificar = input("Indique el ID del nodo que desea alterar su tiempo de duracion: ")
    #         while verificar not in nodesId or verificar == "inicio":
    #             print("El ID indicado no se encuentra en el grafo o es inicio.")
    #             verificar = input("Indique el ID del nodo que desea verificar su tiempo de duracion: ")
    #         else:
    #             print("Duracion anterior: ")
    #             print(graph.nodes_dict[verificar].duration)
    #             dura = input("Ingrese la nueva duracion de la actividad: ")
    #             boos = check_user_input(dura)
    #             while boos == False:
    #                 dura = input("Ingrese la duracion de la actividad: ")
    #                 if dura == '':
    #                     dura = 's'
    #                 boos = check_user_input(dura)
    #             dura = float(dura) 
    #             graph.nodes_dict[verificar].set_duration(dura)

    #     elif opcion == "7":
    #         newGraph = Graph()
    #         graph = newGraph
            
    #         print("Arme su nuevo grafo con sus actividades")
    #         print("\n")
    #         graph = create()
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
