import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

puerto = int(sys.argv[1])

s.connect(("localhost", puerto))

lista = ["Juan", "Pedro", "Luis"]

f = s.makefile(encoding="utf8", newline="\n")

for i in lista:
    mensaje = "Hola me llamo " + i
    longitud  = "%d\n" % len(bytes(mensaje, "utf8"))  # Pasamos a ASCII la longitud en bytes
                                                  #e incluimos el delimitador
    s.sendall(bytes(longitud + mensaje, "utf8"))      # Enviamos la concatenación

for i in lista:
    recibido = f.readline()

    tam = int(recibido)
    recibido = f.read(tam)
    print(repr(recibido))

s.close()


    