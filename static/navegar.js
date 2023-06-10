$(document).ready(function() {

    // ------------------------------------- ARCHIVOS -------------------------------------
    $("#archivo").click(function(event) {
        var archivoElement = document.getElementById("archivo");
        var valor = archivoElement.dataset.value;
        var values = Object.values(valor);

        alert(valor)
        alert(values)
        // Obtener el contenido del archivo (puedes hacer una llamada AJAX aquí para obtenerlo)
        var fileContent = "Este es el contenido del archivo."; // Aquí debes reemplazar con tu lógica de obtención del contenido del archivo
        
        // Mostrar el contenido del archivo en el pop-up
        $("#fileContent").text(fileContent);
        $("#sizeP").text(valor.size);
        
        $("#popup1").fadeIn();
        
    });

    

    // ------------------------------------- CARPETAS -------------------------------------
    
    $("#carpeta").click(function(event) {
        
        // Evita que el enlace realice la acción predeterminada (navegar a una nueva página)
        event.preventDefault();
  
        // Actualiza el contenido de la carpeta "Sistemas Operativos"
        // Puedes hacer una llamada AJAX aquí para obtener los archivos y actualizar la tabla
        
        // Actualiza el breadcrumb para seguir la ruta del file system
        var breadcrumb = $(".breadcrumb");
        var sistemasOperativos = $("<li class='breadcrumb-item'><a href='#'>Sistemas Operativos</a></li>");
        
        // Limpia el breadcrumb existente antes de agregar el nuevo elemento
        breadcrumb.empty();
        
        // Agrega el nuevo elemento al breadcrumb
        breadcrumb.append("<li class='breadcrumb-item'><a href='#'>home</a></li>");
        breadcrumb.append(sistemasOperativos);

        // Limpia el contenido de la tabla
        $(".drive-items-table-wrapper").empty();

        // Cargar el nuevo contenido de la tabla FALTA IMPLEMENTARLO

        /*
        // Simulación de llamada AJAX para obtener el nuevo contenido de la tabla
        var nuevosItems = obtenerNuevosItems(); // Función que obtiene los nuevos elementos de la tabla

        // Agrega los nuevos elementos a la tabla
        $(".drive-items-table-wrapper").append(nuevosItems);
        });

        // Función para obtener los nuevos elementos de la tabla (simulación de llamada AJAX)
        function obtenerNuevosItems() {
            // Aquí puedes hacer una llamada AJAX real para obtener los nuevos elementos de la tabla
            // En este ejemplo, simplemente creamos elementos de ejemplo manualmente

            var nuevosItems = '';

            // Agrega los elementos de ejemplo a la variable nuevosItems
            nuevosItems += '<tr>';
            nuevosItems += '<td class="type"><i class="fa fa-file-text-o text-primary"></i></td>';
            nuevosItems += '<td class="name truncate"><a href="#">Nuevo archivo.txt</a></td>';
            nuevosItems += '<td class="date">Jun 9, 2023</td>';
            nuevosItems += '<td class="size">25 KB</td>';
            nuevosItems += '</tr>';

            nuevosItems += '<tr>';
            nuevosItems += '<td class="type"><i class="fa fa-folder text-primary"></i></td>';
            nuevosItems += '<td class="name truncate"><a href="#">Nueva carpeta</a></td>';
            nuevosItems += '<td class="date">Jun 9, 2023</td>';
            nuevosItems += '<td class="size">--</td>';
            nuevosItems += '</tr>';

            // Retorna los nuevos elementos
            return nuevosItems;
        }*/
    });
});
  