from flask import jsonify, current_app

def buscar_contacto():
    con = current_app.config['DATABASE']
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor(dictionary=True)  # Para que devuelva un diccionario
    cursor.execute("SELECT * FROM tst0_contacto ORDER BY Id_Contacto DESC")
    registros = cursor.fetchall()

    cursor.close()
    con.close()
    
    return registros

def obtener_contacto(id_contacto):
    con = current_app.config['DATABASE']
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor(dictionary=True)
    
    # Usa el ID del contacto para hacer la consulta
    sql = "SELECT * FROM tst0_contacto WHERE Id_Contacto = %s"
    cursor.execute(sql, (id_contacto,))
    registro = cursor.fetchone()  # Devuelve un solo registro

    cursor.close()
    con.close()
    
    return registro

def registrar_contacto(args):
    con = current_app.config['DATABASE']
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    
    sql = "INSERT INTO tst0_contacto (Correo_Electronico, Nombre, Asunto) VALUES (%s, %s, %s)"
    val = (args["correo"], args["nombre"], args["asunto"])
    cursor.execute(sql, val)

    con.commit()
    cursor.close()
    con.close()

    return {"mensaje": "Curso registrado exitosamente."}


def actualizar_contacto(id_contacto, args):
    # Establecemos conexión a la base de datos
    con = current_app.config['DATABASE']
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    # SQL para actualizar el contacto
    sql = """
    UPDATE tst0_contacto 
    SET Correo_Electronico = %s, Nombre = %s, Asunto = %s 
    WHERE Id_Contacto = %s
    """
    
    # Aseguramos que todos los parámetros están disponibles en args
    correo_electronico = args.get("correoElectronico")
    nombre = args.get("nombre")
    asunto = args.get("asunto")

    # Verificamos que los valores no estén vacíos o inválidos
    if not correo_electronico or not nombre or not asunto:
        return {"error": "Faltan campos requeridos"}, 400

    # Empaquetamos los valores para la consulta
    val = (correo_electronico, nombre, asunto, id_contacto)
    
    try:
        # Ejecutamos la consulta
        cursor.execute(sql, val)
        con.commit()  # Confirmamos los cambios
    except Exception as e:
        con.rollback()  # En caso de error, revertimos la transacción
        return {"error": str(e)}, 500
    finally:
        # Cerramos cursor y conexión
        cursor.close()
        con.close()

    return {"id_contacto": id_contacto, "mensaje": "Contacto actualizado exitosamente."}



def eliminar_contacto(id_curso):
    con = current_app.config['DATABASE']
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    sql = "DELETE FROM tst0_contacto WHERE Id_Contacto = %s"
    val = (id_curso,)
    cursor.execute(sql, val)

    con.commit()
    cursor.close()
    con.close()

    return {"id_curso": id_curso, "mensaje": "Curso eliminado exitosamente."}
