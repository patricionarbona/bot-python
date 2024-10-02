import cv2
import pyautogui
import time
import numpy as np
import easyocr
import datetime

COLOR_MASKS = [
    [0, 0, 143],
    [148, 213, 255]
]
b1 = 0
s1 = 0

# Crear el lector de EasyOCR
reader = easyocr.Reader(['en'])  # Puedes agregar más idiomas si es necesario

# Espera 2 segundos para dar tiempo al usuario a preparar la captura de pantalla
time.sleep(2)

# Realiza la captura de pantalla
pyautogui.screenshot('ah.png')
img = cv2.imread('ah.png')

# Redimensionar la imagen si es demasiado grande (ajusta el tamaño según lo necesites)
width = 1500  # Cambia este valor según lo que prefieras
height = int(img.shape[0] * (width / img.shape[1]))  # Mantener proporción
img_resized = cv2.resize(img, (width, height))

# Selección de ROI en la imagen redimensionada
roi = cv2.selectROI('Selecciona el ROI', img_resized)
cv2.destroyWindow('Selecciona el ROI')

# Ajusta las coordenadas del ROI en función del redimensionamiento
scale_x = img.shape[1] / width
scale_y = img.shape[0] / height

roi_original = (int(roi[0] * scale_x), int(roi[1] * scale_y), int(roi[2] * scale_x), int(roi[3] * scale_y))

while True:
    now = datetime.datetime.now()  # Actualizar la hora en cada iteración

    # Recorta la imagen original utilizando las coordenadas ajustadas
    img_crop = img[roi_original[1]:roi_original[1]+roi_original[3], roi_original[0]:roi_original[0]+roi_original[2]]

    ########################
    ## Filtrado de color 
    imagen_hsv = cv2.cvtColor(img_crop, cv2.COLOR_BGR2HSV)
    color_bajo = np.array(COLOR_MASKS[0])
    color_alto = np.array(COLOR_MASKS[1])

    # Crear una máscara basada en los valores HSV
    mascara = cv2.inRange(imagen_hsv, color_bajo, color_alto)

    # Aplicar la máscara a la imagen original
    img_filtrada = cv2.bitwise_and(img_crop, img_crop, mask=mascara)

    ###################
    ## OCR con EasyOCR

    # Convertir la imagen a escala de grises
    img_gris = cv2.cvtColor(img_filtrada, cv2.COLOR_BGR2GRAY)

    # Redimensionar y aplicar preprocesamiento
    img_ocr = cv2.resize(img_gris, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    img_ocr = cv2.GaussianBlur(img_ocr, (3, 3), 0)
    img_ocr = cv2.equalizeHist(img_ocr)

    # Usar EasyOCR para realizar la lectura OCR en la imagen preprocesada
    resultado = reader.readtext(img_ocr)

    # Imprimir los resultados reconocidos con la hora actual
    for res in resultado:
        print(f'Texto reconocido: {res[1]} a las')
        print(type(res[1]))
        if res[1] == '51':
            pyautogui.screenshot(f'./detecciones/s1{s1}.png')
            s1 += 1
        if res[1] == 'B1':
            pyautogui.screenshot(f'./detecciones/b1{b1}.png')
            b1 += 1
    print(f'{now.time()}')
    # Control para salir del bucle con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Pausa de 5 segundos antes de la siguiente iteración
    time.sleep(300)
    pyautogui.screenshot('ah.png')
    img = cv2.imread('ah.png')

cv2.destroyAllWindows()
