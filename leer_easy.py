import easyocr
import cv2

# Inicializa el lector de EasyOCR
reader = easyocr.Reader(['es'])  # Cambia 'es' por el idioma que necesites

# Carga la imagen
image_path = './demos/percent.png'  # Reemplaza con la ruta de tu imagen
image = cv2.imread(image_path)

# Lee el texto de la imagen
result = reader.readtext(image)

# Imprime los resultados
for (bbox, text, prob) in result:
    print(f'Texto: {text} (Confianza: {prob:.2f})')
    print(text.split()[0]) #value
    print(text.split('(')[1].replace(')',''))# percent
