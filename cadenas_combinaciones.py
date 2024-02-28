import tkinter as tk
from tkinter import filedialog
import pandas as pd
from datetime import datetime

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if file_path:
        process_file(file_path)

def process_file(file_path):
    posiciones, alteraciones, strings_a_modificar = leer_datos_desde_csv(file_path)
    if posiciones and alteraciones and strings_a_modificar:
        cadena_original = strings_a_modificar[0]
        variantes = reemplazar_caracteres(cadena_original, posiciones, alteraciones)
        combinaciones = generar_combinaciones(variantes, cadena_original)
        guardar_combinaciones_csv("combinaciones.csv", variantes, combinaciones)
        contenedor_datos = leer_combinaciones_csv("combinaciones.csv")
        show_options(contenedor_datos, cadena_original)

def leer_datos_desde_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        posiciones = df['posicion'].tolist()
        alteraciones = df['alteracion'].tolist()
        strings_a_modificar = df['string_a_modificar'].tolist()
        return posiciones, alteraciones, strings_a_modificar
    except FileNotFoundError:
        print("El archivo especificado no existe.")
        return [], [], []

def reemplazar_caracteres(cadena, indices, caracteres_nuevos):
    variantes = []
    for espacio in range(0, len(cadena) - 9, 5):
        lista_caracteres = list(cadena)
        cambios_en_ventana = False
        for indice, caracter_nuevo in zip(indices, caracteres_nuevos):
            if espacio <= indice < espacio + 10:
                lista_caracteres[indice] = caracter_nuevo
                cambios_en_ventana = True
        nueva_cadena = ''.join(lista_caracteres)
        if cambios_en_ventana:
            variantes.append(nueva_cadena)
    return variantes

def generar_combinaciones(variantes, cadena_original):
    combinaciones = []
    for variante in variantes:
        cambios = [(i, c1) for i, (c1, c2) in enumerate(zip(variante, cadena_original)) if c1 != c2]
        if cambios:
            combinaciones_variante = []
            for cambio in cambios:
                nueva_variante = list(variante)
                nueva_variante[cambio[0]] = cadena_original[cambio[0]]
                nueva_variante_str = "".join(nueva_variante)
                if nueva_variante_str != cadena_original:
                    combinaciones_variante.append(nueva_variante_str)
            combinaciones.append(combinaciones_variante)
        else:
            combinaciones.append([])
    return combinaciones

def guardar_combinaciones_csv(nombre_archivo, variantes, combinaciones):
    with open(nombre_archivo, 'w') as file:
        for i, (variante, comb_list) in enumerate(zip(variantes, combinaciones), start=1):
            file.write(f"{i},{variante},{','.join(comb_list)}\n")

def leer_combinaciones_csv(nombre_archivo):
    contenedor_datos = {}
    with open(nombre_archivo, 'r') as file:
        for line in file:
            indice, variante, *combinaciones = line.strip().split(',')
            contenedor_datos[int(indice)] = (variante, combinaciones)
    return contenedor_datos

def combinar_variantes(contenedor_datos, num_variante_1, num_variante_2, cadena_original):
    variante_1 = contenedor_datos[num_variante_1][0]
    variante_2 = contenedor_datos[num_variante_2][0]
    caracteres_diferentes = [(i, c1) for i, (c1, c3) in enumerate(zip(variante_1, cadena_original)) if c3 != c1]
    caracteres_diferentes += [(i, c2) for i, (c2, c3) in enumerate(zip(variante_2, cadena_original)) if c2 != c3]
    nueva_variante_combinada = list(cadena_original)
    for indice, caracter in caracteres_diferentes:
        nueva_variante_combinada[indice] = caracter
    return ''.join(nueva_variante_combinada)

