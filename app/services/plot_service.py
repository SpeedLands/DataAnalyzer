import plotly.express as px
import pandas as pd
import os
import json

def create_plot_line(data):
    df = pd.DataFrame(data)
    fig = px.line(df, x='fecha', y='valor', title='Datos Analizados')
    return fig.to_json()

def create_plot_from_file(form_data):
    xName = form_data['xName']
    yName = form_data['yName']
    title = form_data['title']
    file_name = form_data['file']
    
    file_path = os.path.join('data', file_name)
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    df = pd.DataFrame(data)
    fig = px.line(df, x=xName, y=yName, title=title)
    return fig.to_json()
