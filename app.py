from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from config import Config

app = Flask(__name__)

# Configuración de la conexión a la base de datos
db_config = {
    'user': Config.MYSQL_USER,
    'password': Config.MYSQL_PASSWORD,
    'host': Config.MYSQL_HOST,
    'database': Config.MYSQL_DB
}

# Ruta para la página de inicio
@app.route('/')
def index():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Destinos")
    destinos = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', destinos=destinos)

# Ruta para la página de destinos
@app.route('/destinos')
def destinos():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Destinos")
    destinos = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('destinos.html', destinos=destinos)

# Ruta para agregar un nuevo destino
@app.route('/agregar_destino', methods=['POST'])
def agregar_destino():
    destino = request.form['destino']
    paquete = request.form['paquete']
    precio = request.form['precio']
    imagen = request.form['imagen']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Destinos (Destino, Paquete, Precio, Imagen) VALUES (%s, %s, %s, %s)
    """, (destino, paquete, precio, imagen))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('destinos'))

# Ruta para mostrar el formulario de modificación de un destino
@app.route('/modificar_destino/<int:id>', methods=['GET', 'POST'])
def modificar_destino(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    if request.method == 'POST':
        destino = request.form['destino']
        paquete = request.form['paquete']
        precio = request.form['precio']
        imagen = request.form['imagen']

        cursor.execute("""
            UPDATE Destinos SET Destino=%s, Paquete=%s, Precio=%s, Imagen=%s WHERE IDDestino=%s
        """, (destino, paquete, precio, imagen, id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('destinos'))
    else:
        cursor.execute("SELECT * FROM Destinos WHERE IDDestino = %s", (id,))
        destino = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('modificar_destino.html', destino=destino)

# Ruta para eliminar un destino
@app.route('/eliminar_destino/<int:id>')
def eliminar_destino(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Destinos WHERE IDDestino = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('destinos'))

# Ruta para la página de clientes
@app.route('/clientes')
def clientes():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Clientes')
    clientes = cursor.fetchall()
    cursor.execute('SELECT * FROM Destinos')
    destinos = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('clientes.html', clientes=clientes, destinos=destinos)

    

# Ruta para agregar un nuevo cliente
@app.route('/agregar_cliente', methods=['GET', 'POST'])
def agregar_cliente():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    dni = request.form['dni']
    destino = request.form['destino']
    fecha_ida = request.form['fecha_ida']
    fecha_vuelta = request.form['fecha_vuelta']
    habitaciones = request.form['habitaciones']
    mayores = request.form['mayores']
    menores = request.form['menores']
    forma_de_pago = request.form['forma_de_pago']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Clientes (Nombre, Apellido, DNI, Destino, Fecha_ida, Fecha_vuelta, Habitaciones, Mayores, Menores, Forma_de_pago)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (nombre, apellido, dni, destino, fecha_ida, fecha_vuelta, habitaciones, mayores, menores, forma_de_pago))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('clientes'))

# Ruta para mostrar el formulario de modificación de un cliente
@app.route('/modificar_cliente/<int:id>', methods=['GET', 'POST'])
def modificar_cliente(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        destino = request.form['destino']
        fecha_ida = request.form['fecha_ida']
        fecha_vuelta = request.form['fecha_vuelta']
        habitaciones = request.form['habitaciones']
        mayores = request.form['mayores']
        menores = request.form['menores']
        forma_de_pago = request.form['forma_de_pago']

        cursor.execute("""
            UPDATE Clientes SET Nombre=%s, Apellido=%s, DNI=%s, Destino=%s, Fecha_ida=%s, Fecha_vuelta=%s, Habitaciones=%s, Mayores=%s, Menores=%s, Forma_de_pago=%s
            WHERE IDCliente=%s
        """, (nombre, apellido, dni, destino, fecha_ida, fecha_vuelta, habitaciones, mayores, menores, forma_de_pago, id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('clientes'))
    else:
        cursor.execute("SELECT * FROM Clientes WHERE IDCliente = %s", (id,))
        cliente = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('modificar_cliente.html', cliente=cliente)

# Ruta para eliminar un cliente
@app.route('/eliminar_cliente/<int:id>')
def eliminar_cliente(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Clientes WHERE IDCliente = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('clientes'))

# Ruta para la página de reserva y procesamiento del formulario
@app.route('/reserva', methods=['GET', 'POST'])
def reserva():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        destino = request.form['destino']
        fecha_ida = request.form['fecha_ida']
        fecha_vuelta = request.form['fecha_vuelta']
        habitaciones = request.form['habitaciones']
        mayores = request.form['mayores']
        menores = request.form['menores']
        forma_de_pago = request.form['forma_de_pago']

        # Guardar los datos en la base de datos (aquí deberías insertar en la tabla Clientes)
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Clientes (Nombre, Apellido, DNI, Destino, Fecha_ida, Fecha_vuelta, Habitaciones, Mayores, Menores, Forma_de_pago)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, dni, destino, fecha_ida, fecha_vuelta, habitaciones, mayores, menores, forma_de_pago))
        connection.commit()
        cursor.close()
        connection.close()

        # Redireccionar a la página de clientes después de la reserva
        return redirect(url_for('clientes'))
    
    else:
        # Si es un GET, mostrar la página de reserva con los destinos disponibles
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Destinos")
        destinos = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return render_template('reserva.html', destinos=destinos)


if __name__ == '__main__':
    app.run(debug=True)
