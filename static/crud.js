function agregarArchivo() {
    document.getElementById("myForm").style.display = "block";
}
function agregarCarpeta() {
    document.getElementById("formCarpeta").style.display = "block";
}
function eliminarCarpeta() {
    document.getElementById("formElimCarpeta").style.display = "block";
}
function enviarForm(){
    
    // Obtener datos
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;

    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");

    var contenido = document.getElementById("contenido").value;
    var nombre = document.getElementById("nombre1").value;
    var extension = document.getElementById("extension").value;
    var rutasElement = document.getElementById("rutas");
    
    // Obtener la ruta actual
    var rutasValue = rutasElement.getAttribute("data-value");
    rutasValue = rutasValue.replace(/[\[\]']+/g, '');
    var rutasArray = rutasValue.split(",");
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

function enviarCarpeta(){
    // Obtener datos
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;
    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");
    var rutasElement = document.getElementById("rutas");
    var nombre = document.getElementById("nombre2").value;
    
    // Obtener la ruta actual
    var rutasValue = rutasElement.getAttribute("data-value");
    rutasValue = rutasValue.replace(/[\[\]']+/g, '');
    var rutasArray = rutasValue.split(",");
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
function enviarEliminar(){
    // Obtener datos
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;
    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");
    var rutasElement = document.getElementById("rutas");
    
    // Obtener la ruta actual
    var rutasValue = rutasElement.getAttribute("data-value");
    rutasValue = rutasValue.replace(/[\[\]']+/g, '');
    var rutasArray = rutasValue.split(",");
    var ultimaRuta = rutasArray[rutasArray.length - 1];
    
    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('ruta', ultimaRuta);
    
    var url = '/eliminarCarpeta?' + params.toString();
    window.location.href = url;
}

function closeForm() {
    document.getElementById("myForm").style.display = "none";
    document.getElementById("formCarpeta").style.display = "none";
    document.getElementById("formElimCarpeta").style.display = "none";
}