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
        self.vecinos = set(vecinos)
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        
        #Atributos propios del algoritmo BFS
        self.padre = None if id_nodo != 0 else id_nodo #Si es nodo raíz 0 se asigna así mismo como el nodo padre 
        self.hijos = list()
        self.distancia = float('inf') if id_nodo != 0 else 0 #La distancia es -1 si se trata del nodo raíz 0
        self.msj_esperados = 0
        self.nivel = 0


    def bfs(self, env):
        ''' Algoritmo BFS. '''
        if self.id_nodo == 0:  #Si somos el nodo raíz
            self.padre = self.id_nodo
            self.distancia = 0
            yield env.timeout(TICK)
            self.canal_salida.envia(["GO",self.id_nodo,self.distancia],self.vecinos)
            
        while True:
            #Esperamos un mensaje 
            mensaje = yield self.canal_entrada.get()
            
            nodo_mensajero = mensaje[1]
            distancia_recorrida = mensaje[2] 
            
            if mensaje[0] == "GO": 
                if(self.padre == None):
                    self.padre = nodo_mensajero
                    self.hijos.clear()
                    self.nivel = distancia_recorrida + 1
                    self.msj_esperados = len(self.vecinos) - 1   
                    self.distancia = distancia_recorrida + 1
                    resp = "yes"
                    
                    if(self.msj_esperados == 0):    
                        yield env.timeout(TICK)
                        self.canal_salida.envia(["BACK",self.id_nodo,self.distancia,self.nivel,resp],[self.padre])
                    else:
                        yield env.timeout(TICK)
                        self.canal_salida.envia(["GO",self.id_nodo,self.distancia],[v for v in self.vecinos if v!= self.padre])
                else:
                    if (self.nivel > distancia_recorrida + 1):
                        self.padre = nodo_mensajero
                        self.hijos.clear()
                        self.nivel = distancia_recorrida + 1
                        self.msj_esperados = len(self.vecinos) - 1   
                        if(self.msj_esperados == 0):
                            yield env.timeout(TICK)
                            self.canal_salida.envia(["BACK",self.id_nodo,self.distancia,self.nivel,resp],[self.padre])
                        else:
                            yield env.timeout(TICK)
                            self.canal_salida.envia(["GO",self.id_nodo,self.distancia],[v for v in self.vecinos if v!= self.padre])
                    else:
                        resp ="no"
                        yield env.timeout(TICK)
                        self.canal_salida.envia(["BACK",self.id_nodo,self.distancia,self.nivel,resp],[nodo_mensajero])
                                                   
            elif mensaje[0] == "BACK":
    
                nivel_mensaje = mensaje[3]
                resp = mensaje[4]
                
                if(distancia_recorrida == self.nivel+1):
                    self.msj_esperados = self.msj_esperados - 1
                    if(resp == "yes"):
                        self.hijos.append(nodo_mensajero)
                        if(self.msj_esperados == 0):
                            if(self.padre != self.id_nodo):
                                resp = "yes"
                                yield env.timeout(TICK)
                                self.canal_salida.envia(["BACK",self.id_nodo,self.distancia,self.nivel,resp],[self.padre])
                            else:
                                print("El nodo raíz sabe que el algoritmo BFS ha terminado")
                                break
                            
                                
                            
                                
                    
                    

        
