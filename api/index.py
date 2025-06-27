from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import json
from urllib.parse import urlparse

class GraduacionesHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Cambiar al directorio raíz del proyecto
        os.chdir(os.path.dirname(os.path.dirname(__file__)))
        super().__init__(*args, **kwargs)
    
    def end_headers(self):
        # Agregar headers CORS para permitir acceso desde cualquier origen
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Manejar rutas específicas
        if self.path == '/':
            self.path = '/index.html'
        elif self.path.startswith('/api/'):
            # Endpoints de API
            if self.path == '/api/health':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'status': 'ok',
                    'message': 'Graduaciones FI API funcionando correctamente'
                }).encode())
                return
            else:
                self.send_response(404)
                self.end_headers()
                return
        
        # Servir archivos estáticos
        return super().do_GET()

def handler(request, context):
    """Handler para Vercel"""
    # Crear un servidor temporal para manejar la request
    server = HTTPServer(('localhost', 0), GraduacionesHandler)
    server.handle_request()
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': '*'
        },
        'body': 'Graduaciones FI - Universidad Austral'
    }

# Para desarrollo local
if __name__ == "__main__":
    server = HTTPServer(('localhost', 8000), GraduacionesHandler)
    print("🚀 Servidor iniciado en http://localhost:8000")
    server.serve_forever() 