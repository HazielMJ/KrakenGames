from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configura la conexión a la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Juegos'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Define el filtro b64encode
def b64encode_filter(s):
    return base64.b64encode(s).decode() if s else None

# Registrar el filtro en el entorno de Jinja2
app.jinja_env.filters['b64encode'] = b64encode_filter


@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT categoria FROM juegos")
    categorias = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT DISTINCT marca FROM juegos")
    marcas = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM juegos")
    juegos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('index.html', juegos=juegos, categorias=categorias, marcas=marcas)

@app.route('/filter')
def filter_games():
    categoria = request.args.get('categoria')

    query = "SELECT * FROM juegos WHERE 1=1"
    params = []

    if categoria:
        query += " AND categoria = %s"
        params.append(categoria)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    juegos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('index.html', juegos=juegos)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND password = %s", (usuario, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['id'] = user[0]
            session['tipo_usuario'] = user[3]  # Asumiendo que 'tipo_usuario' está en la columna 4 (índice 3)
            if user[3] == 'administrador':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
        else:
            return "Usuario o contraseña incorrectos"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('id', None)  # Elimina el id de usuario de la sesión
    session.pop('tipo_usuario', None)  # Elimina el tipo de usuario de la sesión
    return redirect(url_for('index'))  # Redirige al formulario de inicio de sesión

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (%s, %s)", (usuario, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')
            
@app.route('/password', methods=['GET', 'POST'])
def password():
    if request.method == 'POST':
        if 'email' in request.form:
            email = request.form['email']
            return redirect(url_for('login'))
        elif 'new_password' in request.form and 'confirm_password' in request.form:
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            if new_password == confirm_password:
                return redirect(url_for('login'))
            else:
                return render_template('password.html')
    else:  # Manejar el método GET devolviendo el formulario de cambio de contraseña
        return render_template('password.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Handle add, edit, delete operations
        pass
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM juegos")
    juegos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin.html', juegos=juegos)

@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/xbox')
def xbox():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT categoria FROM juegos")
    categorias = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT DISTINCT marca FROM juegos")
    marcas = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM juegos")
    juegos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('xbox.html', juegos=juegos, categorias=categorias, marcas=marcas)

@app.route('/ps')
def ps():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT categoria FROM juegos")
    categorias = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT DISTINCT marca FROM juegos")
    marcas = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM juegos")
    juegos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('ps.html', juegos=juegos, categorias=categorias, marcas=marcas)
 

@app.route('/nintendo')
def nintendo():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Obtener todas las categorías
    cursor.execute("SELECT DISTINCT categoria FROM juegos")
    categorias = [row[0] for row in cursor.fetchall()]
    
    # Obtener todas las marcas
    cursor.execute("SELECT DISTINCT marca FROM juegos")
    marcas = [row[0] for row in cursor.fetchall()]
    
    # Obtener todos los juegos
    cursor.execute("SELECT * FROM juegos")
    juegos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('nintendo.html', juegos=juegos, categorias=categorias, marcas=marcas)

 


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        address = request.form['address']
        payment_method = request.form['payment_method']
        user_id = session.get('id')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO compras (usuarios_id, producto_id, cantidad, total) VALUES (%s, %s, %s, %s)", (user_id, 1, 1, 100.00)) # ejemplo de inserción, ajustar según tu lógica
        conn.commit()
        cursor.close()
        conn.close()

        # Redirect to the home page after successful payment
        return redirect(url_for('index'))
    return render_template('payment.html')



@app.route('/add', methods=['POST'])
def add_game():
    if 'id' not in session:
        return redirect(url_for('login'))
    if session['tipo_usuario'] != 'administrador':
        return redirect(url_for('index'))
    
    nombre = request.form['nombre']
    precio = request.form['precio']
    categoria = request.form['categoria']
    descripcion = request.form['descripcion']
    marca = request.form['marca']  
    imagen = request.files['imagen'].read() if request.files['imagen'].filename else None
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO juegos (nombre, precio, categoria, descripcion, marca, imagen) VALUES (%s, %s, %s, %s, %s, %s)",
                   (nombre, precio, categoria, descripcion, marca, imagen))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('admin'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit_game(id):
    if 'id' not in session:
        return redirect(url_for('login'))
    if session['tipo_usuario'] != 'administrador':
        return redirect(url_for('index'))
    
    nombre = request.form['nombre']
    precio = request.form['precio']
    categoria = request.form['categoria']
    descripcion = request.form['descripcion']
    marca = request.form['marca']  
    imagen = request.files['imagen'].read() if request.files['imagen'].filename else None
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if imagen:
        cursor.execute("UPDATE juegos SET nombre = %s, precio = %s, categoria = %s, descripcion = %s, marca = %s, imagen = %s WHERE id = %s",
                       (nombre, precio, categoria, descripcion, marca, imagen, id))
    else:
        cursor.execute("UPDATE juegos SET nombre = %s, precio = %s, categoria = %s, descripcion = %s, marca = %s WHERE id = %s",
                       (nombre, precio, categoria, descripcion, marca, id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('admin'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_game(id):
    if 'id' not in session:
        return redirect(url_for('login'))
    if session['tipo_usuario'] != 'administrador':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM juegos WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
