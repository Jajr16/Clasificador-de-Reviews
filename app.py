from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import csv  # Importa el módulo csv
import os
import Proyecto as Proyecto

app=Flask(__name__)

app.config['UPLOAD_FOLDER'] = "static/uploads"
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='g3r4rd0'
app.config['MYSQL_DB']='tln'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)

@app.route('/')
def home():
    return render_template('proyecto.html')

@app.route('/comentario', methods=["POST"])
def comentar():
    if request.form['comment-evaluate']:
        _Comment = request.form['comment-evaluate']

        text_classified = Proyecto.Clasificar(_Comment)

        return jsonify({'message': 'La reseña que ingresó es positiva' if text_classified == 'POSITIVE' else 'La reseña que ingresó es negativa'})
    else:
        return jsonify({'message', 'Ingrese una reseña para su clasificación'})




@app.route('/cargar_csv', methods=["POST"])
def carga():     
        if 'file-1' not in request.files:
            return jsonify({'message': 'No se seleccionó ningún archivo.'})
        
        file = request.files['file-1']

        if file.filename == '':
            return jsonify({'message': 'No se seleccionó ningún archivo'})
        
        if file and file.filename.endswith('.csv'):

            # Obtén el valor de '_Columna' del cuerpo de la solicitud POST
            _Columna = request.form['nom_Column']

            filename = secure_filename(file.filename)
            file.save(os.path.join(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)) 

            # Procesar el archivo CSV
            csv_file_path = os.path.join(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)
            datos_csv = []

            with open(csv_file_path, newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    datos_csv.append(row)

            df = pd.read_csv(csv_file_path)
            if _Columna in df:
                Csv_Procesado = df[_Columna].tolist()

            Positivos = 0
            # Clasificar archivo y contar reseñas positivas y negativas
            for index in range(0, len(Csv_Procesado)):
                resultado = Proyecto.Clasificar(Csv_Procesado[index])
                if resultado == 'POSITIVE':
                    Positivos += 1
            Negativos = len(Csv_Procesado)-Positivos

            return jsonify({'data': [Positivos, Negativos]})
        else:
            return jsonify({'message': 'El archivo debe tener la extención .csv'})

@app.route('/Registro', methods= ["GET", "POST"])
def reg():
    if request.method == 'POST' and 'correo' in request.form and 'contra':
        _correo = request.form['correo']
        _contra = request.form['contra']

        cur=mysql.connection.cursor()

        cur.execute("INSERT INTO usuarios (correo, contrasena) VALUES (%s,%s)", (_correo, _contra))
        mysql.connection.commit()

        return render_template("proyecto.html")

@app.route('/Login', methods = ["GET", "POST"])
def log():
    if request.method == 'POST' and 'correoo' in request.form and 'contraa':
        _correo = request.form['correoo']
        _contra = request.form['contraa']

        cur=mysql.connection.cursor()

        cur.execute("SELECT * FROM usuarios WHERE correo=%s AND contrasena=%s", (_correo, _contra,))
        account = cur.fetchone()
        
        if account:
            session['logueado'] = True
            session['id'] = account['id']
            return render_template("analizar.html")
        else:
            return render_template("proyecto.html")

if __name__ == '__main__':
    app.run(debug=True)
