import socket
import sys
import random

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

puerto = int(sys.argv[1])
s.bind(("", puerto))
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while (True):
    datagrama, origen = s.recvfrom(1024) #recibe una dupla
    mensajeCliente = datagrama.decode("utf-8")
    print("Hemos recibido esto: ", mensajeCliente)
    print("Desde el origen: ", origen)
    if (mensajeCliente == "HOLA"):
        confirmacion = "HOLA: " + str(origen[0])
        confirmacionCodificado = confirmacion.encode("utf-8")
        
    elif (mensajeCliente == "BUSCANDO HOLA"):
        confirmacion = "IMPLEMENTO HOLA"
        confirmacionCodificado = confirmacion.encode("utf-8")

    s.sendto(confirmacionCodificado, origen) #admite la dupa entera
    

