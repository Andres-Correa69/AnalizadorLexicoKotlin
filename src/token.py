"""
Módulo que define la estructura de un token léxico.
Este módulo contiene la clase Token que representa las unidades léxicas
identificadas durante el análisis del código fuente Kotlin.
"""

class Token:
    """
    Clase que representa un token léxico identificado en el código fuente.
    
    Un token es la unidad mínima de significado en el análisis léxico y contiene:
    - El lexema (texto exacto encontrado en el código)
    - El tipo de token (identificador, número, operador, etc.)
    - La posición exacta donde se encontró (fila y columna)
    """
    def __init__(self, lexema: str, tipo: str, fila: int, columna: int):
        """
        Inicializa un nuevo token.
        
        Args:
            lexema (str): El texto del token identificado
            tipo (str): La categoría del token (ej: 'IDENTIFICADOR', 'NUMERO', etc.)
            fila (int): Número de línea donde se encontró el token
            columna (int): Posición en la línea donde comienza el token
        """
        self.lexema = lexema
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
    
    def __str__(self) -> str:
        """
        Representación en string del token.
        
        Returns:
            str: Cadena con formato "Token(lexema='X', tipo='Y', pos=(fila, columna))"
        """
        return f"Token(lexema='{self.lexema}', tipo='{self.tipo}', pos=({self.fila}, {self.columna}))"
    
    def to_dict(self) -> dict:
        """
        Convierte el token a un diccionario para facilitar su uso en la GUI.
        
        Returns:
            dict: Diccionario con las propiedades del token en formato:
                 {
                     'Lexema': str,
                     'Categoría': str,
                     'Fila': int,
                     'Columna': int
                 }
        """
        return {
            'Lexema': self.lexema,
            'Categoría': self.tipo,
            'Fila': self.fila,
            'Columna': self.columna
        } 