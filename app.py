from flask import Flask, render_template, request, session, redirect
from pymongo import MongoClient
from flask_socketio import SocketIO, send
from flask_session import Session
import secrets
import complementos


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
    storage = determinarEspacio(userName)
    if email:
        
        # Cargar el JSON
        data = complementos.obtenerJson(userName)
        
        # Obtener carpetas y archivos del usuario
        folders, archivos = complementos.obtenerFileSystem(data)
        
        # Usuario autenticado, mostrar dashboard
        return render_template('dashboard.html', email=email, name=userName, folders=folders, 
                               archivos=archivos, rutas = currentRoute, error=False, storage=storage)
    else:
        # Usuario no autenticado, redirigir al inicio de sesión
        return redirect('/login',  error='')

# ---------------------- RUTAS NAVEGACION ----------------------

@app.route('/subcarpeta')
def subcarpeta():
    
    email = request.args.get('email')
    userName = request.args.get('name')
    currentRoute = eval(request.args.get('ruta'))
    storage = determinarEspacio(userName)
    # Cargar el JSON
    data = complementos.obtenerJson(userName)

    # Obtener nombre de la carpeta actual
    carpeta = request.args.get('carpeta')

    # Actualizar ruta
    currentRoute.append(" / " + carpeta) 
    
    # Obtener archivos y subcarpetas
    archivos, folders = complementos.buscar_carpeta(data, currentRoute)
    
    # Redirigir
    return render_template('dashboard.html', email=email, name=userName, folders=folders, 
                           archivos=archivos, rutas = currentRoute, error=False, storage=storage)


@app.route('/rutaAnterior')
def rutaAnterior():

    email = request.args.get('email')
    userName = request.args.get('name')
    currentRoute = eval(request.args.get('rutas'))
    

    data = complementos.obtenerJson(userName)
        
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
    storage = determinarEspacio(userName)
    return render_template('dashboard.html', email=email, name=userName, folders=folders, 
                           archivos=archivos, rutas = currentRoute, error=False, storage=storage)


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
    
    storage = determinarEspacio(userName)
    if(error != None):
        return render_template('dashboard.html', email=email, name=userName, folders=folders,
                            archivos=archivos, rutas = rutas, error=error,
                            nombreArchivo=nombreArchivo, contenido = contenido, storage=storage)
    else:
        return render_template('dashboard.html', email=email, name=userName, folders=folders,
                            archivos=archivos, rutas = rutas, errorEspacio=True, storage=storage)


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
    
    storage = determinarEspacio(userName)
    if(exito):
        return render_template('dashboard.html', email=email, name=userName, folders=folders, 
                            archivos=archivos, rutas = rutas, error=False, storage=storage)
    else:
        return render_template('dashboard.html', email=email, name=userName, folders=folders,
                            archivos=archivos, rutas = rutas, errorEspacio=True, storage=storage)

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
    
    storage = determinarEspacio(userName)
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
    
    storage = determinarEspacio(userName)
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
    
    storage = determinarEspacio(userName)
    return render_template('dashboard.html', email=email, name=userName, folders=folders, 
                           archivos=archivos, rutas = rutas, errorCarpeta=error, 
                           nombreCarpeta=nombreCarpeta, storage=storage)
    

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
    
    storage = determinarEspacio(userName)
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
        # Agregar el archivo al json
        complementos.eliminar_carpeta(data, rutas, userName)
        # Eliminar la ruta actual de la lista de rutas
        rutas.pop()
        # Agregar el archivo al json
        data = complementos.obtenerJson(userName)
        complementos.nuevaCarpeta(nombreCarpeta, userName, rutas, data)
        archivos, folders = complementos.buscar_carpeta(data, rutas)
    else:
        folders, archivos = complementos.obtenerFileSystem(data)
    
    storage = determinarEspacio(userName)
    return render_template('dashboard.html', email=email, name=userName, folders=folders,
                            archivos=archivos, rutas = rutas, error=False, storage=storage)


def determinarEspacio(usuario):
    user = collection.find_one({"name": usuario})
    storage = user.get("storage", 0)
    return storage

if __name__ == '__main__':
    app.run()