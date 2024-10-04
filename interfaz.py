import tkinter as tk

# Función para abrir la segunda ventana con el botón STOP
def open_second_window(value):
    # Cerrar la ventana principal
    root.destroy()

    # Crear la segunda ventana
    second_window = tk.Tk()
    second_window.title("Segunda ventana")
    
    # Mostrar el valor seleccionado en la consola (puedes utilizarlo como prefieras)
    print(f"Valor seleccionado: {value}")
    
    # Crear el botón STOP en la segunda ventana
    stop_button = tk.Button(second_window, text="STOP", command=second_window.quit)
    stop_button.pack(pady=20)

    # Ejecutar el bucle de la segunda ventana
    second_window.mainloop()

# Crear la ventana principal
root = tk.Tk()
root.title("Ventana principal")

# Crear los tres botones en la ventana principal, cada uno con un valor distinto
button1 = tk.Button(root, text="Botón 1 (Valor 10)", command=lambda: open_second_window(10))
button1.pack(pady=10)

button2 = tk.Button(root, text="Botón 2 (Valor 20)", command=lambda: open_second_window(20))
button2.pack(pady=10)

button3 = tk.Button(root, text="Botón 3 (Valor 30)", command=lambda: open_second_window(30))
button3.pack(pady=10)

# Ejecutar el bucle de la ventana principal
root.mainloop()
