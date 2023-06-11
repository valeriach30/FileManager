from flask import Flask, render_template, request, session, redirect, flash
from pymongo import MongoClient
from flask_socketio import SocketIO, send
import json


client = MongoClient('mongodb+srv://Kdaniel06:Dani060401$@cluster0.t10iglg.mongodb.net/?retryWrites=true&w=majority')
db = client['Users']
collection = db['User']

app = Flask(__name__)
app.secret_key = 'testing'
socketio = SocketIO(app)

folders = []
archivos = []

@app.route('/')
def home():
    # Página de inicio
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = collection.find_one({'email': email, 'password': int(password)})
        # Imprimir el usuario que encuentra, si no existe muestra None
        # print(f"User: {user}")
        
        # Muestra todos los usuarios
        # docs = collection.find()
        # for doc in docs:
        #    print(doc)

        if user:
            # Usuario autenticado
            userName = user['name']
            print(userName)
            session['email'] = email
            session['name'] = userName
            return redirect('/dashboard')
        else:
            # Credenciales inválidas
            return render_template('login.html', error='error')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        # Obtener carpetas y archivos del usuario
        obtenerFileSystem()

        # Usuario autenticado, mostrar dashboard
        return render_template('dashboard.html', email=session['email'], name=session['name'], 
                               folders=folders, archivos=archivos)
    else:
        # Usuario no autenticado, redirigir al inicio de sesión
        return redirect('/login',  error='')


# Obtener la estructura del usuario
def obtenerFileSystem():
    # Cargar el JSON
    nombreArchivo = session['name'] + '.json'
    with open(nombreArchivo) as json_file:
        data = json.load(json_file)

    # Obtener carpetas y archivos
    for item in data['files']:
        if item['type'] == 'folder':
            if(item not in folders):
                folders.append(item)
        elif item['type'] == 'archivo':
            if(item not in archivos):
                archivos.append(item)

if __name__ == '__main__':
    socketio.run(app)
    app.run()
