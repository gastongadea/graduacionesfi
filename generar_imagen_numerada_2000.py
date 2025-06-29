import cv2
import os
import json
import numpy as np

# Ruta a la carpeta de imágenes
IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'public')
# Archivo con los datos de caras detectadas
FACES_JSON = os.path.join(os.path.dirname(__file__), 'faces.json')

def generar_imagen_numerada():
    """Genera la imagen 2000.jpg con recuadros y números sobre las caras detectadas"""
    
    # Leer los datos de caras detectadas
    if not os.path.exists(FACES_JSON):
        print(f"Error: No se encontró el archivo {FACES_JSON}")
        return
    
    with open(FACES_JSON, 'r', encoding='utf-8') as f:
        faces_data = json.load(f)
    
    # Verificar que existe la entrada para 2000.jpg
    if "2000.jpg" not in faces_data:
        print("Error: No se encontraron datos de caras para 2000.jpg")
        print("Primero ejecuta el reconocimiento de caras con: python detectar_caras_2000.py")
        return
    
    # Cargar la imagen original
    image_path = os.path.join(IMAGES_DIR, "2000.jpg")
    if not os.path.exists(image_path):
        print(f"Error: No se encontró la imagen {image_path}")
        return
    
    image = cv2.imread(image_path)
    if image is None:
        print(f"No se pudo leer la imagen: 2000.jpg")
        return
    
    # Crear una copia para dibujar
    image_with_boxes = image.copy()
    
    # Obtener las caras detectadas
    caras = faces_data["2000.jpg"]
    
    print(f"Generando imagen numerada para 2000.jpg...")
    print(f"Caras detectadas: {len(caras)}")
    
    # Dibujar recuadros y números para cada cara
    for cara in caras:
        x = cara['x']
        y = cara['y']
        w = cara['w']
        h = cara['h']
        cara_id = cara['id']
        
        # Dibujar rectángulo
        cv2.rectangle(image_with_boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Dibujar número
        # Crear un rectángulo de fondo para el número
        text = str(cara_id)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        thickness = 2
        
        # Obtener el tamaño del texto
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        
        # Posición del texto (arriba a la izquierda del rectángulo)
        text_x = x
        text_y = y - 10 if y - 10 > text_height else y + text_height
        
        # Dibujar rectángulo de fondo para el número
        cv2.rectangle(image_with_boxes, 
                     (text_x - 2, text_y - text_height - 2), 
                     (text_x + text_width + 2, text_y + 2), 
                     (0, 255, 0), -1)
        
        # Dibujar el número
        cv2.putText(image_with_boxes, text, (text_x, text_y), 
                   font, font_scale, (0, 0, 0), thickness)
        
        print(f"  Cara {cara_id}: x={x}, y={y}, w={w}, h={h}")
    
    # Guardar la imagen numerada
    output_path = os.path.join(IMAGES_DIR, "2000 - numerada.jpg")
    cv2.imwrite(output_path, image_with_boxes)
    
    print(f"\n✅ Imagen numerada guardada como: {output_path}")
    print(f"📊 Resumen:")
    print(f"   - Caras detectadas: {len(caras)}")
    print(f"   - Imagen original: {image_path}")
    print(f"   - Imagen numerada: {output_path}")
    
    # Mostrar información sobre cómo usar la imagen
    print(f"\n📝 Instrucciones:")
    print(f"   1. Abre la imagen '2000 - numerada.jpg'")
    print(f"   2. Identifica cada persona por su número")
    print(f"   3. Edita el archivo 'caras.txt' agregando las líneas:")
    print(f"      2000\t1\tNombre Apellido")
    print(f"      2000\t2\tNombre Apellido")
    print(f"      ...")
    print(f"   4. Ejecuta: python detectar_caras_2000.py")
    print(f"   5. Ejecuta: python server.py")

if __name__ == "__main__":
    generar_imagen_numerada() 