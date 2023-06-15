from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from flask_socketio import SocketIO, send
from flask_session import Session
import secrets
import complementos
import json


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


@app.route('/crearUsuario', methods=['POST'])
def crearUsuarioRoute():
    # Obtener los datos del formulario
    email = request.form['email']
    password = int(request.form['password'])
    nombre = request.form['nombre']
    espacio = int(request.form['espacio'])

    usuario = {
        'name': nombre,
        'password': password,
        'email': email,
        'files':[],
        'storage': espacio
    }

    existeUsuario = collection.find_one({"email": email})
    #El usuario ya esta registrado, manda error
    if existeUsuario:
        return render_template('login.html', error1='error1')
    else:
        #Lo mete en la base de datos
        collection.insert_one(usuario)
        #Crea el json para el usuario con el contenido del json template
        rutaPlantilla = 'template.json'
        archivoDestino = nombre + ".json"

        #Archivo template.json
        with open(rutaPlantilla, 'r') as archivo_original:
            contenido_json = json.load(archivo_original)

        with open(archivoDestino, 'w') as archivoDestino:
            json.dump(contenido_json, archivoDestino)



        return render_template('login.html', exito='exito')


# ---------------------- DASHBOARD ----------------------

@app.route('/dashboard')
def dashboard():
    # Obtener nombre de la carpeta actual
    email = request.args.get('email')
    userName = request.args.get('name')
    currentRoute = eval(request.args.get('route'))
    storage = complementos.determinarEspacio(userName)
    
    
    if email:
        
        # Cargar el JSON
        data = complementos.obtenerJson(userName)

        # Obtener carpetas y archivos del usuario
        folders, archivos = complementos.obtenerFileSystem(data)
        
        # Usuario autenticado, mostrar dashboard
        return render_template('dashboard.html', email=email, name=userName, folders=folders, 
                               archivos=archivos, rutas = currentRoute, error=False, 
                               storage=storage)
    else:
        # Usuario no autenticado, redirigir al inicio de sesión
        return redirect('/login',  error='')

# ---------------------- RUTAS NAVEGACION ----------------------

@app.route('/subcarpeta')
def subcarpeta():
    
    email = request.args.get('email')
    userName = request.args.get('name')
    carpetasRutas = request.args.get('carpetasRutas')
    currentRoute = eval(request.args.get('ruta'))
    storage = complementos.determinarEspacio(userName)
    
    
    # Cargar el JSON
    data = complementos.obtenerJson(userName)
    
    if(carpetasRutas):
        carpetasRutas = eval(carpetasRutas)
    else:
        carpetasRutas = obtenerCarpetas(data)

    # Obtener nombre de la carpeta actual
    carpeta = request.args.get('carpeta')

    # Actualizar ruta
    currentRoute.append(" / " + carpeta) 
    
    # Obtener archivos y subcarpetas
    archivos, folders = complementos.buscar_carpeta(data, currentRoute)
    
    # Redirigir
    return render_template('dashboard.html', email=email, name=userName, folders=folders, 
                           archivos=archivos, rutas = currentRoute, error=False, 
                           storage=storage, carpetasRutas=carpetasRutas)


@app.route('/rutaAnterior')
def rutaAnterior():

    email = request.args.get('email')
    userName = request.args.get('name')
    currentRoute = eval(request.args.get('rutas'))
    carpetasRutas = request.args.get('carpetasRutas')
    data = complementos.obtenerJson(userName)
    
    if(carpetasRutas):
        carpetasRutas = eval(carpetasRutas)
    else:
        carpetasRutas = obtenerCarpetas(data)

    # Obtener nombre de la carpeta actual
    carpeta = request.args.get('ruta')
     
    # Determinar el indice de la ruta seleccionada
    indice = currentRoute.index(carpeta) 

    if(len(currentRoute) != 1):
        # Actualizar ruta
        currentRoute = currentRoute[:indice+1]
        if(len(currentRoute) != 1):
            # Obtener archivos y subcarpetas
            archivos, folders = complementos.buscar_carpeta(data, currentRoute)
        else:
            folders, archivos = complementos.obtenerFileSystem(data)
    else:
        folders, archivos = complementos.obtenerFileSystem(data)

    # Redirigir
    storage = complementos.determinarEspacio(userName)
    return render_template('dashboard.html', email=email, name=userName, folders=folders, 
                           archivos=archivos, rutas = currentRoute, error=False, 
                           storage=storage, carpetasRutas=carpetasRutas)


