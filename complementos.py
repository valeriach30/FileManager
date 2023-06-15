import random
import json
from datetime import date
from pymongo import MongoClient
from flask import flash

# Conexion con la bd
client = MongoClient('mongodb+srv://Kdaniel06:Dani060401$@cluster0.t10iglg.mongodb.net/?retryWrites=true&w=majority')
db = client['Users']
collection = db['User']

# ---------------------- NUEVO ARCHIVO ----------------------

def nuevoArchivo(nombreArchivo, contenido, extension, usuario, rutas, data):
    nombreArchivo = nombreArchivo + '.txt'
    rutas = [ruta.strip().lstrip('/').strip() for ruta in rutas if ruta.strip()]
    rutas.pop(0)
    carpeta = buscarContenido(data["files"], rutas)
    
    # Determinar tamaño
    bytes_texto = contenido.encode('utf-8')
    sizeContenido = len(bytes_texto)
    
    # Determinar si hay un archivo con el mismo nombre dentro de la carpeta
    presente = archivoRepetido(carpeta, nombreArchivo)
    
    # Determinar si hay espacio para el archivo
    actualizado = actualizarEspacio(usuario, sizeContenido)
    if(actualizado):
        if carpeta is not None and not presente:
            size = str(sizeContenido) + ' KB'
            fecha_actual = date.today()
            fecha_actual = fecha_actual.strftime("%d/%m/%Y")
            nuevo_archivo = {
                "name": nombreArchivo,
                "type": "archivo",
                "size": size,  
                "created_at": fecha_actual,
                "updated": fecha_actual,  
                "user": usuario,
                "content": contenido
            }
            # Agrega el nuevo archivo a la carpeta encontrada
            carpeta["files"].append(nuevo_archivo)

            # Convierte el objeto Python de vuelta a JSON
            updated_json = json.dumps(data)

            # Actualiza el archivo local con el nuevo JSON
            nombreArchivo = usuario + '.json'
            with open(nombreArchivo, "w") as file:
                file.write(updated_json)
            return False
        else:
            return True
    else:
        return None

# Funcion que determina si dentro de una carpeta ya esta un archivo
def archivoRepetido(json_carpeta, nombre_archivo):
    files = json_carpeta["files"]
    for archivo in files:
        if archivo["name"] == nombre_archivo and archivo["type"] == "archivo":
            return True
    return False


# ---------------------- EDITAR ARCHIVO ----------------------

def editarArchivo(rutas, data, nombreArchivo, nuevoContenido, usuario):
    rutas = [ruta.strip().lstrip('/').strip() for ruta in rutas if ruta.strip()]
    rutas.pop(0)
    
    bytes_texto = nuevoContenido.encode('utf-8')
    sizeContenido = len(bytes_texto)
    

    # Editar archivo
    newFiles = cambiarContenido(data["files"], rutas, nombreArchivo, nuevoContenido, usuario)

    if(cambiarContenido != False):
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

        return True
    else:
        return False

def cambiarContenido(files, ruta_carpeta, nombreArchivo, nuevoContenido, usuario):
    if len(ruta_carpeta) == 0:
        return None

    nombre_carpeta = ruta_carpeta[0]

    for file in files:
        if file["name"] == nombre_carpeta and file["type"] == "folder":
            if len(ruta_carpeta) == 1:
                # Se encontro la carpeta, ahora se buscara el archivo
                for archivo in file['files']:
                  if archivo["name"] == nombreArchivo and archivo["type"] == "archivo":
                    
                    bytes_texto = nuevoContenido.encode('utf-8')
                    sizeContenido = len(bytes_texto)

                    # Restaurar espacio anterior
                    restaurarEspacio(usuario, int(archivo["size"][:-3]))

                    # Agregar espacio nuevo
                    actualizado = actualizarEspacio(usuario, sizeContenido)

                    if(actualizado):
                        size = str(sizeContenido) + ' KB'
                        
                        # Actualizar
                        archivo["content"] = nuevoContenido
                        archivo["size"] = size
                        fecha_actual = date.today()
                        fecha_actual = fecha_actual.strftime("%d/%m/%Y")
                        archivo["updated"] = fecha_actual

                        # Retornar archivos
                        return files
                    else:
                        return False

            if "files" in file:
                carpeta_encontrada = cambiarContenido(file["files"], ruta_carpeta[1:], nombreArchivo, nuevoContenido, usuario)
                if carpeta_encontrada is not None:
                    return carpeta_encontrada

    return None

# ---------------------- ELIMINAR ARCHIVO ----------------------

def eliminarArchivo(rutas, data, nombreArchivo, usuario):
    
    rutas = [ruta.strip().lstrip('/').strip() for ruta in rutas if ruta.strip()]
    rutas.pop(0)
    
    # Editar archivo
    newFiles = eliminarContenido(data["files"], rutas, nombreArchivo, usuario)
    
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

