# Importar las bibliotecas necesarias
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# Clase para la interfaz principal
class Interfaz:
    def __init__(self, master):
        # Inicializar la ventana principal
        self.master = master
        master.title("Edición de cadenas de caracteres")

        # Crear elementos de la interfaz
        self.label_titulo = tk.Label(master, text="Selecciona un archivo CSV", font=("Arial", 16))
        self.label_titulo.pack(pady=20)

        self.boton_explorar = tk.Button(master, text="Explorar", command=self.explorar_archivo)
        self.boton_explorar.pack()

        self.label_archivo = tk.Label(master, text="No hay archivo seleccionado", font=("Arial", 12))
        self.label_archivo.pack(pady=10)

        self.boton_variar = tk.Button(master, text="Variar", command=self.variar, state=tk.DISABLED)
        self.boton_variar.pack(pady=20)

    # Método para explorar y seleccionar un archivo CSV
    def explorar_archivo(self):
        filename = filedialog.askopenfilename(filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")))
        if filename:
            self.label_archivo.config(text="Archivo seleccionado: " + filename)
            self.boton_variar.config(state=tk.NORMAL)
            self.archivo_seleccionado = filename

    # Método para leer el archivo CSV seleccionado
    def variar(self):
        df = self.leer_archivo_csv()
        if df is not None:
            matriz = df.values.tolist()
            print("Contenido del archivo:")
            for fila in matriz:
                print(fila)
            self.mostrar_opciones(matriz)

    # Método para leer el archivo CSV y manejar errores
    def leer_archivo_csv(self):
        try:
            return pd.read_csv(self.archivo_seleccionado)
        except Exception as e:
            messagebox.showerror("Error")

    # Método para mostrar las opciones de variación
    def mostrar_opciones(self, matriz):
        opciones_window = tk.Toplevel(self.master)
        Opciones(opciones_window, matriz)

# Clase para las opciones de combinación
class Opciones:
    def __init__(self, master, matriz):
        self.master = master
        master.title("Opciones de Combinación")
    
        self.label_titulo = tk.Label(master, text="Opciones para variar", font=("Arial", 16))
        self.label_titulo.pack(pady=20)

        self.matriz = matriz

        opciones = ["Combinar Todo", "Combinar por Pares", "Combinar por Rango"]
        for opcion in opciones:
            boton = tk.Button(master, text=opcion, command=lambda o=opcion: self.combinar_opcion(o))
            boton.pack()

        boton_regresar = tk.Button(master, text="Regresar", command=self.cerrar)
        boton_regresar.pack(pady=20)

    # Método para seleccionar la opción de combinación
    def combinar_opcion(self, opcion):
        if opcion == "Combinar Todo":
            self.combinar_todo()
        elif opcion == "Combinar por Pares":
            self.combinar_pares()
        elif opcion == "Combinar por Rango":
            self.combinar_rango()

    # Método para combinar todos los elementos de la matriz
    def combinar_todo(self):
        messagebox.showinfo("Combinar Todo", "Combinando todo...")
        self.cerrar()

    # Método para combinar elementos por pares
    def combinar_pares(self):
        pares_window = tk.Toplevel(self.master)
        IngresarPares(pares_window, self.matriz)

    # Método para combinar elementos por rango
    def combinar_rango(self):
        rango_window = tk.Toplevel(self.master)
        IngresarRango(rango_window, self.matriz)

    # Método para cerrar la ventana actual
    def cerrar(self):
        self.master.destroy()

# Clase para ingresar pares de variantes
class IngresarPares:
    def __init__(self, master, matriz):
        self.master = master
        master.title("Ingresar Pares de Variantes")

        label = tk.Label(master, text="Ingrese los pares de variantes (solo números enteros):", font=("Arial", 14))
        label.pack(pady=20)

        self.entry_variante_1 = tk.Entry(master)
        self.entry_variante_1.pack(pady=10)

        self.entry_variante_2 = tk.Entry(master)
        self.entry_variante_2.pack(pady=10)

        boton_ingresar = tk.Button(master, text="Ingresar", command=self.ingresar_pares)
        boton_ingresar.pack(pady=20)

        boton_regresar = tk.Button(master, text="Regresar", command=self.cerrar)
        boton_regresar.pack(pady=10)

        self.matriz = matriz

    # Método para cerrar la ventana actual
    def cerrar(self):
        self.master.destroy()

    # Método para ingresar pares de variantes y manejar errores
    def ingresar_pares(self):
        try:
            var1 = int(self.entry_variante_1.get())
            var2 = int(self.entry_variante_2.get())
            messagebox.showinfo("Pares de Variantes", f"Pares ingresados: ({var1}, {var2})")
        except ValueError:
            messagebox.showerror("Error", "Ingrese solo números enteros")

# Clase para ingresar un rango de variantes
class IngresarRango:
    def __init__(self, master, matriz):
        self.master = master
        master.title("Ingresar Rango")

        label = tk.Label(master, text="Ingrese el rango (solo números enteros):", font=("Arial", 14))
        label.pack(pady=20)

        self.entry_min = tk.Entry(master)
        self.entry_min.pack(pady=10)

        self.entry_max = tk.Entry(master)
        self.entry_max.pack(pady=10)

        boton_ingresar = tk.Button(master, text="Ingresar", command=self.ingresar_rango)
        boton_ingresar.pack(pady=20)

        boton_regresar = tk.Button(master, text="Regresar", command=self.cerrar)
        boton_regresar.pack(pady=10)

        self.matriz = matriz

    # Método para cerrar la ventana actual
    def cerrar(self):
        self.master.destroy()

    # Método para ingresar un rango de variantes y manejar errores
    def ingresar_rango(self):
        try:
            min_valor = int(self.entry_min.get())
            max_valor = int(self.entry_max.get())
            messagebox.showinfo("Rango", f"Rango ingresado: {min_valor} - {max_valor}")
        except ValueError:
            messagebox.showerror("Error", "Ingrese solo números enteros")

# Función principal para ejecutar la aplicación
def main():
    root = tk.Tk()
    root.resizable(0, 0)  # Bloquea el cambio de tamaño de la ventana
    root.geometry("650x350")
    root.config(bg="grey")
    aplicacion = Interfaz(root)
    root.mainloop()

# Llamar a la función principal
main()
