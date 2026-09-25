import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
texto = ""
contador = 1
puerto = int(sys.argv[1])
timeout = 0.1
s.settimeout(timeout)
#s.connect(("localhost", 1234)) no se usa al usar broadcast
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

def mensajes2(origen):

    while ((texto != "FIN") & (timeout < 2)):
        texto = input(">")
        tContador = str(contador)
        mensaje = tContador+": "+texto
        contador += 1
        textoCodificado = mensaje.encode("utf8")
        s.send(textoCodificado) 
        
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

inicio = "BUSCANDO HOLA"
inicioCodificado = inicio.encode()
s.sendto(inicioCodificado, ("192.168.1.255", 12345)) #es la dirección de broadcast de la máquina linux

def mensajes(datosServidor):
    
    mensaje = "HOLA"
    textoCodificado = mensaje.encode("utf8")
    s.connect((datosServidor[0], datosServidor[1]))
    s.send(textoCodificado) 
    
    try:
        datagrama = s.recv(1024)
        recibido = datagrama.decode()
        print(recibido)
    except socket.timeout:
        timeout *= 2
        s.settimeout(timeout)
        print("ERROR. El datagrama de confirmación no llega")

primeraIP = None
while (True):
    try: 
        datagrama, origen = s.recvfrom(1024)
        if primeraIP == None:
            primeraIP = origen
        print("Nos ha respondido: ", origen[0])
        
    except socket.timeout:
        if primeraIP != None:
            mensajes(primeraIP)
        break