def eliminarContenido(files, ruta_carpeta, nombreArchivo, usuario):
    if len(ruta_carpeta) == 0:
        return None

    nombre_carpeta = ruta_carpeta[0]
    for file in files:
        if file["name"] == nombre_carpeta and file["type"] == "folder":
            if len(ruta_carpeta) == 1:
                # Se encontro la carpeta, ahora se buscara el archivo
                for archivo in file['files']:
                  if archivo["name"] == nombreArchivo and archivo["type"] == "archivo":
                      # Restaurar el espacio
                      restaurarEspacio(usuario, int(archivo["size"][:-3]))
                      # Eliminar aca
                      file['files'].remove(archivo)
                      return files

            if "files" in file:
                carpeta_encontrada = eliminarContenido(file["files"], ruta_carpeta[1:], nombreArchivo, usuario)
                if carpeta_encontrada is not None:
                    return carpeta_encontrada
    return None

# ---------------------- NUEVA CARPETA ----------------------

def nuevaCarpeta(nombreCarpeta, usuario, rutas, data):
    rutas = [ruta.strip().lstrip('/').strip() for ruta in rutas if ruta.strip()]
    rutas.pop(0)
    carpeta = buscarContenido(data["files"], rutas)
    
    # Determinar si hay una carpeta con el mismo nombre 
    if(carpeta is not None):
        presente = carpetaRepetida(carpeta, nombreCarpeta)
    else:
        presente = False
        
    if carpeta is not None and not presente:
        fecha_actual = date.today()
        fecha_actual = fecha_actual.strftime("%d/%m/%Y")
        carpetaNueva = {
            "name": nombreCarpeta,
            "type": "folder",
            "created_at": fecha_actual,
            "updated": fecha_actual,
            "user": "valeria",
            "files": []
        }
        # Agrega el nuevo archivo a la carpeta encontrada
        carpeta["files"].append(carpetaNueva)

        # Convierte el objeto Python de vuelta a JSON
        updated_json = json.dumps(data)

        # Actualiza el archivo local con el nuevo JSON
        nombreArchivo = usuario + '.json'
        with open(nombreArchivo, "w") as file:
            file.write(updated_json)
        return False
    else:
        return True

# Funcion que determina si dentro de una carpeta ya esta una carpeta con ese nombre
def carpetaRepetida(json_carpeta, nombre_carpeta):
    files = json_carpeta["files"]
    for archivo in files:
        if archivo["name"] == nombre_carpeta and archivo["type"] == "folder":
            return True
    return False
# ---------------------- ELIMINAR CARPETA ----------------------

def eliminar_carpeta(data, rutas, usuario):
    rutas = [ruta.strip().lstrip('/').strip() for ruta in rutas if ruta.strip()]
    rutas.pop(0)
    
    eliminar_directorio(data["files"], rutas)
    # Convierte el objeto Python de vuelta a JSON
    updated_json = json.dumps(data)

    # Actualiza el archivo local con el nuevo JSON
    nombreArchivo = usuario + '.json'
    with open(nombreArchivo, "w") as file:
        file.write(updated_json)

# Función recursiva para eliminar un directorio y sus archivos/subdirectorios
def eliminar_directorio(files, rutas_directorio):
    if len(rutas_directorio) == 0:
        return False
    
    ruta_directorio = rutas_directorio[0]

    for file in files:
        if file["name"] == ruta_directorio and file["type"] == "folder":
            if len(rutas_directorio) == 1:
                files.remove(file)
                return True
            else:
                return eliminar_directorio(file["files"], rutas_directorio[1:])
        elif file["type"] == "folder" and "files" in file:
            if eliminar_directorio(file["files"], rutas_directorio):
                return True
    return False


# ---------------------- BUSCAR CONTENIDO ----------------------

# Función recursiva para encontrar contenido de una carpeta
def buscarContenido(files, ruta_carpeta):
    if len(ruta_carpeta) == 0:
        return None

    nombre_carpeta = ruta_carpeta[0]

    for file in files:
        if file["name"] == nombre_carpeta and file["type"] == "folder":
            if len(ruta_carpeta) == 1:
                return file
            if "files" in file:
                carpeta_encontrada = buscarContenido(file["files"], ruta_carpeta[1:])
                if carpeta_encontrada is not None:
                    return carpeta_encontrada

    return None

# ---------------------- OBTENER JSON ----------------------
def obtenerJson(userName):
    # Cargar el JSON
    nombreArchivo = userName + '.json'
    with open(nombreArchivo) as json_file:
        data = json.load(json_file)
    return data

# ---------------------- BUSCAR CARPETA ----------------------
def buscar_carpeta(json_data, ruta_carpeta):
    
    ruta_carpeta = [ruta.strip().lstrip('/').strip() for ruta in ruta_carpeta if ruta.strip()]
    ruta_carpeta.pop(0)
    
    archivos_encontrados = []
    carpetas_encontradas = []

    def buscar_recursivo(data, ruta_actual):
        if len(ruta_actual) == 0:
            for item in data['files']:
                if item['type'] == 'archivo':
                    archivos_encontrados.append(item)
                elif item['type'] == 'folder':
                    carpetas_encontradas.append(item)
        else:
            nombre_carpeta = ruta_actual[0]
            for item in data['files']:
                if item['type'] == 'folder' and item['name'] == nombre_carpeta:
                    if len(ruta_actual) == 1:
                        for archivo in item['files']:
                            if archivo['type'] == 'archivo':
                                archivos_encontrados.append(archivo)
                        for carpeta in item['files']:
                            if carpeta['type'] == 'folder':
                                carpetas_encontradas.append(carpeta)
                    else:
                        buscar_recursivo(item, ruta_actual[1:])
                
    buscar_recursivo(json_data, ruta_carpeta)
    return archivos_encontrados, carpetas_encontradas

