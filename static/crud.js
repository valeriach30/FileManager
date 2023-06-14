// --------------------------- ABRIR POP UPS ---------------------------
function agregarArchivo() {
    document.getElementById("myForm").style.display = "block";
}
function agregarCarpeta() {
    document.getElementById("formCarpeta").style.display = "block";
}
function eliminarCarpeta() {
    document.getElementById("formElimCarpeta").style.display = "block";
}
function editarArchivo() {
    document.getElementById("formEditarArchivo").style.display = "block";
}
function moverCarpeta() {
    document.getElementById("formMoverCarpeta").style.display = "block";
}
function moverArchivo() {
    document.getElementById("formMoverArchivo").style.display = "block";
}

// --------------------------- CREAR ARCHIVO ---------------------------
function enviarForm(){
    
    // Obtener datos
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;

    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");

    var contenido = document.getElementById("contenido").value;
    var nombre = document.getElementById("nombre1").value;
    var extension = document.getElementById("extension").value;
    
    var rutasArray = obtenerRutas();
    var ultimaRuta = rutasArray[rutasArray.length - 1];

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('ruta', ultimaRuta);
    params.append('nombre', nombre);
    params.append('contenido', contenido);
    params.append('extension', extension);
    
    var url = '/crearArchivo?' + params.toString();
    window.location.href = url;
}

// --------------------------- UPDATE ARCHIVO ---------------------------
function updateArchivo(){
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;
    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");
    var nuevoContenido = document.getElementById("nuevoContenido").value;
    var rutasArray = obtenerRutas();
    var ultimaRuta = rutasArray[rutasArray.length - 1];
    var nombre = document.getElementById("nombre");
    nombre = nombre.innerText;

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('ruta', ultimaRuta);
    params.append('nuevoContenido', nuevoContenido);
    params.append('nombreArch', nombre);

    var url = '/editarArchivo?' + params.toString();
    window.location.href = url;
}

// --------------------------- AGREGAR CARPETA ---------------------------
function enviarCarpeta(){
    // Obtener datos
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;
    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");
    var nombre = document.getElementById("nombre2").value;
    
    var rutasArray = obtenerRutas();
    var ultimaRuta = rutasArray[rutasArray.length - 1];
    
    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('ruta', ultimaRuta);
    params.append('nombre', nombre);
    
    var url = '/crearCarpeta?' + params.toString();
    window.location.href = url;
}

// --------------------------- ELIMINAR CARPETA ---------------------------
function enviarEliminar(){
    // Obtener datos
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;
    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");
    
    var rutasArray = obtenerRutas();
    var ultimaRuta = rutasArray[rutasArray.length - 1];
    
    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    
    var url = '/eliminarCarpeta?' + params.toString();
    window.location.href = url;
}

// --------------------------- MOVER CARPETA ---------------------------
function moverCarpetaF(){
    alert("MOVER CARPETA")
}

// --------------------------- MOVER ARCHIVO ---------------------------
function moverArchivoF(){
    alert("MOVER ARCHIVO")
}

// --------------------------- CLOSE FORM ---------------------------
function closeForm() {
    document.getElementById("myForm").style.display = "none";
    document.getElementById("formCarpeta").style.display = "none";
    document.getElementById("formElimCarpeta").style.display = "none";
    document.getElementById("formEditarArchivo").style.display = "none";
    document.getElementById("formMoverCarpeta").style.display = "none";
    document.getElementById("formMoverArchivo").style.display = "none";
}

function obtenerRutas(){
    var rutasElement = document.getElementById("rutas");
    var rutasValue = rutasElement.getAttribute("data-value");
    rutasValue = rutasValue.replace(/[\[\]']+/g, '');
    var rutasArray = rutasValue.split(",");
    return rutasArray
}

// --------------------------- ELIMINAR ARCHIVO ---------------------------

function eliminarArchivo(){
    // Obtener datos
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;
    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");    
    var rutasArray = obtenerRutas();
    var nombre = document.getElementById("nombre");
    nombre = nombre.innerText;

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('nombreAr', nombre);
    
    var url = '/eliminarArchivo?' + params.toString();
    window.location.href = url;
}

// --------------------------- ARCHIVO REPETIDO ---------------------------

function sustituirArchivo(element){
    quitarPopUp(element);
    
    // Obtener datos
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;

    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");

    var contenido = document.getElementById("contenido2");
    contenido = contenido.getAttribute("data-value");
    var nombre = document.getElementById("nombreArchivo");
    nombre = nombre.getAttribute("data-value");
    var extension = document.getElementById("extension").value;
    
    var rutasArray = obtenerRutas();
    var ultimaRuta = rutasArray[rutasArray.length - 1];

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('nombre', nombre);
    params.append('contenido', contenido);
    params.append('extension', extension);
    
    var url = '/sustituirArchivo?' + params.toString();
    window.location.href = url;
};

function cancelarArchivo(element){
    quitarPopUp(element);
};

// --------------------------- CARPETA REPETIDA ---------------------------

function sustituirCarpeta(element){
    quitarPopUp(element);
    
    // Obtener datos
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;
    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");
    var nombre = document.getElementById("nombreCarpeta");
    nombre = nombre.getAttribute("data-value");
    
    var rutasArray = obtenerRutas();
    var ultimaRuta = rutasArray[rutasArray.length - 1];
    
    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('nombre', nombre);
    
    var url = '/sustituirCarpeta?' + params.toString();
    window.location.href = url;
}
function cancelarCarpeta(element){
    quitarPopUp(element);
};
function quitarPopUp(element){
    $(element).parents('.dialog-ovelay').find('.dialog').removeClass('zoomIn').addClass('zoomOut');
    $(element).parents('.dialog-ovelay').fadeOut(function () {
        $(element).remove();
    });
}