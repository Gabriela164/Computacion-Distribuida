import simpy
from Nodo import Nodo

TICK = 1

class NodoConvergecast(Nodo):
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        '''
        Inicializa un nodo de Convergecast.

        :param id_nodo: Identificador único del nodo.
        :param vecinos: Lista de IDs de nodos vecinos.
        :param canal_entrada: Canal de entrada para recibir mensajes.
        :param canal_salida: Canal de salida para enviar mensajes.
        '''
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
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
        if not self.hijos:
            # Caso base: nodo hoja (sin hijos)
            yield env.timeout(TICK)  # Espera un tiempo antes de enviar el mensaje
            mensaje = ("BACK", self.id_nodo, self.val_set) 
            self.canal_salida.envia(mensaje, [self.padre])
        else:
            # Nodo interno: espera mensajes de todos los hijos
            self.esperando_de = set(self.hijos)
            while self.esperando_de:
                # Espera un mensaje de los canales de entrada
                mensaje = yield self.canal_entrada.get()
                if mensaje[0] == "BACK":
                    sender_id = mensaje[1]  
                    val_set_hijo = mensaje[2]  
                    self.val_set.update(val_set_hijo)  
                    self.esperando_de.remove(sender_id)  

            # Una vez recibidos todos los mensajes de los hijos
            if self.padre is not None:
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
