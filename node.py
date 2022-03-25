#Clase nodo
class  Node:

    def __init__(self, id: str or int, description: str, duration: float, predecesores: list) -> None:
        #Id de la actividad
        self.id = id
        #Descripción de la actividad
        self.description = description
        #Duración de la actividad
        self.duration = duration
        #Predecesores de la actividad
        self.pred = predecesores
        #Sucesores
        self.suces = []
        #Visitados
        self.visitedForward = False
        self.visitedBackward = False
        #Variables de ES, EF, LS y lF
        self.es = 0 
        self.ef = 0
        self.ls = 0
        self.lf = 0
        #Holgura
        self.holgura = 0

    #Funciones para definir/colocar los datos deseados actualizados -dependiendo del grafo-
    def visitForward (self):
        self.visitedForward = True

    def visitBackward (self):
        self.visitedBackward = True

    def add_predecesor (self, pred: str):
        self.pred.append(pred)

    def add_sucesor (self, suc:str):
        self.suces.append(suc)

    def set_description(self, description: str):
        self.description = description
    
    def set_duration(self, duration: float):
        self.duration = duration

    def set_es(self, es: float):
        self.es = es

    def set_ef(self, ef: float):
        self.ef = ef

    def set_ls(self, ls: float):
        self.ls = ls

    def set_lf(self, lf: float):
        self.lf = lf

    def set_holgura(self, holgura: int):
        self.holgura = holgura
