from flask import Flask, render_template, request, session, redirect
from pymongo import MongoClient


client = MongoClient('mongodb+srv://Kdaniel06:Dani060401$@cluster0.t10iglg.mongodb.net/?retryWrites=true&w=majority')
db = client['Users']
collection = db['User']

app = Flask(__name__)
app.secret_key = 'testing'

@app.route('/')
def home():
    # Página de inicio
    return render_template('index.html')

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
            return render_template('login.html', error='Credenciales inválidas')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        # Usuario autenticado, mostrar dashboard
        return render_template('dashboard.html', email=session['email'], name=session['name'])
    else:
        # Usuario no autenticado, redirigir al inicio de sesión
        return redirect('/login')


if __name__ == '__main__':
    print("Hola a todos")
    app.run()
