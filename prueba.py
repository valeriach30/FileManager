import json

# JSON existente
existing_json = '''
{
  "files": [
    {
      "name": "notas.txt",
      "type": "archivo",
      "size": "1565 KB",
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
          "size": "564 KB",
          "created_at": "2023-06-09",
          "updated": "2023-06-10",
          "user": "valeria",
          "content": "M-V 9:30 > Sistemas. M-V 5:00 > Calidad. K 9:30 > Seminario"
        },
        {
          "name": "IO",
          "type": "folder",
          "created_at": "2023-06-11",
          "updated": "2023-06-15",
          "user": "valeria",
          "files": [
            {
              "name": "Tareas",
              "type": "folder",
              "created_at": "2023-03-10",
              "updated": "2023-05-15",
              "user": "valeria",
              "files": []
            },
            {
              "name": "Quiz 1.txt",
              "type": "archivo",
              "size": "1000 KB",
              "created_at": "2023-06-09",
              "updated": "2023-06-10",
              "user": "valeria",
              "content": "Respuesta 1> A. Respuesta 2> B. Respuesta 3> C"
            }
          ]
        }
      ]
    }
  ]
}
'''

# Convierte el JSON en un objeto Python (diccionario)
data = json.loads(existing_json)

# Ruta del directorio a eliminar
ruta_directorio = "IO"

# Función recursiva para eliminar un directorio y sus archivos/subdirectorios
def eliminar_directorio(files, ruta_directorio):
    for file in files:
        if file["name"] == ruta_directorio and file["type"] == "folder":
            files.remove(file)
            return True
        if file["type"] == "folder" and "files" in file:
            if eliminar_directorio(file["files"], ruta_directorio):
                return True
    return False

# Elimina el directorio y sus archivos/subdirectorios
if eliminar_directorio(data["files"], ruta_directorio):
    # Convierte el objeto Python de vuelta a JSON
    updated_json = json.dumps(data)

    # Imprime el JSON actualizado
    print(updated_json)
else:
    print("No se encontró el directorio correspondiente.")
