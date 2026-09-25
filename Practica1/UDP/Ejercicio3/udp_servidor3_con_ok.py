import socket
import sys
import random

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

puerto = int(sys.argv[1])
s.bind(("", puerto))
confirmacion = "OK"

while (True):
    datagrama, origen = s.recvfrom(1024) #recibe una dupla
    numero = random.randint(0,1)
    if (numero == 1): 
        print("Hemos recibido esto: ", datagrama.decode("utf-8"))
        print("Desde el origen: ", origen)
        confirmacionCodificado = confirmacion.encode("utf-8")
        s.sendto(confirmacionCodificado, ("localhost", origen[1]))
    else:
        print("Simulando paquete perdido")

