from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os

app = Flask(__name__)
mysql = MySQL()

#regalado
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mtd010202'
app.config['MYSQL_DATABASE_DB'] = 'empleados'

UPLOADS = os.path.join('uploads')
app.config['UPLOADS'] = UPLOADS

mysql.init_app(app)

@app.route('/') #index  (, methods=["GET"])
def index():
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "SELECT * FROM empleados;"
    cursor.execute(sql)
    empleados = cursor.fetchall()
    connection.commit()
    return render_template('empleados/index.html', empleados = empleados)

@app.route('/create')
def create():
    return render_template('empleados/create.html')
    
#procesa info del form
@app.route('/store', methods=["POST"])
def store():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']

    now = datetime.now()
    print(now)
    tiempo = now.strftime("%Y%H%M%S")

    if (_foto.filename != ''):
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO empleados (nombre, correo, foto) values (%s, %s, %s);"
    datos = (_nombre, _correo, nuevoNombreFoto)

    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql, datos)
    connection.commit()
    #return render_template('empleados/create.html')
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    sql = "DELETE FROM empleados WHERE id=%s;"
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql, id)
    connection.commit()
    return redirect('/')

@app.route('/modify/<int:id>')
def modify(id):
    sql = "SELECT * FROM empleados WHERE id=%s;"
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql, id)
    empleado = cursor.fetchone()
    connection.commit()
    return render_template('empleados/edit.html', empleado=empleado)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto'] #form
    id = request.form['txtId']

    datos = (_nombre, _correo, id)

    connection = mysql.connect()
    cursor = connection.cursor()

    if (_foto.filename != ''):
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)

    sql = "SELECT foto FROM empleados WHERE id=%s;"
    cursor.execute(sql, id)

    nombreFoto = cursor.fetchone()[0]
    os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))

    connection = mysql.connect()
    cursor = connection.cursor()

    sql = "UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s;"
    cursor.execute(sql, datos)
    connection.commit()
    #return render_template('empleados/create.html')

if __name__ == '__main__':
    app.run(debug=True)