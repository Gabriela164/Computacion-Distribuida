'''
Practica 01: Implementación del algoritmo de recorrido BFS (Breadth First Search)
Curso: Computación distribuida 2025-1
Fecha de entrega: 03/Sep/24
Equipo:
- López Diego Gabriela 
- San Martı́n Macı́as Juan Daniel
- Martı́nez Hidalgo Paola Mildred
'''
import queue

grafica = {
  'A' : ['B','C', 'D', 'E'],
  'B' : ['A', 'C', 'G'],
  'C' : ['A', 'B', 'D'],
  'D' : ['H', 'E', 'A', 'C'],
  'E' : ['A', 'D', 'F'],
  'F' : ['G', 'E', 'H', 'I'],
  'G' : ['F', 'B'],
  'H' : ['F', 'D'],
  'I' : ['F']
}  

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
  nodo_raiz = 'A'

  print("Recorrido BFS de la grafica")
  bfs(grafica, nodo_raiz, nodos_visitados)
    