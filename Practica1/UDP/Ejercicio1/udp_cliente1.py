import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
texto = ""
while (texto != "FIN"):
    texto = input(">")
    textoCodificado = texto.encode("utf8")
    s.sendto(textoCodificado, ("localhost", int(sys.argv[1])))    

print("Fin de la conexión")