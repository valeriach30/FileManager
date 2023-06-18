def obtener_tamanio_carpeta(json_data):
    if json_data["type"] != "folder":
        raise ValueError("El JSON proporcionado no representa una carpeta")

    tamanio_total = 0

    # Recorrer los archivos de la carpeta
    for archivo in json_data["files"]:
        if archivo["type"] == "archivo":
            # Obtener el tamaño del archivo y sumarlo al tamaño total
            tamanio_archivo = sizeAux(archivo)
            tamanio_total += tamanio_archivo
        elif archivo["type"] == "folder":
            # Obtener el tamaño de la subcarpeta de manera recursiva
            tamanio_subcarpeta = obtener_tamanio_carpeta(archivo)
            tamanio_total += tamanio_subcarpeta

    return tamanio_total


def sizeAux(archivo):
    # Extraer el tamaño del archivo del JSON
    size_str = archivo["size"]
    size_parts = size_str.split(" ")
    size = int(size_parts[0])
    return size

json_data = {
    "name": "Tareas",
    "type": "folder",
    "created_at": "14/06/2023",
    "updated": "14/06/2023",
    "user": "valeria",
    "files": [
        {
            "name": "dddd.txt",
            "type": "archivo",
            "size": "3 KB",
            "created_at": "14/06/2023",
            "updated": "14/06/2023",
            "user": "Valeria",
            "content": "ddd"
        },
        {
            "name": "subcarpeta",
            "type": "folder",
            "created_at": "14/06/2023",
            "updated": "14/06/2023",
            "user": "valeria",
            "files": [
                {
                    "name": "archivo1.txt",
                    "type": "archivo",
                    "size": "2 KB",
                    "created_at": "14/06/2023",
                    "updated": "14/06/2023",
                    "user": "Valeria",
                    "content": "contenido archivo1"
                },
                {
                    "name": "archivo2.txt",
                    "type": "archivo",
                    "size": "500 KB",
                    "created_at": "14/06/2023",
                    "updated": "14/06/2023",
                    "user": "Valeria",
                    "content": "contenido archivo2"
                }
            ]
        }
    ]
}

tamanio = obtener_tamanio_carpeta(json_data)
print("El tamaño total de la carpeta es:", tamanio, "bytes")
