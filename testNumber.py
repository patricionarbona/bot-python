import tkinter as tk
from tkinter import ttk

def on_percentage(max_value, min_value):
    print(f"Botón de porcentaje presionado. Max: {max_value}, Min: {min_value}")
    root.destroy()

def on_numbers(max_value, min_value):
    print(f"Botón de números presionado. Max: {max_value}, Min: {min_value}")
    root.destroy()

def submit_percentage():
    max_value = entry_max.get()
    min_value = entry_min.get()
    on_percentage(max_value, min_value)

def submit_numbers():
    max_value = entry_max.get()
    min_value = entry_min.get()
    on_numbers(max_value, min_value)

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz de Tkinter")

# Campo para el valor máximo
label_max = ttk.Label(root, text="Valor máximo:")
label_max.pack(pady=5)
entry_max = ttk.Entry(root)
entry_max.pack(pady=5)

# Campo para el valor mínimo
label_min = ttk.Label(root, text="Valor mínimo:")
label_min.pack(pady=5)
entry_min = ttk.Entry(root)
entry_min.pack(pady=5)

# Botón para porcentaje
button_percentage = ttk.Button(root, text="Porcentaje", command=submit_percentage)
button_percentage.pack(pady=10)

# Botón para números
button_numbers = ttk.Button(root, text="Números", command=submit_numbers)
button_numbers.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()
