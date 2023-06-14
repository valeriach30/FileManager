texto = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequatLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat laboris nisi ut aliquip ex ea commodo consequat laboris nisi ut aliquip ex ea commodo consequat laboris nisi ut aliquip ex ea commodo consequat laboris nisi ut aliquip ex"
bytes_texto = texto.encode('utf-8')
tamaño_bytes = len(bytes_texto)

print(f"El texto ocupa {tamaño_bytes} bytes.")
