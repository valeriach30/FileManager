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
/*Funciones de copiado*/
function cargarArchivo() {
    document.getElementById("formCargarArchivo").style.display = "block";
}
function descargarArchivo() {
    document.getElementById("formDescargarArchivo").style.display = "block";
}
function copiarArchivo() {
    document.getElementById("formCopiarArchivo").style.display = "block";
}
function cargarCarpeta() {
    document.getElementById("formCargarCarpeta").style.display = "block";
}
function descargarCarpeta() {
    document.getElementById("formDescargarCarpeta").style.display = "block";
}
function copiarCarpeta() {
    document.getElementById("formCopiarCarpeta").style.display = "block";
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

// --------------------------- COPIAR CARPETA ---------------------------
function copiarCarpetaF(){
    // Obtener datos
    var emailElement = document.getElementById("email");  
    var emailValue = emailElement.innerHTML;
    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");
    var rutasArray = obtenerRutas();
    var selectElement = document.getElementById("carpetaSelect");
    var selectedValue = selectElement.value;

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('selectedValue', selectedValue);
    
    var url = '/copiarCarpeta?' + params.toString();
    window.location.href = url;
}

// --------------------------- CARGAR CARPETA ---------------------------
function cargarCarpetaF(){
    //Obtener datos
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;
    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");
    var fileElement = document.getElementById("archivo"); 
    //pregunta si hay archivo
    if (fileElement) {
        var lector = new FileReader();

        const archivo = fileElement.files[0];

        if (archivo) {
            const lector = new FileReader();

            lector.onload = function(e) {
                contenido = e.target.result;
                console.log('Contenido del archivo:', contenido);
                //var contenido = contenidoElement.value;
                var nombre = archivo.name; 
                nombre = nombre.split('.').slice(0, -1).join('.');
                var extension = archivo.type;
                var rutasArray = obtenerRutas();
                var ultimaRuta = rutasArray[rutasArray.length - 1];

                //Construir los parámetros de consulta
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
            };

            lector.readAsText(archivo);
  
        }

    } else {
        // No se seleccionó ningún archivo
        console.log("No se seleccionó ningún archivo.");
    }
  
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
// --------------------------- MOVER CARPETA ---------------------------
function moverCarpetaF(){
     // Obtener datos
     var emailElement = document.getElementById("email");
     var emailValue = emailElement.innerHTML;
     var userElement = document.getElementById("name");
     var userValue = userElement.getAttribute("data-value");
     var rutasArray = obtenerRutas();
     var selectElement = document.getElementById("carpetaSelect");
     var selectedValue = selectElement.value;
 
     // Construir los parámetros de consulta
     var params = new URLSearchParams();
     params.append('email', emailValue);
     params.append('name', userValue);
     params.append('rutas', rutasArray);
     params.append('selectedValue', selectedValue);
     
     var url = '/moverCarpeta?' + params.toString();
     window.location.href = url;
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
    document.getElementById("formCargarArchivo").style.display = "none";
    document.getElementById("formDescargarArchivo").style.display = "none";
    document.getElementById("formCopiarArchivo").style.display = "none";
    document.getElementById("formCargarCarpeta").style.display = "none";
    document.getElementById("formDescargarCarpeta").style.display = "none";
    document.getElementById("formCopiarCarpeta").style.display = "none";

}

function obtenerRutas(){
    var rutasElement = document.getElementById("rutas");
    var rutasValue = rutasElement.getAttribute("data-value");
    rutasValue = rutasValue.replace(/[\[\]']+/g, '');
    var rutasArray = rutasValue.split(",");
    console.log("XD\n");
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

function copiarArchivoF(){
    
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
    
    var selectElement = document.getElementById("carpetaSelect");
    var selectedValue = selectElement.value;


    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('nombre', nombre);
    params.append('contenido', contenido);
    params.append('extension', extension);
    params.append('selectedValue', selectedValue);
    
    var url = '/copiarArchivo?' + params.toString();
    window.location.href = url;
};
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

function sustitucionMovimiento(element){
    
    quitarPopUp(element);
    
    // Obtener datos
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;
    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");
    
    var rutasElement = document.getElementById("destino");
    var rutasValue = rutasElement.getAttribute("data-value");
    rutasValue = rutasValue.replace(/[\[\]']+/g, '');
    var destino = rutasValue.split(",");
    var rutasArray = obtenerRutas();
    

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('destino', destino);
    params.append('rutas', rutasArray);
    
    var url = '/sustituirMover?' + params.toString();
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