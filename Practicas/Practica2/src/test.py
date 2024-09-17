import simpy
from Canales.CanalBroadcast import CanalBroadcast
from Canales.CanalConvergecast import CanalConvergecast
from NodoBroadcast import NodoBroadcast
from NodoGenerador import NodoGenerador
from NodoVecinos import NodoVecinos
from NodoConvergecast import NodoConvergecast

# Las unidades de tiempo que les daremos a las pruebas
TIEMPO_DE_EJECUCION = 50

class TestPractica1:
    ''' Clase para las pruebas unitarias de la práctica 1. '''
    
    # Las aristas de adyacencias de la gráfica.
    adyacencias = [[1, 2], [0, 3], [0, 3, 5], [1, 2, 4], [3, 5], [2, 4]]

    # Aristas de adyacencias del árbol
    adyacencias_arbol = [[1, 2], [3], [5], [4], [], []]

    # Prueba para el algoritmo de conocer a los vecinos de vecinos.
    def test_ejercicio_uno(self):
        ''' Método que prueba el algoritmo de conocer a los vecinos de vecinos. '''
        # Creamos el ambiente y el objeto Canal
        env = simpy.Environment()
        bc_pipe = CanalBroadcast(env)

        # La lista que representa la gráfica
        grafica = []

        # Creamos los nodos
        for i in range(0, len(self.adyacencias)):
            grafica.append(NodoVecinos(i, self.adyacencias[i],
                                       bc_pipe.crea_canal_de_entrada(), bc_pipe))

        # Le decimos al ambiente lo que va a procesar ...
        for nodo in grafica:
            env.process(nodo.conoceVecinos(env))
        # ...y lo corremos
        env.run(until=TIEMPO_DE_EJECUCION)

        # Ahora si, probamos
        identifiers_esperados = [[0, 3, 5], [1, 2, 4],
                                 [1, 2, 4], [0, 3, 5], [1, 2, 4], [0, 3, 5]]
        # Para cada nodo verificamos que su lista de identifiers sea la esperada.
        for i in range(0, len(grafica)):
            nodo = grafica[i]
            assert set(identifiers_esperados[i]) == set(
                nodo.identifiers), ('El nodo %d está mal' % nodo.id_nodo)

    # Prueba para el algoritmo que construye un árbol generador.
    def test_ejercicio_dos(self):
        ''' Prueba para el algoritmo que construye un árbol generador. '''
        # Creamos el ambiente y el objeto Canal
        env = simpy.Environment()
        bc_pipe = CanalBroadcast(env)

        # La lista que representa la gráfica
        grafica = []

        # Creamos los nodos
        for i in range(0, len(self.adyacencias)):
            grafica.append(NodoGenerador(i, self.adyacencias[i],
                                         bc_pipe.crea_canal_de_entrada(), bc_pipe))

        # Le decimos al ambiente lo que va a procesar ...
        for nodo in grafica:
            env.process(nodo.genera_arbol(env))
        # ...y lo corremos
        env.run(until=TIEMPO_DE_EJECUCION)

        # Y probamos que los padres y los hijos sean los correctos.
        padres = [0, 0, 0, 1, 3, 2]
        hijos = [[1, 2], [3], [5], [4], [], []]
        for i in range(0, len(grafica)):
            nodo = grafica[i]
            assert nodo.padre == padres[i], (
                'El nodo %d tiene un padre erróneo' % nodo.id_nodo)
            assert set(nodo.hijos) == set(hijos[i]), ('El nodo %d no tiene a los hijos correctos'
                                                      % nodo.id_nodo)

    # Prueba para el algoritmo de Broadcast.
    def test_ejercicio_tres(self):
        ''' Prueba para el algoritmo de Broadcast. '''
        # Creamos el ambiente y el objeto Canal
        env = simpy.Environment()
        bc_pipe = CanalBroadcast(env)
        # La lista que representa la gráfica
        grafica = []

        # Creamos los nodos
        for i in range(0, len(self.adyacencias)):
            grafica.append(NodoBroadcast(i, self.adyacencias_arbol[i],
                                         bc_pipe.crea_canal_de_entrada(), bc_pipe))

        # Le decimos al ambiente lo que va a procesar ...
        for nodo in grafica:
            env.process(nodo.broadcast(env))
        # ...y lo corremos
        env.run(until=TIEMPO_DE_EJECUCION)

        # Probamos que todos los nodos tengan ya el mensaje
        mensaje_enviado = grafica[0].mensaje
        for nodo in grafica:
            assert mensaje_enviado == nodo.mensaje, (
                'El nodo %d no tiene el mensaje correcto' % nodo.id_nodo)


    # Prueba para el algoritmo de Convergecast.
    def test_ejercicio_cuatro(self):
        ''' Prueba para el algoritmo de Convergecast. '''
        # Creamos el ambiente y el objeto Canal
        env = simpy.Environment()
        capacidad = 10 
        cc_pipe = CanalConvergecast(env, capacidad)

        # La lista que representa el árbol
        grafica = []

        # Creamos los nodos
        for i in range(len(self.adyacencias_arbol)):
            grafica.append(NodoConvergecast(i, self.adyacencias_arbol[i],
                                            cc_pipe.crea_canal_de_entrada(i), cc_pipe))

        # Asignamos los padres a los nodos para construir el árbol
        for i, nodo in enumerate(grafica):
            for hijo in nodo.vecinos:
                grafica[hijo].padre = nodo.id_nodo
                nodo.hijos.append(hijo)

        # Le decimos al ambiente lo que va a procesar
        for nodo in grafica:
            env.process(nodo.convergecast(env))
        # Se ejecuta
        env.run(until=TIEMPO_DE_EJECUCION)

        # Probamos que el resultado en la raíz sea el esperado
        valor_esperado = sum(range(len(grafica)))  # La suma de los IDs de los nodos
        raiz = grafica[0]
        assert raiz.val_set == set((i, i) for i in range(len(grafica))), (
            'El conjunto de valores en el nodo raíz es incorrecto')

        resultado = sum(val for _, val in raiz.val_set)
        assert resultado == valor_esperado, (
            'El valor total procesado por la raíz es incorrecto')