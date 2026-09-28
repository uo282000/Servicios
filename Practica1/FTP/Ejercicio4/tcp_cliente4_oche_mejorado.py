import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

puerto = int(sys.argv[1])

s.connect(("localhost", puerto))

lista = [b"Juan", b"Pedro", b"Luis"]

texto = b"Hola me llamo guamelo \r\n" #lo hacemos de tipo bytes con la b

def recibe_mensaje(socket):
    buffer = []
    while True:
        mensaje = socket.recv(1)
        if not mensaje:
            return None # cliente desconectado
        buffer.append(mensaje)

        if len(buffer) >= 2 and buffer[-2] == b"\r" and buffer[-1] == b"\n":
            break
    return b"".join(buffer)

for i in lista:
    texto = b"Hola me llamo "+ i +b"\r\n"
    s.sendall(texto)

for i in lista:
    recibido = recibe_mensaje(s)
    recibido = str(recibido, "utf-8")
    print(repr(recibido))

s.close()


    