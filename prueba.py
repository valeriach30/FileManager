import json
from datetime import date

def cambiarContenido(files, ruta_carpeta, nombreArchivo, nuevoContenido):
    if len(ruta_carpeta) == 0:
        return None

    nombre_carpeta = ruta_carpeta[0]

    for file in files:
        if file["name"] == nombre_carpeta and file["type"] == "folder":
            if len(ruta_carpeta) == 1:
                # Se encontro la carpeta, ahora se buscara el archivo
                for archivo in file['files']:
                  if archivo["name"] == nombreArchivo and archivo["type"] == "archivo":
                      archivo["content"] = nuevoContenido
                      fecha_actual = date.today()
                      fecha_actual = fecha_actual.strftime("%d/%m/%Y")
                      archivo["updated"] = fecha_actual
                      return files

            if "files" in file:
                carpeta_encontrada = cambiarContenido(file["files"], ruta_carpeta[1:], nombreArchivo, nuevoContenido)
                if carpeta_encontrada is not None:
                    return carpeta_encontrada

    return None

def editarArchivo(nombreCarpeta, rutas, data, nombreArchivo, nuevoContenido):
    newFiles = cambiarContenido(data["files"], rutas, nombreArchivo, nuevoContenido)
    data["files"] = newFiles
    return data
    


existing_json = '''{"files": [{"name": "Shared", "type": "folder", "created_at": "2023-06-11", "updated": "2023-06-15", "user": "valeria", "files": []}, {"name": "Raiz", "type": "folder", "created_at": "2023-06-11", "updated": "2023-06-15", "user": "valeria", "files": [{"name": "notas.txt", "type": "archivo", "size": "1565 KB", "created_at": "2023-06-09", "updated": "2023-06-10", "user": "valeria", "content": "Recuerda priorizar las tareas y marcarlas como completadas una vez que hayas terminado. Mucho exito en tus tareas!"}, {"name": "TEC", "type": "folder", "created_at": "2023-06-11", "updated": "2023-06-15", "user": "valeria", "files": [{"name": "Horario.txt", "type": "archivo", "size": "564 KB", "created_at": "2023-06-09", "updated": "2023-06-10", "user": "valeria", "content": "M-V 9:30 > Sistemas. M-V 5:00 > Calidad. K 9:30 > Seminario"}, {"name": "New Note.txt", "type": "archivo", "size": "7894 KB", "created_at": "2023-06-09", "updated": "2023-06-10", "user": "valeria", "content": "Esta es una nueva nota!"}, {"name": "IO", "type": "folder", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "valeria", "files": [{"name": "Tarea1", "type": "archivo", "size": "950 KB", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "Valeria", "content": "La tarea 1 es de modelaje"}]}, {"name": "NotasSeminario", "type": "archivo", "size": "50 KB", "created_at": "2023-06-20", "updated": "2023-06-25", "user": "Valeria", "content": "El ensayo 2 es para el 15 de junio"}, {"name": "SO", "type": "folder", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "valeria", "files": [{"name": "Proyectos", "type": "folder", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "valeria", "files": [{"name": "Proyecto I", "type": "archivo", "size": "154 KB", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "Valeria", "content": "Objetivos del proyecto \u2022 Aprender a desarrollar un esquema de cliente-servidor. \u2022 Conocer la comunicaci\u00f3n por medio de sockets. \u2022 Desarrollar un programa donde se utilicen threads. \u2022 Poner en pr\u00e1ctica la teor\u00eda del Planificador de CPU"}]}, {"name": "IO", "type": "folder", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "valeria", "files": [{"name": "QUIZ1", "type": "archivo", "size": "623 KB", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "Valeria", "content": "contenido del quiz1!"}, {"name": "QUIZ2", "type": "archivo", "size": "904 KB", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "Valeria", "content": "XD"}, {"name": "QUIZ3", "type": "archivo", "size": "883 KB", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "Valeria", "content": "333"}]}, {"name": "Tarea1", "type": "archivo", "size": "955 KB", "created_at": "13/06/2023", "updated": "13/06/2023", "user": "Valeria", "content": "Primera tarea de so"}, {"name": "Tarea2", "type": "archivo", "size": "59 KB", "created_at": "13/06/2023", "updated": "13/06/2023", "user": "Valeria", "content": "tarea 2 de so"}]}]}]}]}'''
data = json.loads(existing_json)

rutas = ["Raiz","TEC", "SO", "IO"]
nuevo_contenido = "PRUEBAAA NUEVO CONTENIDOOO"
nombre_archivo = "QUIZ1"
print(editarArchivo(rutas[-1], rutas, data, nombre_archivo, nuevo_contenido))
