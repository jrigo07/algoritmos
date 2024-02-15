#

import pandas as pd
import tkinter as tk
from tkinter import filedialog

def open_file_dialog():
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        print("Archivo seleccionado:", filepath)
        try:
            # Leer el contenido del archivo CSV y mostrarlo en la consola
            df = pd.read_csv(filepath)
            print("Contenido del archivo:")
            print(df.to_string(index=False))

        except Exception as e:
            print("Error", e)

root = tk.Tk()

frm = tk.Frame(root)
frm.grid(padx=10, pady=10)
tk.Label(frm, text="Hello World!").grid(column=0, row=0)

tk.Button(frm, text="Select CSV File", command=open_file_dialog).grid(column=1, row=0)
tk.Button(frm, text="Quit", command=root.destroy).grid(column=2, row=0)

root.mainloop()
