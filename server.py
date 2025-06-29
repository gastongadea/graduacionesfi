import http.server
import socketserver
import os
import webbrowser
from urllib.parse import urlparse
import json

# Configuración del servidor
PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_POST(self):
        if self.path == '/save-stats':
            # Obtener el contenido del body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parsear JSON
                stats_data = json.loads(post_data.decode('utf-8'))
                
                # Guardar en archivo
                with open('stats.json', 'w', encoding='utf-8') as f:
                    json.dump(stats_data, f, indent=2, ensure_ascii=False)
                
                # Responder con éxito
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode())
                
            except Exception as e:
                # Responder con error
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def end_headers(self):
        # Agregar headers CORS para permitir acceso desde cualquier origen
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        # Personalizar el log para mostrar las rutas accedidas
        print(f"[{self.log_date_time_string()}] {format % args}")

def start_server():
    """Inicia el servidor web"""
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"🚀 Servidor iniciado en http://localhost:{PORT}")
        print(f"📁 Directorio: {DIRECTORY}")
        print(f"🌐 Abriendo navegador automáticamente...")
        print(f"⏹️  Presiona Ctrl+C para detener el servidor")
        print("-" * 50)
        
        # Abrir el navegador automáticamente
        try:
            webbrowser.open(f'http://localhost:{PORT}')
        except:
            print("No se pudo abrir el navegador automáticamente")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor detenido")

if __name__ == "__main__":
    start_server() 