import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import os

# Definición de la clase NodoHuffman para representar los nodos del árbol Huffman
class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

# Función para construir el árbol de Huffman a partir de una lista de frecuencias
def construir_arbol_huffman(lista_frecuencias):
    nodos = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in lista_frecuencias]

    while len(nodos) > 1:
        nodos.sort(key=lambda x: x.frecuencia)

        izquierda = nodos.pop(0)
        derecha = nodos.pop(0)

        nodo_padre = NodoHuffman(None, izquierda.frecuencia + derecha.frecuencia)
        nodo_padre.izquierda = izquierda
        nodo_padre.derecha = derecha

        nodos.append(nodo_padre)

    return nodos[0]

# Función para asignar códigos Huffman a cada carácter del árbol Huffman
def asignar_codigos_huffman(arbol, codigo='', diccionario_codigos={}):
    if arbol is not None:
        if arbol.caracter is not None:
            diccionario_codigos[arbol.caracter] = codigo
        asignar_codigos_huffman(arbol.izquierda, codigo + '0', diccionario_codigos)
        asignar_codigos_huffman(arbol.derecha, codigo + '1', diccionario_codigos)
    return diccionario_codigos

# Función para comprimir un archivo utilizando el diccionario de códigos Huffman
def comprimir_archivo(ruta_archivo, diccionario_codigos):
    ruta_programa = os.path.dirname(os.path.abspath(__file__))
    archivo_comprimido = os.path.join(ruta_programa, 'ArchivoComprimido.bin')
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo_origen:
        contenido = archivo_origen.read()
        contenido_comprimido = ''.join(diccionario_codigos[caracter] for caracter in contenido if caracter in diccionario_codigos)
        with open(archivo_comprimido, 'wb') as archivo_destino:
            archivo_destino.write(contenido_comprimido.encode('utf-8'))
    return archivo_comprimido

# Función para descomprimir un archivo utilizando el diccionario de códigos Huffman
def descomprimir_archivo(ruta_archivo_comprimido, diccionario_codigos):
    ruta_programa = os.path.dirname(os.path.abspath(__file__))
    archivo_descomprimido = os.path.join(ruta_programa, 'ArchivoDescomprimido.txt')
    with open(ruta_archivo_comprimido, 'rb') as archivo_origen:
        contenido_comprimido = archivo_origen.read().decode('utf-8')
        bits = ''
        contenido_descomprimido = ''
        for bit in contenido_comprimido:
            bits += bit
            if bits in diccionario_codigos.values():
                contenido_descomprimido += next((caracter for caracter, codigo in diccionario_codigos.items() if codigo == bits), '')
                bits = ''
    with open(archivo_descomprimido, 'w', encoding='utf-8') as archivo_destino:
        archivo_destino.write(contenido_descomprimido)
    return archivo_descomprimido

# Función principal de la aplicación que interactúa con la interfaz de usuario
def app():
    global lista_frecuencias
    global diccionario_codigos
    global archivo_seleccionado
    archivo_seleccionado = tk.filedialog.askopenfilename()
    if archivo_seleccionado:
        resultado = contar_caracteres(archivo_seleccionado)
        if resultado:
            print("Caracteres ordenados por cantidad:")
            for caracter, cantidad in resultado:
                print(f"Caracter: {caracter}, Cantidad: {cantidad}")
            archivo_resultado = guardar_resultado(resultado)
            mostrar_archivo(archivo_resultado, root)
            # Almacenar la lista de frecuencias y el diccionario de códigos para su uso en el backend
            lista_frecuencias = resultado
            arbol_huffman = construir_arbol_huffman(lista_frecuencias)
            diccionario_codigos = asignar_codigos_huffman(arbol_huffman)
            mensaje_label.config(text="Frecuencias calculadas correctamente.", foreground="green")

