import simpy

class CanalConvergecast:
    def __init__(self, env, capacidad):
        '''
        Inicializa el canal de convergecast.

        :param env: Entorno de simulación de SimPy.
        :param capacidad: Capacidad máxima del canal (número de mensajes que puede almacenar).
        '''
        self.env = env
        self.capacidad = capacidad
        self.canales = {} 

    def crea_canal_de_entrada(self, id_nodo):
        '''
        Crea un canal de entrada para un nodo específico.

        :param id_nodo: Identificador único del nodo para el cual se crea el canal.
        :return: Canal de entrada (simpy.Store) asociado al nodo.
        '''
        canal = simpy.Store(self.env, capacity=self.capacidad) 
        self.canales[id_nodo] = canal
        return canal

    def envia(self, mensaje, destinatarios):
        '''
        Envía un mensaje a los destinatarios especificados.

        :param mensaje: Mensaje a enviar (debe ser un objeto serializable).
        :param destinatarios: Lista de IDs de los nodos destinatarios.
        '''
        for destinatario in destinatarios:
            if destinatario in self.canales:
                self.canales[destinatario].put(mensaje)
