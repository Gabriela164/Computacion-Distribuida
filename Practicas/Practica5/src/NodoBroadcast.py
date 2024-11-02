import simpy
from Nodo import *
from Canales.CanalRecorridos import *
from random import randint

#El tiempo de espera ahora sera de entre 1 a 5 segundos (de forma aleatoria)
TICK = randint(1, 5)

class NodoBroadcast(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast con reloj de Lamport.'''
    def __init__(self, id_nodo: int, vecinos: list, canal_entrada: simpy.Store,
                 canal_salida: simpy.Store):
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.mensaje = None
        self.reloj = 0
        self.eventos = []
        self.data = "mensaje"

    def broadcast(self, env: simpy.Environment, data="Mensaje"):
        ''' Algoritmo de Broadcast. Desde el nodo distinguido (0) vamos a enviar un mensaje a todos los demás nodos.'''
        if self.id_nodo == 0:  # Solo el nodo raíz (id = 0) distribuye el mensaje. 
            
            for k in self.vecinos:
                yield env.timeout(TICK)
                self.reloj += 1   
                #Guardamos cada evento ocurrido: E, es decir, cada envio de mensaje a cada vecino del nodo 0.  
                self.eventos.append([self.reloj, 'E', self.data, self.id_nodo,k])
                #Tambien se mandara el reloj de cada nodo que envie un mensaje
                self.canal_salida.envia([self.id_nodo, self.data, self.reloj], [k])
            
        while True:
            yield env.timeout(TICK)
            
            #Capturamos el mensaje recibido: El id del nodo emisor, el contenido del mensaje, el reloj del nodo emisor. 
            nodo_emisor, data, reloj_m = yield self.canal_entrada.get()
            # Actualizamos el reloj Lamport 
            self.reloj = max(reloj_m, self.reloj) + 1
            #Guardamos el evento ocurrido: R, es decir, se recibio un mensaje de otro nodo. 
            self.eventos.append([self.reloj, 'R', self.data, nodo_emisor, self.id_nodo])

            yield env.timeout(TICK)

            for k in self.vecinos:  
                self.reloj += 1     
                #Guardamos cada evento ocurrido: E, es decir, cada envio de mensaje a cada vecino del nodo actual.             
                self.eventos.append([self.reloj, 'E', self.data, self.id_nodo, k])
                self.canal_salida.envia([self.id_nodo, self.data, self.reloj], [k])