# Función para contar la frecuencia de cada carácter en un archivo
def contar_caracteres(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()

    cuenta_caracteres = {}
    for caracter in contenido:
        if caracter in cuenta_caracteres:
            cuenta_caracteres[caracter] += 1
        else:
            cuenta_caracteres[caracter] = 1

    caracteres_ordenados = sorted(cuenta_caracteres.items(), key=lambda x: x[1], reverse=True)
    return caracteres_ordenados

# Función para guardar el resultado del conteo de caracteres en un archivo de texto
def guardar_resultado(resultado):
    ruta_programa = os.path.dirname(os.path.abspath(__file__))
    ruta_resultado = os.path.join(ruta_programa, 'resultado.txt')

    with open(ruta_resultado, 'w', encoding='utf-8') as f:
        f.write("Caracteres ordenados:\n")
        for caracter, cantidad in resultado:
            f.write(f"Caracter: {caracter}, Cantidad: {cantidad}\n")
    print("El resultado se ha guardado en 'resultado.txt'.")
    return ruta_resultado

# Función para mostrar el contenido de un archivo en una ventana de texto
def mostrar_archivo(archivo, root):
    # Crea una nueva ventana
    ventana_archivo = tk.Toplevel(root)
    ventana_archivo.title("Resultado")
    
    # Crea un widget Text para mostrar el contenido del archivo
    texto_archivo = tk.Text(ventana_archivo)
    texto_archivo.pack(expand=True, fill='both')
    
    # Abre el archivo y muestra su contenido en el widget Text
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
        texto_archivo.insert('1.0', contenido)

# Función para comprimir un archivo seleccionado
def comprimir():
    global lista_frecuencias
    global diccionario_codigos
    global archivo_seleccionado
    if lista_frecuencias and diccionario_codigos and archivo_seleccionado:
        archivo_comprimido = comprimir_archivo(archivo_seleccionado, diccionario_codigos)
        mensaje_label.config(text="Compresión correcta", foreground="green")
    else:
        mensaje_label.config(text="Error: no se han calculado las frecuencias o los códigos de Huffman, o no se ha seleccionado ningún archivo", foreground="red")

# Función para descomprimir un archivo seleccionado
def descomprimir():
    global lista_frecuencias
    global diccionario_codigos
    global archivo_seleccionado
    if lista_frecuencias and diccionario_codigos:
        archivo_comprimido = tk.filedialog.askopenfilename()
        if archivo_comprimido:
            archivo_descomprimido = descomprimir_archivo(archivo_comprimido, diccionario_codigos)
            mensaje_label.config(text="Descompresión correcta", foreground="green")
    else:
        mensaje_label.config(text="Error: no se han calculado las frecuencias o los códigos de Huffman", foreground="red")

# Función principal que crea la interfaz gráfica de usuario
def main():
    global root
    root = tk.Tk()
    root.title("Arbol de Huffman / Comprimir y descomprimir")

    # Establecer el estilo de los widgets
    estilo = ttk.Style()
    estilo.configure('TLabel', font=('Helvetica', 12))
    estilo.configure('TButton', font=('Helvetica', 12))

    # Calcula el tamaño de la pantalla
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()

    # Calcula las dimensiones de la ventana a la mitad de la pantalla
    ancho_ventana = ancho_pantalla // 2
    alto_ventana = alto_pantalla // 2

    # Posiciona la ventana en el centro de la pantalla
    x = (ancho_pantalla - ancho_ventana) // 2
    y = (alto_pantalla - alto_ventana) // 2

    # Establece la geometría de la ventana
    root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    frm = ttk.Frame(root, padding=10)
    frm.pack(expand=True, fill='both')

    ttk.Label(frm, text="Contador de caracteres").pack()

    btn_abrir = ttk.Button(frm, text="Examinar", command=app)
    btn_abrir.pack(side='top', padx=5, pady=5)

    btn_comprimir = ttk.Button(frm, text="Comprimir", command=comprimir)
    btn_comprimir.pack(side='top', padx=5, pady=5)

    btn_descomprimir = ttk.Button(frm, text="Descomprimir", command=descomprimir)
    btn_descomprimir.pack(side='top', padx=5, pady=5)

    # Crear la etiqueta para mostrar el mensaje
    global mensaje_label
    mensaje_label = ttk.Label(frm, text="", font=('Helvetica', 12))
    mensaje_label.pack(side='top', padx=5, pady=5)

    root.mainloop()

main()
