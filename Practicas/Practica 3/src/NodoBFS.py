import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoBFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo BFS. '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        
        #Atributos propios del algoritmo BFS
        self.padre = None if id_nodo != 0 else id_nodo #Si es nodo raíz 0 se asigna así mismo como el nodo padre 
        self.hijos = list()
        self.distancia = float('inf') if id_nodo != 0 else 0 #La distancia es 0 si se trata del nodo raíz 0

    def bfs(self, env):
        ''' Algoritmo BFS. '''
        pass

        
