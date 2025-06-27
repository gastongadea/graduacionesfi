import json
import os

# Archivos de entrada y salida
CARAS_TXT = os.path.join(os.path.dirname(__file__), 'caras.txt')
FACES_JSON = os.path.join(os.path.dirname(__file__), 'faces.json')
OUTPUT_JSON = os.path.join(os.path.dirname(__file__), 'faces-numbered.json')

def leer_caras_txt():
    """Lee el archivo caras.txt y retorna un diccionario con los nombres"""
    nombres_caras = {}
    
    if not os.path.exists(CARAS_TXT):
        print(f"Error: No se encontró el archivo {CARAS_TXT}")
        return nombres_caras
    
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
    
    return nombres_caras

def leer_faces_json():
    """Lee el archivo faces.json y retorna los datos de caras detectadas"""
    if not os.path.exists(FACES_JSON):
        print(f"Error: No se encontró el archivo {FACES_JSON}")
        return {}
    
    with open(FACES_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def crear_faces_numbered():
    """Crea el archivo faces-numbered.json con los nombres asignados"""
    
    # Leer datos de entrada
    nombres_caras = leer_caras_txt()
    faces_data = leer_faces_json()
    
    if not faces_data:
        print("No se pudieron leer los datos de entrada")
        return
    
    # Crear el nuevo diccionario con nombres asignados
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
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(faces_numbered, f, indent=2, ensure_ascii=False)
    
    # Mostrar estadísticas
    total_caras = sum(len(caras) for caras in faces_numbered.values())
    total_con_nombre = sum(
        sum(1 for cara in caras if cara['nombre']) 
        for caras in faces_numbered.values()
    )
    
    print(f"Procesamiento completado:")
    print(f"- Total de caras detectadas: {total_caras}")
    print(f"- Caras con nombre asignado: {total_con_nombre}")
    print(f"- Archivo generado: {OUTPUT_JSON}")
    
    # Mostrar estadísticas por año
    print("\nEstadísticas por año:")
    for filename, caras in faces_numbered.items():
        año = os.path.splitext(filename)[0]
        caras_con_nombre = sum(1 for cara in caras if cara['nombre'])
        print(f"  {año}: {len(caras)} caras, {caras_con_nombre} con nombre")

if __name__ == "__main__":
    crear_faces_numbered() 