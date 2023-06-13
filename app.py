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
    
    if email:
        
        # Cargar el JSON
        data = complementos.obtenerJson(userName)
        
        # Obtener carpetas y archivos del usuario
        folders, archivos = complementos.obtenerFileSystem(data)
        
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
    data = complementos.obtenerJson(userName)

    # Obtener nombre de la carpeta actual
    carpeta = request.args.get('carpeta')

    # Actualizar ruta
    currentRoute.append(" / " + carpeta) 
    
    # Obtener archivos y subcarpetas
    archivos, folders = complementos.buscar_carpeta(data, currentRoute)
    
    # Redirigir
    return render_template('dashboard.html', email=email, name=userName, 
                               folders=folders, archivos=archivos, rutas = currentRoute)


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
    return render_template('dashboard.html', email=email, name=userName, 
                               folders=folders, archivos=archivos, rutas = currentRoute)


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
        complementos.nuevoArchivo(nombreArchivo, contenido, extension, userName, rutas, data)
        archivos, folders = complementos.buscar_carpeta(data, rutas)
    else:
        folders, archivos = complementos.obtenerFileSystem(data)
    
    return render_template('dashboard.html', email=email, name=userName, 
                               folders=folders, archivos=archivos, rutas = rutas)
    


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
        complementos.editarArchivo(rutas, data, nombreArchivo, nuevoContenido, userName)    
        archivos, folders = complementos.buscar_carpeta(data, rutas)
    else:
        folders, archivos = complementos.obtenerFileSystem(data)
    
    return render_template('dashboard.html', email=email, name=userName, 
                               folders=folders, archivos=archivos, rutas = rutas)

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
        complementos.nuevaCarpeta(nombreCarpeta, userName, rutas, data)
        archivos, folders = complementos.buscar_carpeta(data, rutas)
    else:
        folders, archivos = complementos.obtenerFileSystem(data)
    
    return render_template('dashboard.html', email=email, name=userName, 
                               folders=folders, archivos=archivos, rutas = rutas)
    

# ---------------------- ELIMINAR CARPETA ----------------------

@app.route('/eliminarCarpeta')
def eliminarCarpeta():
    userName = request.args.get('name')
    email = request.args.get('email')
    rutas = request.args.get('rutas')
    rutas = [ruta.strip() for ruta in rutas.split(',')]
    rutas = [ruta.replace('/', ' /') for ruta in rutas]
    carpeta = request.args.get('ruta') 
    data = complementos.obtenerJson(userName)

    if(len(rutas) != 1):
        # Agregar el archivo al json
        complementos.eliminar_carpeta(data, rutas, userName)
        # Eliminar la ruta actual de la lista de rutas
        rutas.pop()
        carpeta = rutas[-1]
        archivos, folders = complementos.buscar_carpeta(data, rutas)
    else:
        folders, archivos = complementos.obtenerFileSystem(data)
    
    return render_template('dashboard.html', email=email, name=userName, 
                               folders=folders, archivos=archivos, rutas = rutas)



if __name__ == '__main__':
    app.run()
