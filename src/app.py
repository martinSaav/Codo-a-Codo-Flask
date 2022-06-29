from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

#regalado
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mtd010202'
app.config['MYSQL_DATABASE_DB'] = 'empleados'

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
    sql = "INSERT INTO empleados (nombre, correo, foto) values (%s, %s, %s);"
    datos = (_nombre, _correo, _foto.filename)
    
    connection = mysql.connect()
    cursor = connection.cursor()
    cursor.execute(sql, datos)
    connection.commit()
    #return render_template('empleados/create.html')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)