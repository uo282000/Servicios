import socket
 
s = socket.socket()
s.connect(("localhost", 23))
respuesta = s.recv(1024)


def mostar_hex(datos):
    cadena_respuesta = []
    for byte in datos:
        cadena_respuesta.append(hex(byte))
    
    for i in cadena_respuesta:
        print(i)

mostar_hex(respuesta)
