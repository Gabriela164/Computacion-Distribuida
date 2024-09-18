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

El algoritmo **Convergecast** es una técnica utilizada para recolectar información desde los nodos hoja de un árbol hacia un nodo raíz. Este proceso involucra a cada nodo transmitiendo sus datos a su nodo padre, hasta que toda la información llega al nodo raíz. En esta práctica, se implementó este algoritmo para un árbol de nodos con comunicación a través de canales.

1. **Clase `NodoConvergecast`**:
   - Cada nodo tiene una lista de `vecinos`, un `padre`, y una lista de `hijos`.
   - El proceso de Convergecast inicia desde los nodos hoja, que envían su información al nodo padre.
   - Cada nodo recibe información de sus hijos, agrega su propia información, y la envía a su padre hasta que la información llega al nodo raíz.

2. **Clase `CanalConvergecast`**:
   - Los nodos se comunican a través de un canal de entrada y salida, que permite modelar el comportamiento de la comunicación en una red distribuida.
   - El canal tiene una capacidad que puede limitar la cantidad de mensajes que pueden ser procesados al mismo tiempo.

### Explicación del `main.py`

El archivo `main.py` contiene la lógica principal para inicializar la simulación, crear los nodos y definir las relaciones entre ellos. Los pasos principales incluyen:

1. **Creación del Entorno de Simulación**:
   Se utiliza `simpy.Environment()` para crear el entorno de simulación en el que los nodos se comunicarán a través de los canales definidos.

2. **Construcción del Árbol**:
   - Los nodos y sus relaciones padre-hijo se configuran manualmente para crear la estructura del árbol.
   - A cada nodo se le asigna un canal de entrada y se conecta a un canal común que se utiliza para transmitir los mensajes durante el proceso de Convergecast.

3. **Ejecución del Algoritmo**:
   - Cada nodo ejecuta su proceso de Convergecast, que involucra recibir los datos de los nodos hijos, agregar su propio dato, y transmitirlo al nodo padre.
   - El entorno de simulación se ejecuta durante un tiempo definido, suficiente para completar el proceso de Convergecast.

### Método de Prueba en `test.py`

Se agregó un método de prueba en `test.py` para asegurar que el algoritmo de Convergecast se esté ejecutando correctamente. Este método simula el proceso y verifica que los resultados en el nodo raíz sean los esperados.

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

