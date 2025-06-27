import cv2
import os
import json
import cv2.data

# Ruta a la carpeta de imágenes
IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'public')
# Archivo de salida
OUTPUT_JSON = os.path.join(os.path.dirname(__file__), 'faces.json')
# Archivo con los nombres de las caras
CARAS_TXT = os.path.join(os.path.dirname(__file__), 'caras.txt')

# Obtener la ruta del archivo haarcascade de OpenCV
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
if not os.path.exists(cascade_path):
    raise FileNotFoundError(f'No se encontró el archivo haarcascade_frontalface_default.xml en {cascade_path}')

face_cascade = cv2.CascadeClassifier(cascade_path)

# Extensiones de imagen válidas
VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}

# Leer el archivo de nombres de caras
nombres_caras = {}
if os.path.exists(CARAS_TXT):
    with open(CARAS_TXT, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                partes = line.split('\t')
                if len(partes) >= 3:
                    año = partes[0]
                    numero_cara = int(partes[1])
                    nombre = partes[2]
                    if año not in nombres_caras:
                        nombres_caras[año] = {}
                    nombres_caras[año][numero_cara] = nombre

faces_data = {}

for filename in os.listdir(IMAGES_DIR):
    name, ext = os.path.splitext(filename)
    if ext not in VALID_EXTENSIONS:
        continue
    
    # Obtener el año del nombre del archivo (sin extensión)
    año = name
    
    image_path = os.path.join(IMAGES_DIR, filename)
    image = cv2.imread(image_path)
    if image is None:
        print(f"No se pudo leer la imagen: {filename}")
        continue
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    caras = []
    for idx, (x, y, w, h) in enumerate(faces, start=1):
        # Buscar el nombre en el diccionario de nombres
        nombre = nombres_caras.get(año, {}).get(idx, '')
        
        caras.append({
            'id': idx,
            'x': int(x),
            'y': int(y),
            'w': int(w),
            'h': int(h),
            'nombre': nombre
        })
    
    faces_data[filename] = caras
    
    caras_con_nombre = sum(1 for cara in caras if cara['nombre'])
    print(f"{filename}: {len(caras)} cara(s) detectada(s), {caras_con_nombre} con nombre")

# Guardar resultados en faces.json
with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(faces_data, f, indent=2, ensure_ascii=False)

print(f"\nDetección completada. Resultados guardados en {OUTPUT_JSON}") 