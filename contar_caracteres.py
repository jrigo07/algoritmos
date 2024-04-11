import os

def contar_caracteres(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Crear un diccionario para almacenar
    cuenta_caracteres = {}

    for caracter in contenido:
        if caracter in cuenta_caracteres:
            cuenta_caracteres[caracter] += 1
        else:
            cuenta_caracteres[caracter] = 1

    # Ordenar 
    caracteres_ordenados = sorted(cuenta_caracteres.items(), key=lambda x: x[1], reverse=True)

    return caracteres_ordenados

def guardar_resultado(resultado):
    ruta_programa = os.path.dirname(os.path.abspath(__file__))  
    ruta_resultado = os.path.join(ruta_programa, 'resultado.txt') 

    with open(ruta_resultado, 'w', encoding='utf-8') as f:
        f.write("Caracteres ordenados:\n")
        for caracter, cantidad in resultado:
            f.write(f"Caracter: {caracter}, Cantidad: {cantidad}\n")
    print("El resultado se ha guardado en 'resultado.txt'.")

archivo = r'C:\Users\usuario\Desktop\alg\Gullivers_Travels.txt'
resultado = contar_caracteres(archivo)

if resultado:
    print("Caracteres ordenados por cantidad:")
    for caracter, cantidad in resultado:
        print(f"Caracter: {caracter}, Cantidad: {cantidad}")
    guardar_resultado(resultado)
