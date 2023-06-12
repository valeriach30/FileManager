from flask import Flask, render_template, request, session, redirect
from pymongo import MongoClient
from flask_socketio import SocketIO, send
from flask_session import Session
import json
import secrets


client = MongoClient('mongodb+srv://Kdaniel06:Dani060401$@cluster0.t10iglg.mongodb.net/?retryWrites=true&w=majority')
db = client['Users']
collection = db['User']

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = False
Session(app)

socketio = SocketIO(app)

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
            currentRoute = [' / raiz']
            return redirect('/dashboard?email=' + email + '&name=' + userName + '&route=' + str(currentRoute))
        else:
            # Credenciales inválidas
            return render_template('login.html', error='error')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Obtener nombre de la carpeta actual
    email = request.args.get('email')
    userName = request.args.get('name')
    currentRoute = eval(request.args.get('route'))
    
    if email:
        # Obtener carpetas y archivos del usuario
        # Cargar el JSON
        nombreArchivo = userName + '.json'
        with open(nombreArchivo) as json_file:
            data = json.load(json_file)
        
        folders, archivos = obtenerFileSystem(data)
        # Usuario autenticado, mostrar dashboard
        return render_template('dashboard.html', email=email, name=userName, 
                               folders=folders, archivos=archivos, rutas = currentRoute)
    else:
        # Usuario no autenticado, redirigir al inicio de sesión
        return redirect('/login',  error='')

@app.route('/subcarpeta')
def subcarpeta():
    
    email = request.args.get('email')
    userName = request.args.get('name')
    currentRoute = eval(request.args.get('ruta'))
    
    # Cargar el JSON
    nombreArchivo = userName + '.json'
    with open(nombreArchivo) as json_file:
        data = json.load(json_file)

    # Obtener nombre de la carpeta actual
    carpeta = request.args.get('carpeta')

    # Actualizar ruta
    currentRoute.append(" / " + carpeta) 
    
    # Obtener archivos y subcarpetas
    archivos, folders = buscar_carpeta(data, carpeta)
    
    # Redirigir
    return render_template('dashboard.html', email=email, name=userName, 
                               folders=folders, archivos=archivos, rutas = currentRoute)


@app.route('/rutaAnterior')
def rutaAnterior():

    email = request.args.get('email')
    userName = request.args.get('name')
    currentRoute = eval(request.args.get('rutas'))

    # Cargar el JSON
    nombreArchivo = userName + '.json'
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
    return render_template('dashboard.html', email=email, name=userName, 
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
    app.run()
