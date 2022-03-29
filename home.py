# Importaciones respectivas
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
from turtle import width
from PIL import Image, ImageTk
from graph import *
from node import *
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
import matplotlib as mpl


# Configuración de la interfaz gráfica

# Creación de la ventana
home = Tk()

# Título de la ventana
home.title("Ruta Critica")

# Para que la ventana no sea redimensionable
home.resizable(0, 0)
# Configuración del frame que va a contener todos los widgets que se van a mostar en la interfaz gráfica
homeFrame = Frame()
homeFrame.pack()
homeFrame.config(bg="#f0ebe7")
homeFrame.config(width="1300", height="700")

# Etiquetas que se muestran en pantalla con mensajes de Bienvenida
Label(homeFrame, text="¡Bienvenido a la Calculadora de Ruta Crítica CPM/PERT!", fg="#000000", font=("Poppins", 18, "bold"), bg="#f0ebe7").place(x="600", y="50", anchor="center")
Label(homeFrame, text="Por favor, edite su Archivo TXT con sus actividades y datos respectivos.", fg="#000000",
      font=("Roboto", 12, "bold"), bg="#f0ebe7") \
    .place(x="600", y="115", anchor="center")
Label(homeFrame, text="Una vez colocadas las mismas en el archivo de datos, oprima el siguiente botón para calcular la ruta crítica del Proyecto.", fg="#000000",
      font=("Roboto", 12, "bold"), bg="#f0ebe7") \
    .place(x="600", y="145", anchor="center")


#Variables
graph : Graph
newGraph : Graph
graphX1: Graph
nodesId = []
activities = []
start = ''
end = ''
num_nodes = 0
num_holg = 0


# Función para leer el archivo txt del proyecto
def read_file():
    # Variable de actividades
    global activities
    # Se abre el TXT y se lee
    f = open("Archivo.txt", "r")
    # Se eliminan los \n con Splitline
    temp = f.read().splitlines()

    # Se recorre el documento leído
    for x in temp:
        # Se guardan las actividades -con sus datos id, descripción, duración, predecesores-
        # Se separan los datos que se encuentran divididos por -
        activity = x.split('-')
        activities.append(activity)
    # Se cierra el TXT
    f.close()
    # Retorna las actividades guardadas
    return activities


# Función para validar la información del TXT
def validate_txt(activities):

    # Variable para saber que el nodo Start no tiene predecesores
    start = ''

    # Para validar los ids repetidos se hace:

    # Se guardan los Ids de las actividades
    ids = [act[0] for act in activities]
    # Se hace una lista con todos los Ids que no estan duplicados
    ids_sin_dup = list(set(ids))
    # Si el tañano de la lista de los Ids es diferente al tamaño de la lista de los Ids sin duplicado
    if len(ids) != len(ids_sin_dup):
        # Eso quiere decir que hay IDs duplicados y eso no se permite, por lo que se lanza el siguiente mensaje
        messagebox.showerror('Error en archivo de disco', 'No pueden existir Ids de las actividades duplicados. Arregle el archivo txt y vuelva a presionar el botón.')
        return False

    # Para validar las duraciones de las actividades -que no puede tener letras y no puede ser 0- se tiene:

    # Se guardan las duraciones de las actividades que SOLO TENGAN como duración "0"
    durations_0 = [act[2] for act in activities if act[2] == 0]
    # Se guardan todas las duraciones de las actividades que están en el TXT
    durations = [act[2] for act in activities]

    # Se recorren las duraciones
    for dur in durations:
        # Si una de las duraciones NO es un dígito
        if not dur.isdigit():
            # Se lanza el siguiente mensaje
            messagebox.showerror('Error en archivo de disco', 'No pueden existir letras en las duraciones de las actividades. Arregle el archivo txt y vuelva a presionar el botón.')
            return False
    # Si el tamaño de la lista donde solo se guardan las actividades de duración 0 es mayor a 0
    if len(durations_0) > 0:
        # Se lanza el siguiente mensaje
        messagebox.showerror('Error en archivo de disco', 'No pueden existir duraciones en las actividades igual a cero. Arregle el archivo txt y vuelva a presionar el botón.')
        return False

    # Para validar si solo hay 1 nodo inicio, si los predecesores existen:

    # Se guardan todos los predecesores del TXT
    predecessors = [act[3] for act in activities]
    # Variable que se usará para validar si hay más de dos nodos inicio
    num_starts = 0
    # Se recorren los predecesores
    for pred in predecessors:
        # Se separan los mismo porque en el TXT se encuntran separados por ","
        pred_sin_coma = pred.split(',')
        # Se recorren los predecesores guardaddos sin "," para ver si existen
        for id in pred_sin_coma:
            # Si el predecesor existe o uno de ellos tiene como predecesor vacío ""
            if id in ids or id == '':
                # No pasa nda
                # Si el predecesor es vacío
                if id == '':
                    # Se suma uno a la varibale para validar si hay más de dos nodos inicio
                    num_starts += 1
            else:
                # Si el predecesor no exite
                messagebox.showerror('Error en archivo de disco', 'El id del predecesor no existe. Arregle el archivo txt y vuelva a presionar el botón.')
                return False

    # Para verificar si hay más de un nodo inicio o si NO existe
    # Si la varibale para validar si hay más de dos nodos inicio es mayor a 1 es que hay dos
    if num_starts > 1:
        # Por ello se lanza el siguiente mensaje
        messagebox.showerror('Error en archivo de disco', 'En su archivo hay más de una actividad inicio y eso no es posible. Arregle el archivo txt y vuelva a presionar el botón.')
        return False
    # Si la varibale para validar si hay más de dos nodos inicio es mayor a 0, eso quiere decir que No hay nodo inicio
    elif num_starts == 0:
        # Por ello se lanza el siguiente mensaje
        messagebox.showerror('Error en archivo de disco', 'No hay una actividad inicio. Arregle el archivo txt y vuelva a presionar el botón.')
        return False

    return True


