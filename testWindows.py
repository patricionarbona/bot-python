import tkinter as tk

val_mode = "numbers"
val_max = 1000
val_min = 20

def submit_percentage():
    global val_max, val_min, val_mode
    val_max = entry_max.get()
    val_min = entry_min.get()
    val_mode = "percent"

def submit_numbers():
    global val_max, val_min, val_mode
    val_max = entry_max.get()
    val_min = entry_min.get()
    val_mode = "numbers"

def start_window():
    print(f'Max: {val_max}, Min: {val_min}, mode: {val_mode}')
    new_window = tk.Toplevel()
    new_window.title("Nueva Ventana")

    button1 = tk.Button(new_window, text="Sin operaciones")
    button1.pack(pady=10)

    button2 = tk.Button(new_window, text="Long Abierta")
    button2.pack(pady=10)

    button3 = tk.Button(new_window, text="Short Abierta")
    button3.pack(pady=10)

    # Asegurarte de que la ventana principal se oculta
    

# Crear la ventana principal
root = tk.Tk()
root.title("Ventana principal")

label_max = tk.Label(root, text="Valor máximo:")
label_max.pack(pady=5)
entry_max = tk.Entry(root)
entry_max.pack(pady=5)

# Campo para el valor mínimo
label_min = tk.Label(root, text="Valor mínimo:")
label_min.pack(pady=5)
entry_min = tk.Entry(root)
entry_min.pack(pady=5)

# Botón para porcentaje
button_percentage = tk.Button(root, text="Porcentaje", command=lambda: (submit_percentage(), root.destroy()))
button_percentage.pack(pady=10)

# Botón para números
button_numbers = tk.Button(root, text="Números", command=lambda: (submit_numbers(), root.destroy()))
button_numbers.pack(pady=10)

# Ejecutar el bucle de la ventana principal
root.mainloop()

start_window()

while True:
    print('hola')