import json

def buscar_carpeta(json_data, nombre_carpeta):
    archivos_encontrados = []
    carpetas_encontradas = []

    def buscar_recursivo(data):
        for item in data['files']:
            if item['type'] == 'folder' and item['name'] == nombre_carpeta:
                for archivo in item['files']:
                    if archivo['type'] == 'archivo':
                        archivos_encontrados.append(archivo['name'])
                for carpeta in item['files']:
                    if carpeta['type'] == 'folder':
                        carpetas_encontradas.append(carpeta['name'])
            elif item['type'] == 'folder':
                buscar_recursivo(item)

    buscar_recursivo(json_data)
    return archivos_encontrados, carpetas_encontradas
json_string = '''
{
    "files": [
      {
        "name": "notas.txt",
        "type": "archivo",
        "size": "10 KB",
        "created_at": "2023-06-09",
        "updated": "2023-06-10",
        "user": "valeria",
        "content": "Recuerda priorizar las tareas y marcarlas como completadas una vez que hayas terminado. Mucho exito en tus tareas!"
      },
      {
        "name": "TEC",
        "type": "folder",
        "created_at": "2023-06-11",
        "updated": "2023-06-15",
        "user": "valeria",
        "files": [
        {
            "name": "Horario.txt",
            "type": "archivo",
            "size": "10 KB",
            "created_at": "2023-06-09",
            "updated": "2023-06-10",
            "user": "valeria",
            "content": "M-V 9:30 > Sistemas. M-V 5:00 > Calidad. K 9:30 > Seminario"
        },
        {
            "name": "IO.txt",
            "type": "archivo",
            "size": "10 KB",
            "created_at": "2023-06-09",
            "updated": "2023-06-10",
            "user": "valeria",
            "content": "XDDDDDDDDDDDDDDD"
        },
        {
            "name": "so",
            "type": "folder",
            "created_at": "2023-06-11",
            "updated": "2023-06-15",
            "user": "valeria",
            "files": []
        }
        ]
      }
    ]
}'''

# Convertir la cadena JSON en un objeto Python
json_data = json.loads(json_string)

# Llamar a la función para buscar la carpeta
nombre_carpeta = 'TEC'
archivos_encontrados, carpetas_encontradas = buscar_carpeta(json_data, nombre_carpeta)

# Imprimir los resultados
print("Archivos encontrados:", archivos_encontrados)
print("Carpetas encontradas:", carpetas_encontradas)