# Función para crear el grafo a partir de la información del txt
def create():
    # Varibales
    global graph
    graph = Graph()
    global nodesId
    global activities
    nodesId = []
    global start
    global end
    auxiliaryArray = []
    global num_nodes

    # Se recorre las actividades para agregarlas al grafo
    for activity in activities:
        # Primero se guardan separados los predecesores sin las "," de la actividad
        predecessors = activity[3].split(',')
        # Si la actividad tiene un predecesor vacío
        if predecessors[0] == '':
            # Se guarda que esa es la actividad/nodo de inicio
            start = activity[0]
        # Y se guarda la actividad en una nueva lista
        nodesId.append(activity[0])

        # Se recorren los predecesores para revisar si existe el predecesor.
        for pred in predecessors:
            # Si no es así
            if pred not in nodesId and pred != '':
                messagebox.showerror('Error en archivo de disco', 
                    'Error, no existe la actividad ' + pred + ', revise que en el archivo TXT esté ingresando todas las actividades y en orden y vuelva a presionar el botón.')

        # Se añade la actividad, con toda la información respectiva, en un grafo
        graph.add_node(activity[0], activity[1], float(activity[2]), predecessors)
        # Se suma el contador de nodos/actividades que existen
        num_nodes += 1

    # Se guarda en un array aux. los predecesores
    for i in nodesId:
        for j in graph.nodes_dict[i].pred:
            if j not in auxiliaryArray:
                auxiliaryArray.append(j)

    # Se guardan todas las actividades
    setAll = set(nodesId)
    # Se guardan todos los predecesores
    setPred = set(auxiliaryArray)
    # Se guarda el nodo que es la última actividad
    setLast = (setAll - setPred)
    end = list(setLast)[0]

    # Se retorna el grafo con las actividades
    return graph


