import cv2
import pytesseract
import numpy as np

# Ruta a la imagen que subiste
# ruta_imagen = './demos/ejemplo2.png'
ruta_imagen = './demos/filtro_ej4.png'

# Leer la imagen
imagen = cv2.imread(ruta_imagen)

# Convertir la imagen a escala de grises
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Coordenadas para recortar las áreas de S1 y B1
# Puedes seguir ajustando estas coordenadas si es necesario
recorte_s1 = imagen_gris[210:245, 450:490]  # Ajustar según ubicación de S1
recorte_b1 = imagen_gris[300:340, 500:540]  # Ajustar según ubicación de B1

# Aumentar el tamaño de los recortes para mejorar el OCR
recorte_s1 = cv2.resize(recorte_s1, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
recorte_b1 = cv2.resize(recorte_b1, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

# Aplicar filtro de suavizado para reducir el ruido
recorte_s1 = cv2.GaussianBlur(recorte_s1, (3, 3), 0)
recorte_b1 = cv2.GaussianBlur(recorte_b1, (3, 3), 0)

# Aumentar el contraste con ecualización de histograma
recorte_s1 = cv2.equalizeHist(recorte_s1)
recorte_b1 = cv2.equalizeHist(recorte_b1)

# Aplicar OCR en los recortes
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
texto_s1 = pytesseract.image_to_string(recorte_s1, config=custom_config)
texto_b1 = pytesseract.image_to_string(recorte_b1, config=custom_config)

# Mostrar los textos detectados en las áreas de recorte
print("Texto detectado en área S1:", texto_s1.strip())
print("Texto detectado en área B1:", texto_b1.strip())

# Mostrar las imágenes recortadas para verlas (opcional)
cv2.imshow('Recorte S1', recorte_s1)
cv2.imshow('Recorte B1', recorte_b1)
cv2.waitKey(0)
cv2.destroyAllWindows()
