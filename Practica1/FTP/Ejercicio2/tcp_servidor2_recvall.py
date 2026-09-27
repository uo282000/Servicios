import sys
import socket

# Creación del socket de escucha
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# Podríamos haber omitido los parámetros, pues por defecto `socket()` en python
# crea un socket de tipo TCP
sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

puerto = int(sys.argv[1])
# Asignarle puerto
s.bind(("localhost", puerto))

# Ponerlo en modo pasivo
s.listen(5)  # Máximo de clientes en la cola de espera al accept()

def recvall(socket, bytesSolicitados):
    partes = []
    recibidos = int(0)

    while recibidos < bytesSolicitados:
        faltan = bytesSolicitados - recibidos
        mensaje = socket.recv(faltan)

        if not mensaje:
            return None #el cliente de desconecto antes de enviar todo
        
        partes.append(mensaje)
        recibidos += len(mensaje)
    return b"".join(partes) #lo unimos como unico mensaje de bytes

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)
    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
        datos = recvall(sd, 5)
        datos = datos.decode("ascii")  # Pasar los bytes a caracteres
                # En este ejemplo se asume que el texto recibido es ascii puro
        if datos=="":  # Si no se reciben datos, es que el cliente cerró el socket
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif datos=="FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            print("Recibido mensaje: %s" % datos)