# ---------------------- CREAR ARCHIVO ----------------------

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
    data = complementos.obtenerJson(userName)

    if(len(rutas) != 1):
        # Agregar el archivo al json
        error = complementos.nuevoArchivo(nombreArchivo, contenido, extension, userName, rutas, data)
        archivos, folders = complementos.buscar_carpeta(data, rutas)
    else:
        folders, archivos = complementos.obtenerFileSystem(data)
    
    storage = complementos.determinarEspacio(userName)
    if(error != None):
        return render_template('dashboard.html', email=email, name=userName, folders=folders,
                            archivos=archivos, rutas = rutas, error=error,
                            nombreArchivo=nombreArchivo, contenido = contenido, 
                            storage=storage)
    else:
        return render_template('dashboard.html', email=email, name=userName, folders=folders,
                            archivos=archivos, rutas = rutas, errorEspacio=True, 
                            storage=storage)


# ---------------------- EDITAR ARCHIVO ----------------------

@app.route('/editarArchivo')
def editarArchivo():

    # Obtener la info
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    nombreArchivo = request.args.get('nombreArch')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    nuevoContenido = request.args.get('nuevoContenido')
    data = complementos.obtenerJson(userName)

    if(len(rutas) != 1):
        # Editar el archivo
        exito = complementos.editarArchivo(rutas, data, nombreArchivo, nuevoContenido, userName)    
        archivos, folders = complementos.buscar_carpeta(data, rutas)
    else:
        folders, archivos = complementos.obtenerFileSystem(data)
    
    storage = complementos.determinarEspacio(userName)
    if(exito):
        return render_template('dashboard.html', email=email, name=userName, folders=folders, 
                            archivos=archivos, rutas = rutas, error=False, storage=storage)
    else:
        return render_template('dashboard.html', email=email, name=userName, folders=folders,
                            archivos=archivos, rutas = rutas, errorEspacio=True, 
                            storage=storage)

# ---------------------- COPIAR ARCHIVO ----------------------
#COPIAR
@app.route('/copiarArchivo')
def copiarArchivo():
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    data = complementos.obtenerJson(userName)
#CARGAR
@app.route('/cargarArchivo')
def cargarArchivo():
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    data = complementos.obtenerJson(userName)
#DESCARGAR
@app.route('/descargarArchivo')
def descargarArchivo():
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    data = complementos.obtenerJson(userName)
# ---------------------- ELIMINAR ARCHIVO ----------------------

@app.route('/eliminarArchivo')
def eliminarArchivo():
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    nombreArchivo = request.args.get('nombreAr')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    data = complementos.obtenerJson(userName)

    if(len(rutas) != 1):
        # Agregar el archivo al json
        complementos.eliminarArchivo(rutas, data, nombreArchivo, userName)
        archivos, folders = complementos.buscar_carpeta(data, rutas)
    else:
        folders, archivos = complementos.obtenerFileSystem(data)
    
    storage = complementos.determinarEspacio(userName)
    return render_template('dashboard.html', email=email, name=userName, folders=folders, 
                           archivos=archivos, rutas = rutas, error=False, storage=storage)


# ---------------------- SUSTITUIR ARCHIVO ----------------------
@app.route('/sustituirArchivo')
def sustituirArchivo():
    nombreArchivo = request.args.get('nombre')
    contenido = request.args.get('contenido')
    extension = request.args.get('extension')
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    data = complementos.obtenerJson(userName)

    if(len(rutas) != 1):
        # Eliminar el archivo del json
        complementos.eliminarArchivo(rutas, data, nombreArchivo + '.txt', userName)
        # Agregar el archivo al json
        data = complementos.obtenerJson(userName)
        complementos.nuevoArchivo(nombreArchivo, contenido, extension, userName, rutas, data)

        archivos, folders = complementos.buscar_carpeta(data, rutas)
    else:
        folders, archivos = complementos.obtenerFileSystem(data)
    
    storage = complementos.determinarEspacio(userName)
    return render_template('dashboard.html', email=email, name=userName, folders=folders,
                            archivos=archivos, rutas = rutas, error=False, storage=storage)


# ---------------------- CREAR CARPETA ----------------------

