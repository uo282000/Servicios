import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

puerto = int(sys.argv[1])

s.connect(("localhost", puerto))

lista = [b"Juan", b"Pedro", b"Luis"]

texto = b"Hola me llamo guamelo \r\n" #lo hacemos de tipo bytes con la b

f = s.makefile(encoding="utf8", newline="\r\n")

for i in lista:
    texto = b"Hola me llamo "+ i +b"\r\n"
    s.sendall(texto)

for i in lista:
    recibido = f.readline()
    #recibido = str(recibido, "utf-8")
    print(repr(recibido))

s.close()


    