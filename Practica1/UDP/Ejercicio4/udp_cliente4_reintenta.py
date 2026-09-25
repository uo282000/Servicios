import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
texto = ""
contador = 1
puerto = int(sys.argv[1])
timeout = 0.1
s.settimeout(timeout)
while ((texto != "FIN") & (timeout < 2)):
    texto = input(">")
    tContador = str(contador)
    mensaje = tContador+": "+texto
    contador += 1
    textoCodificado = mensaje.encode("utf8")
    s.sendto(textoCodificado, ("localhost", puerto)) 
    
    try:
        datagrama, origen = s.recvfrom(1024)
        recibido = datagrama.decode()
        print(recibido)
    except socket.timeout:
        timeout *= 2
        s.settimeout(timeout)
        print("ERROR. El datagrama de confirmación no llega")

print("Puede que el servidor esté caído. Inténtelo más tarde")
print("Fin de la conexión")