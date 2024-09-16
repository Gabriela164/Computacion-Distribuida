import simpy
from Canales import CanalBroadcast
from Nodo import *

TICK = 1

class NodoGenerador(Nodo):
    
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        
        # Atributos propios del algoritmo
        self.padre = None if id_nodo != 0 else id_nodo # Si es el nodo distinguido, el padre es el mismo 
        self.hijos = list()
        self.mensajes_esperados = len(vecinos) # Cantidad de mensajes que esperamos
        
    def genera_arbol(self, env):
        '''Implementa el algoritmo de construir un árbol generador'''

        # Lineas del algoritmo 1-10
        if self.id_nodo == 0:  # Si soy el nodo distinguido
            yield env.timeout(TICK)
            self.padre = 0
            self.mensajes_esperados = len(self.vecinos)
            
            #linea  5
            self.canal_salida.envia(["GO", self.id_nodo], self.vecinos)
        
        # Lineas 11-22 del pseudocodigo
        while True: 
            #Esperamos mensajes 
            mensaje = yield self.canal_entrada.get()
            
            #SI SE RECIBE UN MENSAJE GO
            if mensaje[0] == "GO":
                if self.padre == None: #Si aun NO tiene un padre asignado 
                    self.padre = mensaje[1] # Asignamos como nodo padre al nodo quien envio el mensaje GO
                    self.mensajes_esperados = len(self.vecinos) - 1
                    
                    if self.mensajes_esperados == 0:
                        yield env.timeout(TICK)
                        #Enviamos un mensaje con back al nodo que precviamente le mando msj y que sabemos se convirtio en su padre
                        self.canal_salida.envia(["BACK", self.id_nodo], [self.padre])
                    else:
                        yield env.timeout(TICK)
                        #Continuamos enviado mensaje GO a sus demas vecinos (a excepcion del nodo pj que le mando el mensaje)
                        self.canal_salida.envia(["GO", self.id_nodo], [v for v in self.vecinos if v!= self.padre])
                else:
                    #Si ya tiene un nodo asignado 
                    yield env.timeout(TICK)
                    # -1 indica que ya se ha asignado un nodo padre al nodo que previamente le habia mandado msj con GO 
                    self.canal_salida.envia(["BACK", -1], [mensaje[1]])
                        
            
            #lineas 23-33 del pseudocodigo
            #SI SE RECIBE UN MENSAJE BACK
            elif mensaje[0] == "BACK":
                self.mensajes_esperados -= 1
                
                if mensaje[1] != -1:
                    #el nodo que envio el mensaje back, es hijo del nodo actual
                    self.hijos.append(mensaje[1]) 
                    
                if self.mensajes_esperados == 0:
                    if self.padre != self.id_nodo: #Si el nodo actual no es su propio nodo padre
                        yield env.timeout(TICK)
                        #Continuamos mandando mensajes a los nodos padres, hasta llegar al nodo distinguido
                        self.canal_salida.envia(["BACK", self.id_nodo], [self.padre])
                    else:
                        print("El nodo distinguido recibio el ultimo mensaje back. Se ha terminado de construir el arbol generador.")
                        break