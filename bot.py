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
fase = -1
stop_requested = False  # Variable global para detener el bucle
val_mode = "numbers"
val_max = 1000
val_min = 20
prev = -1000 #variable para el incremento
reader = easyocr.Reader(['es']) 

def submit_percentage():
    global val_max, val_min, val_mode
    val_max = float(entry_max.get())
    val_min = float(entry_min.get())
    val_mode = "percent"

def submit_numbers():
    global val_max, val_min, val_mode
    val_max = float(entry_max.get())
    val_min = float(entry_min.get()) * -1
    val_mode = "numbers"

def start_window():
    print(f'Max: {val_max}, Min: {val_min}, mode: {val_mode}')
    new_window = tk.Toplevel()
    new_window.title("Nueva Ventana")

    button1 = tk.Button(new_window, text="Sin operaciones", command=lambda: open_second_window(0))
    button1.pack(pady=10)

    button2 = tk.Button(new_window, text="Long Abierta", command=lambda: open_second_window(2))
    button2.pack(pady=10)

    button3 = tk.Button(new_window, text="Short Abierta", command=lambda: open_second_window(4))
    button3.pack(pady=10)

def stop_program():
    global stop_requested
    stop_requested = True  # Cuando se pulse STOP, cambia a True

def cambio_short():
    global fase
    fase = 4

def cambio_long():
    global fase
    fase = 2

def no_operacion():
    global fase
    fase = 0

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
    stop_button = tk.Button(second_window, text="STOP", command=lambda: (stop_program(),second_window.destroy()))
    stop_button.pack(pady=20)
    short_button = tk.Button(second_window, text="Short abierta", command=cambio_short)
    short_button.pack(pady=20)
    long_button = tk.Button(second_window, text="Long abierta", command=cambio_long)
    long_button.pack(pady=20)
    no_button = tk.Button(second_window, text="No hay operacion", command=no_operacion)
    no_button.pack(pady=20)

    # Ejecutar el bucle de la segunda ventana
    second_window.mainloop()

#Abrir opcion short o long
def abrir_operacion():
    global roi_buttons
    # print('Abriendo operacion en la region', roi_buttons)
    # time.sleep(2)
    # pyautogui.screenshot('test.png',region=roi_buttons)
    buttonDrag = pyautogui.locateOnScreen('./muestras/buttonAbrir.png', confidence=0.8, region=roi_buttons)
    buttonDragCenter = pyautogui.center(buttonDrag)
    pyautogui.moveTo(buttonDragCenter.x, buttonDragCenter.y)
    pyautogui.click()
    time.sleep(0.5)

#Mover Slide
def drag_operacion():
    global roi_buttons
    buttonDrag = pyautogui.locateOnScreen('./muestras/buttonDrag.png', confidence=0.8, region=roi_buttons)
    buttonDragCenter = pyautogui.center(buttonDrag)
    pyautogui.moveTo(buttonDragCenter.x, buttonDragCenter.y)
    pyautogui.dragRel(1200, 0, duration=0.2)
    pyautogui.click()
    time.sleep(0.5)

#Abrir short
def abrir_short():
    global roi_buttons
    drag_operacion()
    buttonDrag = pyautogui.locateOnScreen('./muestras/buttonShort.png', confidence=0.8, region=roi_buttons)
    buttonDragCenter = pyautogui.center(buttonDrag)
    pyautogui.moveTo(buttonDragCenter.x, buttonDragCenter.y)
    time.sleep(1)
    pyautogui.click()

#Abrir long
def abrir_long():
    global roi_buttons
    drag_operacion()
    buttonDrag = pyautogui.locateOnScreen('./muestras/buttonLong.png', confidence=0.8 , region=roi_buttons)
    buttonDragCenter = pyautogui.center(buttonDrag)
    pyautogui.moveTo(buttonDragCenter.x, buttonDragCenter.y)
    time.sleep(1)
    pyautogui.click()

#Cerrar operacion
def cerrar_operacion():
    global roi_buttons
    buttonDrag = pyautogui.locateOnScreen('./muestras/buttonCerrar.png', confidence=0.8, region=roi_buttons)
    buttonDragCenter = pyautogui.center(buttonDrag)
    pyautogui.moveTo(buttonDragCenter.x, buttonDragCenter.y)
    pyautogui.click()

def control_increment(prev, next, op_open):
    global fase
    print(f'Prev: {prev}, Next: {next}')
    next = float(next)
    if(next <= val_min):
        print('corta operacion bajo')
        cerrar_operacion()
        time.sleep(0.1)
        fase = 0
    elif(next >= val_max and (next - prev) < -2):
        cerrar_operacion()
        time.sleep(0.1)

        fase = 0
        return -1000
    else:
        return next



