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
function compartirCarpeta() {
    document.getElementById("formCompartirCarpeta").style.display = "block";
}
function compartirArchivo() {
    document.getElementById("formCompartirArchivo").style.display = "block";
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

    var carpetasRutas = dropdown();

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('ruta', ultimaRuta);
    params.append('nombre', nombre);
    params.append('contenido', contenido);
    params.append('extension', extension);
    params.append('dropdown', carpetasRutas);

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
    var carpetasRutas = dropdown();

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('ruta', ultimaRuta);
    params.append('nuevoContenido', nuevoContenido);
    params.append('nombreArch', nombre);
    params.append('dropdown', carpetasRutas);

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
    var carpetasRutas = dropdown();

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('ruta', ultimaRuta);
    params.append('nombre', nombre);
    params.append('dropdown', carpetasRutas);

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
    var carpetasRutas = dropdown();

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('dropdown', carpetasRutas);

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
    var selectElement = document.getElementById("carpetaSelectCopiar");
    var selectedValue = selectElement.value;
    var carpetasRutas = dropdown();

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('selectedValue', selectedValue);
    params.append('dropdown', carpetasRutas);

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
    var carpetasRutas = dropdown();

    //pregunta si hay archivo
    if (fileElement) {
        var lector = new FileReader();

        const archivo = fileElement.files[0];

        if (archivo) {
            const lector = new FileReader();

            lector.onload = function(e) {
                contenido = e.target.result;
                //console.log('Contenido del archivo:', contenido);
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
                params.append('dropdown', carpetasRutas);

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
//prueba
function selectFolder(e) {
    for (var i = 0; i < e.target.files.length; i++) {
       var s = e.target.files[i].name + '\n';
       s += e.target.files[i].size + ' Bytes\n';
       s += e.target.files[i].type;
       alert(s);
    }
 }

// --------------------------- CARGAR ARCHIVO ---------------------------
function cargarArchivoF(){
    //Obtener datos
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;
    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");
    var fileElement = document.getElementById("archivo"); 
    var carpetasRutas = dropdown();

    //pregunta si hay archivo
    if (fileElement) {
        var lector = new FileReader();

        const archivo = fileElement.files[0];

        if (archivo) {
            const lector = new FileReader();

            lector.onload = function(e) {
                contenido = e.target.result;
                //console.log('Contenido del archivo:', contenido);
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
                params.append('dropdown', carpetasRutas);

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
    var carpetasRutas = dropdown();

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('selectedValue', selectedValue);
    params.append('dropdown', carpetasRutas);

    var url = '/moverCarpeta?' + params.toString();
    window.location.href = url;
}

// --------------------------- MOVER ARCHIVO ---------------------------
function moverArchivoF(){
    // Obtener datos
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;
    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");
    var rutasArray = obtenerRutas();
    var selectElement = document.getElementById("archivoSelect");
    var selectedValue = selectElement.value;
    var nombre = document.getElementById("nombre");
    nombre = nombre.innerText;
    var carpetasRutas = dropdown();

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('selectedValue', selectedValue);
    params.append('nombre', nombre);
    params.append('dropdown', carpetasRutas);

    var url = '/moverArchivo?' + params.toString();
    window.location.href = url;
}

// --------------------------- COMPARTIR CARPETA ---------------------------
function compartirCarpetaF(){
    // Obtener datos
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;
    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");
    var rutasArray = obtenerRutas();
    var nombreUsuario = document.getElementById("nombreShareCar").value;
    var carpetasRutas = dropdown();

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('usuario', nombreUsuario);
    params.append('dropdown', carpetasRutas);

    var url = '/compartirCarpeta?' + params.toString();
    window.location.href = url;
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
    document.getElementById("formCompartirCarpeta").style.display = "none";
    document.getElementById("formCompartirArchivo").style.display = "none";

}

function obtenerRutas(){
    var rutasElement = document.getElementById("rutas");
    
    var rutasValue = rutasElement.getAttribute("data-value");
    
    rutasValue = rutasValue.replace(/[\[\]']+/g, '');
    var rutasArray = rutasValue.split(",");
    //alert(rutasArray);
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
    var carpetasRutas = dropdown();

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('nombreAr', nombre);
    params.append('dropdown', carpetasRutas);

    var url = '/eliminarArchivo?' + params.toString();
    window.location.href = url;
}
// --------------------------- COPIAR ARCHIVO ---------------------------
/*hay que arreglarlo*/
function copiarArchivoF(){
    
    // Obtener datos
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;

    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");

    var contenido = document.getElementById("fileContent");
    contenido = contenido.innerText;
    var nombre = document.getElementById("nombre");
    nombre = nombre.innerText;
    var extension = document.getElementById("extension").value;
    
    var selectElement = document.getElementById("copiarArchivoSelect");
    var selectedValue = selectElement.value;

    var rutasArray = obtenerRutas();
    var ultimaRuta = rutasArray[rutasArray.length - 1];
    var carpetasRutas = dropdown();

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('nombre', nombre);
    params.append('contenido', contenido);
    params.append('extension', extension);
    params.append('selectedValue', selectedValue);
    params.append('dropdown', carpetasRutas);

    var url = '/copiarArchivo?' + params.toString();
    window.location.href = url;
};
// --------------------------- DESCARGAR ARCHIVO ---------------------------
function descargarArchivoF() {
    var nombreArchivo = document.getElementById("nombre");
    nombreArchivo = nombreArchivo.innerText;
    var contenidoArchivo = document.getElementById("fileContent");
    contenidoArchivo = contenidoArchivo.innerText;

    console.log(contenidoArchivo,nombreArchivo);
  
    var enlace = document.getElementById("download-link");
    enlace.href = "data:text/plain;charset=utf-8," + encodeURIComponent(contenidoArchivo);
    enlace.download = nombreArchivo;
    enlace.click();
  }

function descargarCarpetaF2() {
    var zip = new JSZip();

    var userElement = document.getElementById("name");
    var userName = userElement.getAttribute("data-value");
    var rutas = obtenerRutas();

    
    //var rutasSplit = rutas.split(',').map(ruta => ruta.trim());
    //rutasSplit = rutas.map(ruta => ruta.replace('/', ' /'));
    data = obtenerJson(userName);
    
    var folderName = 'mi_carpeta'; // Nombre de la carpeta que deseas descargar
    zip.file(folderName + '/archivo2.txt', 'Contenido del archivo 2');
    recorrerArchivos(data.files, zip);
    // ...
  
    // Genera el archivo ZIP
    zip.generateAsync({ type: 'blob' }).then(function(content) {
        // Descargar archivo comprimido
        var a = document.createElement('a');
        var url = URL.createObjectURL(content);
        a.href = url;
        a.download = folderName + '.zip';
        a.click();
        URL.revokeObjectURL(url);
      });
  }
  
  function agregarArchivo(zip, rutaArchivo, contenidoArchivo) {
    zip.file(rutaArchivo, contenidoArchivo);
  }
  
function recorrerArchivos(files, zip, ruta = '') {
    files.forEach(function(file) {
      if (file.type !== 'folder') {
        var contenido = file.content;
        var nombreArchivo = ruta + file.name;
        zip.file(nombreArchivo, contenido);
      } else if (file.type === 'folder' && file.files) {
        var nuevaRuta = ruta + file.name + '/';
        recorrerArchivos(file.files, zip, nuevaRuta);
      }
    });
  }

function buscarContenido(files, ruta_carpeta) {
    if (ruta_carpeta.length === 0) {
      return null;
    }
  
    var nombre_carpeta = ruta_carpeta[0];
  
    for (var i = 0; i < files.length; i++) {
      var file = files[i];
      if (file.name === nombre_carpeta && file.type === "folder") {
        if (ruta_carpeta.length === 1) {
          return file;
        }
        if ("files" in file) {
          var carpeta_encontrada = buscarContenido(file.files, ruta_carpeta.slice(1));
          if (carpeta_encontrada !== null) {
            return carpeta_encontrada;
          }
        }
      }
    }
  
    return null;
  }
  

// ---------------------- OBTENER JSON ----------------------
function descargarCarpetaF() {
    var userElement = document.getElementById("name");
    var userName = userElement.getAttribute("data-value");
    nombreArchivo = userName+".json";
    var rutas = obtenerRutas();
    fetch('/obtenerArchivo', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ userName: userName , rutas: rutas})
    })
    .then(response => response.json())
    .then(data => {
      var zip = new JSZip();

      
      
      var folderName = 'mi_carpeta'; // Nombre de la carpeta que deseas descargar
      zip.file(folderName + '/archivo2.txt', 'Contenido del archivo 2');
      recorrerArchivos(data.files, zip);
      // ...
    
      // Genera el archivo ZIP
      zip.generateAsync({ type: 'blob' }).then(function(content) {
          // Descargar archivo comprimido
          var a = document.createElement('a');
          var url = URL.createObjectURL(content);
          a.href = url;
          a.download = folderName + '.zip';
          a.click();
          URL.revokeObjectURL(url);
        });

        console.log(data);
        return data;
    })
    .catch(error => {
      console.error('Error al obtener el archivo:', error);
    });
    return null;
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
    var carpetasRutas = dropdown();
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
    params.append('dropdown', carpetasRutas);

    var url = '/sustituirArchivo?' + params.toString();
    window.location.href = url;
};

function cancelarArchivo(element){
    quitarPopUp(element);
};

// --------------------------- COMPARTIR ARCHIVO ---------------------------

function compartirArchivoF(){
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;
    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");
    var rutasArray = obtenerRutas();
    var ultimaRuta = rutasArray[rutasArray.length - 1];
    var nombre = document.getElementById("nombre");
    nombre = nombre.innerText;
    var nombreUsuario = document.getElementById("nombreShareAr").value;
    var carpetasRutas = dropdown();

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('nombreArchivo', nombre);
    params.append('nombreUsuario', nombreUsuario);
    params.append('dropdown', carpetasRutas);

    var url = '/compartirArchivo?' + params.toString();
    window.location.href = url;
}

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
    var carpetasRutas = dropdown();

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('rutas', rutasArray);
    params.append('nombre', nombre);
    params.append('dropdown', carpetasRutas);

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
    var carpetasRutas = dropdown();
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
    params.append('dropdown', carpetasRutas);

    var url = '/sustituirMover?' + params.toString();
    window.location.href = url;
}

function sustitucionArchivoMov(element){
    
    quitarPopUp(element);
    
    // Obtener datos
    var emailElement = document.getElementById("email");
    var emailValue = emailElement.innerHTML;
    var userElement = document.getElementById("name");
    var userValue = userElement.getAttribute("data-value");
    var nombreArchivo = document.getElementById("nombreArchivo");
    var nombreArchivoValue = nombreArchivo.getAttribute("data-value");
    var carpetasRutas = dropdown();
    var rutasElement = document.getElementById("destino");
    var destino = rutasElement.getAttribute("data-value");
    var rutasArray = obtenerRutas();
    

    // Construir los parámetros de consulta
    var params = new URLSearchParams();
    params.append('email', emailValue);
    params.append('name', userValue);
    params.append('destino', destino);
    params.append('rutas', rutasArray);
    params.append('nombre', nombreArchivoValue);
    params.append('dropdown', carpetasRutas);
    
    var url = '/sustituirArchivoMover?' + params.toString();
    window.location.href = url;
}

// Obtener carpetas  del dropdown
function dropdown(){
    var carpetasRutasElement = document.getElementById("carpetasRutas");
    var carpetasRutasValue = carpetasRutasElement.getAttribute("data-value");
    return carpetasRutasValue
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