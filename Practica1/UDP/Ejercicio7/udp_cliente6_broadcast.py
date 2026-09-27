import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
texto = ""
contador = 1
broadcast = str("172.18.255.255") #broadcast de la subred pruebas
#puerto = int(sys.argv[1])
puerto = int(8080)
timeout = 0.1
s.settimeout(timeout)
#s.connect(("localhost", 1234)) no se usa al usar broadcast
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

inicio = "BUSCANDO HOLA"
inicioCodificado = inicio.encode()
s.sendto(inicioCodificado, (broadcast, puerto)) 

def mensajes(datosServidor):
    mensaje = "HOLA"
    textoCodificado = mensaje.encode("utf8")
    s.connect(datosServidor) #recibe una tupla
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
print("Finalizada la conexion")

