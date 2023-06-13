from flask import Flask, render_template, request, session, redirect
from pymongo import MongoClient
from flask_socketio import SocketIO, send
from flask_session import Session
from datetime import date
import json
import secrets
import random


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

# ---------------------- INICIAR SESION ----------------------

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
            currentRoute = [' / home']
            return redirect('/dashboard?email=' + email + '&name=' + userName + '&route=' + str(currentRoute))
        else:
            # Credenciales inválidas
            return render_template('login.html', error='error')

    return render_template('login.html')

# ---------------------- DASHBOARD ----------------------

@app.route('/dashboard')
def dashboard():
    # Obtener nombre de la carpeta actual
    email = request.args.get('email')
    userName = request.args.get('name')
    currentRoute = eval(request.args.get('route'))
    
    if email:
        
        # Cargar el JSON
        data = obtenerJson(userName)
        
        # Obtener carpetas y archivos del usuario
        folders, archivos = obtenerFileSystem(data)
        
        # Usuario autenticado, mostrar dashboard
        return render_template('dashboard.html', email=email, name=userName, 
                               folders=folders, archivos=archivos, rutas = currentRoute)
    else:
        # Usuario no autenticado, redirigir al inicio de sesión
        return redirect('/login',  error='')

# ---------------------- RUTAS NAVEGACION ----------------------

@app.route('/subcarpeta')
def subcarpeta():
    
    email = request.args.get('email')
    userName = request.args.get('name')
    currentRoute = eval(request.args.get('ruta'))
    
    # Cargar el JSON
    data = obtenerJson(userName)

    # Obtener nombre de la carpeta actual
    carpeta = request.args.get('carpeta')

    # Actualizar ruta
    currentRoute.append(" / " + carpeta) 
    
    # Obtener archivos y subcarpetas
    archivos, folders = buscar_carpeta(data, currentRoute)
    
    # Redirigir
    return render_template('dashboard.html', email=email, name=userName, 
                               folders=folders, archivos=archivos, rutas = currentRoute)


@app.route('/rutaAnterior')
def rutaAnterior():

    email = request.args.get('email')
    userName = request.args.get('name')
    currentRoute = eval(request.args.get('rutas'))

    data = obtenerJson(userName)
        
    # Obtener nombre de la carpeta actual
    carpeta = request.args.get('ruta')
     
    # Determinar el indice de la ruta seleccionada
    indice = currentRoute.index(carpeta) 

    if(len(currentRoute) != 1):
        # Actualizar ruta
        currentRoute = currentRoute[:indice+1]
        if(len(currentRoute) != 1):
            # Obtener archivos y subcarpetas
            archivos, folders = buscar_carpeta(data, currentRoute)
        else:
            folders, archivos = obtenerFileSystem(data)
    else:
        folders, archivos = obtenerFileSystem(data)

    # Redirigir
    return render_template('dashboard.html', email=email, name=userName, 
                               folders=folders, archivos=archivos, rutas = currentRoute)

# ---------------------- FUNCIONES CREAR ----------------------

@app.route('/crearArchivo')
def crearArchivo():
    nombreArchivo = request.args.get('nombre')
    contenido = request.args.get('contenido')
    extension = request.args.get('extension')
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    carpeta = request.args.get('ruta')    
    data = obtenerJson(userName)
    
    if(len(rutas) != 1):
        # Agregar el archivo al json
        nuevoArchivo(nombreArchivo, contenido, extension, userName, rutas, data)
        archivos, folders = buscar_carpeta(data, rutas)
    else:
        folders, archivos = obtenerFileSystem(data)
    
    return render_template('dashboard.html', email=email, name=userName, 
                               folders=folders, archivos=archivos, rutas = rutas)
    

@app.route('/crearCarpeta')
def crearCarpeta():
    nombreCarpeta = request.args.get('nombre')
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    carpeta = request.args.get('ruta')    
    data = obtenerJson(userName)

    if(len(rutas) != 1):
        # Agregar el archivo al json
        nuevaCarpeta(nombreCarpeta, userName, rutas, data)
        archivos, folders = buscar_carpeta(data, rutas)
    else:
        folders, archivos = obtenerFileSystem(data)
    
    return render_template('dashboard.html', email=email, name=userName, 
                               folders=folders, archivos=archivos, rutas = rutas)
    

@app.route('/eliminarCarpeta')
def eliminarCarpeta():
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    carpeta = request.args.get('ruta') 
    data = obtenerJson(userName)

    if(len(rutas) != 1):
        # Agregar el archivo al json
        eliminar_carpeta(data, rutas, userName)
        # Eliminar la ruta actual de la lista de rutas
        rutas.pop()
        carpeta = rutas[-1]
        archivos, folders = buscar_carpeta(data, rutas)
    else:
        folders, archivos = obtenerFileSystem(data)
    
    return render_template('dashboard.html', email=email, name=userName, 
                               folders=folders, archivos=archivos, rutas = rutas)