def combinar_variante_con_combinaciones(contenedor_datos, rango, cadena_original):
    nuevas_combinaciones = {}
    for i in range(rango[0], rango[1]+1):
        variante_actual = contenedor_datos.get(i)
        if variante_actual:
            variante, combinaciones = variante_actual
            for j, combinacion in enumerate(combinaciones, start=1):
                nueva_variante = combinar_variantes(contenedor_datos, i, i, cadena_original)
                nuevas_combinaciones[f"Variante {i} con combinación {j}"] = nueva_variante
            for k in range(rango[0], rango[1]+1):
                if k != i:
                    variante_k, combinaciones_k = contenedor_datos[k]
                    if combinaciones_k:
                        for l, combinacion_k in enumerate(combinaciones_k, start=1):
                            nueva_variante = combinar_variantes(contenedor_datos, i, k, cadena_original)
                            nuevas_combinaciones[f"Variante {i} con variante {k} combinación {l}"] = nueva_variante
                    else:
                        nueva_variante = combinar_variantes(contenedor_datos, i, k, cadena_original)
                        nuevas_combinaciones[f"Variante {i} con variante {k}"] = nueva_variante
        else:
            print(f"La variante {i} no existe en el contenedor.")
    return nuevas_combinaciones

def show_options(contenedor_datos, cadena_original):
    options_window = tk.Tk()
    options_window.title("Opciones")
    options_window.geometry("300x200")

    label = tk.Label(options_window, text="Seleccione una opción:")
    label.pack(pady=10)

    def combine_pairs():
        pair_window = tk.Tk()
        pair_window.title("Combinar pares")
        pair_window.geometry("300x200")

        label_var1 = tk.Label(pair_window, text="Número de la primera variante:")
        label_var1.pack(pady=5)
        var1_entry = tk.Entry(pair_window)
        var1_entry.pack(pady=5)

        label_var2 = tk.Label(pair_window, text="Número de la segunda variante:")
        label_var2.pack(pady=5)
        var2_entry = tk.Entry(pair_window)
        var2_entry.pack(pady=5)

        def combine():
            num_variante_1 = int(var1_entry.get())
            num_variante_2 = int(var2_entry.get())
            if num_variante_1 in contenedor_datos and num_variante_2 in contenedor_datos:
                nueva_variante_combinada = combinar_variantes(contenedor_datos, num_variante_1, num_variante_2, cadena_original)
                result_label = tk.Label(pair_window, text=f"Variante combinada: {nueva_variante_combinada}")
                result_label.pack(pady=5)
                guardar_combinaciones_csv(f"variante_combinada_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", [nueva_variante_combinada], [[]])
            else:
                result_label = tk.Label(pair_window, text="Uno o ambos números de variante no existen en el contenedor de datos.")
                result_label.pack(pady=5)

        combine_button = tk.Button(pair_window, text="Combinar", command=combine)
        combine_button.pack(pady=10)

        pair_window.mainloop()

    def combine_ranges():
        range_window = tk.Tk()
        range_window.title("Combinar por rangos")
        range_window.geometry("300x200")

        label_start = tk.Label(range_window, text="Número de inicio del rango:")
        label_start.pack(pady=5)
        start_entry = tk.Entry(range_window)
        start_entry.pack(pady=5)

        label_end = tk.Label(range_window, text="Número de fin del rango:")
        label_end.pack(pady=5)
        end_entry = tk.Entry(range_window)
        end_entry.pack(pady=5)

        def combine():
            rango_inicio = int(start_entry.get())
            rango_fin = int(end_entry.get())
            rango = (rango_inicio, rango_fin)
            nuevas_combinaciones = combinar_variante_con_combinaciones(contenedor_datos, rango, cadena_original)
            for nombre, combinacion in nuevas_combinaciones.items():
                result_label = tk.Label(range_window, text=f"{nombre}: {combinacion}")
                result_label.pack(pady=5)
            guardar_combinaciones_csv(f"nuevas_combinaciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", list(nuevas_combinaciones.values()), [[]])

        combine_button = tk.Button(range_window, text="Combinar", command=combine)
        combine_button.pack(pady=10)

        range_window.mainloop()

    pairs_button = tk.Button(options_window, text="Combinar pares", command=combine_pairs)
    pairs_button.pack(pady=5)

    ranges_button = tk.Button(options_window, text="Combinar por rangos", command=combine_ranges)
    ranges_button.pack(pady=5)

    options_window.mainloop()

def main():
    window = tk.Tk()
    window.title("Combinación de Cadenas")
    window.geometry("400x200")

    button = tk.Button(window, text="Seleccionar Archivo CSV", command=select_file)
    button.pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    main()
