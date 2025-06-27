#!/usr/bin/env python3
"""
Script de deploy para Graduaciones FI
Configura automáticamente el proyecto para GitHub
"""

import os
import sys
import subprocess
import json

def check_requirements():
    """Verifica que se cumplan los requisitos mínimos"""
    print("🔍 Verificando requisitos...")
    
    # Verificar Python
    if sys.version_info < (3, 6):
        print("❌ Error: Se requiere Python 3.6 o superior")
        return False
    
    # Verificar archivos necesarios
    required_files = [
        'public/',
        'caras.txt',
        'detectar_caras_opencv.py',
        'crear_faces_numbered.py',
        'index.html',
        'app.js',
        'server.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        return False
    
    print("✅ Requisitos cumplidos")
    return True

def install_dependencies():
    """Instala las dependencias de Python"""
    print("📦 Instalando dependencias...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        print("✅ Dependencias instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def generate_data_files():
    """Genera los archivos de datos necesarios"""
    print("🔄 Generando archivos de datos...")
    
    # Detectar caras
    try:
        subprocess.run([sys.executable, 'detectar_caras_opencv.py'], check=True)
        print("✅ Caras detectadas")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error detectando caras: {e}")
        return False
    
    # Asignar nombres
    try:
        subprocess.run([sys.executable, 'crear_faces_numbered.py'], check=True)
        print("✅ Nombres asignados")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error asignando nombres: {e}")
        return False
    
    return True

def create_package_json():
    """Crea un package.json básico para el proyecto"""
    package_data = {
        "name": "graduacionesfi",
        "version": "1.0.0",
        "description": "Plataforma web para visualizar graduaciones de la Facultad de Ingeniería - Universidad Austral",
        "main": "server.py",
        "scripts": {
            "start": "python server.py",
            "detect": "python detectar_caras_opencv.py",
            "names": "python crear_faces_numbered.py",
            "deploy": "python deploy.py"
        },
        "keywords": [
            "graduaciones",
            "universidad-austral",
            "opencv",
            "face-detection",
            "web-app"
        ],
        "author": "Facultad de Ingeniería - Universidad Austral",
        "license": "MIT",
        "repository": {
            "type": "git",
            "url": "https://github.com/tu-usuario/graduacionesfi.git"
        },
        "bugs": {
            "url": "https://github.com/tu-usuario/graduacionesfi/issues"
        },
        "homepage": "https://github.com/tu-usuario/graduacionesfi#readme"
    }
    
    with open('package.json', 'w', encoding='utf-8') as f:
        json.dump(package_data, f, indent=2, ensure_ascii=False)
    
    print("✅ package.json creado")

def main():
    """Función principal del script de deploy"""
    print("🚀 Iniciando deploy de Graduaciones FI...")
    print("=" * 50)
    
    # Verificar requisitos
    if not check_requirements():
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        sys.exit(1)
    
    # Generar archivos de datos
    if not generate_data_files():
        sys.exit(1)
    
    # Crear package.json
    create_package_json()
    
    print("=" * 50)
    print("✅ Deploy completado exitosamente!")
    print("\n🎯 Próximos pasos:")
    print("1. git add .")
    print("2. git commit -m 'Initial commit'")
    print("3. git push origin main")
    print("\n🌐 Para ejecutar localmente:")
    print("python server.py")
    print("\n📖 Para más información, consulta el README.md")

if __name__ == "__main__":
    main() 