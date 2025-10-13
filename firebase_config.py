import firebase_admin
from firebase_admin import credentials, auth, db
import requests
import json
from flask import session
import os

# Configuración de Firebase - usando el proyecto del archivo firebase-key.json
FIREBASE_CONFIG = {
    "projectId": "proyecto-fc729",
    "databaseURL": "https://proyecto-fc729-default-rtdb.firebaseio.com"
}

# URLs de Firebase REST API
FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts"
FIREBASE_DB_URL = f"https://{FIREBASE_CONFIG['projectId']}-default-rtdb.firebaseio.com"

# Inicializar Firebase Admin SDK
def initialize_firebase():
    """Inicializa Firebase Admin SDK si no está ya inicializado"""
    if not firebase_admin._apps:
        try:
            # Usar variables de entorno para credenciales (más seguro para producción)
            if os.environ.get('FIREBASE_SERVICE_ACCOUNT'):
                # Para producción: usar credenciales desde variable de entorno
                import json
                service_account_info = json.loads(os.environ.get('FIREBASE_SERVICE_ACCOUNT'))
                cred = credentials.Certificate(service_account_info)
            else:
                # Para desarrollo local: usar archivo firebase-key.json
                cred = credentials.Certificate('firebase-key.json')
            
            firebase_admin.initialize_app(cred, {
                'databaseURL': FIREBASE_CONFIG['databaseURL']
            })
            print("Firebase inicializado correctamente")
        except Exception as e:
            print(f"Error al inicializar Firebase: {e}")
            print("Asegúrate de tener el archivo firebase-key.json o la variable FIREBASE_SERVICE_ACCOUNT configurada")

# Inicializar Firebase al importar el módulo
initialize_firebase()

class FirebaseAuth:
    @staticmethod
    def login_user(email, password):
        """Autentica un usuario con email y contraseña usando REST API"""
        try:
            # Usar REST API para autenticación - necesitamos obtener la API key del proyecto
            # Por ahora usamos una API key genérica, pero debería ser la del proyecto proyecto-fc729
            api_key = os.environ.get('FIREBASE_API_KEY', 'AIzaSyCRPLCoWBUFEU8iEvqkh7d1z_-qDtArce0')
            url = f"{FIREBASE_AUTH_URL}:signInWithPassword?key={api_key}"
            data = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            response = requests.post(url, json=data)
            result = response.json()
            
            if response.status_code == 200:
                return {"success": True, "user": result}
            else:
                error_msg = result.get('error', {}).get('message', 'Error desconocido')
                return {"success": False, "error": error_msg}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def register_user(email, password):
        """Registra un nuevo usuario usando REST API"""
        try:
            api_key = os.environ.get('FIREBASE_API_KEY', 'AIzaSyCRPLCoWBUFEU8iEvqkh7d1z_-qDtArce0')
            url = f"{FIREBASE_AUTH_URL}:signUp?key={api_key}"
            data = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            response = requests.post(url, json=data)
            result = response.json()
            
            if response.status_code == 200:
                return {"success": True, "user": result}
            else:
                error_msg = result.get('error', {}).get('message', 'Error desconocido')
                return {"success": False, "error": error_msg}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def logout_user():
        """Cierra la sesión del usuario"""
        try:
            session.clear()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_current_user():
        """Obtiene el usuario actual autenticado"""
        return session.get('user')

class StudentData:
    @staticmethod
    def save_student_data(user_id, student_data):
        """Guarda los datos del estudiante en Firebase Realtime Database usando Admin SDK"""
        try:
            # Usar Firebase Admin SDK para escribir en Realtime Database
            ref = db.reference(f'students/{user_id}')
            ref.set(student_data)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_student_data(user_id):
        """Obtiene los datos del estudiante desde Firebase Realtime Database usando Admin SDK"""
        try:
            ref = db.reference(f'students/{user_id}')
            data = ref.get()
            
            if data:
                return {"success": True, "data": data}
            else:
                return {"success": False, "error": "No se encontraron datos del estudiante"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def update_student_progress(user_id, tema, ejercicio_completado=False):
        """Actualiza el progreso del estudiante"""
        try:
            # Obtener datos actuales
            current_data = StudentData.get_student_data(user_id)
            if not current_data["success"]:
                return current_data
            
            data = current_data["data"]
            if "progreso" not in data:
                data["progreso"] = {}
            
            if tema not in data["progreso"]:
                data["progreso"][tema] = {
                    "ejercicios_completados": 0,
                    "ultimo_acceso": None,
                    "videos_vistos": 0
                }
            
            if ejercicio_completado:
                data["progreso"][tema]["ejercicios_completados"] += 1
            
            data["progreso"][tema]["ultimo_acceso"] = {
                "fecha": str(__import__('datetime').datetime.now()),
                "tipo": "ejercicio" if ejercicio_completado else "visualizacion"
            }
            
            return StudentData.save_student_data(user_id, data)
        except Exception as e:
            return {"success": False, "error": str(e)}
