#  ⏰ Práctica 5 de Laboratorio

* ✍🏻 **OBJETIVO**: Relojes Lamport y Vectorial en los algoritmos Broadcast y DFS. 
* 📚 **CURSO**: Computación distribuida 2025-1 <br>
* 👨🏼‍🏫 **PROFESOR**: Mauricio Riva Palacio Orozco <br>
* 👦🏻 **AYUDANTE LAB**: Yael Antonio Calzada Martín <br>
* 👦🏻 **AYUDANTE TEORÍA**: Alan Alexis Martínez López <br>



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
<img src="img/ss.png" height="300">
</div>

## 💭 Explicación de la implementación

**Implementación del reloj Lamport:**

 Para la implementación del reloj Lamport se usó como base el algoritmo de BroadCast. 

Línea 7: Empezamos usando randint para el tiempo de espera para el envío y recepción de mensajes el cual será de 1 a 5 segundos.

Línea 21: Para la implementación del algoritmo empezamos por el nodo raíz el cual será el encargado de iniciar el broadcast distribuyendo el mensaje.

Línea 23-29: El nodo raíz envía el mensaje a cada vecino k, se hace uso de TICK para esperar un tiempo aleatorio antes de enviar el mensaje y se incrementa en +1 el reloj de Lamport.
Después en la línea 27 guardamos cada evento ocurrido (E), el valor del reloj y el mensaje.
En la línea 29 envía el mensaje a través de canal_salida, en el cual incluye el id_nodo, el contenido del mensaje y el valor que tiene actualmente el reloj. 

Línea 31-41: Se usa while para que cada uno de los nodos restantes pueda recibir y esperar los mensajes en un intervalo de tiempo (TICK).
En la línea 35 cada nodo recibe un mensaje del canal_entrada, para esto el nodo_emisor manda el contenido del mensaje y el valor que tiene el reloj Lamport en el momento del envío.
En la línea 37 se actualiza el valor del reloj de Lamport del nodo receptor incrementando en uno.
En la línea 39 guardamos el evento ocurrido R,es decir, que se recibió un mensaje de otro nodo, guardamos el valor del reloj actualizado y los detalles del mensaje. 

Línea 41: Se espera un cierto tiempo antes de retransmitir el mensaje a los demás nodos.

Línea 43-47: Cada nodo retransmite el mensaje a sus vecinos, para esto se incrementa el reloj Lamport antes de enviar el mensaje, 
En la línea 46 guardamos cada evento ocurrido E así como el valor del reloj y los detalles del mensaje.
En la línea 47 mediante el canal_salida se envía el mensaje a cada vecino en donde se incluye el id_nodo, el contenido del mensaje y la información del reloj.

En resumen la implementación de este algoritmo tiene como objetivo pasar el algoritmo BroadCast a un sistema asíncrono con ayuda de los relojes Lamport, donde todos los nodos tienen una visión del orden de eventos y el tiempo de entrega de mensajes puede variar.

**Implementación del reloj vectorial**

Para la implementación del reloj vectorial se usó como base el algoritmo DFS.

Línea 47-54: si id_nodo es igual a 0, es decir, el nodo raíz, se inicia el DFS incrementando uno el reloj vectorial. 
En la línea 49 a 51 agregamos el id_nodo a los nodos visitados y seleccionamos el vecino con el menor ID y después se registra el evento de envío E.
En la línea 52 y 53 se espera un tiempo aleatorio y se envía el mensaje “GO” al vecino k, así como la información del reloj vectorial.
En la línea 54 se agrega k a la lista de hijos.

Línea 57-59: Se tiene un mensaje del canal_entrada, el cual tiene el tipo de mensaje, nodos visitados, el nodo_mensajero y el reloj_mensajero.

Línea 62-64: Se actualiza el reloj vectorial y toma el valor máximo entre el reloj actual y el del mensaje. 
En la línea 63 se incrementa el reloj del nodo actual y en la línea 64 se registra el evento R con el estado actual del reloj y los nodos visitados.

Línea 67-76: Si el tipo de mensaje es “GO” El nodo se marca como padre del remitente, verifica si los vecinos han sido visitados, el reloj lo aumenta en uno y si es así registra un evento E, en el que envía un mensaje “BACK” al nodo padre, para finalmente limpiar la lista de los hijos.

Línea 79-85: Si tenemos vecinos que aún no han sido visitados seleccionamos uno de ellos y le enviamos el mensaje “GO” a través de ese vecino, registra el evento E y actualiza la lista de hijos agregando a este nuevo vecino. 

Línea 87-91: Si se recibe un mensaje “BACK” verifica si todos los vecinos han sido visitados, si todo los vecinos fueron visitados y el nodo es el padre termina el DFS. 

Línea 95-98: Si el nodo no es el padre aumenta en uno el reloj, registra el evento en E y envía “BACK” al nodo padre.

Línea 101-107: Si aún hay vecinos sin visitar seleccionamos uno, se actualiza el valor del reloj y se envía un “GO”, los nodos visitados, el id_nodo y la información del reloj actual. 

Para implementar este algoritmo como se dijo anteriormente se hizo uso del reloj vectorial, este reloj nos permite tener un arreglo o lista la cual nos ayuda a representar el tiempo en que se encuentran los demás nodos. 


