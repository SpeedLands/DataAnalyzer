from flask import Blueprint, render_template, request, jsonify
from app.services.firebase_service import register_user, login_user
from app.services.plot_service import create_plot_line, create_plot_from_file
from app.services.pusher_service import send_pusher_event
from app.services.database_service import buscar_contacto, eliminar_contacto, registrar_contacto, actualizar_contacto, obtener_contacto
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

@main.route('/fetch_contacto', methods=['GET'])
def ver():
    return buscar_contacto()

@main.route('/obtener_contacto/<int:id_contacto>', methods=['GET'])
def api_obtener_contacto(id_contacto):
    contacto = obtener_contacto(id_contacto)
    if contacto:
        return jsonify(contacto), 200
    else:
        return jsonify({"mensaje": "Contacto no encontrado."}), 404

@main.route('/add_contacto', methods=['GET'])
def add_contacto():
    args = request.args
    registrar_contacto(args=args)
    send_pusher_event('my-channel', 'my-event', {'message': 'cambio'})
    return jsonify({"mensaje": "Contacto registrado exitosamente", "data": args}), 201

@main.route('/actualizar_contacto/<int:id_contacto>', methods=['PUT'])
def api_actualizar_contacto(id_contacto):
    # Obtén los datos de la solicitud
    args = request.get_json()

    # Llama a la función de actualización
    resultado = actualizar_contacto(id_contacto, args)

    return jsonify(resultado), 200

@main.route('/eliminar_contacto/<int:id_contacto>', methods=['DELETE'])
def api_eliminar_contacto(id_contacto):

    # Llama a la función de actualización
    resultado = eliminar_contacto(id_contacto)

    return jsonify(resultado), 200

@main.route('/line', methods=['POST'])
def line():
    return create_plot_from_file(request.form)
