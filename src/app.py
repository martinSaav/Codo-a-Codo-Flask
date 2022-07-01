from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from datetime import datetime
import os

app = Flask(__name__)
mysql = MySQL()

#regalado
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mtd010202'
app.config['MYSQL_DATABASE_DB'] = 'empleados'
app.config['SECRET_KEY'] = "codoacodo"

UPLOADS = os.path.join('src/uploads')#guardamos la ruta como valor en la app
app.config['UPLOADS'] = UPLOADS

mysql.init_app(app)
connection = mysql.connect()
cursor = connection.cursor(cursor=DictCursor) 

def query_my_sql(query, datos = None, tipo_de_retorno = ""):
    if (datos != None):
        cursor.execute(query, datos)
    else:
        cursor.execute(query)

    if (tipo_de_retorno == "one"):
        registro = cursor.fetchone()
        return registro
    elif (tipo_de_retorno == "all"):
        registro = cursor.fetchall()
        return registro

    connection.commit()

@app.route('/foto_usuario/<path:nombre_foto>') 
def uploads(nombre_foto): #se pasa arriba
    return send_from_directory(os.path.join('uploads'), nombre_foto)

@app.route('/') #index  (, methods=["GET"])
def index():
    sql = "SELECT * FROM empleados;"
    empleados = query_my_sql(sql, None, "all")
    return render_template('empleados/index.html', empleados = empleados)

@app.route('/empleado/crear', methods=["GET", "POST"])
def alta_empleado():
    if (request.method == "GET"):
        return render_template('empleados/create.html')
    if (request.method == "POST"):
        _nombre = request.form['txtNombre']
        _correo = request.form['txtCorreo']
        _foto = request.files['txtFoto']
        if (_nombre == "" or _correo == "" or _foto.filename == ""):
            flash("Todos los campos son obligatorios.")
            return redirect(url_for('alta_empleado'))
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")

        if (_foto.filename != ''):
            nuevoNombreFoto = tiempo + '_' + _foto.filename
            _foto.save("src/uploads/" + nuevoNombreFoto)

        sql = "INSERT INTO empleados (nombre, correo, foto) values (%s, %s, %s);"
        datos = (_nombre, _correo, nuevoNombreFoto)

        query_my_sql(sql, datos)
        return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    sql = "SELECT foto FROM empleados where id=%s"
    nombre_foto = query_my_sql(sql, (id, ), "one")["foto"]
    try:
        os.remove(os.path.join(app.config['UPLOADS'], nombre_foto))
    except:
        pass
    sql = "DELETE FROM empleados WHERE id=%s;"
    query_my_sql(sql, (id, ))

    return redirect('/')

@app.route('/modify/<int:id>')
def modify(id):
    sql = "SELECT * FROM empleados WHERE id=%s;"
    empleado = query_my_sql(sql, (id, ), "one")
    return render_template('empleados/edit.html', empleado=empleado)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    id = request.form['txtId']

    datos = (_nombre, _correo, id)

    if (_foto.filename != ''):
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevo_nombre_foto = tiempo + '_' + _foto.filename
        _foto.save("src/uploads/" + nuevo_nombre_foto)

        sql = "SELECT foto FROM empleados WHERE id=%s;"
        nombre_foto = query_my_sql(sql, (id, ), "one")["foto"]
        print(nombre_foto)
        try:
            os.remove(os.path.join(app.config['UPLOADS'], nombre_foto))
        except:
            pass
        sql = "UPDATE empleados SET foto=%s WHERE id=%s;"
        query_my_sql(sql, (nuevo_nombre_foto, id))

    sql = "UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s;"
    query_my_sql(sql, datos)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)