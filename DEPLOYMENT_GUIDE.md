# 🚀 Guía de Despliegue - IA Educativa

## Opción 1: Render.com (Recomendada - GRATIS)

### Paso 1: Preparar el Proyecto
1. Todos los archivos ya están listos:
   - ✅ `requirements.txt` - Dependencias de Python
   - ✅ `render.yaml` - Configuración de Render
   - ✅ `app.py` - Modificado para producción

### Paso 2: Subir a GitHub
1. Ve a [GitHub.com](https://github.com)
2. Crea un nuevo repositorio llamado `ia-educativa`
3. Sube todos los archivos de tu proyecto

### Paso 3: Configurar Render
1. Ve a [render.com](https://render.com)
2. Regístrate con tu cuenta de GitHub
3. Haz clic en "New +" → "Web Service"
4. Selecciona tu repositorio `ia-educativa`
5. Configura el servicio:
   - **Name:** `ia-educativa`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Instance Type:** `Free`

### Paso 4: Variables de Entorno
En la sección "Environment Variables", agrega:
- `FLASK_ENV` = `production`
- `FLASK_DEBUG` = `False`

### Paso 5: Desplegar
1. Haz clic en "Create Web Service"
2. Render construirá y desplegará tu aplicación
3. Te dará una URL como: `https://ia-educativa.onrender.com`

## Opción 2: Railway.app (Alternativa)

### Paso 1: Subir a GitHub
Mismo proceso que Render

### Paso 2: Configurar Railway
1. Ve a [railway.app](https://railway.app)
2. Regístrate con GitHub
3. Haz clic en "New Project" → "Deploy from GitHub repo"
4. Selecciona tu repositorio
5. Railway detectará automáticamente que es una app Python

### Paso 3: Configurar Variables
En Railway, agrega:
- `PORT` = `5000`
- `FLASK_ENV` = `production`

## Opción 3: Heroku (Tradicional)

### Paso 1: Instalar Heroku CLI
1. Descarga desde [devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

### Paso 2: Crear Procfile
Crea un archivo llamado `Procfile` (sin extensión):
```
web: python app.py
```

### Paso 3: Desplegar
```bash
heroku login
heroku create ia-educativa-app
git add .
git commit -m "Initial commit"
git push heroku main
```

## 🔧 Configuración de Firebase para Producción

### Paso 1: Actualizar Reglas de Firebase
En Firebase Console:
1. Ve a **Authentication** → **Settings**
2. Agrega tu dominio de Render a "Authorized domains"
3. Ejemplo: `ia-educativa.onrender.com`

### Paso 2: Reglas de Realtime Database
```json
{
  "rules": {
    ".read": "auth != null",
    ".write": "auth != null"
  }
}
```

## ✅ Checklist Final

- [ ] Código subido a GitHub
- [ ] Render/Railway configurado
- [ ] Variables de entorno configuradas
- [ ] Firebase autoriza el nuevo dominio
- [ ] App desplegada y funcionando
- [ ] Probar login/registro en producción

## 🌐 URLs de Ejemplo

Después del despliegue, tu app estará disponible en:
- Render: `https://ia-educativa.onrender.com`
- Railway: `https://ia-educativa-production.up.railway.app`
- Heroku: `https://ia-educativa-app.herokuapp.com`

## 📱 Acceso Móvil

Una vez desplegada, cualquier persona puede acceder desde:
- 💻 Computadora: URL directa
- 📱 Móvil: URL directa (diseño responsivo)
- 🌍 Cualquier país: Acceso global 24/7

## 🔄 Actualizaciones

Para actualizar tu app:
1. Modifica el código localmente
2. Sube cambios a GitHub
3. Render/Railway se actualiza automáticamente
4. ¡Tu app se actualiza en vivo!
