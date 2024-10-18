import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoConsenso(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Consenso.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo de consenso. '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        
        # Atributos extra
        self.V = [None] * (len(vecinos) + 1) # Llenamos la lista de Nodos
        self.V[id_nodo] = id_nodo
        self.New = set([id_nodo]) #Conjunto de mensajes 
        self.rec_from = [None] * (len(vecinos) + 1)
        self.fallare = False      # Colocaremos esta en True si el nodo fallará
        self.lider = None         # La elección del lider.
    
    def consenso(self, env, f):
        '''
        Implementa el algoritmo de consenso
        Args: 
            env (simpy.Environment): Entorno de simulación
            f (int): Numero de procesos que fallan
        '''
        ultima_ronda = f + 1

        while True:
            # Si el id del nodo actual es menor al número máximo de fallos
            if self.id_nodo < f:
                self.fallare = True
                break

            if len(self.New) != 0:
                yield env.timeout(TICK)
                self.canal_salida.envia([self.id_nodo, self.New], self.vecinos)
            
            if env.now == ultima_ronda:
                for _ in range(len(self.vecinos)):  # Esperaramos por un mensaje de algún vecino
                    msg = yield self.canal_entrada.get()
                    id_nodo_mensajero = msg[0]
                    self.rec_from[id_nodo_mensajero] = msg
                
                self.New = set([])  # Vaciamos el conjunto de mensajes nuevos
                
                for i in range(len(self.rec_from)):
                    if i != self.id_nodo and self.rec_from[i] is not None:
                        mensaje_vecino = self.rec_from[i]
                        for y in mensaje_vecino[1]:
                            if self.V[y] is None:
                                self.V[y] = y
                                self.New.add(y)
                
                if env.now == ultima_ronda:
                        for elem in self.V:
                            if elem != None:
                                self.lider = elem
                                return elem  