# ---------------------- MOVER CARPETA ----------------------
def moverCarpeta(data, usuario, rutas, destino):
    rutas = [ruta.strip().lstrip('/').strip() for ruta in rutas if ruta.strip()]
    rutas.pop(0)
    
    destino = destino.split("/")
    carpetaNueva = buscarContenido(data["files"], rutas)
    
    carpetaDestino = buscarContenido(data["files"], destino)
    
    # Agregar la carpeta en el destino
    
    # Determinar si hay una carpeta con el mismo nombre 
    if(carpetaDestino is not None):
        presente = carpetaRepetida(carpetaDestino, carpetaNueva["name"])
    else:
        presente = False
    
    if not presente:
        # Eliminar la carpeta de la direccion pasada
        eliminar_directorio(data["files"], rutas)

        # Agrega la carpeta al destino
        carpetaDestino["files"].append(carpetaNueva)

        # Convierte el objeto Python de vuelta a JSON
        updated_json = json.dumps(data)

        # Actualiza el archivo local con el nuevo JSON
        nombreArchivo = usuario + '.json'
        with open(nombreArchivo, "w") as file:
            file.write(updated_json)
        return False, None
    else:
        # Convierte el objeto Python de vuelta a JSON
        updated_json = json.dumps(data)

        # Actualiza el archivo local con el nuevo JSON
        nombreArchivo = usuario + '.json'
        with open(nombreArchivo, "w") as file:
            file.write(updated_json)

        return True, carpetaNueva


def moverSustituir(data, usuario, rutas, destino):
    rutas = [ruta.strip().lstrip('/').strip() for ruta in rutas if ruta.strip()]
    rutas.pop(0)
    
    if("/" in destino):
        destino = destino.split("/")
    else:
        lista = []
        lista.append(destino)
        destino = lista
    
    carpetaNueva = buscarContenido(data["files"], rutas)
    eliminar_directorio(data["files"], rutas)
    
    # Eliminar la carpeta repetida del destino
    destino.append(carpetaNueva["name"])
    respuesta = eliminar_directorio(data["files"], destino)
    
    # Agrega la carpeta al destino
    destino.pop()
    carpetaDestino = buscarContenido(data["files"], destino)
    carpetaDestino["files"].append(carpetaNueva)

    # Convierte el objeto Python de vuelta a JSON
    updated_json = json.dumps(data)

    # Actualiza el archivo local con el nuevo JSON
    nombreArchivo = usuario + '.json'
    with open(nombreArchivo, "w") as file:
        file.write(updated_json)

    
# ---------------------- OBTENER FILE SYSTEM ----------------------

# Obtener la estructura del usuario
def obtenerFileSystem(data):
    folders = []
    archivos = []

    # Obtener carpetas y archivos
    for item in data['files']:
        if item['type'] == 'folder':
            if(item not in folders):
                folders.append(item)
        elif item['type'] == 'archivo':
            if(item not in archivos):
                archivos.append(item)

    return folders, archivos


# ---------------------- OBTENER CARPETAS ----------------------
def obtenerCarpetas(data, ruta_actual="", rutas_carpetas=[]):
    if "files" in data:
        for item in data["files"]:
            if item["type"] == "folder":
                nombre_carpeta = item["name"]
                nueva_ruta = f"{ruta_actual}/{nombre_carpeta}" if ruta_actual else nombre_carpeta
                rutas_carpetas.append(nueva_ruta)
                obtenerCarpetas(item, nueva_ruta, rutas_carpetas)
    
    return rutas_carpetas


# ---------------------- FUNCIONES STORAGE ----------------------

def determinarEspacio(usuario):
    user = collection.find_one({"name": usuario})
    storage = user.get("storage", 0)
    return storage

def actualizarEspacio(usuario, sizeArchivo):
    # Determinar el espacio disponible del usuario
    espacio = determinarEspacio(usuario)
    
    # Ya no queda espacio
    if(sizeArchivo > espacio):
        return False
    else:
        espacio -= sizeArchivo
        user = collection.find_one({"name": usuario})
        user['storage'] = espacio
        # Actualiza el documento en la colección
        collection.update_one({"name": usuario}, {"$set": {"storage": espacio}})
        return True

def restaurarEspacio(usuario, sizeArchivo):
    # Determinar el espacio disponible del usuario
    espacio = determinarEspacio(usuario)
    
    # Restaurar espacio
    espacio += sizeArchivo
    
    # Actualizar en la bd
    user = collection.find_one({"name": usuario})
    user['storage'] = espacio
    collection.update_one({"name": usuario}, {"$set": {"storage": espacio}})
    