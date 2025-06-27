# 🎓 Graduaciones FI - Universidad Austral

Una plataforma web interactiva para visualizar las fotos de graduación de la Facultad de Ingeniería de la Universidad Austral con detección automática de caras y reconocimiento de nombres de graduados.

![Graduaciones FI](https://img.shields.io/badge/Universidad-Austral-blue)
![Python](https://img.shields.io/badge/Python-3.6+-green)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Características

- **🔍 Detección automática de caras** usando OpenCV
- **👤 Reconocimiento de nombres** de graduados
- **🖱️ Interfaz web moderna** con diseño responsivo
- **🔍 Zoom interactivo** con navegación por teclado y mouse
- **📱 Compatible con móviles** y gestos táctiles
- **🎨 Tooltips dinámicos** al pasar el mouse sobre las caras
- **📊 Navegación entre fotos** con flechas del teclado
- **🖼️ Visualización en pantalla completa** con controles de zoom

## 🚀 Demo

[Ver demo en vivo](https://tu-demo-url.com) *(pendiente de deploy)*

## 📋 Requisitos

- Python 3.6 o superior
- OpenCV 4.8+
- Navegador web moderno

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/graduacionesfi.git
cd graduacionesfi
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Preparar los datos

Asegúrate de tener:
- Fotos de graduación en la carpeta `public/`
- Archivo `caras.txt` con los nombres (formato: año, número, nombre)

### 4. Generar archivos de datos

```bash
# Detectar caras en las fotos
python detectar_caras_opencv.py

# Asignar nombres a las caras
python crear_faces_numbered.py
```

### 5. Ejecutar la aplicación

```bash
python server.py
```

La aplicación se abrirá automáticamente en `http://localhost:8000`

## 📁 Estructura del proyecto

```
graduacionesfi/
├── public/                     # Fotos de graduación
│   ├── 1999.jpg
│   ├── 2000.jpg
│   └── ...
├── caras.txt                   # Nombres de graduados
├── faces.json                  # Caras detectadas (generado)
├── faces-numbered.json         # Caras con nombres (generado)
├── index.html                  # Página principal
├── app.js                      # Lógica de la aplicación
├── server.py                   # Servidor web local
├── detectar_caras_opencv.py    # Detección de caras
├── crear_faces_numbered.py     # Asignación de nombres
├── requirements.txt            # Dependencias Python
├── .gitignore                  # Archivos a ignorar
├── LICENSE                     # Licencia MIT
└── README.md                   # Este archivo
```

## 🎯 Uso

### Interfaz Web

1. **Galería de fotos**: Visualiza todas las graduaciones ordenadas por año
2. **Clic en foto**: Abre en pantalla completa
3. **Hover en caras**: Muestra nombres de graduados
4. **Navegación**: Usa flechas ← → para cambiar de foto
5. **Zoom**: Rueda del mouse o botones +/− para hacer zoom
6. **Arrastrar**: Mueve la imagen cuando está zoomada

### Controles de teclado

- **← →**: Navegar entre fotos
- **ESC**: Cerrar modal
- **Rueda del mouse**: Zoom in/out

### Gestos táctiles (móviles)

- **Pellizco**: Zoom in/out
- **Arrastrar**: Mover imagen zoomada
- **Tap**: Abrir/cerrar modal

## 📊 Formato de datos

### caras.txt
```
1999	1	Mercedes Augspach
1999	2	Mariano Güemes
2000	1	Jorge Pereyra Iraola
```

### faces-numbered.json
```json
{
  "1999.jpg": [
    {
      "id": 1,
      "x": 100,
      "y": 150,
      "w": 50,
      "h": 50,
      "nombre": "Mercedes Augspach"
    }
  ]
}
```

## 🔧 Personalización

### Agregar nuevas fotos
1. Coloca las fotos en `public/` con formato `YYYY.jpg`
2. Ejecuta `python detectar_caras_opencv.py`
3. Agrega nombres en `caras.txt`
4. Ejecuta `python crear_faces_numbered.py`

### Modificar el diseño
- Edita `index.html` para cambiar la estructura
- Modifica los estilos CSS en el `<style>` del HTML
- Ajusta la lógica en `app.js`

## 🐛 Solución de problemas

### Error: "No se encontró el archivo haarcascade"
```bash
pip install opencv-python
```

### Error: "No se pudo leer la imagen"
- Verifica que las fotos estén en `public/`
- Asegúrate de que tengan extensiones válidas (.jpg, .png)

### Las caras no se muestran correctamente
1. Ejecuta `python detectar_caras_opencv.py`
2. Ejecuta `python crear_faces_numbered.py`
3. Verifica que `faces-numbered.json` se haya generado

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **Facultad de Ingeniería** - Universidad Austral
- **Desarrollado para** - Visualización de graduaciones

## 🙏 Agradecimientos

- OpenCV por la detección de caras
- Universidad Austral por las fotos de graduación
- Comunidad de desarrolladores por las herramientas utilizadas

---

**Desarrollado con ❤️ para la Facultad de Ingeniería - Universidad Austral** 🎓 