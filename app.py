from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta del dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Ruta para manejar el error 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Ruta para cargar datos
@app.route('/upload', methods=['POST'])
def upload_data():
    file = request.files['file']
    if file:
        # Guardar archivo en la carpeta 'data'
        file_path = os.path.join('data', file.filename)
        file.save(file_path)

        # Leer datos con Pandas
        df = pd.read_json(file_path)
        return jsonify(df.to_dict())
    return jsonify({"error": "No se pudo cargar el archivo"}), 400

# Ruta para los archivos dentre de data
@app.route('/list-files', methods=['GET'])
def list_files():
    # Obtener lista de archivos en la carpeta 'data'
    files = os.listdir('data')
    
    # Devolver la lista de archivos en formato JSON
    return jsonify(files)

# Ruta para crear gráficos
@app.route('/plot', methods=['POST'])
def create_plot():
    data = request.get_json()  # Datos enviados desde el frontend
    df = pd.DataFrame(data)
    
    # Crear un gráfico simple con Plotly
    fig = px.line(df, x='fecha', y='valor', title='Datos Analizados')
    graph_json = fig.to_json()
    
    return graph_json

if __name__ == '__main__':
    app.run(debug=True)
