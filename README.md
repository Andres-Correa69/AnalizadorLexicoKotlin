# Analizador Léxico para Kotlin

Este proyecto implementa un analizador léxico para el lenguaje Kotlin, desarrollado como proyecto final para la materia de Teoría de Lenguajes Formales.

## Características

- Análisis léxico basado en Autómatas Finitos Deterministas (AFD)
- Interfaz gráfica para análisis de código
- Detección de tokens para:
  - Números (naturales y reales)
  - Identificadores
  - Palabras reservadas
  - Operadores (aritméticos, lógicos, comparación)
  - Cadenas de texto
  - Comentarios
  - Y más...

## Requisitos

- Python 3.x
- Tkinter (incluido en la instalación estándar de Python)

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Para ejecutar el analizador léxico:

```bash
python main.py
```

## Estructura del Proyecto

- `main.py`: Punto de entrada de la aplicación
- `analizador_lexico.py`: Implementación del analizador léxico
- `token.py`: Definición de la clase Token
- `gui.py`: Interfaz gráfica de usuario

## Pruebas

El proyecto incluye casos de prueba en la documentación y el código. Para ver ejemplos de uso, consultar los comentarios en el código fuente. 