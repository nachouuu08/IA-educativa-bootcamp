from flask import Flask, render_template, request, redirect, url_for, flash, session
from busquedas import buscar_videos_youtube
from temas import temas
from ejercicios import generar_ejercicio_aleatorio
from firebase_config import FirebaseAuth, StudentData
import random

app = Flask(__name__)
app.secret_key = "clave_secreta_demo"

# Decorador para verificar autenticación
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# ---------------------- AUTENTICACIÓN ------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        if not email or not password:
            flash("Por favor completa todos los campos.")
            return redirect(url_for("login"))
        
        result = FirebaseAuth.login_user(email, password)

        if result["success"]:
            user_id = result['user']['localId']
            session['user'] = user_id
            session['email'] = email
            session['id_token'] = result.get('id_token')

            # Cargar datos del estudiante
            student_data = StudentData.get_student_data(user_id, session.get('id_token'))
            if student_data["success"]:
                session['student_data'] = student_data["data"]

            flash("Inicio de sesión exitoso.")
            return redirect(url_for("index"))
        else:
            flash(f"Error al iniciar sesión: {result['error']}")
    
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        nombre = request.form.get("nombre")
        edad = request.form.get("edad")
        nivel_educativo = request.form.get("nivel_educativo")
        intereses = request.form.get("intereses")
        
        # Validar campos obligatorios
        required_fields = [email, password, confirm_password, nombre, edad, nivel_educativo, intereses]
        if not all(required_fields):
            flash("Por favor completa todos los campos.")
            return redirect(url_for("register"))
        
        if password != confirm_password:
            flash("Las contraseñas no coinciden.")
            return redirect(url_for("register"))
        
        if len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.")
            return redirect(url_for("register"))
        
        # Crear usuario en Firebase Auth
        result = FirebaseAuth.register_user(email, password)

        if result["success"]:
            user_id = result["user"]["localId"]
            id_token = result["user"].get("idToken")

            # Guardar datos adicionales del estudiante
            student_data = {
                "email": email,
                "nombre": nombre,
                "edad": int(edad),
                "nivel_educativo": nivel_educativo,
                "intereses": intereses,
                "fecha_registro": str(__import__('datetime').datetime.now()),
                "progreso": {},
                "activo": True
            }

            save_result = StudentData.save_student_data(user_id, student_data, id_token)
            
            if save_result["success"]:
                flash("Cuenta creada exitosamente. Ahora puedes iniciar sesión.")
                return redirect(url_for("login"))
            else:
                flash(f"Error al guardar datos del estudiante: {save_result['error']}")
        else:
            flash(f"Error al crear la cuenta: {result['error']}")
    
    return render_template("register.html")

@app.route("/perfil")
@login_required
def perfil():
    user_id = session.get('user')
    student_data = session.get('student_data')
    
    if not student_data:
        # Intentar cargar desde la base de datos
        result = StudentData.get_student_data(user_id, session.get('id_token'))
        if result["success"]:
            student_data = result["data"]
            session['student_data'] = student_data
        else:
            flash("Error al cargar datos del perfil.")
            return redirect(url_for("index"))
    
    return render_template("perfil.html", student_data=student_data)

@app.route("/logout")
def logout():
    FirebaseAuth.logout_user()
    flash("Sesión cerrada exitosamente.")
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    asignatura = "Estadística"
    if request.method == "POST":
        nombre = request.form.get("nombre")
        tema = request.form.get("tema")
        estilo = request.form.get("estilo")

        if not nombre or not tema or not estilo:
            flash("⚠️ Por favor completa todos los campos.")
            return redirect(url_for("index"))

        if estilo == "Visual":
            return redirect(url_for("visual", nombre=nombre, tema=tema))
        elif estilo == "Práctico":
            return redirect(url_for("practico", nombre=nombre, tema=tema))

    return render_template("index.html", temas=temas["Estadística"])
    asignatura = "Estadística"
    if request.method == "POST":
        nombre = request.form.get("nombre")
        tema = request.form.get("tema")
        estilo = request.form.get("estilo")

        if not nombre or not tema or not estilo:
            flash("⚠️ Por favor completa todos los campos.")
            return redirect(url_for("index"))

        if estilo == "Visual":
            return redirect(url_for("visual", nombre=nombre, tema=tema))
        elif estilo == "Práctico":
            return redirect(url_for("practico", nombre=nombre, tema=tema))

    return render_template("index.html", temas=temas["Estadística"])


# ---------------------- VISUAL ------------------------
@app.route("/visual")
@login_required
def visual():
    nombre = request.args.get("nombre")
    tema = request.args.get("tema")

    # Evitar errores si el tema llega vacío
    if not tema:
        tema = "Tema no especificado"

    # Introducción dinámica
    introduccion = (
        f"📘 El tema '{tema}' trata sobre los conceptos fundamentales de "
        f"{tema.lower()} en el campo de la estadística. "
        f"En esta sección aprenderás su aplicación práctica, ejemplos visuales y cómo interpretarlo."
    )

    # Obtener videos aleatorios
    videos = buscar_videos_youtube(f"{tema} Estadística", 6)
    random.shuffle(videos)
    videos = videos[:3]  # muestra 3 aleatorios

    # Registrar progreso del estudiante
    user_id = session.get('user')
    if user_id:
        StudentData.update_student_progress(user_id, tema, ejercicio_completado=False, id_token=session.get('id_token'))

    return render_template(
        "visual.html",
        nombre=nombre,
        tema=tema,
        introduccion=introduccion,
        videos=videos
    )


# ---------------------- PRÁCTICO ------------------------
@app.route("/practico", methods=["GET", "POST"])
@login_required
def practico():
    nombre = request.args.get("nombre")
    tema = request.args.get("tema")

    # Si el usuario hace clic en "Generar otro ejercicio"
    if request.method == "POST":
        return redirect(url_for("practico", nombre=nombre, tema=tema))

    ejercicio = generar_ejercicio_aleatorio(tema)

    return render_template(
        "practico.html",
        nombre=nombre,
        tema=tema,
        ejercicio=ejercicio
    )



if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
