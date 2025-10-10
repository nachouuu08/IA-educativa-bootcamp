# 📋 Configuración del Proyecto - IA Educativa Bootcamp

## Descripción General
Aplicación web Flask para educación interactiva con integración de Firebase para autenticación y base de datos, desplegada en Render.com.

## 🏗️ Arquitectura
- **Backend:** Flask (Python)
- **Frontend:** HTML/CSS/JS (Jinja2 templates)
- **Base de Datos:** Firebase Realtime Database
- **Autenticación:** Firebase Authentication
- **Despliegue:** Render.com
- **APIs Externas:** YouTube Data API v3

## 🔧 Configuración de Firebase

### 1. Proyecto Firebase
- **Project ID:** proyecto-fc729
- **Auth Domain:** proyecto-fc729.firebaseapp.com
- **Database URL:** https://proyecto-fc729-default-rtdb.firebaseio.com

### 2. API Keys
```python
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyDZN6HJ_4VD_MUgWnEvSkHhy7TpPvb5w0Y",
    "authDomain": "proyecto-fc729.firebaseapp.com",
    "projectId": "proyecto-fc729",
    "storageBucket": "proyecto-fc729.firebasestorage.app",
    "messagingSenderId": "772596105663",
    "appId": "1:772596105663:web:bacf8fbee158e615f6210a"
}
```

### 3. Servicios Utilizados
- **Firebase Authentication:** Login/registro de usuarios
- **Firebase Realtime Database:** Almacenamiento de datos de estudiantes
- **Firebase Hosting:** (No utilizado en esta versión)

### 4. Estructura de Base de Datos
```
students/
  {user_id}/
    email: string
    nombre: string
    edad: number
    nivel_educativo: string
    intereses: string
    fecha_registro: string
    progreso: {
      {tema}: {
        ejercicios_completados: number
        ultimo_acceso: {
          fecha: string
          tipo: string
        }
        videos_vistos: number
      }
    }
    activo: boolean
```

### 5. Reglas de Seguridad (Realtime Database)
```json
{
  "rules": {
    ".read": "auth != null",
    ".write": "auth != null"
  }
}
```

## 🌐 Configuración de Render.com

### 1. Archivo render.yaml
```yaml
services:
  - type: web
    name: ia-educativa
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: FLASK_ENV
        value: production
      - key: FLASK_DEBUG
        value: False
```

### 2. Variables de Entorno
- `FLASK_ENV`: production
- `FLASK_DEBUG`: False
- `PORT`: (Asignado automáticamente por Render)

### 3. Configuración de Build
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python app.py`
- **Instance Type:** Free

## 📦 Dependencias (requirements.txt)
```
Flask==2.3.3
firebase-admin==7.1.0
requests==2.32.5
google-auth==2.41.1
google-cloud-firestore==2.21.0
google-cloud-storage==3.4.1
httpx==0.28.1
```

## 🔗 Integración en app.py

### 1. Importaciones
```python
from flask import Flask, render_template, request, redirect, url_for, flash, session
from firebase_config import FirebaseAuth, StudentData
from busquedas import buscar_videos_youtube
from temas import temas
from ejercicios import generar_ejercicio_aleatorio
```

### 2. Configuración de Flask
```python
app = Flask(__name__)
app.secret_key = "clave_secreta_demo"
```

### 3. Rutas Principales
- `/`: Página principal (requiere login)
- `/login`: Autenticación
- `/register`: Registro
- `/perfil`: Perfil del usuario
- `/visual`: Modo visual de aprendizaje
- `/practico`: Modo práctico con ejercicios

### 4. Decorador de Autenticación
```python
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function
```

### 5. Conexión con Firebase
- **Login:** `FirebaseAuth.login_user(email, password)`
- **Registro:** `FirebaseAuth.register_user(email, password)`
- **Guardar datos:** `StudentData.save_student_data(user_id, data)`
- **Obtener datos:** `StudentData.get_student_data(user_id)`
- **Actualizar progreso:** `StudentData.update_student_progress(user_id, tema)`

## 🎥 Integración con YouTube API

### 1. Archivo busquedas.py
- Función: `buscar_videos_youtube(query, max_results=6)`
- API Key: Configurada internamente
- Endpoint: YouTube Data API v3

### 2. Uso en app.py
```python
videos = buscar_videos_youtube(f"{tema} Estadística", 6)
```

## 📚 Temas y Ejercicios

### 1. Archivo temas.py
Define los temas disponibles por asignatura:
```python
temas = {
    "Estadística": [
        "Media y Mediana",
        "Moda y Varianza",
        "Distribuciones",
        # ...
    ]
}
```

### 2. Archivo ejercicios.py
- Función: `generar_ejercicio_aleatorio(tema)`
- Genera ejercicios dinámicos basados en el tema seleccionado

## 🚀 Proceso de Despliegue

### 1. Desarrollo Local
```bash
pip install -r requirements.txt
python app.py
```
- Acceso: http://127.0.0.1:5000

### 2. Git y GitHub
- Repositorio: https://github.com/nachouuu08/IA-educativa-bootcamp
- Rama principal: main
- Commits incluyen: código, templates, configuraciones

### 3. Despliegue Automático
- Push a GitHub → Render detecta cambios → Build automático → Deploy
- URL de producción: https://ia-educativa-bootcamp.onrender.com

## 🔒 Seguridad

### 1. Autenticación
- Firebase Auth maneja login/registro
- Sesiones de Flask para estado del usuario
- Decorador `@login_required` para rutas protegidas

### 2. Variables Sensibles
- API Keys: En código (considerar variables de entorno para producción real)
- Secret Key de Flask: En código (cambiar en producción)

### 3. CORS y Dominios
- Firebase configurado para permitir el dominio de Render
- Authorized domains en Firebase Auth

## 📱 Características de la App

### 1. Modo Visual
- Búsqueda de videos en YouTube
- Introducción dinámica por tema
- Seguimiento de progreso

### 2. Modo Práctico
- Generación de ejercicios aleatorios
- Verificación de respuestas (no implementada aún)
- Progreso por tema

### 3. Perfil de Usuario
- Datos personales
- Historial de progreso
- Estadísticas de aprendizaje

## 🔄 Actualizaciones y Mantenimiento

### 1. Actualización de Código
1. Modificar código local
2. Probar localmente
3. Commit y push a GitHub
4. Render redeploya automáticamente

### 2. Actualización de Dependencias
1. Modificar `requirements.txt`
2. Probar compatibilidad
3. Push → Build automático

### 3. Monitoreo
- Logs en Render dashboard
- Firebase Console para datos
- GitHub para control de versiones

## 📞 Soporte y Troubleshooting

### Errores Comunes
- **TemplateNotFound:** Verificar carpeta `templates` en minúscula
- **UnicodeDecodeError:** Archivos HTML deben ser UTF-8 sin BOM
- **ConnectionError:** Verificar configuración de Firebase
- **AuthError:** Verificar dominio autorizado en Firebase

### Logs
- Render: Dashboard > Service > Logs
- Local: Ejecutar `python app.py` en terminal

## 🎯 Próximas Mejoras
- Implementar verificación de respuestas en ejercicios
- Agregar más asignaturas y temas
- Mejorar UI/UX con CSS avanzado
- Implementar notificaciones push
- Agregar análisis de aprendizaje con IA