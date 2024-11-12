import pyautogui
import time
import cv2
import numpy as np
import easyocr

# Localiza el botón en la pantalla
buttonDrag = pyautogui.locateOnScreen('./muestras/percentReference.png', confidence=0.8)
print(buttonDrag)

# Verifica si se encontró el botón
if buttonDrag is not None:
    buttonDragCenter = pyautogui.center(buttonDrag)
    print(buttonDragCenter.x, buttonDragCenter.y)
    
    # Mueve el cursor a la posición del botón
    pyautogui.moveTo(buttonDragCenter.x, buttonDragCenter.y)
    time.sleep(1)

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
    elif green_count > red_count:
        print("El número es positivo")
    else:
        print("No se pudo determinar el signo del número")

    # Usa EasyOCR para leer el texto
    reader = easyocr.Reader(['es']) 
    result = reader.readtext(screenshot_cv)

    # Imprime los resultados
    for (bbox, text, prob) in result:
        print(f'Texto: {text} (Confianza: {prob:.2f})')
        if '(' in text:
            print(text.split('(')[1].replace(')',''))  # porcentaje

    # Muestra la imagen usando OpenCV
    cv2.imshow('Captura', screenshot_cv)

    # Mantiene la ventana abierta hasta que se presione una tecla
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
else:
    print("No se encontró el botón en la pantalla.")