# Método de la Ruta Crítica
def cpm(graphVal: Graph):
    # Variables
    alterNodesId: list = []
    arrayQueue: list = []
    graphX: Graph = graphVal
    global num_holg

    # Array auxiliar con las actividades
    for node in nodesId:
        alterNodesId.append(node)


    # Haciendo el Forward Pass:

    # Se saca del array la actividad inicial
    alterNodesId.pop(0)
    # Y se calcula -de la actividad inicial- su EF mediante la suma de: su ES que es 0 y su duración
    graphX.nodes_dict[start].ef += graphX.nodes_dict[start].duration

    # Ahora se recorre el array auxiliar con el resto de las actividades
    for i in alterNodesId:
        # Si el predecesor es igual al nodo inicio
        if graphX.nodes_dict[i].pred[0] == start:
            # Se guarda en una lista auxiliar arrayQueue
            arrayQueue.append(graphX.nodes_dict[i].id)

    # Si esa lista auxiliar -arrayQueue- es diferente a cero, o sea, hay predecesores, se hace
    while len(arrayQueue) != 0:

        # Lista aux. de los nodos predecesores
        predNodes: list = []
        # Se guarda en la actividad que se esta trabajando y se saca de la lista auxiliar
        actual = arrayQueue.pop()
        # Se guarda en una lista auxiliar los predecesores del nodo en que se está trabajando
        predNodes = graphX.nodes_dict[actual].pred
        # Bandera
        valid = True

        # Si la lista de los predecesores de la actividad con la que se trabaja es igual a cero no se continúa más
        for k in predNodes:
            if graphX.nodes_dict[k].ef == 0:
                valid = False
                break
        # En el caso contrario
        if valid:
            # Variable para guardar el máximo EF
            maxEF = 0
            # De los nodos predecesores se revisa si es mayor a maxEF y se guarda
            for n in predNodes:
                if graphX.nodes_dict[n].ef > maxEF:
                    maxEF = graphX.nodes_dict[n].ef
            # Ahora, en base a lo anterior, se calcula el EF y el EF respectivo de la actividad en la que se trabaja
            graphX.nodes_dict[actual].es = maxEF
            graphX.nodes_dict[actual].ef = graphX.nodes_dict[actual].es + graphX.nodes_dict[actual].duration

            # Si la actividad con la que se esta trabajando es predecesora de otro se guarda
            for l in alterNodesId:
                if actual in graphX.nodes_dict[l].pred:
                    arrayQueue.append(l)


    # Haciendo el Backward Pass:

    # En una lista aux se guardan los predecesores del nodo/actividad final
    firstList = graphX.nodes_dict[end].pred

    # Ahora, de la actividad final se calcula su respectivo LF y LS
    graphX.nodes_dict[end].lf = graphX.nodes_dict[end].ef
    graphX.nodes_dict[end].ls = graphX.nodes_dict[end].lf - graphX.nodes_dict[end].duration

    # Se crea lista auxiliar sin el nodo final
    indexA = alterNodesId.index(end)
    alterNodesId.pop(indexA)

    # Se guarda en una lista auxiliar los predecesores de la actividad
    for j in firstList:
        arrayQueue.append(j)
        index = alterNodesId.index(j)
        alterNodesId.pop(index)

    # Si el tamaño de la lista auxiliar los predecesores de la actividad es diferente a 0, se hace
    while len(arrayQueue) != 0:

        # Se crean listas auxiliares de predecesores y sucesores
        predNodes: list = []
        sucNodes: list = []
        # Se guarda el nodo con el que se trabajará y se saca de la lista aux
        actual = arrayQueue.pop(0)

        # si el nodo con el que se trabaja esta en la lista auxiliar de los predecesores
        if actual in firstList:
            # Variables
            maxEfbP = 0
            # Se calcula el LF y el LS de la actividad
            for i in firstList:
                if graphX.nodes_dict[i].ef > maxEfbP:
                    maxEfbP = graphX.nodes_dict[i].ef
            graphX.nodes_dict[actual].lf = maxEfbP
            graphX.nodes_dict[actual].ls = maxEfbP - graphX.nodes_dict[actual].duration

            # Se buscan los predecesores de la actividad con la que se trabaja y se agregan a la lista aux
            for i in graphX.nodes_dict[actual].pred:
                if i not in arrayQueue:
                    arrayQueue.append(i)

        # Si no es así
        else:
            # Se recorre la lista de las actividades y se guarda la actividad actual como sucesor
            for i in nodesId:
                if actual in graphX.nodes_dict[i].pred:
                    sucNodes.append(i)
            # Bandera
            valid = True

            # Si el LS del sucesor es cero break
            for j in sucNodes:
                if graphX.nodes_dict[j].ls == 0:
                    valid = False
                    break

            if valid:
                # Variable
                minLS = 99999999999999999
                # Del nodo se saca se respectivo LS y LF
                for i in sucNodes:
                    if graphX.nodes_dict[i].ls < minLS:
                        minLS = graphX.nodes_dict[i].ls
                graphX.nodes_dict[actual].lf = minLS
                graphX.nodes_dict[actual].ls = graphX.nodes_dict[actual].lf - graphX.nodes_dict[actual].duration

                # Si hay predecesores en la actividad y no estan en la lista aux se agregan
                for j in graphX.nodes_dict[actual].pred:
                    if j != 0 and j not in arrayQueue:
                        arrayQueue.append(j)


    # Calculando las Holguras:

    # Se recorre la lista con las actividades
    for i in nodesId:
        # Se calcula la holguna restando LS-ES
        holg = graphX.nodes_dict[i].ls - graphX.nodes_dict[i].es
        # Si la holgura es diferente de 0
        if holg != 0:
            # Se guarda la actividad que tiene holgura
            graphX.nodes_dict[i].holgura = holg
        # Si no es así
        else:
            # Se aumenta el contador de cantidad de actividades sin holgura
            num_holg += 1

    # Se crea una lista para las actividades que tienen holgura
    nodosHolguraId = []

    # Se recorre la lista con las actividades
    for m in nodesId:
        # Si la holgura es diferente de 0
        if graphX.nodes_dict[m].holgura != 0:
            # Se guarda la actividad en la lista, ya que tiene holgura
            nodosHolguraId.append(m)


    # Imprimiendo los resultados del Método de la Ruta Crítica:

    path = []
    startList = []
    inicio = ""
    final = ""
    auxiliaryArray: list = []
    actualId = ""
    loop = True
    path.append(start)

    # Se recorre la lista de las actividades
    for i in nodesId:
        # Si el nodo es diferente al inicial
        if i != start:
            # Y si el predecesor es igual al inicio
            if graphX.nodes_dict[i].pred[0] == start:
                # Se agrega a la lista aux
                startList.append(i)

    # Se recorre la lista aux de las actividades
    for i in alterNodesId:
        # Se recorren los predecesores
        for j in graphX.nodes_dict[i].pred:
            # Si no se encuntra se agrega a la lista aux
            if j not in auxiliaryArray:
                auxiliaryArray.append(j)

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

        if len(sucChoose) != 0:
            for i in sucChoose:
                if graphX.nodes_dict[i].holgura == 0:
                    actualId = i
        else:
            final = actualId
            loop = False

    pathStr = ""
    totalDuration = graphX.nodes_dict[end].lf
    for i in path:
        if i != path[len(path) - 1]:
            pathStr += i + " ==> "
        else:
            pathStr += i

    Texto_holg=''
    Texto_holg_2=''

    if num_holg == num_nodes:
        Texto_holg='En este proyecto todas las actividades son críticas.'
        Texto_holg_2='Una posible ruta crítica puede ser la siguiente:'
    else:
        Texto_holg='                                                                                                                                            '
        Texto_holg_2='                                                                                                                                                 '
    
    Label(homeFrame, text=Texto_holg, fg="#000000", font=("Roboto", 12, "bold"), bg="#f0ebe7").place(x="550", y="435")
    Label(homeFrame, text=Texto_holg_2, fg="#000000", font=("Roboto", 12, "bold"), bg="#f0ebe7").place(x="550", y="458")

    #Mensaje Ruta Crítica
    ruta_critica='Ruta Crítica del Proyecto: '+ str(pathStr)
    Label(homeFrame, text=ruta_critica, fg="#000000", font=("Roboto", 12, "bold"), bg="#f0ebe7").place(x="550", y="485")
    #Mensaje Tiempo de duración
    ruta_critica='Tiempo de Duración del Proyecto: '+ str(totalDuration)
    Label(homeFrame, text=ruta_critica, fg="#000000", font=("Roboto", 12, "bold"), bg="#f0ebe7").place(x="550", y="510")
    #Mensaje de la Actividad Inicial
    actividad_inicial='Actividad Inicial del Proyecto: '+ str(graphX.nodes_dict[start].description)
    Label(homeFrame, text=actividad_inicial, fg="#000000", font=("Roboto", 12, "bold"), bg="#f0ebe7").place(x="550", y="535")
    #Mensaje de la Actividad Final
    actividad_inicial='Actividad Final del Proyecto: '+ str(graphX.nodes_dict[end].description)
    Label(homeFrame, text=actividad_inicial, fg="#000000", font=("Roboto", 12, "bold"), bg="#f0ebe7").place(x="550", y="565")

    # Dibujo del Método de la Ruta Crítica:

    #Configuración de la figura a generar del grafo en la interfaz
    figure= plt.figure(figsize=(4.5, 4.5), dpi=100)
    plt.axis('off')
    subplot= figure.add_subplot(111)

    #Variables
    global graphX1
    graphX1 = graphX
    fromList = []
    toList = []
    flag = False

    for i in nodesId:
        if flag:
            for j in graphX.nodes_dict[i].pred:
                fromList.append(j)
                toList.append(i)
        flag = True
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

    values = [('blue' if node == start or node == end else 'grey') for node in G.nodes()]

    nx.drawing.nx_pylab.draw_networkx (G,  arrows=True, with_labels=True, edgelist=edgesList, edge_color=colorList, node_size = 900, node_color = values)

   
    #Colocando el dibujo en la ventana de Tkinter
    canvas = FigureCanvasTkAgg(figure,master=home)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, home)
    toolbar.update()
    canvas.get_tk_widget().place(x="50", y="210")


   #Imprimiendo datos de las actividades en tabla     
    tabla: Treeview
    tabla = Treeview(homeFrame)
    tabla['columns'] = ('Actividad', 'Descripción', 'Duración', 'ES', 'EF', 'LS', 'LF', 'Holgura')


