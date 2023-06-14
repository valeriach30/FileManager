def obtener_rutas_carpetas(data, ruta_actual="", rutas_carpetas=[]):
    if "files" in data:
        for item in data["files"]:
            if item["type"] == "folder":
                nombre_carpeta = item["name"]
                nueva_ruta = f"{ruta_actual}/{nombre_carpeta}" if ruta_actual else nombre_carpeta
                rutas_carpetas.append(nueva_ruta)
                obtener_rutas_carpetas(item, nueva_ruta, rutas_carpetas)
    
    return rutas_carpetas

import json

# JSON proporcionado
json_data = '''{'files': [{'name': 'Shared', 'type': 'folder', 'created_at': '2023-06-11', 'updated': '2023-06-15', 'user': 'valeria', 'files': []}, {'name': 'Raiz', 'type': 'folder', 'created_at': '2023-06-11', 'updated': '2023-06-15', 'user': 'valeria', 'files': [{'name': 'notas.txt', 'type': 'archivo', 'size': '22 KB', 'created_at': '2023-06-09', 'updated': '14/06/2023', 'user': 'valeria', 'content': 'hacer tarea 1 y tarea2'}, {'name': 'TEC', 'type': 'folder', 'created_at': '2023-06-11', 'updated': '2023-06-15', 'user': 'valeria', 'files': [{'name': 'Horario.txt', 'type': 'archivo', 'size': '72 KB', 'created_at': '2023-06-09', 'updated': '14/06/2023', 'user': 'valeria', 'content': 'M-V 9:30 > Sistemas. M-V 5:00 > Calidad. K 9:30 > Seminario. K 5:00 > IO'}, {'name': 'New Note.txt', 'type': 'archivo', 'size': '41 KB', 'created_at': '2023-06-09', 'updated': '14/06/2023', 'user': 'valeria', 'content': 'Esta es una nueva nota! Puedo editarla :)'}, {'name': 'IO', 'type': 'folder', 'created_at': '12/06/2023', 'updated': '12/06/2023', 'user': 'valeria', 'files': [{'name': 'Tarea1.txt', 'type': 'archivo', 'size': '26 KB', 'created_at': '13/06/2023', 'updated': '14/06/2023', 'user': 'Valeria', 'content': 'Esta tarea es de modelaje.'}, {'name': 'Tarea2.txt', 'type': 'archivo', 'size': '26 KB', 'created_at': '14/06/2023', 'updated': '14/06/2023', 'user': 'Valeria', 'content': 'La tarea 2 es sobre x tema'}, {'name': 'Tareas', 'type': 'folder', 'created_at': '14/06/2023', 'updated': '14/06/2023', 'user': 'valeria', 'files': []}]}, {'name': 'NotasSeminario.txt', 'type': 'archivo', 'size': '34 KB', 'created_at': '2023-06-20', 'updated': '14/06/2023', 'user': 'Valeria', 'content': 'El ensayo 2 es para el 15 de junio'}, {'name': 'SO', 'type': 'folder', 'created_at': '12/06/2023', 'updated': '12/06/2023', 'user': 'valeria', 'files': [{'name': 'Proyectos', 'type': 'folder', 'created_at': '12/06/2023', 'updated': '12/06/2023', 'user': 'valeria', 'files': [{'name': 'Proyecto I.txt', 'type': 'archivo', 'size': '245 KB', 'created_at': '12/06/2023', 'updated': '14/06/2023', 'user': 'Valeria', 'content': 'Objetivos del proyecto • Aprender a desarrollar un esquema de cliente-servidor. • Conocer la comunicación por medio de sockets. • Desarrollar un programa donde se utilicen threads. • Poner en práctica la teoría del Planificador de CPU'}]}, {'name': 'Tareas', 'type': 'folder', 'created_at': '14/06/2023', 'updated': '14/06/2023', 'user': 'valeria', 'files': [{'name': 'Tarea 1 SO.txt', 'type': 'archivo', 'size': '36 KB', 'created_at': '14/06/2023', 'updated': '14/06/2023', 'user': 'Valeria', 'content': 'Hacer la pregunta 1, 2 y 3 del libro'}, {'name': 'Tarea2.txt', 'type': 'archivo', 'size': '45 KB', 'created_at': '14/06/2023', 'updated': '14/06/2023', 'user': 'Valeria', 'content': 'Realizar algoritmo FIFO, SJF, RR y otros mas.'}]}]}]}]}]}'''

# Parsear el JSON
data = json.loads(json_data)

# Obtener las rutas de carpetas
rutas_carpetas = obtener_rutas_carpetas(data)
rutas_carpetas.pop(0)
# Imprimir las rutas de carpetas
print(rutas_carpetas)

