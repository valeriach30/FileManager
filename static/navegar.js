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
        
        // Obtener carpeta
        var carpetaId = event.target.id;
        var archivoElement = document.getElementById(carpetaId);
        var valor = archivoElement.dataset.value;
        var jsonStringFixed = valor.replace(/'/g, '"');
        var carpetaJson = JSON.parse(jsonStringFixed);
        window.location = '/subcarpeta?carpeta=' + carpetaJson.name;

    });
});
  