#Función para generar tabla con los datos de las actividades del Archivo TXT
def create_table(grafo):

    #Variables
    global tabla
    global nodesId
    j = 0

    #Creando tabla
    tabla = Treeview(homeFrame)
    tabla['columns'] = ('Actividad', 'Descripción', 'Duración', 'ES', 'EF', 'LS', 'LF', 'Holgura')
    tabla.column("#0", width=0,  stretch=NO)
    tabla.column("Actividad",anchor=CENTER, width=80)
    tabla.column("Descripción",anchor=CENTER,width=150)
    tabla.column("Duración",anchor=CENTER,width=80)
    tabla.column("ES",anchor=CENTER,width=80)
    tabla.column("EF",anchor=CENTER,width=80)
    tabla.column("LS",anchor=CENTER,width=80)
    tabla.column("LF",anchor=CENTER,width=80)
    tabla.column("Holgura",anchor=CENTER,width=80)

    tabla.heading("#0",text="",anchor=CENTER)
    tabla.heading("Actividad",text="Actividad",anchor=CENTER)
    tabla.heading("Descripción",text="Descripción",anchor=CENTER)
    tabla.heading("Duración",text="Duración",anchor=CENTER)
    tabla.heading("ES",text="ES",anchor=CENTER)
    tabla.heading("EF",text="EF",anchor=CENTER)
    tabla.heading("LS",text="LS",anchor=CENTER)
    tabla.heading("LF",text="LF",anchor=CENTER)
    tabla.heading("Holgura",text="Holgura",anchor=CENTER)

    #Rellenando tabla
    for i in nodesId:
        tabla.insert(parent='',index='end',iid=j,text='', values=(str(grafo.nodes_dict[i].id),str(grafo.nodes_dict[i].description),str(grafo.nodes_dict[i].duration),str(grafo.nodes_dict[i].es),str(grafo.nodes_dict[i].ef), str(grafo.nodes_dict[i].ls), str(grafo.nodes_dict[i].lf), str(grafo.nodes_dict[i].holgura)))
        j += 1

    #Ubicando la tabla en la interfaz
    tabla.pack()
    tabla.place(x="550", y="210") 


# Main
def ejecucionCPM():

    #Variables
    global nodesId
    nodesId = []
    global activities
    activities = []
    global start
    start = ''
    global end
    end = ''
    global num_nodes
    num_nodes = 0
    global num_holg
    num_holg = 0

    # Se lee el archivo TXT
    read_file()
    # Se valida el archivo TXT
    valid = validate_txt(activities)

    # Si es valido, ejecuta el programa
    if valid:
        #Se crea el grafo
        graph = create()
        #Se ejecuta la ruta crítica
        cpm(graph)
        #Se crea la tabla
        create_table(graph)

    # Si no es valido, indica error
    else:

        print('Txt malo')


#BTN
botonComenzar = Button(homeFrame, text="Calcular Ruta Crítica", width=25,height=1, bg="#B6CBDE", font=("Roboto", 10, "bold"), command=ejecucionCPM).place(x="625", y="180", anchor="center")


home.mainloop()
