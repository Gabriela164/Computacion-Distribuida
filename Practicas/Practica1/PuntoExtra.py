'''
Practica 01: Implementación del algoritmo de recorrido BFS (Breadth First Search)
Punto extra 
Curso: Computación distribuida 2025-1
Fecha de entrega: 03/Sep/24
Equipo:
- López Diego Gabriela 
- San Martı́n Macı́as Juan Daniel
- Martı́nez Hidalgo Paola Mildred
'''
import queue

# Algoritmo BFS 
def bfs(grafica, nodo_raiz, nodos_visitados):
  #Agregamos el nodo raiz a la cola y lo marcamos como visitado
  cola.put(nodo_raiz) 
  nodos_visitados.append(nodo_raiz)
  
  while not cola.empty():
    nodo_actual = cola.get()
    #Vamos construyendo el recorrido
    print(nodo_actual, end = " ")
    
    #Revisamos los nodos vecinos del nodo actual 
    for vecino in grafica[nodo_actual]:
      #Si este aun no ha sido visitado, lo agregamos a la cola y lo marcamos como visitado
      if vecino not in nodos_visitados:
        nodos_visitados.append(vecino)
        cola.put(vecino)
     
      
if __name__ == "__main__":
  cola = queue.Queue()
  nodos_visitados = []
  grafica = {}

  # El usuario ingresa el numero de aristas que tendra la nueva grafica 
  num_aristas = int(input("\nIntroduce el numero de aristas de la grafica: "))
  print("\nIngresa un identificador al nodo inicial y nodo final separado por un espacio. ")
  print("Ejemplo: Introduce una arista (nodo_inicial nodo_final): A B \n ")
    
  # Metodo para nombrar los nodos de la gráfica dada por el usuario, dado que una arista 
  # se compone de 2 vertices, cada arista tendra un nodo inicial y un nodo de final
  for _ in range(num_aristas):
        nodo_inicial, nodo_final = input("Introduce una arista (nodo_inicial nodo_final): ").split()
        if nodo_inicial not in grafica:
            grafica[nodo_inicial] = []
        if nodo_final not in grafica:
            grafica[nodo_final] = []
        grafica[nodo_inicial].append(nodo_final)
        grafica[nodo_final].append(nodo_inicial)

# El usuario elige el nodo raíz
nodo_raiz = input("\nIntroduce el nodo desde donde empezar el recorrido BFS: \n")


print("Recorrido BFS de la grafica")
bfs(grafica, nodo_raiz, nodos_visitados)
    