import cv2
import numpy as np
import pytesseract

# Función vacía necesaria para las trackbars
def nothing(x):
    pass

COLOR_MASKS = [
    [0,0,143],
    [148, 213, 255]
]

# Leer la imagen
imagen = cv2.imread('./demos/ejemplo4.png')
imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# Crear una ventana
cv2.namedWindow('Control HSV')

# Crear las trackbars para ajustar los valores de HSV
cv2.createTrackbar('H Min', 'Control HSV', 0, 179, nothing)
cv2.createTrackbar('H Max', 'Control HSV', 179, 179, nothing)
cv2.createTrackbar('S Min', 'Control HSV', 0, 255, nothing)
cv2.createTrackbar('S Max', 'Control HSV', 255, 255, nothing)
cv2.createTrackbar('V Min', 'Control HSV', 0, 255, nothing)
cv2.createTrackbar('V Max', 'Control HSV', 255, 255, nothing)
while True:
    h_min = cv2.getTrackbarPos('H Min', 'Control HSV')
    h_max = cv2.getTrackbarPos('H Max', 'Control HSV')
    s_min = cv2.getTrackbarPos('S Min', 'Control HSV')
    s_max = cv2.getTrackbarPos('S Max', 'Control HSV')
    v_min = cv2.getTrackbarPos('V Min', 'Control HSV')
    v_max = cv2.getTrackbarPos('V Max', 'Control HSV')

    ##################################################################
    # color_bajo = np.array([h_min, s_min, v_min])
    # color_alto = np.array([h_max, s_max, v_max])
    color_bajo = np.array([COLOR_MASKS[0]])
    color_alto = np.array([COLOR_MASKS[1]])
    

    # Crear una máscara basada en los valores HSV
    mascara = cv2.inRange(imagen_hsv, color_bajo, color_alto)

    # Aplicar la máscara a la imagen original
    resultado = cv2.bitwise_and(imagen, imagen, mask=mascara)
    

    # cv2.imwrite('filtro_ej4.png',resultado)
    cv2.imshow('Resultado: ', resultado)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()