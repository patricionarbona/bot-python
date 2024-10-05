import cv2
import pyautogui
import time
import numpy as np
import easyocr
import datetime
import tkinter as tk
import threading

COLOR_MASKS = [
    [0, 0, 143],
    [148, 213, 255]
]
b1 = 0
s1 = 0
stop_requested = False  # Variable global para detener el bucle

def stop_program():
    global stop_requested
    stop_requested = True  # Cuando se pulse STOP, cambia a True

def open_second_window(value):
    global stop_requested
    stop_requested = False  # Reiniciar el valor cuando se abre la ventana

    # Cerrar la ventana principal
    root.destroy()

    # Crear la segunda ventana
    second_window = tk.Tk()
    second_window.title("Segunda ventana")
    
    print(f"Valor seleccionado: {value}")
    
    # Crear el botón STOP en la segunda ventana
    stop_button = tk.Button(second_window, text="STOP", command=stop_program)
    stop_button.pack(pady=20)

    # Ejecutar el bucle de la segunda ventana
    second_window.mainloop()

def ocr_processing_loop(roi_original, reader):
    global stop_requested
    while not stop_requested:  # El bucle se ejecuta mientras stop_requested sea False
        now = datetime.datetime.now()

        # Realiza la captura de pantalla
        pyautogui.screenshot('ah.png')
        img = cv2.imread('ah.png')

        # Recorta la imagen original utilizando las coordenadas ajustadas
        img_crop = img[roi_original[1]:roi_original[1]+roi_original[3], roi_original[0]:roi_original[0]+roi_original[2]]

        ########################
        # Filtrado de color 
        imagen_hsv = cv2.cvtColor(img_crop, cv2.COLOR_BGR2HSV)
        color_bajo = np.array(COLOR_MASKS[0])
        color_alto = np.array(COLOR_MASKS[1])

        # Crear una máscara basada en los valores HSV
        mascara = cv2.inRange(imagen_hsv, color_bajo, color_alto)

        # Aplicar la máscara a la imagen original
        img_filtrada = cv2.bitwise_and(img_crop, img_crop, mask=mascara)

        ###################
        # OCR con EasyOCR

        img_gris = cv2.cvtColor(img_filtrada, cv2.COLOR_BGR2GRAY)

        img_ocr = cv2.resize(img_gris, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        img_ocr = cv2.GaussianBlur(img_ocr, (3, 3), 0)
        img_ocr = cv2.equalizeHist(img_ocr)

        resultado = reader.readtext(img_ocr)

        # Imprimir los resultados reconocidos con la hora actual
        for res in resultado:
            print(f'Texto reconocido: {res[1]} a las {now.time()}')
            if res[1] == '51':
                pyautogui.screenshot(f'./detecciones/s1{s1}.png')
                s1 += 1
            if res[1] == 'B1':
                pyautogui.screenshot(f'./detecciones/b1{b1}.png')
                b1 += 1

        print(f'{now.time()}')
        time.sleep(5)  # Pausa de 5 segundos antes de la siguiente iteración

    cv2.destroyAllWindows()

# Crear el lector de EasyOCR
reader = easyocr.Reader(['en']) 

time.sleep(2)

# Realiza la captura de pantalla inicial
pyautogui.screenshot('ah.png')
img = cv2.imread('ah.png')

# Redimensionar la imagen si es demasiado grande
width = 1500 
height = int(img.shape[0] * (width / img.shape[1]))
img_resized = cv2.resize(img, (width, height))

# Selección de ROI en la imagen redimensionada
roi = cv2.selectROI('Selecciona el ROI', img_resized)
cv2.destroyWindow('Selecciona el ROI')

scale_x = img.shape[1] / width
scale_y = img.shape[0] / height

roi_original = (int(roi[0] * scale_x), int(roi[1] * scale_y), int(roi[2] * scale_x), int(roi[3] * scale_y))

# Iniciar el hilo para el OCR
ocr_thread = threading.Thread(target=ocr_processing_loop, args=(roi_original, reader))
ocr_thread.start()

# Crear la ventana principal con botones
root = tk.Tk()
root.title("Ventana principal")

# Crear los tres botones en la ventana principal, cada uno con un valor distinto
button1 = tk.Button(root, text="Sin operaciones", command=lambda: open_second_window(0))
button1.pack(pady=10)

button2 = tk.Button(root, text="Long Abierta", command=lambda: open_second_window(1))
button2.pack(pady=10)

button3 = tk.Button(root, text="Short Abierta", command=lambda: open_second_window(3))
button3.pack(pady=10)

# Ejecutar el bucle de la ventana principal
root.mainloop()

# Esperar a que termine el hilo de OCR
ocr_thread.join()
