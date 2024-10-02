import cv2
import pytesseract
import numpy as np

# Ruta a la imagen
ruta_imagen = './demos/ejemplo2.png'

# Leer la imagen
imagen = cv2.imread(ruta_imagen)

# Convertir a escala de grises
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aumentar el tamaño de la imagen (escalar) para mejorar OCR en textos pequeños
imagen_escalada = cv2.resize(imagen_gris, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# Aumentar el contraste de la imagen usando ecualización de histograma
imagen_contraste = cv2.equalizeHist(imagen_escalada)

# Aplicar un filtro de dilatación para mejorar los caracteres
kernel = np.ones((2, 2), np.uint8)
imagen_dilatada = cv2.dilate(imagen_contraste, kernel, iterations=1)

# Aplicar OCR
custom_config = r'--oem 3 --psm 6'  # Ajustar la configuración de Tesseract si es necesario
texto = pytesseract.image_to_string(imagen_dilatada, config=custom_config)

# Mostrar los resultados
print("Texto reconocido tras preprocesamiento:", texto)

# Filtrar específicamente "S1" y "B1"
if "S1" in texto:
    print("S1 detectado")
if "B1" in texto:
    print("B1 detectado")

# Mostrar las imágenes procesadas
cv2.imshow('Imagen Escalada y Contraste Mejorado', imagen_dilatada)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Recortar manualmente las áreas de interés basadas en las posiciones aproximadas
# Estas coordenadas deben ser ajustadas según la imagen
# Recorte para el área de "S1"
recorte_s1 = imagen_gris[218:270, 770:820]  # Ajusta según la posición real de S1
recorte_b1 = imagen_gris[600:650, 800:850]  # Ajusta según la posición real de B1

# Aplicar OCR en los recortes
texto_s1 = pytesseract.image_to_string(recorte_s1, config=custom_config)
texto_b1 = pytesseract.image_to_string(recorte_b1, config=custom_config)

# Mostrar los textos detectados en esas áreas
print("Texto en área S1:", texto_s1)
print("Texto en área B1:", texto_b1)

# Mostrar las imágenes recortadas (opcional)
cv2.imshow('Recorte S1', recorte_s1)
cv2.imshow('Recorte B1', recorte_b1)
cv2.waitKey(0)
cv2.destroyAllWindows()

