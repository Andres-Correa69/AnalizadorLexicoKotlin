import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from .analizador_lexico import AnalizadorLexico

class AnalizadorLexicoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico Kotlin")
        self.analizador = AnalizadorLexico()
        
        # Configurar el tema
        style = ttk.Style()
        style.theme_use('clam')
        
        self._crear_widgets()
        self._configurar_layout()

    def _crear_widgets(self):
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
        Ejecuta las pruebas de los AFND y muestra los resultados
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
            def __init__(self, text_widget):
                self.text_widget = text_widget
            
            def write(self, str):
                self.text_widget.insert(tk.END, str)
                self.text_widget.see(tk.END)
            
            def flush(self):
                pass
        
        sys.stdout = TextRedirector(resultados_text)
        
        try:
            # Ejecutar las pruebas
            self.analizador.probar_afnd()
        finally:
            # Restaurar la salida estándar
            sys.stdout = stdout_original

def main():
    root = tk.Tk()
    app = AnalizadorLexicoGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main() 