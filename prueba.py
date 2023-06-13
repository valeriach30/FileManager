import json

def eliminarArchivo(rutas, data, nombreArchivo, usuario):
    # Editar archivo
    newFiles = eliminarContenido(data["files"], rutas, nombreArchivo)

    if(len(rutas) != 1):
        for carpeta in data['files']:
            if(carpeta['name'] == rutas[-2]):
                carpeta['files'] = newFiles

    # Convierte el objeto Python de vuelta a JSON
    updated_json = json.dumps(data)

    # Actualiza el archivo local con el nuevo JSON
    nombreArchivo = usuario + '.json'
    with open(nombreArchivo, "w") as file:
        file.write(updated_json)

def eliminarContenido(files, ruta_carpeta, nombreArchivo):
    if len(ruta_carpeta) == 0:
        return None

    nombre_carpeta = ruta_carpeta[0]
    print("nombre carpeta> " + str(nombre_carpeta))
    for file in files:
        print(" file name> " + str(file['name']))
        if file["name"] == nombre_carpeta and file["type"] == "folder":
            if len(ruta_carpeta) == 1:
                # Se encontro la carpeta, ahora se buscara el archivo
                for archivo in file['files']:
                  print("archiov> " + str(archivo['name']))
                  if archivo["name"] == nombreArchivo and archivo["type"] == "archivo":
                      # Eliminar aca
                      file['files'].remove(archivo)
                      return files

            if "files" in file:
                carpeta_encontrada = eliminarContenido(file["files"], ruta_carpeta[1:], nombreArchivo)
                if carpeta_encontrada is not None:
                    return carpeta_encontrada
    return None

ruta_archivo = ["Raiz", "TEC"]
nombre_archivo = "Horario.txt"
directorio_json = '''{"files": [{"name": "Shared", "type": "folder", "created_at": "2023-06-11", "updated": "2023-06-15", "user": "valeria", "files": []}, {"name": "Raiz", "type": "folder", "created_at": "2023-06-11", "updated": "2023-06-15", "user": "valeria", "files": [{"name": "notas.txt", "type": "archivo", "size": "1565 KB", "created_at": "2023-06-09", "updated": "13/06/2023", "user": "valeria", "content": "hacer tarea 1 y tarea2"}, {"name": "TEC", "type": "folder", "created_at": "2023-06-11", "updated": "2023-06-15", "user": "valeria", "files": [{"name": "Horario.txt", "type": "archivo", "size": "564 KB", "created_at": "2023-06-09", "updated": "2023-06-10", "user": "valeria", "content": "M-V 9:30 > Sistemas. M-V 5:00 > Calidad. K 9:30 > Seminario"}, {"name": "New Note.txt", "type": "archivo", "size": "7894 KB", "created_at": "2023-06-09", "updated": "13/06/2023", "user": "valeria", "content": "Esta es una nueva nota! Puedo editarla :)"}, {"name": "IO", "type": "folder", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "valeria", "files": [{"name": "Tarea1.txt", "type": "archivo", "size": "950 KB", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "Valeria", "content": "La tarea 1 es de modelaje"}]}, {"name": "NotasSeminario.txt", "type": "archivo", "size": "50 KB", "created_at": "2023-06-20", "updated": "2023-06-25", "user": "Valeria", "content": "El ensayo 2 es para el 15 de junio"}, {"name": "SO", "type": "folder", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "valeria", "files": [{"name": "Proyectos", "type": "folder", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "valeria", "files": [{"name": "Proyecto I.txt", "type": "archivo", "size": "154 KB", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "Valeria", "content": "Objetivos del proyecto \u2022 Aprender a desarrollar un esquema de cliente-servidor. \u2022 Conocer la comunicaci\u00f3n por medio de sockets. \u2022 Desarrollar un programa donde se utilicen threads. \u2022 Poner en pr\u00e1ctica la teor\u00eda del Planificador de CPU"}]}, {"name": "IO", "type": "folder", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "valeria", "files": [{"name": "QUIZ1.txt", "type": "archivo", "size": "623 KB", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "Valeria", "content": "contenido del quiz1!"}, {"name": "QUIZ2.txt", "type": "archivo", "size": "904 KB", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "Valeria", "content": "XD"}, {"name": "QUIZ3.txt", "type": "archivo", "size": "883 KB", "created_at": "12/06/2023", "updated": "12/06/2023", "user": "Valeria", "content": "333"}, {"name": "QUIZ4.txt", "type": "archivo", "size": "375 KB", "created_at": "13/06/2023", "updated": "13/06/2023", "user": "Valeria", "content": "Este es el quiz 4"}]}, {"name": "Tarea1.txt", "type": "archivo", "size": "88 KB", "created_at": "13/06/2023", "updated": "13/06/2023", "user": "Valeria", "content": "Esta es la tarea 1 de so"}]}]}]}]}'''
data = json.loads(directorio_json)


directorio_actualizado = eliminarArchivo(ruta_archivo, data, nombre_archivo)
if directorio_actualizado is not None:
    print("Archivo eliminado correctamente.")
    print(directorio_actualizado)
else:
    print("No se encontró el archivo en la ruta especificada.")
