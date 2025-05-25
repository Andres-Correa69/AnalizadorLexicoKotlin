class AFND:
    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.transiciones = {}
        self.estado_inicial = None
        self.estados_finales = set()
        self.epsilon = 'ε'
    
    def agregar_estado(self, estado):
        self.estados.add(estado)
    
    def agregar_simbolo(self, simbolo):
        if simbolo != self.epsilon:
            self.alfabeto.add(simbolo)
    
    def establecer_estado_inicial(self, estado):
        self.estado_inicial = estado
        self.estados.add(estado)
    
    def agregar_estado_final(self, estado):
        self.estados_finales.add(estado)
        self.estados.add(estado)
    
    def agregar_transicion(self, estado_origen, simbolo, estado_destino):
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
        if isinstance(estados, (str, int)):
            estados = {estados}
        resultado = set()
        for estado in estados:
            if (estado, simbolo) in self.transiciones:
                resultado.update(self.transiciones[(estado, simbolo)])
        return resultado
    
    def convertir_a_afd(self):
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
        Muestra información detallada sobre el AFND y su conversión a AFD
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
        Prueba si una cadena es aceptada por el autómata
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