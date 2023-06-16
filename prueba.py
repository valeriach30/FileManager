string = "Raiz/Tec"
string= string.split("/")
lista = []
for i in string:
    x = ''.join([' / ', i])
    lista.append(x)
print(lista)