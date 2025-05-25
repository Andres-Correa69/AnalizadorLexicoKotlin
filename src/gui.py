"""
Módulo de interfaz gráfica para el analizador léxico.
Este módulo implementa una interfaz gráfica de usuario (GUI) que permite
interactuar con el analizador léxico de manera visual e intuitiva.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from .analizador_lexico import AnalizadorLexico

class AnalizadorLexicoGUI:
    """
    Clase que implementa la interfaz gráfica del analizador léxico.
    
    Proporciona una ventana con:
    - Área de texto para ingresar código fuente
    - Tabla para mostrar los tokens identificados
    - Botones para analizar el código y probar los autómatas
    - Visualización clara de errores léxicos
    """
    
    def __init__(self, root):
        """
        Inicializa la ventana principal y sus componentes.
        
        Args:
            root: Ventana raíz de Tkinter
        """
        self.root = root
        self.root.title("Analizador Léxico Kotlin")
        self.analizador = AnalizadorLexico()
        
        # Configurar el tema
        style = ttk.Style()
        style.theme_use('clam')
        
        self._crear_widgets()
        self._configurar_layout()

    def _crear_widgets(self):
        """
        Crea todos los widgets de la interfaz.
        
        Crea y configura:
        - Frame principal
        - Área de texto con scroll
        - Frame de botones
        - Tabla de tokens con scrollbars
        """
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Área de texto para el código
        self.codigo_label = ttk.Label(self.main_frame, text="Código Kotlin:")
        self.codigo_text = scrolledtext.ScrolledText(
            self.main_frame,
            wrap=tk.WORD,
            width=60,
            height=15,
            font=('Courier', 10)
        )
        
        # Frame para botones
        self.botones_frame = ttk.Frame(self.main_frame)
        
        # Botón de análisis
        self.analizar_btn = ttk.Button(
            self.botones_frame,
            text="Analizar",
            command=self._analizar_codigo
        )
        
        # Botón para probar AFND
        self.probar_afnd_btn = ttk.Button(
            self.botones_frame,
            text="Probar AFND",
            command=self._probar_afnd
        )
        
        # Tabla de tokens
        self.tabla_frame = ttk.Frame(self.main_frame)
        self.tabla = ttk.Treeview(
            self.tabla_frame,
            columns=('Lexema', 'Categoría', 'Fila', 'Columna'),
            show='headings'
        )
        
        # Configurar columnas
        self.tabla.heading('Lexema', text='Lexema')
        self.tabla.heading('Categoría', text='Categoría')
        self.tabla.heading('Fila', text='Fila')
        self.tabla.heading('Columna', text='Columna')
        
        # Scrollbars para la tabla
        self.scrolly = ttk.Scrollbar(
            self.tabla_frame,
            orient=tk.VERTICAL,
            command=self.tabla.yview
        )
        self.scrollx = ttk.Scrollbar(
            self.tabla_frame,
            orient=tk.HORIZONTAL,
            command=self.tabla.xview
        )
        self.tabla.configure(
            yscrollcommand=self.scrolly.set,
            xscrollcommand=self.scrollx.set
        )

    def _configurar_layout(self):
        """
        Configura el layout de la interfaz usando el sistema grid.
        
        Organiza:
        - Posicionamiento de widgets
        - Configuración de pesos de columnas y filas
        - Márgenes y espaciado
        """
        # Configurar el grid
        self.codigo_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.codigo_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame de botones
        self.botones_frame.grid(row=2, column=0, pady=10)
        self.analizar_btn.grid(row=0, column=0, padx=5)
        self.probar_afnd_btn.grid(row=0, column=1, padx=5)
        
        self.tabla_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar la tabla y scrollbars
        self.tabla.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrolly.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.scrollx.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configurar los pesos del grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(3, weight=1)
        self.tabla_frame.columnconfigure(0, weight=1)
        self.tabla_frame.rowconfigure(0, weight=1)

    def _analizar_codigo(self):
        """
        Analiza el código ingresado y muestra los tokens en la tabla.
        
        Proceso:
        1. Limpia la tabla de resultados anteriores
        2. Obtiene el código del área de texto
        3. Ejecuta el analizador léxico
        4. Muestra los tokens encontrados en la tabla
        """
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Obtener código y analizarlo
        codigo = self.codigo_text.get('1.0', tk.END)
        tokens = self.analizador.analizar(codigo)
        
        # Mostrar tokens en la tabla
        for token in tokens:
            token_dict = token.to_dict()
            self.tabla.insert(
                '',
                tk.END,
                values=(
                    token_dict['Lexema'],
                    token_dict['Categoría'],
                    token_dict['Fila'],
                    token_dict['Columna']
                )
            )

    def _probar_afnd(self):
        """
        Ejecuta las pruebas de los AFND y muestra los resultados.
        
        Proceso:
        1. Crea una nueva ventana para los resultados
        2. Configura un área de texto con scroll
        3. Redirige la salida estándar al área de texto
        4. Ejecuta las pruebas del AFND
        5. Restaura la salida estándar
        """
        # Crear una nueva ventana para mostrar los resultados
        ventana_pruebas = tk.Toplevel(self.root)
        ventana_pruebas.title("Resultados de Pruebas AFND")
        
        # Área de texto para mostrar resultados
        resultados_text = scrolledtext.ScrolledText(
            ventana_pruebas,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=('Courier', 10)
        )
        resultados_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Redirigir la salida estándar a nuestra área de texto
        import sys
        stdout_original = sys.stdout
        
        class TextRedirector:
            """
            Clase auxiliar para redirigir la salida estándar a un widget de texto.
            """
            def __init__(self, text_widget):
                """
                Inicializa el redireccionador.
                
                Args:
                    text_widget: Widget de texto donde se mostrará la salida
                """
                self.text_widget = text_widget
            
            def write(self, str):
                """
                Escribe texto en el widget.
                
                Args:
                    str: Texto a escribir
                """
                self.text_widget.insert(tk.END, str)
                self.text_widget.see(tk.END)
            
            def flush(self):
                """
                Implementación requerida para el protocolo de flujo de salida.
                """
                pass
        
        sys.stdout = TextRedirector(resultados_text)
        
        try:
            # Ejecutar las pruebas
            self.analizador.probar_afnd()
        finally:
            # Restaurar la salida estándar
            sys.stdout = stdout_original

def main():
    """
    Función principal que inicia la aplicación.
    
    Crea la ventana principal y ejecuta el bucle de eventos.
    """
    root = tk.Tk()
    app = AnalizadorLexicoGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main() 