from flask import jsonify, current_app
import bcrypt

# Función para hashear la contraseña
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def register_user(data):
    email = data.get('email')
    password = data.get('password')
    
    # Validaciones básicas de email y password
    if not email or not password:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400
    if len(password) < 6:
        return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400
    
    try:
        # Acceder al cliente Firestore desde la configuración de la app
        db = current_app.config['FIRESTORE']
        
        # Verificar si el usuario ya existe
        user_query = db.collection('users').where('email', '==', email).stream()
        for doc in user_query:
            return jsonify({"error": "El usuario ya está registrado"}), 409
        
        # Hashear la contraseña antes de guardarla
        hashed_password = hash_password(password)
        
        # Crear un nuevo documento en la colección 'users'
        user_ref = db.collection('users').document()
        user_ref.set({
            'email': email,
            'password': hashed_password.decode('utf-8')  # Guardar la contraseña hasheada
        })
        
        return jsonify({"message": f"Usuario {user_ref.id} creado con éxito"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def login_user(data):
    email = data.get('email')
    password = data.get('password')

    # Validaciones básicas de email y password
    if not email or not password:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400
    
    try:
        # Acceder al cliente Firestore desde la configuración de la app
        db = current_app.config['FIRESTORE']
        
        # Usar where para buscar al usuario por correo
        user_query = db.collection('users').where('email', '==', email).get()
        
        user = None
        for doc in user_query:
            user = doc.to_dict()
            break

        # Verificar si el usuario existe
        if user is None:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Verificar si la contraseña ingresada coincide con la almacenada
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({"message": "Inicio de sesión exitoso"}), 200
        else:
            return jsonify({"error": "Contraseña incorrecta"}), 401
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
