import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
texto = ""
contador = 1
puerto = int(sys.argv[1])
s.settimeout(0.1)
while (texto != "FIN"):
    texto = input(">")
    tContador = str(contador)
    mensaje = tContador+": "+texto
    contador += 1
    textoCodificado = mensaje.encode("utf8")
    s.sendto(textoCodificado, ("localhost", puerto)) 
    
    try:
        datagrama, origen = s.recvfrom(1024)
        recibido = datagrama.decode()
    except socket.timeout:
        print("ERROR. El datagrama de confirmación no llega")

print("Fin de la conexión") 