@app.route('/crearCarpeta')
def crearCarpeta():
    nombreCarpeta = request.args.get('nombre')
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    carpeta = request.args.get('ruta')    
    data = complementos.obtenerJson(userName)

    if(len(rutas) != 1):
        # Agregar el archivo al json
        error = complementos.nuevaCarpeta(nombreCarpeta, userName, rutas, data)
        archivos, folders = complementos.buscar_carpeta(data, rutas)
    else:
        folders, archivos = complementos.obtenerFileSystem(data)
    
    storage = complementos.determinarEspacio(userName)
    return render_template('dashboard.html', email=email, name=userName, folders=folders, 
                           archivos=archivos, rutas = rutas, errorCarpeta=error, 
                           nombreCarpeta=nombreCarpeta, storage=storage)
    
# ---------------------- COPIAR CARPETA ----------------------
#COPIAR
@app.route('/copiarCarpeta')
def copiarCarpeta():
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    data = complementos.obtenerJson(userName)
#CARGAR
@app.route('/cargarCarpeta')
def cargarCarpeta():
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    data = complementos.obtenerJson(userName)
#DESCARGAR
@app.route('/descargarCarpeta')
def descargarCarpeta():
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    data = complementos.obtenerJson(userName)

# ---------------------- ELIMINAR CARPETA ----------------------

@app.route('/eliminarCarpeta')
def eliminarCarpeta():
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    data = complementos.obtenerJson(userName)

    if(len(rutas) != 1):
        # Agregar el archivo al json
        complementos.eliminar_carpeta(data, rutas, userName)
        # Eliminar la ruta actual de la lista de rutas
        rutas.pop()
        archivos, folders = complementos.buscar_carpeta(data, rutas)
    else:
        folders, archivos = complementos.obtenerFileSystem(data)
    
    storage = complementos.determinarEspacio(userName)
    return render_template('dashboard.html', email=email, name=userName, folders=folders, 
                           archivos=archivos, rutas = rutas, error=False, storage=storage)


# ---------------------- SUSTITUIR CARPETA ----------------------
@app.route('/sustituirCarpeta')
def sustituirCarpeta():
    nombreCarpeta = request.args.get('nombre')
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    rutas.append(' / ' + nombreCarpeta)
    data = complementos.obtenerJson(userName)
    
    if(len(rutas) != 1):
        # Eliminar carpeta
        complementos.eliminar_carpeta(data, rutas, userName)
        # Eliminar la ruta actual de la lista de rutas
        rutas.pop()
        # Agregar nueva carpeta
        data = complementos.obtenerJson(userName)
        complementos.nuevaCarpeta(nombreCarpeta, userName, rutas, data)
        archivos, folders = complementos.buscar_carpeta(data, rutas)
    else:
        folders, archivos = complementos.obtenerFileSystem(data)
    
    storage = complementos.determinarEspacio(userName)
    return render_template('dashboard.html', email=email, name=userName, folders=folders,
                            archivos=archivos, rutas = rutas, error=False, storage=storage)

# ---------------------- MOVER CARPETA ----------------------

@app.route('/moverCarpeta')
def moverCarpeta():
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    destino = request.args.get('selectedValue')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    data = complementos.obtenerJson(userName)
    
    if(len(rutas) != 1):
        error, carpetaNueva = complementos.moverCarpeta(data, userName, rutas, destino)
        archivos, folders = complementos.buscar_carpeta(data, rutas)
    else:
        folders, archivos = complementos.obtenerFileSystem(data)
    
    if(not error):
        storage = complementos.determinarEspacio(userName)
        return render_template('dashboard.html', email=email, name=userName, folders=folders,
                                archivos=archivos, rutas = rutas, storage=storage)
    
    # Carpeta repetida, determinar si se quiere sustituir
    else:
        storage = complementos.determinarEspacio(userName)
        return render_template('dashboard.html', email=email, name=userName, folders=folders,
                                archivos=archivos, rutas = rutas, storage=storage, 
                                errorMovimiento= True, destino=destino)

@app.route('/sustituirMover')
def sustituirMover():
    
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    destino = request.args.get('destino')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    data = complementos.obtenerJson(userName)
    
    if(len(rutas) != 1):
        complementos.moverSustituir(data, userName, rutas, destino)
        archivos, folders = complementos.buscar_carpeta(data, rutas)
    else:
        folders, archivos = complementos.obtenerFileSystem(data)
    storage = complementos.determinarEspacio(userName)
    return render_template('dashboard.html', email=email, name=userName, folders=folders,
                            archivos=archivos, rutas = rutas, storage=storage)

# ---------------------- OBTENER CARPETAS ----------------------
def obtenerCarpetas(data):
    carpetas = []
    carpetas = complementos.obtenerCarpetas(data)
    carpetas.pop(0)
    return carpetas

# ---------------------- MAIN ----------------------
if __name__ == '__main__':
    app.run()