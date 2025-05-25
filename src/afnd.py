"""
Módulo que implementa un Autómata Finito No Determinista (AFND).
Este módulo proporciona la funcionalidad necesaria para crear, manipular
y convertir AFNDs a AFDs para el análisis léxico.
"""

class AFND:
    """
    Clase que implementa un Autómata Finito No Determinista (AFND).
    
    Un AFND es una estructura que permite reconocer patrones en texto mediante:
    - Múltiples estados posibles simultáneos
    - Transiciones con el mismo símbolo a diferentes estados
    - Transiciones epsilon (sin consumir símbolo)
    """
    
    def __init__(self):
        """
        Inicializa un nuevo AFND vacío.
        
        Inicializa las estructuras de datos necesarias:
        - estados: conjunto de estados del autómata
        - alfabeto: conjunto de símbolos válidos
        - transiciones: diccionario de transiciones
        - estado_inicial: estado de inicio
        - estados_finales: conjunto de estados de aceptación
        - epsilon: símbolo para transiciones sin consumo
        """
        self.estados = set()
        self.alfabeto = set()
        self.transiciones = {}
        self.estado_inicial = None
        self.estados_finales = set()
        self.epsilon = 'ε'
    
    def agregar_estado(self, estado):
        """
        Agrega un nuevo estado al conjunto de estados del autómata.
        
        Args:
            estado: Identificador del estado a agregar
        """
        self.estados.add(estado)
    
    def agregar_simbolo(self, simbolo):
        """
        Agrega un símbolo al alfabeto del autómata.
        
        Args:
            simbolo: Símbolo a agregar (no se agrega si es epsilon)
        """
        if simbolo != self.epsilon:
            self.alfabeto.add(simbolo)
    
    def establecer_estado_inicial(self, estado):
        """
        Define el estado inicial del autómata.
        
        Args:
            estado: Identificador del estado inicial
        """
        self.estado_inicial = estado
        self.estados.add(estado)
    
    def agregar_estado_final(self, estado):
        """
        Agrega un estado al conjunto de estados finales.
        
        Args:
            estado: Identificador del estado a marcar como final
        """
        self.estados_finales.add(estado)
        self.estados.add(estado)
    
    def agregar_transicion(self, estado_origen, simbolo, estado_destino):
        """
        Agrega una transición al autómata.
        
        Args:
            estado_origen: Estado desde donde parte la transición
            simbolo: Símbolo que activa la transición
            estado_destino: Estado al que se llega con la transición
        """
        # Agregar el símbolo al alfabeto
        self.agregar_simbolo(simbolo)
        
        # Agregar los estados
        self.estados.add(estado_origen)
        self.estados.add(estado_destino)
        
        # Agregar la transición
        if (estado_origen, simbolo) not in self.transiciones:
            self.transiciones[(estado_origen, simbolo)] = set()
        self.transiciones[(estado_origen, simbolo)].add(estado_destino)
    
    def epsilon_clausura(self, estados):
        """
        Calcula la clausura epsilon de un conjunto de estados.
        
        Args:
            estados: Conjunto de estados iniciales o estado individual
            
        Returns:
            set: Conjunto de estados alcanzables mediante transiciones epsilon
        """
        if isinstance(estados, (str, int)):
            estados = {estados}
        clausura = set(estados)
        pila = list(estados)
        
        while pila:
            estado = pila.pop()
            if (estado, self.epsilon) in self.transiciones:
                for nuevo_estado in self.transiciones[(estado, self.epsilon)]:
                    if nuevo_estado not in clausura:
                        clausura.add(nuevo_estado)
                        pila.append(nuevo_estado)
        return clausura
    
    def mover(self, estados, simbolo):
        """
        Calcula el conjunto de estados alcanzables mediante un símbolo.
        
        Args:
            estados: Conjunto de estados desde donde partir
            simbolo: Símbolo a consumir
            
        Returns:
            set: Estados alcanzables consumiendo el símbolo dado
        """
        if isinstance(estados, (str, int)):
            estados = {estados}
        resultado = set()
        for estado in estados:
            if (estado, simbolo) in self.transiciones:
                resultado.update(self.transiciones[(estado, simbolo)])
        return resultado
    
    def convertir_a_afd(self):
        """
        Convierte el AFND a un Autómata Finito Determinista (AFD).
        
        Returns:
            tuple: (estados_afd, estado_inicial_afd, transiciones_afd, estados_finales_afd)
            
        El proceso utiliza el algoritmo de construcción por subconjuntos:
        1. Obtener estado inicial del AFD mediante clausura epsilon
        2. Procesar estados nuevos y sus transiciones
        3. Identificar estados finales del AFD
        """
        # Obtener el estado inicial del AFD
        estado_inicial_afd = frozenset(self.epsilon_clausura(self.estado_inicial))
        estados_afd = {estado_inicial_afd}
        estados_por_procesar = [estado_inicial_afd]
        transiciones_afd = {}
        estados_finales_afd = set()
        
        # Si el estado inicial contiene algún estado final del AFND,
        # entonces es un estado final en el AFD
        if any(estado in self.estados_finales for estado in estado_inicial_afd):
            estados_finales_afd.add(estado_inicial_afd)
        
        while estados_por_procesar:
            estado_actual = estados_por_procesar.pop()
            
            for simbolo in self.alfabeto:
                # Calcular el siguiente estado usando mover y epsilon-clausura
                siguiente = set()
                for estado in estado_actual:
                    siguiente.update(self.mover(estado, simbolo))
                siguiente = frozenset(self.epsilon_clausura(siguiente))
                
                if siguiente:
                    # Agregar la transición al AFD
                    transiciones_afd[(estado_actual, simbolo)] = siguiente
                    
                    # Si es un nuevo estado, agregarlo a la lista de estados por procesar
                    if siguiente not in estados_afd:
                        estados_afd.add(siguiente)
                        estados_por_procesar.append(siguiente)
                    
                    # Verificar si es un estado final
                    if any(estado in self.estados_finales for estado in siguiente):
                        estados_finales_afd.add(siguiente)
        
        return estados_afd, estado_inicial_afd, transiciones_afd, estados_finales_afd

    def depurar_afnd(self):
        """
        Muestra información detallada sobre el AFND y su conversión a AFD.
        
        Imprime:
        - Estados del AFND
        - Alfabeto
        - Estado inicial
        - Estados finales
        - Transiciones del AFND
        - Información del AFD resultante
        """
        print("\n=== Información del AFND ===")
        print(f"Estados: {self.estados}")
        print(f"Alfabeto: {self.alfabeto}")
        print(f"Estado inicial: {self.estado_inicial}")
        print(f"Estados finales: {self.estados_finales}")
        print("\nTransiciones:")
        for (estado, simbolo), destinos in self.transiciones.items():
            print(f"{estado} --{simbolo}--> {destinos}")
            
        print("\n=== Conversión a AFD ===")
        afd = self.convertir_a_afd()
        estados_afd, estado_inicial_afd, transiciones_afd, estados_finales_afd = afd
        
        print(f"Estados AFD: {estados_afd}")
        print(f"Estado inicial AFD: {estado_inicial_afd}")
        print(f"Estados finales AFD: {estados_finales_afd}")
        print("\nTransiciones AFD:")
        for (estado, simbolo), destino in transiciones_afd.items():
            print(f"{estado} --{simbolo}--> {destino}")
            
    def probar_cadena(self, cadena):
        """
        Prueba si una cadena es aceptada por el autómata.
        
        Args:
            cadena: Cadena a evaluar
            
        Returns:
            bool: True si la cadena es aceptada, False en caso contrario
            
        Imprime el proceso de evaluación paso a paso, mostrando:
        - Estado inicial
        - Transiciones seguidas
        - Estado final
        - Resultado de la evaluación
        """
        afd = self.convertir_a_afd()
        estados_afd, estado_inicial_afd, transiciones_afd, estados_finales_afd = afd
        
        estado_actual = estado_inicial_afd
        print(f"\nProbando cadena: '{cadena}'")
        print(f"Estado inicial: {estado_actual}")
        
        for simbolo in cadena:
            if (estado_actual, simbolo) in transiciones_afd:
                estado_anterior = estado_actual
                estado_actual = transiciones_afd[(estado_actual, simbolo)]
                print(f"{estado_anterior} --{simbolo}--> {estado_actual}")
            else:
                print(f"Rechazada: No hay transición desde {estado_actual} con '{simbolo}'")
                return False
        
        aceptada = estado_actual in estados_finales_afd
        print(f"Estado final: {estado_actual}")
        print(f"Cadena {'aceptada' if aceptada else 'rechazada'}")
        return aceptada 