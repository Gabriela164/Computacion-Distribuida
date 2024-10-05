# 🌲 Práctica 3 de Laboratorio

* 📚 **CURSO**: Computación distribuida 2025-1 <br>
* 👨🏼‍🏫 **PROFESOR**: Mauricio Riva Palacio Orozco <br>
* 👦🏻 **AYUDANTE LAB**: Yael Antonio Calzada Martín <br>
* 👦🏻 **AYUDANTE TEORÍA**: Alan Alexis Martínez López <br>
* ✍🏻 **OBJETIVO**: Implementación del algoritmo **BFS** y **DFS** en sistemas distribuidos.

<br>

<div style="text-align: center;">
    <img src="img/bfs-dfs.png" width="440" height="230">
</div>

<br>

<table>
    <tr>
        <th>Equipo</th>
        <th>No de cuenta</th>
    </tr>
    <tr>
        <td>López Diego Gabriela</td>
        <td>318243485</td>
    </tr>
    <tr>
        <td>San Martín Macías Juan Daniel</td>
        <td>318181637</td>
    </tr>
    <tr>
        <td>Martínez Hidalgo Paola Mildred</td>
        <td>319300217</td>
    </tr>
</table>

## 🔧 Evidencia pasan todas las pruebas
<div style="text-align: center;">
    <img src="img/SS.png" width="440" height="230">
</div>


## Explicación de la implementación del algoritmo BFS 
La clase NodoBFS modela los nodos para poder aplicarles el algoritmo BFS, en el cual cada nodo cuenta con un identificador único (id_nodo) y un conjunto de nodos vecinos a los que le puede enviar un mensaje. Igual tenemos otras clases las cuales son los canales de comunicación para recibir y enviar mensajes. <br>
Explicaremos la implementación del algoritmo BFS. 
Primero empezamos con el nodo raíz, si el nodo raíz es id_nodo=0, entonces enviamos un mensaje "GO" a todos sus vecinos con su ID (self.id_nodo) y también se envía la distancia (self_distancia), usamos (yield env.timeout(TICK)) para el tiempo y el mensaje "GO" le indica a los vecinos que empiecen a explorar los demás nodos.  <br>
Cuando caemos en while True cada nodo espera un mensaje en su canal de entrada. 
Si se recibe un mensaje "GO" tenemos tres casos.
 * Si el nodo aún no tiene un padre se establece como padre al nodo que le envió el mensaje, actualiza su distancia y envía mensajes "GO" a sus vecinos a excepto al padre. 
 * Si el nodo ya tiene un padre y recibe un mensaje de un nodo a una distancia menor, se actualiza su padre y envía un mensaje "GO" a sus vecinos. 
 * Si el nodo ya fue visitado y su nivel es menor o igual que el del nodo remitente, se manda un mnesaje "BACK" para indicar que ya fue visitado. <br>

Cuando un nodo recibe un mensaje "BACK" tiene que actualizar el contador de los mjs_esperados, en caso de que ya no haya mensajes por recibir de sus vecinos se envía un mensaje "BACK" a su padre. <br>
Los mensajes "BACK" se envían de abajo hacia arriba en el árbol de BFS, por lo que hasta que  el nodo raíz recibe el mensaje "BACK" se termina el algoritmo.

## Explicación de la implementación del algoritmo DFS
