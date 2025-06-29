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
# Archivo final con caras numeradas
FACES_NUMBERED_JSON = os.path.join(os.path.dirname(__file__), 'faces-numbered.json')

# Obtener la ruta del archivo haarcascade de OpenCV
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
if not os.path.exists(cascade_path):
    raise FileNotFoundError(f'No se encontró el archivo haarcascade_frontalface_default.xml en {cascade_path}')

face_cascade = cv2.CascadeClassifier(cascade_path)

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

# Leer el archivo faces.json existente
faces_data = {}
if os.path.exists(OUTPUT_JSON):
    with open(OUTPUT_JSON, 'r', encoding='utf-8') as f:
        faces_data = json.load(f)

# Procesar solo la imagen 2000.jpg
filename = "2000.jpg"
image_path = os.path.join(IMAGES_DIR, filename)

if not os.path.exists(image_path):
    print(f"Error: No se encontró la imagen {filename}")
    exit(1)

print(f"Procesando {filename}...")

image = cv2.imread(image_path)
if image is None:
    print(f"No se pudo leer la imagen: {filename}")
    exit(1)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

caras = []
for idx, (x, y, w, h) in enumerate(faces, start=1):
    # Buscar el nombre en el diccionario de nombres
    nombre = nombres_caras.get('2000', {}).get(idx, '')
    
    caras.append({
        'id': idx,
        'x': int(x),
        'y': int(y),
        'w': int(w),
        'h': int(h),
        'nombre': nombre
    })

# Actualizar solo la entrada para 2000.jpg
faces_data[filename] = caras

caras_con_nombre = sum(1 for cara in caras if cara['nombre'])
print(f"{filename}: {len(caras)} cara(s) detectada(s), {caras_con_nombre} con nombre")

# Guardar resultados actualizados en faces.json
with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(faces_data, f, indent=2, ensure_ascii=False)

print(f"Archivo {OUTPUT_JSON} actualizado")

# Ahora regenerar faces-numbered.json
print("Regenerando faces-numbered.json...")

faces_numbered = {}
for filename, caras in faces_data.items():
    # Obtener el año del nombre del archivo (sin extensión)
    año = os.path.splitext(filename)[0]
    
    caras_con_nombres = []
    for cara in caras:
        cara_id = cara['id']
        # Buscar el nombre en el diccionario de nombres
        nombre = nombres_caras.get(año, {}).get(cara_id, '')
        
        cara_con_nombre = {
            'id': cara_id,
            'x': cara['x'],
            'y': cara['y'],
            'w': cara['w'],
            'h': cara['h'],
            'nombre': nombre
        }
        caras_con_nombres.append(cara_con_nombre)
    
    faces_numbered[filename] = caras_con_nombres

# Guardar el resultado
with open(FACES_NUMBERED_JSON, 'w', encoding='utf-8') as f:
    json.dump(faces_numbered, f, indent=2, ensure_ascii=False)

# Mostrar estadísticas
total_caras = sum(len(caras) for caras in faces_numbered.values())
total_con_nombre = sum(
    sum(1 for cara in caras if cara['nombre']) 
    for caras in faces_numbered.values()
)

print(f"\nProcesamiento completado:")
print(f"- Total de caras detectadas: {total_caras}")
print(f"- Caras con nombre asignado: {total_con_nombre}")
print(f"- Archivo generado: {FACES_NUMBERED_JSON}")

# Mostrar estadísticas específicas para 2000
if "2000.jpg" in faces_numbered:
    caras_2000 = faces_numbered["2000.jpg"]
    caras_con_nombre_2000 = sum(1 for cara in caras_2000 if cara['nombre'])
    print(f"\nEstadísticas para 2000:")
    print(f"  Caras detectadas: {len(caras_2000)}")
    print(f"  Caras con nombre: {caras_con_nombre_2000}") 