import simpy
from NodoGenerador import NodoGenerador
from NodoConvergecast import NodoConvergecast
from Canales.CanalConvergecast import CanalConvergecast

def main():
    env = simpy.Environment()
    
    # Crea un canal de convergecast con capacidad sin limte
    canal = CanalConvergecast(env, capacidad=simpy.core.Infinity)

    # Definición de la etructura de vecinos para los nodos
    vecinos = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0],
        3: [1],
        4: [1]
    }

    # Crea nodos generadores y asocia un canal de entrada y salida
    nodos_generadores = {}
    for id_nodo in vecinos:
        canal_entrada = canal.crea_canal_de_entrada(id_nodo) 
        canal_salida = canal  
        nodos_generadores[id_nodo] = NodoGenerador(id_nodo, vecinos[id_nodo], canal_entrada, canal_salida)

    # Construye el árbol generador (utilizando el algoritmo de árbol generador)
    for nodo in nodos_generadores.values():
        env.process(nodo.genera_arbol(env)) 

    # Ejecuta la simulación
    env.run()

    # Imprime la estructura del árbol generador después de la simulación
    for id_nodo, nodo in nodos_generadores.items():
        print(f"Nodo {id_nodo}:")
        print(f"  Padre: {nodo.padre}")
        print(f"  Hijos: {nodo.hijos}")

    # Crea nodos de convergecast y asociarles un canal de entrada y salida
    nodos_convergecast = {}
    for id_nodo in vecinos:
        canal_entrada = canal.crea_canal_de_entrada(id_nodo) 
        canal_salida = canal  
        nodos_convergecast[id_nodo] = NodoConvergecast(id_nodo, vecinos[id_nodo], canal_entrada, canal_salida)

    # Inicia el proceso de convergecast en cada nodo
    for nodo in nodos_convergecast.values():
        env.process(nodo.convergecast(env))

    # Ejecuta la simulación nuevamente para el convergecast
    env.run()

if __name__ == '__main__':
    main()
