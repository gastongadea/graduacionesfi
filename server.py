import http.server
import socketserver
import os
import webbrowser
from urllib.parse import urlparse

# Configuración del servidor
PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Agregar headers CORS para permitir acceso desde cualquier origen
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Personalizar el log para mostrar las rutas accedidas
        print(f"[{self.log_date_time_string()}] {format % args}")

def start_server():
    """Inicia el servidor web"""
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
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