# ---------------------- FUNCIONES COMPLEMENTARIAS ----------------------
def nuevoArchivo(nombreArchivo, contenido, extension, usuario, rutas, data):
    rutas = [ruta.strip().lstrip('/').strip() for ruta in rutas if ruta.strip()]
    rutas.pop(0)
    carpeta = buscarContenido(data["files"], rutas)
    if carpeta is not None:
        size = str(random.randint(1, 1000)) + ' KB'
        fecha_actual = date.today()
        fecha_actual = fecha_actual.strftime("%d/%m/%Y")
        nuevo_archivo = {
            "name": nombreArchivo,
            "type": "archivo",
            "size": size,  
            "created_at": fecha_actual,
            "updated": fecha_actual,  
            "user": usuario,
            "content": contenido
        }
        # Agrega el nuevo archivo a la carpeta encontrada
        carpeta["files"].append(nuevo_archivo)

        # Convierte el objeto Python de vuelta a JSON
        updated_json = json.dumps(data)

        # Actualiza el archivo local con el nuevo JSON
        nombreArchivo = usuario + '.json'
        with open(nombreArchivo, "w") as file:
            file.write(updated_json)

def nuevaCarpeta(nombreCarpeta, usuario, rutas, data):
    rutas = [ruta.strip().lstrip('/').strip() for ruta in rutas if ruta.strip()]
    rutas.pop(0)
    carpeta = buscarContenido(data["files"], rutas)
    if carpeta is not None:
        size = str(random.randint(1, 1000)) + ' KB'
        fecha_actual = date.today()
        fecha_actual = fecha_actual.strftime("%d/%m/%Y")
        carpetaNueva = {
            "name": nombreCarpeta,
            "type": "folder",
            "created_at": fecha_actual,
            "updated": fecha_actual,
            "user": "valeria",
            "files": []
        }
        # Agrega el nuevo archivo a la carpeta encontrada
        carpeta["files"].append(carpetaNueva)

        # Convierte el objeto Python de vuelta a JSON
        updated_json = json.dumps(data)

        # Actualiza el archivo local con el nuevo JSON
        nombreArchivo = usuario + '.json'
        with open(nombreArchivo, "w") as file:
            file.write(updated_json)

def eliminar_carpeta(data, rutas, usuario):
    rutas = [ruta.strip().lstrip('/').strip() for ruta in rutas if ruta.strip()]
    rutas.pop(0)
    eliminar_directorio(data["files"], rutas)
    # Convierte el objeto Python de vuelta a JSON
    updated_json = json.dumps(data)

    # Actualiza el archivo local con el nuevo JSON
    nombreArchivo = usuario + '.json'
    with open(nombreArchivo, "w") as file:
        file.write(updated_json)
    
# Función recursiva para eliminar un directorio y sus archivos/subdirectorios
def eliminar_directorio(files, rutas_directorio):
    if len(rutas_directorio) == 0:
        return False

    ruta_directorio = rutas_directorio[0]

    for file in files:
        if file["name"] == ruta_directorio and file["type"] == "folder":
            if len(rutas_directorio) == 1:
                files.remove(file)
                return True
            else:
                return eliminar_directorio(file["files"], rutas_directorio[1:])
        elif file["type"] == "folder" and "files" in file:
            if eliminar_directorio(file["files"], rutas_directorio):
                return True
    return False

# Función recursiva para encontrar contenido de una carpeta
def buscarContenido(files, ruta_carpeta):
    if len(ruta_carpeta) == 0:
        return None

    nombre_carpeta = ruta_carpeta[0]

    for file in files:
        if file["name"] == nombre_carpeta and file["type"] == "folder":
            if len(ruta_carpeta) == 1:
                return file
            if "files" in file:
                carpeta_encontrada = buscarContenido(file["files"], ruta_carpeta[1:])
                if carpeta_encontrada is not None:
                    return carpeta_encontrada

    return None

def obtenerJson(userName):
    # Cargar el JSON
    nombreArchivo = userName + '.json'
    with open(nombreArchivo) as json_file:
        data = json.load(json_file)
    return data

def buscar_carpeta(json_data, ruta_carpeta):
    
    ruta_carpeta = [ruta.strip().lstrip('/').strip() for ruta in ruta_carpeta if ruta.strip()]
    ruta_carpeta.pop(0)
    
    archivos_encontrados = []
    carpetas_encontradas = []

    def buscar_recursivo(data, ruta_actual):
        if len(ruta_actual) == 0:
            for item in data['files']:
                if item['type'] == 'archivo':
                    archivos_encontrados.append(item)
                elif item['type'] == 'folder':
                    carpetas_encontradas.append(item)
        else:
            nombre_carpeta = ruta_actual[0]
            for item in data['files']:
                if item['type'] == 'folder' and item['name'] == nombre_carpeta:
                    if len(ruta_actual) == 1:
                        for archivo in item['files']:
                            if archivo['type'] == 'archivo':
                                archivos_encontrados.append(archivo)
                        for carpeta in item['files']:
                            if carpeta['type'] == 'folder':
                                carpetas_encontradas.append(carpeta)
                    else:
                        buscar_recursivo(item, ruta_actual[1:])
                
    buscar_recursivo(json_data, ruta_carpeta)
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
