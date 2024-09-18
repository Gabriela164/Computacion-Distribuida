# 👽✨ Práctica 2 de Laboratorio

Implementación del algoritmo **broadcast**, construcción de un **árbol generador**, y **convergecast** (EXTRA).

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

### Estructura del Proyecto

- `main.py`: Contiene la definición del algoritmo principal y los elementos necesarios para construir y simular la red de nodos.
- `NodoConvergecast.py`: Define los nodos que forman parte de la simulación del algoritmo de Convergecast (Se basa en el pseudocódigo dado).
- `CanalConvergecast.py`: Modela los canales de comunicación entre los nodos en el entorno de simulación.
- `test.py`: Incluye pruebas para asegurar el correcto funcionamiento de los algoritmos implementados.

### Implementación de Convergecast

1. **Clase `NodoConvergecast`**:
   - Cada nodo tiene una lista de `vecinos`, un `padre`, y una lista de `hijos`. Psoteriormente el proceso de Convergecast inicia desde los nodos hoja, que envían su información al nodo padre.
   Al final cada nodo recibe información de sus hijos, agrega su propia información, y la envía a su padre hasta que la información llega al nodo raíz.

2. **Clase `CanalConvergecast`**:
   - Los nodos se comunican a través de un canal de entrada y salida, que permite modelar el comportamiento de la comunicación en una red distribuida. El canal tiene una capacidad que puede limitar la cantidad de mensajes que pueden ser procesados al mismo tiempo.

### Explicación del `main.py`

El archivo `main.py` es responsable de la inicialización y ejecución de la simulación. Primero, se crea un entorno de simulación utilizando `simpy.Environment()`, lo cual permite gestionar la interacción entre los nodos y los canales. Posteriormente, se define la estructura del árbol, asignando manualmente las relaciones entre los nodos, es decir, quién es padre de quién. Cada nodo se conecta a través de un canal común de comunicación y, una vez que el árbol está construido, se ejecuta el proceso de Convergecast. Cada nodo ejecuta su algoritmo, acumulando los datos de sus hijos y transmitiéndolos hacia su nodo padre.

### Método de Prueba en `test.py`

En el archivo `test.py`, se añadió un método específico para validar que el algoritmo de Convergecast se ejecute correctamente. La prueba se realiza mediante la simulación de un conjunto de nodos conectados, verificando que el nodo raíz reciba la suma de los valores de todos los nodos de la red. Para ello, se utiliza el método `test_ejercicio_cuatro`, que crea el entorno de simulación y define los nodos junto con sus respectivos canales de comunicación. Posteriormente, el algoritmo de Convergecast es ejecutado y se verifica que el conjunto de valores recibido en el nodo raíz sea correcto. Si todo funciona según lo esperado, el resultado en la raíz será la suma de los IDs de los nodos, confirmando así la correcta ejecución del algoritmo.


#### `test_ejercicio_cuatro`

Este método realiza lo siguiente:

1. **Inicialización del Entorno y los Nodos**:
   - Se crea un entorno de simulación (`simpy.Environment`) y un canal de comunicación con capacidad definida.
   - Se crean los nodos y se les asignan canales de entrada.

2. **Construcción del Árbol**:
   - Se asignan los nodos padres e hijos para formar la estructura del árbol.

3. **Ejecución del Convergecast**:
   - Cada nodo envía su valor a su padre, quien recibe y agrega la información de sus hijos.

4. **Verificación del Resultado**:
   - Se verifica que el nodo raíz haya recibido correctamente todos los valores de los demás nodos y que el valor final sea la suma de los IDs de los nodos, lo cual confirma que el algoritmo de Convergecast ha sido ejecutado correctamente.

### Ejecución del algoritmo
Para ejecutar el código basta con ejecutar el comando `python main.py` para ver los resultados en consola, además se puede probar con `pytest -q test.py`

