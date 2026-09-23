import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
texto = ""
contador = 1
while (texto != "FIN"):
    texto = input(">")
    tContador = str(contador)
    mensaje = tContador+": "+texto
    contador += 1
    textoCodificado = mensaje.encode("utf8")
    s.sendto(textoCodificado, ("localhost", int(sys.argv[1])))    

print("Fin de la conexión")