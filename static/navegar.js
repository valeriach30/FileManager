$(document).ready(function() {

    // Captura el evento de clic en el enlace de "Sistemas Operativos"
    $("#sistemas-operativos").click(function(event) {
        
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
    });
  });
  