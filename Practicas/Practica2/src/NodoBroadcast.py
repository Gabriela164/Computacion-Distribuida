import simpy
import time
from Nodo import *
from Canales.CanalBroadcast import *

# La unidad de tiempo
TICK = 1

class NodoBroadcast(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, mensaje=None):
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.mensaje = mensaje

    def broadcast(self, env):
        ''' Algoritmo de Broadcast. Desde el nodo distinguido (0)
            vamos a enviar un mensaje a todos los demás nodos.'''
        if self.mensaje and self.id_nodo == 0: #  Si es el nodo distinguido (0)
            # mensaje que se quiere difundir
            print(f'tiempo {env.now}: Nodo {self.id_nodo} envia mensaje "{self.mensaje}"' ) 
            # linea 5 del codigo
            for vecino in self.vecinos:
                self.canal_salida.envia((self.id_nodo, self.mensaje), vecino)

        while True:
            # el nodo espera el mensaje del nodo_emisor 
            mensaje = yield self.canal_entrada.get()
            nodo_emisor, contenido = mensaje # recibe el contenido del mensaje y quien lo envio 
            if nodo_emisor not in self.recibido:
                self.recibido.add(nodo_emisor) # si el nodo_emisor ya recibio el mensaje se guarda para que no lo vuelva a recibir 
                print(f'Tiempo {env.now}: Nodo {self.id_nodo} ya recibió el mensaje "{contenido}" del Nodo {nodo_emisor}')

                # Reenvía el mensaje a sus vecinos excepto al nodo_emisor
                for vecino in self.vecinos:
                    if vecino != nodo_emisor:  # Exentamos al nodo_emisor para evitar un duplicado de mensajes en el mismo nodo
                        self.canal_salida.envia((self.id_nodo, contenido), vecino)
            
            yield env.timeout(TICK)  # Usamos yield env.timeout para el tiempo de procesamiento
