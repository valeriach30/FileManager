texto = "Hola, mundo!"
bytes_texto = texto.encode('utf-8')
tamaño_bytes = len(bytes_texto)

print(f"El texto ocupa {tamaño_bytes} bytes.")