#Detectar valor
def detec_value(op_open):
    global prev
    try:
        negativo = False
        buttonDrag = pyautogui.locateOnScreen('./muestras/percentReference.png', confidence=0.8) or pyautogui.locateOnScreen('./muestras/percentAltReference.png', confidence=0.8)
        if buttonDrag is not None:
            buttonDragCenter = pyautogui.center(buttonDrag)
            print(buttonDragCenter.x, buttonDragCenter.y)
            
            # Mueve el cursor a la posición del botón
            # pyautogui.moveTo(buttonDragCenter.x, buttonDragCenter.y)
            # time.sleep(1)

            # Define el ancho y alto para la captura
            width, height = 300, 40  # Cambia estos valores según tus necesidades

            # Calcula las coordenadas del área a capturar
            left = int(buttonDragCenter.x - width // 2) - 165
            top = int(buttonDragCenter.y - height // 2)

            # Verifica que las coordenadas no sean negativas
            if left < 0:
                left = 0
            if top < 0:
                top = 0

            # Obtiene la resolución de la pantalla
            screenWidth, screenHeight = pyautogui.size()
            
            # Asegúrate de que las coordenadas y el tamaño de la región estén dentro de los límites de la pantalla
            if left + width > screenWidth:
                width = screenWidth - left
            if top + height > screenHeight:
                height = screenHeight - top

            # Realiza la captura de pantalla
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            
            # Convierte la imagen a formato OpenCV
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Analiza el color en la región donde se espera el texto
            # Define un rango para los colores
            lower_red = np.array([0, 0, 100])
            upper_red = np.array([50, 50, 255])
            lower_green = np.array([0, 100, 0])
            upper_green = np.array([50, 255, 50])

            mask_red = cv2.inRange(screenshot_cv, lower_red, upper_red)
            mask_green = cv2.inRange(screenshot_cv, lower_green, upper_green)

            red_count = cv2.countNonZero(mask_red)
            green_count = cv2.countNonZero(mask_green)

            # Determina si el número es negativo o positivo
            if red_count > green_count:
                print("El número es negativo")
                negativo = True
            elif green_count > red_count:
                print("El número es positivo")
                negativo = False
            else:
                print("No se pudo determinar el signo del número")

            # reader = easyocr.Reader(['es']) 
            result = reader.readtext(screenshot_cv)

            # Imprime los resultados
            for (bbox, text, prob) in result:
                print(f'Texto: {text} (Confianza: {prob:.2f})')
                # print(text.split())
                # print(text.split()[0]) #value
                # print(text.split('(')[1].replace(')',''))# percent
                if(val_mode == "percent"):
                    num = text.split()[2].replace(')','').replace('%','').replace('(','')
                    if negativo:
                        num = num.replace('-','')
                        num = '-' + num
                    prev = control_increment(prev, num, op_open)
                if(val_mode == "numbers"):
                    num = text.split()[0]
                    if negativo:
                        num = num.replace('-','')
                        num = '-' + num
                    prev = control_increment(prev, num, op_open)

    except Exception as e:
        
        print('error al leer los numeros', e)




        # Muestra la imagen usando OpenCV
        # cv2.imshow('Captura', screenshot_cv)

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
    abrir_operacion()
    time.sleep(0.1)
    abrir_long()
    fase = 2  # Espera a la siguiente fase (esperar confirmación)

# Fase 2: Espera confirmación Long Cerrado
def fase_espera_confirmacion_long(resultado):
    global fase
    detec_value("long")
    for res in resultado:
        if res[1] == '51':  # Si se reconoce "51", cerramos Long
            print('Confirmación - Long Cerrado')
            cerrar_operacion()
            time.sleep(0.1)
            fase = 3  # Cambio a fase Short

# Fase 3: Short Abierto
def fase_short_abierto(resultado):
    global fase, s1
    print('Short Abierto - Capturando pantalla')
    pyautogui.screenshot(f'./detecciones/s1{s1}.png')
    s1 += 1
    abrir_operacion()
    time.sleep(0.1)
    abrir_short()
    fase = 4  # Espera a la siguiente fase (esperar confirmación)

# Fase 4: Espera confirmación Short Cerrado
def fase_espera_confirmacion_short(resultado):
    global fase
    detec_value("short")
    for res in resultado:
        if res[1] == 'B1':  # Si se reconoce "B1", abrimos de nuevo Long
            print('Confirmación - Short Cerrado')
            cerrar_operacion()
            time.sleep(0.1)
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

#Selección de ROI de botones
roi_buttons = cv2.selectROI('Selecciona el ROI de los botones', img_resized)
cv2.destroyWindow('Selecciona el ROI de los botones')

scale_x = img.shape[1] / width
scale_y = img.shape[0] / height

roi_buttons = (int(roi_buttons[0] * scale_x), int(roi_buttons[1] * scale_y), int(roi_buttons[2] * scale_x), int(roi_buttons[3] * scale_y))

# Iniciar el hilo para el OCR
ocr_thread = threading.Thread(target=ocr_processing_loop, args=(roi_original, reader))
ocr_thread.start()

# Crear la ventana principal con botones
root = tk.Tk()
root.title("Ventana principal")

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
button_percentage = tk.Button(root, text="Porcentaje", command=lambda: (submit_percentage(), root.withdraw(),start_window()))
button_percentage.pack(pady=10)

# Botón para números
button_numbers = tk.Button(root, text="Números", command=lambda: (submit_numbers(), root.withdraw(), start_window()))
button_numbers.pack(pady=10)

# Ejecutar el bucle de la ventana principal
root.mainloop()

# Esperar a que termine el hilo de OCR
ocr_thread.join()
