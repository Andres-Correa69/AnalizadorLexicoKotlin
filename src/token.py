class Token:
    """
    Clase que representa un token léxico identificado en el código fuente.
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
        """
        return f"Token(lexema='{self.lexema}', tipo='{self.tipo}', pos=({self.fila}, {self.columna}))"
    
    def to_dict(self) -> dict:
        """
        Convierte el token a un diccionario para facilitar su uso en la GUI.
        """
        return {
            'Lexema': self.lexema,
            'Categoría': self.tipo,
            'Fila': self.fila,
            'Columna': self.columna
        } 