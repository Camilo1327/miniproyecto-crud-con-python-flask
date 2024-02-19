from flask import Flask, render_template, redirect, flash, url_for, request, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
app=Flask(__name__, static_folder='static')

# Conexion mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdatos27'
app.secret_key = 'lola'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/docentes', methods=['GET'])
def get_docentes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM docentes")
    docentes = cur.fetchall()
    cur.close()
    
    return render_template('docentes.html', docentes=docentes)

@app.route('/docentes/<int:id>', methods=['GET'])
def get_docente(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM docentes WHERE id = %s", (id,))
    docente = cur.fetchone()
    cur.close()
    return render_template('verdocente.html', docente=docente)

@app.route('/docentes/add', methods=['GET', 'POST'])
def add_docente():
    if request.method == 'POST':
        # Obtener los datos del formulario del docente
        data = request.form
        nombre = data['nombre']
        apellido = data['apellido']
        documento = data['documento']
        correo = data['correo']
        NumCel = data['NumCel']
        # Obtener la imagen del formulario
        if 'imagen' not in request.files:
            flash('No se seleccionó ninguna imagen', 'error')
            return redirect(request.url)
        file = request.files['imagen']
        if file.filename == '':
            flash('No se seleccionó ninguna imagen', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Imagen subida correctamente', 'success')
            # Guardar el docente en la base de datos junto con la ruta de la imagen
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO docentes (nombre, apellido, documento, correo, NumCel, imagen) VALUES (%s, %s, %s, %s, %s, %s)", (nombre, apellido, documento, correo, NumCel, filename))
            mysql.connection.commit()
            cur.close()
            flash('El docente se registró con éxito.', 'success')  # Mensaje de éxito
            return redirect(url_for('get_docentes'))
        else:
            flash('Formato de archivo no válido. Se admiten solo archivos con extensiones: png, jpg, jpeg, gif', 'error')
            return redirect(request.url)
    return render_template('nuevodoc.html')
@app.route('/docentes/edit/<int:id>', methods=['GET', 'POST'])
def edit_docente(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM docentes WHERE id = %s", (id,))
    docente = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        # Obtener la información del formulario
        data = request.form
        nombre = data['nombre']
        apellido = data['apellido']
        documento = data['documento']
        correo = data['correo']
        NumCel = data['NumCel']
        
        # Verificar si se seleccionó una nueva imagen
        if 'imagen' in request.files:
            imagen = request.files['imagen']
            if imagen.filename != '':
                # Guardar la nueva imagen en la carpeta de subidas
                filename = secure_filename(imagen.filename)
                ruta_imagen = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imagen.save(ruta_imagen)
                # Actualizar la ruta de la imagen en la base de datos
                cur = mysql.connection.cursor()
                cur.execute("UPDATE docentes SET nombre = %s, apellido = %s, documento = %s, correo = %s, NumCel = %s, ruta_imagen = %s WHERE id = %s", (nombre, apellido, documento, correo, NumCel, ruta_imagen, id))
                mysql.connection.commit()
                cur.close()
                flash('El docente se editó con éxito.', 'success')  # Mensaje de éxito y redireccion
                return redirect(url_for('get_docentes'))

        # Actualizar la información del docente en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("UPDATE docentes SET nombre = %s, apellido = %s, documento = %s, correo = %s, NumCel = %s WHERE id = %s", (nombre, apellido, documento, correo, NumCel, id))
        mysql.connection.commit()
        cur.close()
        flash('El docente se editó con éxito.', 'success')  # Mensaje de éxito y redireccion
        return redirect(url_for('get_docentes'))
    
    return render_template('editdocente.html', docente=docente)
@app.route('/docentes/delete/<int:id>', methods=['POST'])
def delete_docente(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM docentes WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('El docente se eliminó correctamente.', 'success')
    return redirect(url_for('get_docentes'))


if __name__ == '__main__':
    app.run(debug=True, port=8080)