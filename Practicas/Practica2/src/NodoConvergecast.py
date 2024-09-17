import simpy
from Nodo import Nodo
from Canales.CanalConvergecast import *

TICK = 1

class NodoConvergecast(Nodo):
    
    ''' Implementa la interfaz de Nodo para el algoritmo de convergecast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        '''
        Inicializa un nodo de Convergecast.
        '''
        self.id_nodo = id_nodo
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.vecinos = vecinos
        
        #Atributos propios del algoritmo
        self.padre = None            
        self.hijos = []    
        self.valor = self.id_nodo   
        self.val_set = set()        
        self.val_set.add((self.id_nodo, self.valor))  
        self.esperando_de = set()   # Conjunto de nodos de los cuales se espera recibir mensajes

    def convergecast(self, env):
        '''
        Implementa el algoritmo de Convergecast para el nodo.
        :param env: Entorno de simulación de SimPy.
        '''
        
        #Lineas 1-7 del pseudocodigo
        if not self.hijos:
            # El algoritmo lo comienza todo nodo hoja (sin hijos)
            yield env.timeout(TICK)  # Espera un tiempo antes de enviar el mensaje
            mensaje = ("BACK", self.id_nodo, self.val_set) 
            self.canal_salida.envia(mensaje, [self.padre])
        else:
            # Nodo interno: espera mensajes de todos los hijos
            self.esperando_de = set(self.hijos)
            while self.esperando_de:
                # Espera un mensaje de los canales de entrada
                mensaje = yield self.canal_entrada.get()
                
                #Lineas 8-16 pseudocodigo
                if mensaje[0] == "BACK":
                    sender_id = mensaje[1]              #id del nodo que acaba de mandar el mensaje
                    val_set_hijo = mensaje[2]           #Conjunto de valores que el hijo ha acumulado hasta ese momento
                    self.val_set.update(val_set_hijo)  
                    self.esperando_de.remove(sender_id)  

            # Una vez recibidos todos los mensajes de los hijos
            #Linea 11 del pseudocodigo
            if self.padre != self.id_nodo:
                yield env.timeout(TICK)  # Espera un tiempo antes de enviar el mensaje al padre
                mensaje = ("BACK", self.id_nodo, self.val_set)  # Mensaje para enviar al padre
                self.canal_salida.envia(mensaje, [self.padre])
            else:
                # Nodo raíz: procesa los valores recibidos
                self.procesar_val_set()

    def procesar_val_set(self):
        '''
        Procesa el conjunto de valores en el nodo raíz.

        Calcula el valor total sumando los valores de todos los nodos y lo imprime.
        '''
        resultado = sum(val for _, val in self.val_set)
        print(f"Nodo raíz {self.id_nodo} ha procesado el valor total: {resultado}")
