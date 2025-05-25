from .token import Token

class AnalizadorLexico:
    def __init__(self):
        """
        Inicializa el analizador léxico con sus conjuntos de caracteres y palabras reservadas.
        """
        # Conjunto de palabras reservadas
        self.palabras_reservadas = {'fun', 'val', 'var', 'if', 'else', 'when'}
        
        # Conjuntos de caracteres
        self.letras = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        self.digitos = set('0123456789')
        self.operadores = {'+', '-', '*', '/', '%', '=', '<', '>', '!', '&', '|'}
        self.delimitadores = {'(', ')', '{', '}', ',', ';'}
        
        # Estado del analizador
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.codigo = ""
        self.tokens = []

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
        if char in self.letras:
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
        Implementa el AFD para identificadores y palabras reservadas.
        """
        inicio = self.posicion
        col_inicio = self.columna
        
        while self.posicion < len(self.codigo) and (
            self.codigo[self.posicion] in self.letras or 
            self.codigo[self.posicion] in self.digitos or 
            self.codigo[self.posicion] == '_'
        ):
            self.posicion += 1
            self.columna += 1
        
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
        Implementa el AFD para números naturales y reales.
        """
        inicio = self.posicion
        col_inicio = self.columna
        es_real = False
        
        # Estado inicial: dígitos antes del punto
        while self.posicion < len(self.codigo) and self.codigo[self.posicion] in self.digitos:
            self.posicion += 1
            self.columna += 1
        
        # Estado: punto decimal
        if self.posicion < len(self.codigo) and self.codigo[self.posicion] == '.':
            es_real = True
            self.posicion += 1
            self.columna += 1
            
            # Estado: dígitos después del punto
            while self.posicion < len(self.codigo) and self.codigo[self.posicion] in self.digitos:
                self.posicion += 1
                self.columna += 1
        
        lexema = self.codigo[inicio:self.posicion]
        tipo = 'NUMERO_REAL' if es_real else 'NUMERO_NATURAL'
        self.tokens.append(Token(lexema, tipo, self.linea, col_inicio))

    def _analizar_operador(self):
        """
        Implementa el AFD para operadores.
        """
        inicio = self.posicion
        col_inicio = self.columna
        
        # Operadores de dos caracteres
        if self.posicion + 1 < len(self.codigo):
            op_doble = self.codigo[self.posicion:self.posicion + 2]
            if op_doble in ['==', '!=', '<=', '>=', '&&', '||', '++', '--']:
                self.posicion += 2
                self.columna += 2
                self.tokens.append(Token(op_doble, 'OPERADOR', self.linea, col_inicio))
                return
        
        # Operadores de un carácter
        op_simple = self.codigo[self.posicion]
        self.posicion += 1
        self.columna += 1
        self.tokens.append(Token(op_simple, 'OPERADOR', self.linea, col_inicio))

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
        Implementa el AFD para comentarios.
        """
        inicio = self.posicion
        col_inicio = self.columna
        
        if self.codigo[self.posicion + 1] == '/':
            # Comentario de línea
            self.posicion += 2
            while self.posicion < len(self.codigo) and self.codigo[self.posicion] != '\n':
                self.posicion += 1
            lexema = self.codigo[inicio:self.posicion]
            self.tokens.append(Token(lexema, 'COMENTARIO_LINEA', self.linea, col_inicio))
        
        elif self.codigo[self.posicion + 1] == '*':
            # Comentario de bloque
            self.posicion += 2
            while self.posicion < len(self.codigo) - 1:
                if self.codigo[self.posicion] == '*' and self.codigo[self.posicion + 1] == '/':
                    self.posicion += 2
                    lexema = self.codigo[inicio:self.posicion]
                    self.tokens.append(Token(lexema, 'COMENTARIO_BLOQUE', self.linea, col_inicio))
                    return
                elif self.codigo[self.posicion] == '\n':
                    self.linea += 1
                    self.columna = 1
                self.posicion += 1
            
            self._error_lexico("Comentario de bloque sin cerrar")

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