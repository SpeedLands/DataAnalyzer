from flask import Flask
from firebase_admin import credentials, firestore, initialize_app
import os
import pusher
import mysql.connector


def create_app():
    app = Flask(__name__)

    # Inicializar Firebase
    cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), '../serviceAccountKey.json'))
    initialize_app(cred, {
        'storageBucket': 'data-be624.appspot.com'
    })

    # Configurar Pusher
    app.config['PUSHER'] = pusher.Pusher(
        app_id='1864827',
        key='f02e4f2876cbdf202f85',
        secret='b6933bfabe9f9bbd1bbd',
        cluster='us2',
        ssl=True
    )

    app.config['DATABASE'] = mysql.connector.connect(
        host="185.232.14.52",
        database="u760464709_tst_sep",
        user="u760464709_tst_sep_usr",
        password="dJ0CIAFF="
    )

    # Guardar el cliente de Firestore en la configuración de la app
    app.config['FIRESTORE'] = firestore.client()

    # Registrar blueprints (rutas)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
