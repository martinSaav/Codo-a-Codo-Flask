from flask import Flask, render_template
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mtd010202'
app.config['MYSQL_DATABASE_DB'] = 'empleados'

mysql.init_app(app)

@app.route('/') #index  (, methods=["GET"])
def index():
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "insert into empleados (nombre, correo, foto) values \
    ('Juan', 'juan@hotmail.com', 'fotodejuan.jpg');"
    cursor.execute(sql)
    connection.commit()
    return render_template('empleados/index.html')

if __name__ == '__main__':
    app.run(debug=True)