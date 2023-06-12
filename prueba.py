import json

# JSON existente
existing_json = '''
{
  "files": [
    {
      "name": "Shared",
      "type": "folder",
      "created_at": "2023-06-11",
      "updated": "2023-06-15",
      "user": "valeria",
      "files": []
    },
    {
      "name": "Raiz",
      "type": "folder",
      "created_at": "2023-06-11",
      "updated": "2023-06-15",
      "user": "valeria",
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
              "name": "New Note.txt",
              "type": "archivo",
              "size": "7894 KB",
              "created_at": "2023-06-09",
              "updated": "2023-06-10",
              "user": "valeria",
              "content": "Esta es una nueva nota!"
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
  ]
}
'''

# Convierte el JSON en un objeto Python (diccionario)
data = json.loads(existing_json)

# Ruta de la carpeta donde se agregará el nuevo archivo
ruta_carpeta = "TEC"

# Función recursiva para buscar la carpeta correspondiente en la estructura de archivos
def buscar_carpeta(files, ruta_carpeta):
    for file in files:
        if file["name"] == ruta_carpeta and file["type"] == "folder":
            return file
        if file["type"] == "folder" and "files" in file:
            carpeta_encontrada = buscar_carpeta(file["files"], ruta_carpeta)
            if carpeta_encontrada is not None:
                return carpeta_encontrada
    return None

# Busca la carpeta correspondiente
carpeta = buscar_carpeta(data["files"], ruta_carpeta)

if carpeta is not None:
    # Crea el nuevo archivo a agregar
    nuevo_archivo = {
        "name": "NuevoArchivo.txt",
        "type": "archivo",
        "size": "100 KB",
        "created_at": "2023-06-20",
        "updated": "2023-06-21",
        "user": "valeria",
        "content": "Este es un nuevo archivo"
    }

    # Agrega el nuevo archivo a la carpeta encontrada
    carpeta["files"].append(nuevo_archivo)

    # Convierte el objeto Python de vuelta a JSON
    updated_json = json.dumps(data)

    # Imprime el JSON actualizado
    print(updated_json)
else:
    print("No se encontró la carpeta correspondiente.")