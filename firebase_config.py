import requests
import json
from flask import session

# Configuración de Firebase
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyCRPLCoWBUFEU8iEvqkh7d1z_-qDtArce0",
    "authDomain": "bootcamp-d8378.firebaseapp.com",
    "databaseURL": "https://bootcamp-d8378-default-rtdb.firebaseio.com",
    "projectId": "bootcamp-d8378",
    "storageBucket": "bootcamp-d8378.appspot.com",
    "messagingSenderId": "437122481987",
    "appId": "1:437122481987:web:22ea0b9aae69068e4d39f6",
    "measurementId": "G-3D0183GS34"
}

# URLs de Firebase REST API
FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts"
FIREBASE_DB_URL = f"https://{FIREBASE_CONFIG['projectId']}-default-rtdb.firebaseio.com"

class FirebaseAuth:
    @staticmethod
    def login_user(email, password):
        """Autentica un usuario con email y contraseña"""
        try:
            url = f"{FIREBASE_AUTH_URL}:signInWithPassword?key={FIREBASE_CONFIG['apiKey']}"
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
        """Registra un nuevo usuario"""
        try:
            url = f"{FIREBASE_AUTH_URL}:signUp?key={FIREBASE_CONFIG['apiKey']}"
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
        """Guarda los datos del estudiante en Firebase Realtime Database"""
        try:
            url = f"{FIREBASE_DB_URL}/students/{user_id}.json"
            response = requests.put(url, json=student_data)
            if response.status_code == 200:
                return {"success": True}
            else:
                return {"success": False, "error": "Error al guardar datos"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_student_data(user_id):
        """Obtiene los datos del estudiante desde Firebase Realtime Database"""
        try:
            url = f"{FIREBASE_DB_URL}/students/{user_id}.json"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return {"success": True, "data": data}
                else:
                    return {"success": False, "error": "No se encontraron datos del estudiante"}
            else:
                return {"success": False, "error": "Error al obtener datos"}
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
