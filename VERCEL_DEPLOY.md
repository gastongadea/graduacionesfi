# 🚀 Deploy en Vercel - Graduaciones FI

Guía paso a paso para desplegar la aplicación Graduaciones FI en Vercel.

## 📋 Requisitos previos

1. **Cuenta en Vercel**: [vercel.com](https://vercel.com)
2. **Repositorio en GitHub**: Con el proyecto subido
3. **Archivos generados**: `faces-numbered.json` debe estar en el repositorio

## 🛠️ Pasos para el deploy

### 1. Preparar el proyecto

Asegúrate de que tu repositorio contenga:
```
graduacionesfi/
├── index.html              ✅
├── app.js                  ✅
├── public/                 ✅ (con las fotos)
├── faces-numbered.json     ✅ (generado)
├── vercel.json            ✅ (configuración)
├── README.md              ✅
└── .gitignore             ✅
```

### 2. Conectar con Vercel

1. **Ve a [vercel.com](https://vercel.com)**
2. **Inicia sesión** con tu cuenta de GitHub
3. **Haz clic en "New Project"**
4. **Importa tu repositorio** `graduacionesfi`
5. **Configura el proyecto**:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (dejar vacío)
   - **Build Command**: (dejar vacío)
   - **Output Directory**: (dejar vacío)

### 3. Configurar variables de entorno

No necesitas variables de entorno para este proyecto.

### 4. Deploy

1. **Haz clic en "Deploy"**
2. **Espera** a que se complete el build
3. **¡Listo!** Tu aplicación estará disponible en `https://tu-proyecto.vercel.app`

## 🔧 Configuración personalizada

### Dominio personalizado

1. Ve a **Settings > Domains**
2. Agrega tu dominio personalizado
3. Configura los DNS según las instrucciones de Vercel

### Configuración avanzada

El archivo `vercel.json` ya está configurado para:
- ✅ Servir archivos estáticos
- ✅ Headers CORS correctos
- ✅ Rutas optimizadas
- ✅ Cache de archivos

## 🐛 Solución de problemas

### Error: "Build failed"
- Verifica que `faces-numbered.json` esté en el repositorio
- Asegúrate de que las fotos estén en `public/`
- Revisa los logs de build en Vercel

### Error: "404 Not Found"
- Verifica que `index.html` esté en la raíz
- Asegúrate de que `vercel.json` esté configurado correctamente

### Error: "CORS policy"
- Los headers CORS ya están configurados en `vercel.json`
- Verifica que la configuración esté correcta

### Las fotos no se cargan
- Verifica que estén en la carpeta `public/`
- Asegúrate de que los nombres coincidan con `faces-numbered.json`

## 📊 Monitoreo

### Analytics
- Ve a **Analytics** en tu dashboard de Vercel
- Monitorea el rendimiento y uso

### Logs
- Ve a **Functions** para ver logs de errores
- Monitorea el rendimiento en tiempo real

## 🔄 Actualizaciones

Para actualizar la aplicación:

1. **Haz cambios** en tu repositorio local
2. **Commit y push** a GitHub
3. **Vercel se actualiza automáticamente**

### Actualizar datos

Para actualizar las caras detectadas:

1. **Ejecuta localmente**:
   ```bash
   python detectar_caras_opencv.py
   python crear_faces_numbered.py
   ```

2. **Commit y push** los archivos generados:
   ```bash
   git add faces-numbered.json
   git commit -m "Update face detection data"
   git push
   ```

3. **Vercel se redeploya automáticamente**

## 🌟 Características del deploy

### ✅ Ventajas de Vercel:
- **Deploy automático** desde GitHub
- **CDN global** para mejor rendimiento
- **HTTPS automático**
- **Dominios personalizados**
- **Analytics integrados**
- **Rollback fácil**

### 🚀 Optimizaciones incluidas:
- **Cache de archivos estáticos**
- **Compresión automática**
- **Headers optimizados**
- **Rutas eficientes**

## 📞 Soporte

Si tienes problemas:
1. **Revisa los logs** en Vercel
2. **Consulta la documentación** de Vercel
3. **Abre un issue** en el repositorio

---

**¡Tu aplicación estará online en minutos!** 🎉 