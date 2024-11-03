import simpy
from Nodo import *
from Canales.CanalRecorridos import *
from random import randint

TICK = 1

class NodoDFS(Nodo):
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, num_nodos):
        """
        Inicializa un nodo en el algoritmo DFS.

        Args:
            id_nodo (int): Identificador único del nodo.
            vecinos (list): Lista de nodos adyacentes (vecinos) de este nodo.
            canal_entrada (Canal): Canal de entrada para recibir mensajes.
            canal_salida (Canal): Canal de salida para enviar mensajes.
            num_nodos (int): Número total de nodos en la red, utilizado para inicializar el reloj vectorial.
        """
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.padre = self.id_nodo       
        self.hijos = []                 
        self.eventos = []              
        self.reloj = [0] * num_nodos    
        self.visitados = set()        

    def registrar_evento(self, tipo, visitados, remitente, receptor):
        """
        Registra un evento en el nodo, incluyendo el reloj vectorial y el conjunto de nodos visitados.

        Args:
            tipo (str): Tipo de evento, 'E' para envío y 'R' para recepción.
            visitados (set): Conjunto de nodos visitados hasta el momento del evento.
            remitente (int): ID del nodo que envía el mensaje.
            receptor (int): ID del nodo que recibe el mensaje.
        """
        # Guarda el estado actual del reloj vectorial y convierte 'visitados' a un frozenset para que sea hashable.
        evento = (self.reloj.copy(), tipo, frozenset(visitados), remitente, receptor)
        self.eventos.append(evento)

    def dfs(self, env):
        """
        Realiza el recorrido DFS asíncrono en una red de nodos distribuidos, utilizando SimPy para la simulación.

        Args:
            env (simpy.Environment): Entorno de simulación de eventos discretos de SimPy.
        """
        # Si el nodo es el nodo raíz (id_nodo == 0), inicia el recorrido DFS.
        if self.id_nodo == 0:
            self.reloj[self.id_nodo] += 1
            self.visitados.add(self.id_nodo)
            k = min(self.vecinos)  # Selecciona el vecino con el menor ID.
            self.registrar_evento('E', self.visitados, self.id_nodo, k)
            yield env.timeout(randint(1, 3))
            self.canal_salida.envia(["GO", self.visitados, self.id_nodo, self.reloj.copy()], [k])
            self.hijos.append(k)

        # Bucle principal para recibir y procesar mensajes.
        while True:
            mensaje = yield self.canal_entrada.get()
            tipo_mensaje, visitados, nodo_mensajero, reloj_mensajero = mensaje

            # Sincroniza el reloj vectorial con el reloj recibido en el mensaje.
            self.reloj = [max(self.reloj[i], reloj_mensajero[i]) for i in range(len(self.reloj))]
            self.reloj[self.id_nodo] += 1
            self.registrar_evento('R', visitados, nodo_mensajero, self.id_nodo)

            # Procesa el mensaje según su tipo.
            if tipo_mensaje == "GO":
                self.padre = nodo_mensajero
                if set(self.vecinos).issubset(visitados):
                    # Si todos los vecinos ya fueron visitados, envía un mensaje "BACK" al nodo padre.
                    visitados.add(self.id_nodo)
                    self.reloj[self.id_nodo] += 1
                    self.registrar_evento('E', visitados, self.id_nodo, nodo_mensajero)
                    yield env.timeout(randint(1, 3))
                    self.canal_salida.envia(["BACK", visitados, self.id_nodo, self.reloj.copy()], [nodo_mensajero])
                    self.hijos.clear()
                else:
                    # Si aún hay vecinos sin visitar, envía un mensaje "GO" al siguiente nodo.
                    k = min(set(self.vecinos).difference(visitados))
                    visitados.add(self.id_nodo)
                    self.reloj[self.id_nodo] += 1
                    self.registrar_evento('E', visitados, self.id_nodo, k)
                    yield env.timeout(randint(1, 3))
                    self.canal_salida.envia(["GO", visitados, self.id_nodo, self.reloj.copy()], [k])
                    self.hijos = [k]

            elif tipo_mensaje == "BACK":
                if set(self.vecinos).issubset(visitados):
                    # Si todos los vecinos fueron visitados y el nodo es la raíz, termina el DFS.
                    if self.padre == self.id_nodo:
                        print("El recorrido DFS ha terminado")
                        break
                    else:
                        # Si el nodo no es la raíz, envía un mensaje "BACK" al nodo padre.
                        self.reloj[self.id_nodo] += 1
                        self.registrar_evento('E', visitados, self.id_nodo, self.padre)
                        yield env.timeout(randint(1, 3))
                        self.canal_salida.envia(["BACK", visitados, self.id_nodo, self.reloj.copy()], [self.padre])
                else:
                    # Si hay vecinos sin visitar, envía un mensaje "GO" al siguiente nodo.
                    k = min(set(self.vecinos).difference(visitados))
                    visitados.add(self.id_nodo)
                    self.reloj[self.id_nodo] += 1
                    self.hijos.append(k)
                    self.registrar_evento('E', visitados, self.id_nodo, k)
                    yield env.timeout(randint(1, 3))
                    self.canal_salida.envia(["GO", visitados, self.id_nodo, self.reloj.copy()], [k])
