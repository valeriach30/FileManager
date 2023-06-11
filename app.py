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

currentRoute = [' / raiz']


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
        # Cargar el JSON
        nombreArchivo = session['name'] + '.json'
        with open(nombreArchivo) as json_file:
            data = json.load(json_file)
        
        folders, archivos = obtenerFileSystem(data)
        # Usuario autenticado, mostrar dashboard
        return render_template('dashboard.html', email=session['email'], name=session['name'], 
                               folders=folders, archivos=archivos, rutas = currentRoute)
    else:
        # Usuario no autenticado, redirigir al inicio de sesión
        return redirect('/login',  error='')

@app.route('/subcarpeta')
def subcarpeta():
    # Cargar el JSON
    nombreArchivo = session['name'] + '.json'
    with open(nombreArchivo) as json_file:
        data = json.load(json_file)

    # Obtener nombre de la carpeta actual
    carpeta = request.args.get('carpeta')

    # Actualizar ruta
    currentRoute.append(" / " + carpeta) 
    
    # Obtener archivos y subcarpetas
    archivos, folders = buscar_carpeta(data, carpeta)

    # Redirigir
    return render_template('dashboard.html', email=session['email'], name=session['name'], 
                               folders=folders, archivos=archivos, rutas = currentRoute)


@app.route('/rutaAnterior')
def rutaAnterior():

    # Cargar el JSON
    nombreArchivo = session['name'] + '.json'
    with open(nombreArchivo) as json_file:
        data = json.load(json_file)
        
    # Obtener nombre de la carpeta actual
    carpeta = request.args.get('ruta')
    

    
    if(len(currentRoute) != 1):
        # Actualizar ruta
        currentRoute.pop()
        if(len(currentRoute) != 1):
            # Obtener archivos y subcarpetas
            archivos, folders = buscar_carpeta(data, carpeta[3:])
        else:
            folders, archivos = obtenerFileSystem(data)
    else:
        folders, archivos = obtenerFileSystem(data)

    # Redirigir
    return render_template('dashboard.html', email=session['email'], name=session['name'], 
                               folders=folders, archivos=archivos, rutas = currentRoute)

def buscar_carpeta(json_data, nombre_carpeta):
    archivos_encontrados = []
    carpetas_encontradas = []

    def buscar_recursivo(data):
        for item in data['files']:
            if item['type'] == 'folder' and item['name'] == nombre_carpeta:
                for archivo in item['files']:
                    if archivo['type'] == 'archivo':
                        archivos_encontrados.append(archivo)
                for carpeta in item['files']:
                    if carpeta['type'] == 'folder':
                        carpetas_encontradas.append(carpeta)
            elif item['type'] == 'folder':
                buscar_recursivo(item)

    buscar_recursivo(json_data)
    return archivos_encontrados, carpetas_encontradas

# Obtener la estructura del usuario
def obtenerFileSystem(data):
    folders = []
    archivos = []

    # Obtener carpetas y archivos
    for item in data['files']:
        if item['type'] == 'folder':
            if(item not in folders):
                folders.append(item)
        elif item['type'] == 'archivo':
            if(item not in archivos):
                archivos.append(item)

    return folders, archivos

if __name__ == '__main__':
    socketio.run(app)
    app.run()
