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
fase = 0
stop_requested = False  # Variable global para detener el bucle

def stop_program():
    global stop_requested
    stop_requested = True  # Cuando se pulse STOP, cambia a True

def open_second_window(value):
    global fase
    fase = value
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

#Abrir opcion short o long
def abrir_operacion(resultado):
    buttonDrag = pyautogui.locateOnScreen('./muestras/buttonAbrir.png', confidence=0.8)
    buttonDragCenter = pyautogui.center(buttonDrag)
    pyautogui.moveTo(buttonDragCenter.x, buttonDragCenter.y)
    pyautogui.click()

#Mover Slide
def drag_operacion(resultado):
    buttonDrag = pyautogui.locateOnScreen('./muestras/buttonDrag.png', confidence=0.8)
    buttonDragCenter = pyautogui.center(buttonDrag)
    pyautogui.moveTo(buttonDragCenter.x, buttonDragCenter.y)
    pyautogui.dragRel(1000, 0, duration=0.2)
    pyautogui.click()
    time.sleep(1)

#Abrir short
def abrir_short(resultado):
    buttonDrag = pyautogui.locateOnScreen('./muestras/buttonShort.png', confidence=0.8)
    buttonDragCenter = pyautogui.center(buttonDrag)
    pyautogui.moveTo(buttonDragCenter.x, buttonDragCenter.y)
    pyautogui.click()

#Abrir long
def abrir_long(resultado):
    buttonDrag = pyautogui.locateOnScreen('./muestras/buttonLong.png', confidence=0.8)
    buttonDragCenter = pyautogui.center(buttonDrag)
    pyautogui.moveTo(buttonDragCenter.x, buttonDragCenter.y)
    pyautogui.click()

#Cerrar operacion
def cerrar_operacion(resultado):
    buttonDrag = pyautogui.locateOnScreen('./muestras/buttonCerrar.png', confidence=0.8)
    buttonDragCenter = pyautogui.center(buttonDrag)
    pyautogui.moveTo(buttonDragCenter.x, buttonDragCenter.y)
    pyautogui.click()

# Fase 0: Sin Operaciones
def fase_sin_operaciones(resultado):
    global fase
    for res in resultado:
        if res[1] == 'B1':
            print('Transición a Long Abierto')
            fase = 1
        elif res[1] == '51':
            print('Transición a Short Abierto')
            fase = 3

# Fase 1: Long Abierto
def fase_long_abierto(resultado):
    global fase, b1
    print('Long Abierto - Capturando pantalla')
    pyautogui.screenshot(f'./detecciones/b1{b1}.png')
    b1 += 1
    fase = 2  # Espera a la siguiente fase (esperar confirmación)

# Fase 2: Espera confirmación Long Cerrado
def fase_espera_confirmacion_long(resultado):
    global fase
    for res in resultado:
        if res[1] == '51':  # Si se reconoce "51", cerramos Long
            print('Confirmación - Long Cerrado')
            fase = 3  # Cambio a fase Short

# Fase 3: Short Abierto
def fase_short_abierto(resultado):
    global fase, s1
    print('Short Abierto - Capturando pantalla')
    pyautogui.screenshot(f'./detecciones/s1{s1}.png')
    s1 += 1
    fase = 4  # Espera a la siguiente fase (esperar confirmación)

# Fase 4: Espera confirmación Short Cerrado
def fase_espera_confirmacion_short(resultado):
    global fase
    for res in resultado:
        if res[1] == 'B1':  # Si se reconoce "B1", abrimos de nuevo Long
            print('Confirmación - Short Cerrado')
            fase = 1  # Cambio a fase Long

def ocr_processing_loop(roi_original, reader):
    global stop_requested, fase
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

        # Control de Fases
        if fase == 0:
            fase_sin_operaciones(resultado)
        elif fase == 1:
            fase_long_abierto(resultado)
        elif fase == 2:
            fase_espera_confirmacion_long(resultado)
        elif fase == 3:
            fase_short_abierto(resultado)
        elif fase == 4:
            fase_espera_confirmacion_short(resultado)

        print(f'Fase actual: {fase} a las {now.time()}')
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
