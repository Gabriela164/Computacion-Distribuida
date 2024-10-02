import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoDFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        self.id_nodo = id_nodo
        self.vecinos = set(vecinos) #Lo convertimos en conjunto para poder trabajar con la variable
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        
        #Atributos propios del algoritmo DFS
        self.padre = self.id_nodo
        self.hijos = []
        self.visitados = set()

    def dfs(self, env):
        ''' Algoritmo DFS. '''
        
        #Si somos el nodo distinguido 
        if self.id_nodo == 0:
            
            self.padre = 0  #El nodo raíz se asigna asimismo como el propio nodo padre
            self.visitados.add(self.id_nodo)
            k = min(self.vecinos) #Tomamos k vecino más pequeño

            #Enviaos GO al k vecino 
            yield env.timeout(TICK)
            self.canal_salida.envia(["GO", self.id_nodo, set([self.id_nodo])], [k])
            self.hijos.append(k)
                                
        while True:
            #Esperamos a recibir un mensaje
            mensaje = yield self.canal_entrada.get()
            
            nodo_mensajero = mensaje[1]   #Nodo vecino pj que mando el mensaje
            conj_visitados = mensaje[2]   #Conjunto de nodos marcados como visitados 
            
            if mensaje[0] == "GO":
                self.padre = nodo_mensajero   #Asignamos como nodo padre al nodo que envio el mensaje GO

                #Verificamos si todos los nodos vecinos del nodo actual ya han sido visitados
                if self.vecinos.issubset(conj_visitados):
                    conj_visitados.add(self.id_nodo)
                    #Mandamos mensaje BACK para avisar que se termino de visitar todos los nodos vecinos
                    yield env.timeout(TICK)
                    self.canal_salida.envia(["BACK", self.id_nodo, conj_visitados], [nodo_mensajero])
                    self.hijos.clear() #Vaciamos la lista
                else:
                    #Escogemos un nodo vecino que aún no ha sido visitado
                    k = min(self.vecinos.difference(conj_visitados))
                    conj_visitados.add(self.id_nodo)
                    yield env.timeout(TICK)
                    self.canal_salida.envia(["GO", self.id_nodo, conj_visitados], [k])
                    self.hijos = [k]
                    
            elif mensaje[0] == "BACK":
                #Verificamos si todos los nodos vecinos ya han sido visitados
                if self.vecinos.issubset(conj_visitados):
                    if self.padre == self.id_nodo: #Si es el nodo raíz 
                        print("El recorrido DFS ha terminado")
                        break
                    else:
                        yield env.timeout(TICK)
                        self.canal_salida.envia(["BACK", self.id_nodo, conj_visitados], [self.padre])
                else:
                    k = min(self.vecinos.difference(conj_visitados))
                    conj_visitados.add(self.id_nodo)
                    yield env.timeout(TICK)
                    self.canal_salida.envia(["GO",self.id_nodo, conj_visitados], [k])
                    self.hijos.append(k)
                        
                        
            
                        