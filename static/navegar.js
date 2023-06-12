$(document).ready(function() {

    // ------------------------------------- ARCHIVOS -------------------------------------
    $(".archivo").click(function(event) {
        var archivoId = event.target.id;
        var archivoElement = document.getElementById(archivoId);
        var valor = archivoElement.dataset.value;
        var jsonStringFixed = valor.replace(/'/g, '"');
        var jsonObj = JSON.parse(jsonStringFixed);
        
        // Mostrar el contenido del archivo en el pop-up
        $("#nombre").text(jsonObj.name);
        $("#fileContent").text(jsonObj.content);
        $("#sizeP").text(jsonObj.size);
        $("#fechaCP").text(jsonObj.created_at);
        $("#fechaMP").text(jsonObj.updated);
        $("#usuarioP").text(jsonObj.user);
        
        $("#popup1").fadeIn();
        
    });

    

    // ------------------------------------- CARPETAS -------------------------------------
    
    $(".carpeta").click(function(event) {
        // Obtener datos
        var emailElement = document.getElementById("email");
        var emailValue = emailElement.innerHTML;

        var userElement = document.getElementById("name");
        var userValue = userElement.getAttribute("data-value");

        var rutaElement = document.getElementById("rutas");
        var rutaValue = rutaElement.getAttribute("data-value");

        // Obtener carpeta
        var carpetaId = event.target.id;
        var archivoElement = document.getElementById(carpetaId);
        var valor = archivoElement.dataset.value;
        var jsonStringFixed = valor.replace(/'/g, '"');
        var carpetaJson = JSON.parse(jsonStringFixed);
        
        // Construir los parámetros de consulta
        var params = new URLSearchParams();
        params.append('carpeta', carpetaJson.name);
        params.append('email', emailValue);
        params.append('name', userValue);
        params.append('ruta', rutaValue);

        var url = '/subcarpeta?' + params.toString();
        window.location.href = url;
    });

    // -------------------------------------- EVENT LISTENERS --------------------------------------
    // Add event listener to the button
    $("#addButton").click(function() {
        $("#popup").modal();
    });
});
  