#!/usr/bin/env python3
"""
Script de prueba para verificar el sistema de estadísticas
"""

import urllib.request
import urllib.parse
import json
import time

def test_stats_system():
    """Prueba el sistema de estadísticas"""
    base_url = "http://localhost:8000"
    
    print("🧪 Probando sistema de estadísticas...")
    
    # 1. Verificar que el servidor está funcionando
    try:
        response = urllib.request.urlopen(f"{base_url}/")
        print("✅ Servidor funcionando")
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return
    
    # 2. Crear estadísticas de prueba
    test_stats = {
        "2000.jpg": {
            "clicks": 5,
            "lastClick": "2025-01-15T10:30:00.000Z"
        },
        "2001.jpg": {
            "clicks": 3,
            "lastClick": "2025-01-15T11:45:00.000Z"
        },
        "2002.jpg": {
            "clicks": 7,
            "lastClick": "2025-01-15T12:15:00.000Z"
        }
    }
    
    # 3. Enviar estadísticas al servidor
    try:
        data = json.dumps(test_stats).encode('utf-8')
        req = urllib.request.Request(
            f"{base_url}/save-stats",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        response = urllib.request.urlopen(req)
        
        if response.getcode() == 200:
            print("✅ Estadísticas guardadas en el servidor")
        else:
            print(f"❌ Error guardando estadísticas: {response.getcode()}")
            return
    except Exception as e:
        print(f"❌ Error enviando estadísticas: {e}")
        return
    
    # 4. Leer estadísticas del servidor
    try:
        response = urllib.request.urlopen(f"{base_url}/stats.json")
        
        if response.getcode() == 200:
            server_stats = json.loads(response.read().decode('utf-8'))
            print("✅ Estadísticas leídas del servidor")
            print(f"📊 Estadísticas en servidor: {json.dumps(server_stats, indent=2)}")
        else:
            print(f"❌ Error leyendo estadísticas: {response.getcode()}")
            return
    except Exception as e:
        print(f"❌ Error leyendo estadísticas: {e}")
        return
    
    # 5. Verificar que las estadísticas coinciden
    if server_stats == test_stats:
        print("✅ Las estadísticas coinciden correctamente")
    else:
        print("❌ Las estadísticas no coinciden")
        print(f"Enviadas: {json.dumps(test_stats, indent=2)}")
        print(f"Recibidas: {json.dumps(server_stats, indent=2)}")
    
    print("\n🎉 Prueba completada!")

if __name__ == "__main__":
    test_stats_system() 