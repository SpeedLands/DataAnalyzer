from flask import Blueprint, render_template, request, jsonify
from app.services.firebase_service import register_user, login_user
from app.services.plot_service import create_plot_line, create_plot_from_file
from app.services.pusher_service import send_pusher_event
import os
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/works')
def works():
    return render_template('works.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula = request.form["txtMatriculaFA"]
    nombre = request.form["txtNombreApellidoFA"]
    return f"Matrícula: {matricula} Nombre y Apellido: {nombre}"

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data)

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data)

@main.route('/upload', methods=['POST'])
def upload_data():
    file = request.files['file']
    if file:
        file_path = os.path.join('data', file.filename)
        file.save(file_path)
        df = pd.read_json(file_path)
        return jsonify(df.to_dict())
    return jsonify({"error": "No se pudo cargar el archivo"}), 400

@main.route('/list-files', methods=['GET'])
def list_files():
    files = os.listdir('data')
    return jsonify(files)

@main.route('/trigger', methods=['GET'])
def trigger_pusher():
    # data = request.json  # Datos enviados desde el cliente
    send_pusher_event('my-channel', 'my-event', {'message': 'message de prueba'})

    return jsonify({'status': 'Event triggered!'}), 200


@main.route('/line', methods=['POST'])
def line():
    return create_plot_from_file(request.form)
