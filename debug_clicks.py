#!/usr/bin/env python3
"""
Script de depuración para verificar el registro de clicks
"""

import json
import time
import os

def check_stats_file():
    """Verifica el archivo de estadísticas"""
    stats_file = 'stats.json'
    
    print("🔍 Verificando archivo de estadísticas...")
    
    if os.path.exists(stats_file):
        try:
            with open(stats_file, 'r', encoding='utf-8') as f:
                stats = json.load(f)
            
            print(f"✅ Archivo {stats_file} encontrado")
            print(f"📊 Contenido actual:")
            print(json.dumps(stats, indent=2, ensure_ascii=False))
            
            # Contar total de clicks
            total_clicks = sum(photo['clicks'] for photo in stats.values())
            print(f"\n📈 Total de clicks registrados: {total_clicks}")
            
            return stats
        except Exception as e:
            print(f"❌ Error leyendo {stats_file}: {e}")
            return None
    else:
        print(f"❌ Archivo {stats_file} no encontrado")
        return None

def monitor_stats_changes():
    """Monitorea cambios en el archivo de estadísticas"""
    print("\n👀 Monitoreando cambios en stats.json...")
    print("Haz clicks en las fotos de la aplicación web y observa los cambios aquí")
    print("Presiona Ctrl+C para detener\n")
    
    last_content = None
    
    try:
        while True:
            if os.path.exists('stats.json'):
                with open('stats.json', 'r', encoding='utf-8') as f:
                    current_content = f.read()
                
                if current_content != last_content:
                    print(f"[{time.strftime('%H:%M:%S')}] 📝 Archivo actualizado!")
                    try:
                        stats = json.loads(current_content)
                        total_clicks = sum(photo['clicks'] for photo in stats.values())
                        print(f"   Total de clicks: {total_clicks}")
                        
                        # Mostrar últimos clicks
                        for photo, data in stats.items():
                            if data.get('lastClick'):
                                last_click = data['lastClick']
                                print(f"   {photo}: {data['clicks']} clicks (último: {last_click})")
                    except:
                        print("   Error parseando JSON")
                    
                    last_content = current_content
                    print()
            
            time.sleep(1)  # Verificar cada segundo
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoreo detenido")

if __name__ == "__main__":
    print("🐛 DEPURADOR DE CLICKS")
    print("=" * 40)
    
    # Verificar estado actual
    stats = check_stats_file()
    
    # Monitorear cambios
    monitor_stats_changes() 