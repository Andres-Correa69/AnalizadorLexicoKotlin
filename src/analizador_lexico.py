from .token import Token
from .afnd import AFND

class AnalizadorLexico:
    def __init__(self):
        """
        Inicializa el analizador léxico con sus conjuntos de caracteres y palabras reservadas.
        """
        # Conjunto de palabras reservadas
        self.palabras_reservadas = {'fun', 'val', 'var', 'if', 'else', 'when', 'Int', 'Double', 'String', 'return'}
        
        # Conjuntos de caracteres
        self.letras = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.digitos = set('0123456789')
        self.operadores = {'+', '-', '*', '/', '%', '=', '<', '>', '!', '&', '|'}
        self.delimitadores = {'(', ')', '{', '}', ',', ';', ':'}
        
        # Estado del analizador
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.codigo = ""
        self.tokens = []
        
        # Inicializar AFNDs
        self._inicializar_afnds()

    def _inicializar_afnds(self):
        """
        Inicializa los AFNDs para los diferentes patrones léxicos
        """
        # AFND para identificadores
        self.afnd_identificador = AFND()
        self._construir_afnd_identificador()
        
        # AFND para números
        self.afnd_numero = AFND()
        self._construir_afnd_numero()
        
        # Convertir AFNDs a AFDs para su uso
        self.afd_identificador = self.afnd_identificador.convertir_a_afd()
        self.afd_numero = self.afnd_numero.convertir_a_afd()

    def _construir_afnd_identificador(self):
        """
        Construye el AFND para identificadores
        Patrón: (letra|_)(letra|digito|_)*
        """
        self.afnd_identificador.establecer_estado_inicial('q0')
        self.afnd_identificador.agregar_estado_final('q1')
        
        # Agregar transiciones para la primera letra o guión bajo
        for letra in self.letras:
            self.afnd_identificador.agregar_transicion('q0', letra, 'q1')
        self.afnd_identificador.agregar_transicion('q0', '_', 'q1')
        
        # Agregar transiciones para el resto del identificador
        for letra in self.letras:
            self.afnd_identificador.agregar_transicion('q1', letra, 'q1')
        for digito in self.digitos:
            self.afnd_identificador.agregar_transicion('q1', digito, 'q1')
        self.afnd_identificador.agregar_transicion('q1', '_', 'q1')
    
    def _construir_afnd_numero(self):
        """
        Construye el AFND para números
        Patrón: digito+ ('.' digito+)?
        """
        self.afnd_numero.establecer_estado_inicial('q0')
        self.afnd_numero.agregar_estado_final('q1')
        self.afnd_numero.agregar_estado_final('q3')
        
        # Parte entera
        for digito in self.digitos:
            self.afnd_numero.agregar_transicion('q0', digito, 'q1')
            self.afnd_numero.agregar_transicion('q1', digito, 'q1')
        
        # Punto decimal
        self.afnd_numero.agregar_transicion('q1', '.', 'q2')
        
        # Parte decimal
        for digito in self.digitos:
            self.afnd_numero.agregar_transicion('q2', digito, 'q3')
            self.afnd_numero.agregar_transicion('q3', digito, 'q3')

    def analizar(self, codigo: str) -> list:
        """
        Analiza el código fuente y retorna una lista de tokens.
        
        Args:
            codigo (str): Código fuente a analizar
            
        Returns:
            list: Lista de tokens encontrados
        """
        self.codigo = codigo
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []
        
        while self.posicion < len(self.codigo):
            self._analizar_siguiente_token()
            
        return self.tokens

    def _analizar_siguiente_token(self):
        """
        Analiza y extrae el siguiente token del código fuente.
        """
        char = self.codigo[self.posicion]
        
        # Ignorar espacios en blanco
        if char.isspace():
            if char == '\n':
                self.linea += 1
                self.columna = 1
            else:
                self.columna += 1
            self.posicion += 1
            return
        
        # Identificadores y palabras reservadas
        if char in self.letras or char == '_':
            self._analizar_identificador()
        
        # Números
        elif char in self.digitos:
            self._analizar_numero()
        
        # Operadores
        elif char in self.operadores:
            self._analizar_operador()
        
        # Delimitadores
        elif char in self.delimitadores:
            self._analizar_delimitador()
        
        # Cadenas
        elif char == '"':
            self._analizar_cadena()
        
        # Comentarios
        elif char == '/' and self.posicion + 1 < len(self.codigo):
            if self.codigo[self.posicion + 1] in ['/', '*']:
                self._analizar_comentario()
            else:
                self._analizar_operador()
        
        # Caracteres no reconocidos
        else:
            self._error_lexico(f"Carácter no reconocido: {char}")

    def _analizar_identificador(self):
        """
        Analiza identificadores usando el AFD generado del AFND
        """
        inicio = self.posicion
        col_inicio = self.columna
        
        # Leer el identificador completo
        while self.posicion < len(self.codigo):
            char = self.codigo[self.posicion]
            if char in self.letras or char in self.digitos or char == '_':
                self.posicion += 1
                self.columna += 1
            else:
                break
        
        lexema = self.codigo[inicio:self.posicion]
        
        # Verificar longitud máxima
        if len(lexema) > 10:
            self._error_lexico(f"Identificador '{lexema}' excede el límite de 10 caracteres")
            return
        
        # Determinar si es palabra reservada o identificador
        tipo = 'PALABRA_RESERVADA' if lexema in self.palabras_reservadas else 'IDENTIFICADOR'
        self.tokens.append(Token(lexema, tipo, self.linea, col_inicio))

    def _analizar_numero(self):
        """
        Analiza números usando el AFD generado del AFND
        """
        estados_afd, estado_inicial, transiciones, estados_finales = self.afd_numero
        estado_actual = estado_inicial
        inicio = self.posicion
        col_inicio = self.columna
        es_real = False
        
        while self.posicion < len(self.codigo):
            char = self.codigo[self.posicion]
            if (estado_actual, char) in transiciones:
                if char == '.':
                    es_real = True
                estado_actual = transiciones[(estado_actual, char)]
                self.posicion += 1
                self.columna += 1
            else:
                break
        
        if estado_actual in estados_finales:
            lexema = self.codigo[inicio:self.posicion]
            tipo = 'NUMERO_REAL' if es_real else 'NUMERO_NATURAL'
            self.tokens.append(Token(lexema, tipo, self.linea, col_inicio))
        else:
            self._error_lexico("Número inválido")

    def _analizar_operador(self):
        """
        Implementa el AFD para operadores, incluyendo detección de operadores inválidos.
        """
        inicio = self.posicion
        col_inicio = self.columna
        
        # Verificar operadores inválidos de dos o más caracteres
        if self.posicion + 1 < len(self.codigo):
            op_doble = self.codigo[self.posicion:self.posicion + 2]
            op_triple = self.codigo[self.posicion:self.posicion + 3] if self.posicion + 2 < len(self.codigo) else ''
            
            # Detectar operadores mal escritos
            if op_doble == '=<':
                self._error_lexico("Operador inválido '=<', ¿querías decir '<='?")
                self.posicion += 2
                self.columna += 2
                return
            
            # Detectar operadores juntos inválidos
            elif op_doble == '+*' or op_doble == '*+' or op_doble == '+-' or op_doble == '-+':
                self._error_lexico(f"Operadores juntos inválidos '{op_doble}'")
                self.posicion += 2
                self.columna += 2
                return
            
            # Detectar operador >>> que no existe en Kotlin
            elif op_triple == '>>>':
                self._error_lexico("Operador '>>>' no existe en Kotlin")
                self.posicion += 3
                self.columna += 3
                return
            
            # Operadores válidos de dos caracteres
            elif op_doble in ['==', '!=', '<=', '>=', '&&', '||', '++', '--']:
                self.tokens.append(Token(op_doble, 'OPERADOR', self.linea, col_inicio))
                self.posicion += 2
                self.columna += 2
                return
        
        # Operadores de un carácter
        op_simple = self.codigo[self.posicion]
        if op_simple in self.operadores:
            self.tokens.append(Token(op_simple, 'OPERADOR', self.linea, col_inicio))
            self.posicion += 1
            self.columna += 1
        else:
            self._error_lexico(f"Operador inválido '{op_simple}'")
            self.posicion += 1
            self.columna += 1

    def _analizar_delimitador(self):
        """
        Implementa el AFD para delimitadores.
        """
        delim = self.codigo[self.posicion]
        self.tokens.append(Token(delim, 'DELIMITADOR', self.linea, self.columna))
        self.posicion += 1
        self.columna += 1

    def _analizar_cadena(self):
        """
        Implementa el AFD para cadenas de texto.
        """
        inicio = self.posicion
        col_inicio = self.columna
        self.posicion += 1  # Saltar la comilla inicial
        self.columna += 1
        
        while self.posicion < len(self.codigo):
            if self.codigo[self.posicion] == '\\':
                # Manejar caracteres escapados
                if self.posicion + 1 < len(self.codigo):
                    self.posicion += 2
                    self.columna += 2
                else:
                    self._error_lexico("Carácter de escape al final de la cadena")
                    return
            elif self.codigo[self.posicion] == '"':
                # Fin de la cadena
                self.posicion += 1
                self.columna += 1
                lexema = self.codigo[inicio:self.posicion]
                self.tokens.append(Token(lexema, 'CADENA', self.linea, col_inicio))
                return
            elif self.codigo[self.posicion] == '\n':
                self._error_lexico("Cadena sin cerrar")
                return
            else:
                self.posicion += 1
                self.columna += 1
        
        self._error_lexico("Cadena sin cerrar")

    def _analizar_comentario(self):
        """
        Implementa el AFD para comentarios de línea (//) y de bloque (/* */).
        """
        inicio = self.posicion
        col_inicio = self.columna

        if self.codigo[self.posicion:self.posicion + 2] == '//':
            # Comentario de línea
            self.posicion += 2
            self.columna += 2

            while self.posicion < len(self.codigo) and self.codigo[self.posicion] != '\n':
                self.posicion += 1
                self.columna += 1

            lexema = self.codigo[inicio:self.posicion]
            self.tokens.append(Token(lexema, 'COMENTARIO_LINEA', self.linea, col_inicio))

        elif self.codigo[self.posicion:self.posicion + 2] == '/*':
            # Comentario de bloque
            self.posicion += 2
            self.columna += 2

            while self.posicion < len(self.codigo) - 1:
                if self.codigo[self.posicion] == '\n':
                    self.linea += 1
                    self.columna = 1
                    self.posicion += 1
                    continue

                if self.codigo[self.posicion:self.posicion + 2] == '*/':
                    self.posicion += 2
                    self.columna += 2
                    lexema = self.codigo[inicio:self.posicion]
                    self.tokens.append(Token(lexema, 'COMENTARIO_BLOQUE', self.linea, col_inicio))
                    return

                self.posicion += 1
                self.columna += 1

            # Si se termina el archivo sin encontrar cierre
            self._error_lexico("Comentario de bloque sin cerrar")

        else:
            # No es comentario, probablemente sea operador "/"
            self._analizar_operador()


    def _error_lexico(self, mensaje: str):
        """
        Maneja errores léxicos encontrados durante el análisis.
        """
        self.tokens.append(Token(
            f"ERROR: {mensaje}",
            'ERROR_LEXICO',
            self.linea,
            self.columna
        ))
        self.posicion += 1
        self.columna += 1

    def probar_afnd(self):
        """
        Realiza pruebas de los AFND para identificadores y números
        """
        print("\n=== Pruebas del AFND para Identificadores ===")
        self.afnd_identificador.depurar_afnd()
        
        # Probar casos válidos de identificadores
        print("\nPruebas de identificadores válidos:")
        self.afnd_identificador.probar_cadena("variable")
        self.afnd_identificador.probar_cadena("_test")
        self.afnd_identificador.probar_cadena("x1")
        
        # Probar casos inválidos de identificadores
        print("\nPruebas de identificadores inválidos:")
        self.afnd_identificador.probar_cadena("1variable")  # No puede empezar con número
        self.afnd_identificador.probar_cadena("@var")      # Carácter inválido
        
        print("\n=== Pruebas del AFND para Números ===")
        self.afnd_numero.depurar_afnd()
        
        # Probar casos válidos de números
        print("\nPruebas de números válidos:")
        self.afnd_numero.probar_cadena("123")
        self.afnd_numero.probar_cadena("123.456")
        
        # Probar casos inválidos de números
        print("\nPruebas de números inválidos:")
        self.afnd_numero.probar_cadena("12.34.56")  # Múltiples puntos
        self.afnd_numero.probar_cadena(".123")      # Punto al inicio
        self.afnd_numero.probar_cadena("123.")      # Punto al final 