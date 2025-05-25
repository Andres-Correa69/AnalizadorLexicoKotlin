# Fundamentos Teóricos del Analizador Léxico

## Gramáticas Regulares

### Identificadores
```
<identificador> ::= <letra> <resto_id>
<resto_id> ::= <letra_digito> <resto_id> | ε
<letra_digito> ::= <letra> | <digito> | _
<letra> ::= a | b | ... | z | A | B | ... | Z
<digito> ::= 0 | 1 | ... | 9
```

### Números
```
<numero> ::= <natural> | <real>
<natural> ::= <digito> <natural> | <digito>
<real> ::= <natural> . <natural>
```

### Cadenas
```
<cadena> ::= " <contenido> "
<contenido> ::= <caracter> <contenido> | ε
<caracter> ::= <cualquier_char> | \\ <escape>
<escape> ::= \\ | "
```

## Expresiones Regulares Teóricas

- Identificador: `[a-zA-Z][a-zA-Z0-9_]{0,9}`
- Número natural: `[0-9]+`
- Número real: `[0-9]+\.[0-9]+`
- Operadores: `[\+\-\*/\%]|==|!=|<=|>=|&&|\|\||!|\+\+|\-\-`
- Delimitadores: `[\(\)\{\},;]`
- Cadenas: `"([^"\\]|\\.)*"`
- Comentarios: `//.*|/\*[\s\S]*?\*/`

## Comparación AFN vs AFD

### Ejemplo: Identificador

#### AFN para Identificadores
```
Estado inicial: q0
Estados finales: q2
Transiciones:
- q0 --[a-zA-Z]--> q1
- q1 --[a-zA-Z0-9_]--> q1
- q1 --ε--> q2
```

#### AFD para Identificadores (Implementado)
```python
def _analizar_identificador(self):
    inicio = self.posicion
    while self.posicion < len(self.codigo) and (
        self.codigo[self.posicion] in self.letras or 
        self.codigo[self.posicion] in self.digitos or 
        self.codigo[self.posicion] == '_'
    ):
        self.posicion += 1
```

La principal diferencia es que el AFN puede tener transiciones epsilon y múltiples estados activos simultáneamente, mientras que el AFD implementado siempre tiene un único estado activo y transiciones deterministas.

## Lógica Proposicional

Los operadores lógicos implementados siguen las reglas de la lógica proposicional:
- AND (&&): Conjunción
- OR (||): Disyunción
- NOT (!): Negación

## Teoría de Conjuntos

El analizador utiliza conjuntos para organizar y clasificar tokens:
```python
self.palabras_reservadas = {'fun', 'val', 'var', 'if', 'else', 'when'}
self.letras = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
self.digitos = set('0123456789')
self.operadores = {'+', '-', '*', '/', '%', '=', '<', '>', '!', '&', '|'}
self.delimitadores = {'(', ')', '{', '}', ',', ';'}
``` 