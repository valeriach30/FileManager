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
            },
            {
              "name": "TEC",
              "type": "folder",
              "created_at": "2023-06-11",
              "updated": "2023-06-15",
              "user": "valeria",
              "files": []
            }
          ]
        }
      ]
    }
  ]
}
'''

import json

data = json.loads(existing_json)

ruta_carpeta = ['TEC', 'IO', 'TEC']
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

resultado = buscarContenido(data['files'], ruta_carpeta)

if resultado is not None:
    print("Carpeta encontrada:")
    print(resultado)
else:
    print("No se encontró la carpeta especificada.")
