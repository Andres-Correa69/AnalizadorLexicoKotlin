"""
Analizador Léxico para el lenguaje Kotlin.
Este módulo implementa un analizador léxico que reconoce tokens del lenguaje Kotlin
utilizando Autómatas Finitos Deterministas (AFD) y No Deterministas (AFND).
"""

from .token import Token
from .afnd import AFND

class AnalizadorLexico:
    """
    Clase principal del analizador léxico para Kotlin.
    
    Esta clase implementa un analizador léxico completo que puede:
    - Reconocer identificadores válidos (letras, dígitos y guiones bajos)
    - Identificar palabras reservadas del lenguaje
    - Procesar números (enteros y decimales)
    - Manejar operadores aritméticos y lógicos
    - Reconocer delimitadores
    - Procesar cadenas de texto
    - Manejar comentarios de línea (//) y de bloque (/* */)
    
    El analizador utiliza AFNDs convertidos a AFDs para el reconocimiento
    de patrones complejos como identificadores y números.
    """
    
    def __init__(self):
        """
        Inicializa el analizador léxico con sus conjuntos de caracteres y palabras reservadas.
        
        Define:
        - Conjunto de palabras reservadas de Kotlin
        - Conjuntos de caracteres válidos (letras, dígitos, operadores, delimitadores)
        - Estado inicial del analizador (posición, línea, columna)
        - Inicializa los AFNDs para identificadores y números
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
        Inicializa los Autómatas Finitos No Deterministas (AFND) para los patrones léxicos.
        
        Crea y configura:
        - AFND para identificadores: reconoce patrones (letra|_)(letra|digito|_)*
        - AFND para números: reconoce patrones digito+(.digito+)?
        
        Los AFNDs son convertidos a AFDs para su uso en el análisis.
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
        Construye el AFND para reconocer identificadores válidos en Kotlin.
        
        Patrón reconocido: (letra|_)(letra|digito|_)*
        Estados:
        - q0: Estado inicial
        - q1: Estado final (identificador válido)
        
        Transiciones:
        - De q0 a q1: letras y guión bajo
        - De q1 a q1: letras, dígitos y guión bajo
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
        Construye el AFND para reconocer números (enteros y decimales).
        
        Patrón reconocido: digito+(.digito+)?
        Estados:
        - q0: Estado inicial
        - q1: Estado final (número entero)
        - q2: Estado intermedio (después del punto decimal)
        - q3: Estado final (número decimal)
        
        Transiciones:
        - De q0 a q1: dígitos (parte entera)
        - De q1 a q2: punto decimal
        - De q2 a q3: dígitos (parte decimal)
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
        Analiza el código fuente completo y genera una lista de tokens.
        
        Args:
            codigo (str): Código fuente en Kotlin a analizar
            
        Returns:
            list: Lista de objetos Token encontrados en el código
            
        El análisis se realiza token por token hasta procesar todo el código,
        manteniendo un seguimiento de la posición, línea y columna actual.
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
        
        Este método es el núcleo del analizador, determina el tipo de token
        basándose en el carácter actual y delega el análisis al método
        específico correspondiente.
        
        Maneja:
        - Espacios en blanco y saltos de línea
        - Comentarios (// y /* */)
        - Identificadores y palabras reservadas
        - Números
        - Operadores
        - Delimitadores
        - Cadenas
        - Caracteres no reconocidos
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
        
        # Comentarios - Importante: verificar esto antes que operadores
        if char == '/' and self.posicion + 1 < len(self.codigo):
            siguiente = self.codigo[self.posicion + 1]
            if siguiente in ['/', '*']:
                self._analizar_comentario()
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
        
        # Caracteres no reconocidos
        else:
            self._error_lexico(f"Carácter no reconocido: {char}")

    def _analizar_identificador(self):
        """
        Analiza identificadores usando el AFD generado del AFND.
        
        Proceso:
        1. Lee caracteres válidos (letras, dígitos, guión bajo)
        2. Verifica la longitud máxima (10 caracteres)
        3. Determina si es palabra reservada o identificador
        4. Genera el token correspondiente
        
        Restricciones:
        - Longitud máxima: 10 caracteres
        - Debe comenzar con letra o guión bajo
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
        Analiza números usando el AFD generado del AFND.
        
        Reconoce:
        - Números naturales: secuencia de dígitos
        - Números reales: parte entera + punto decimal + parte decimal
        
        El análisis utiliza el AFD convertido del AFND para números,
        siguiendo las transiciones según los caracteres encontrados.
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
        
        Reconoce:
        - Operadores simples: +, -, *, /, %, =, <, >, !, &, |
        - Operadores compuestos: ==, !=, <=, >=, &&, ||, ++, --
        
        Detecta errores:
        - Operadores mal escritos (=< en lugar de <=)
        - Operadores juntos inválidos (+*, *+, +-, -+)
        - Operadores no existentes en Kotlin (>>>)
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
        
        Reconoce los siguientes delimitadores:
        - Paréntesis: ( )
        - Llaves: { }
        - Coma: ,
        - Punto y coma: ;
        - Dos puntos: :
        """
        delim = self.codigo[self.posicion]
        self.tokens.append(Token(delim, 'DELIMITADOR', self.linea, self.columna))
        self.posicion += 1
        self.columna += 1

    def _analizar_cadena(self):

        """
        Implementa el AFD para cadenas de texto.
        
        Características:
        - Reconoce cadenas delimitadas por comillas dobles
        - Maneja caracteres escapados = (\)
        - Detecta cadenas sin cerrar
        - Maneja saltos de línea dentro de cadenas
        
        Errores detectados:
        - Carácter de escape al final de la cadena
        - Cadena sin cerrar (falta comilla final)
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
        
        Tipos de comentarios:
        1. Comentarios de línea (//):
           - Consume todo hasta el fin de línea
           - No requiere cierre explícito
        
        2. Comentarios de bloque (/* */):
           - Puede abarcar múltiples líneas
           - Requiere cierre explícito con */
           - Detecta comentarios sin cerrar
        
        Manejo de errores:
        - Detecta y reporta comentarios de bloque sin cerrar
        - Evita el procesamiento del contenido como tokens en caso de error
        """
        inicio = self.posicion
        col_inicio = self.columna
        
        # Ya sabemos que tenemos '/' y hay un siguiente carácter
        siguiente = self.codigo[self.posicion + 1]
        
        if siguiente == '/':  # Comentario de línea
            # Consumir todo hasta el fin de línea
            self.posicion += 2  # Saltar '//'
            self.columna += 2
            
            while self.posicion < len(self.codigo) and self.codigo[self.posicion] != '\n':
                self.posicion += 1
                self.columna += 1
            
            lexema = self.codigo[inicio:self.posicion]
            self.tokens.append(Token(lexema, 'COMENTARIO_LINEA', self.linea, col_inicio))
            return
        
        elif siguiente == '*':  # Comentario de bloque
            self.posicion += 2  # Saltar '/*'
            self.columna += 2
            
            # Buscar el cierre '*/'
            while self.posicion < len(self.codigo) - 1:
                if self.codigo[self.posicion] == '*' and self.posicion + 1 < len(self.codigo) and self.codigo[self.posicion + 1] == '/':
                    # Encontramos el cierre
                    self.posicion += 2  # Saltar '*/'
                    self.columna += 2
                    lexema = self.codigo[inicio:self.posicion]
                    self.tokens.append(Token(lexema, 'COMENTARIO_BLOQUE', self.linea, col_inicio))
                    return
                
                if self.codigo[self.posicion] == '\n':
                    self.linea += 1
                    self.columna = 1
                else:
                    self.columna += 1
                
                self.posicion += 1
            
            # Si llegamos aquí, no se encontró el cierre
            self.tokens.append(Token(
                f"ERROR: Comentario de bloque sin cerrar",
                'ERROR_LEXICO',
                self.linea,
                col_inicio
            ))
            # Importante: avanzar hasta el final para no procesar el contenido como tokens
            self.posicion = len(self.codigo)

    def _error_lexico(self, mensaje: str):
        """
        Maneja errores léxicos encontrados durante el análisis.
        
        Args:
            mensaje (str): Descripción del error encontrado
        
        Genera un token de error con:
        - Mensaje descriptivo del error
        - Tipo 'ERROR_LEXICO'
        - Posición exacta (línea y columna) donde ocurrió el error
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
        Realiza pruebas de los AFND para identificadores y números.
        
        Pruebas realizadas:
        1. Para identificadores:
           - Casos válidos: variable, _test, x1
           - Casos inválidos: 1variable, @var
        
        2. Para números:
           - Casos válidos: 123, 123.456
           - Casos inválidos: 12.34.56, .123, 123.
        
        Muestra información detallada del AFND y los resultados de cada prueba.
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