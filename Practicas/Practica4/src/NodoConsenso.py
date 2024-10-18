import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoConsenso(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Consenso.'''
    '''
    Atributos:
        id_nodo (int): Identificador único del nodo.
        vecinos (list): Lista de nodos vecinos a los cuales el nodo puede enviar mensajes.
        canal_entrada (Canal): Canal por donde recibe mensajes.
        canal_salida (Canal): Canal por donde envía mensajes.
        V (list): Lista que almacena el estado del conocimiento sobre los nodos.
        New (set): Conjunto de nuevos mensajes recibidos en cada ronda de comunicación.
        rec_from (list): Lista para registrar los mensajes recibidos de cada nodo.
        fallare (bool): Indica si el nodo está programado para fallar.
        lider (int): Identificador del nodo líder elegido.
    '''
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
        Returns:
            int: El identificador del nodo líder una vez que se alcanza el consenso.
        '''
        ultima_ronda = f + 1

        # Si el nodo tiene nuevos mensajes que compartir
        while True:
            # Si el id del nodo actual es menor al número máximo de fallos
            if self.id_nodo < f:
                self.fallare = True
                break

            # Si el nodo tiene nuevos mensajes que compartir
            if len(self.New) != 0:
                yield env.timeout(TICK) # Espera un tick antes de enviar los mensajes
                # Envía los mensajes nuevos a sus vecinos
                self.canal_salida.envia([self.id_nodo, self.New], self.vecinos)

            # Si ha alcanzado la última ronda, recopila mensajes de los vecinos
            if env.now == ultima_ronda:
                for _ in range(len(self.vecinos)):  # Esperaramos por un mensaje de algún vecino
                    msg = yield self.canal_entrada.get()
                    id_nodo_mensajero = msg[0]
                    self.rec_from[id_nodo_mensajero] = msg
                
                self.New = set([])  # Vaciamos el conjunto de mensajes nuevos
                
                # Procesa los mensajes recibidos de los vecinos
                for i in range(len(self.rec_from)):
                    if i != self.id_nodo and self.rec_from[i] is not None:
                        mensaje_vecino = self.rec_from[i]
                        # Actualiza el conocimiento si hay nodos que no conocía
                        for y in mensaje_vecino[1]:
                            if self.V[y] is None:
                                self.V[y] = y
                                self.New.add(y)
                
                # Después de la última ronda, selecciona un líder
                if env.now == ultima_ronda:
                        # El primer nodo conocido que no es None se convierte en el líder
                        for elem in self.V:
                            if elem != None:
                                self.lider = elem
                                return elem  # Retorna el identificador del líder
