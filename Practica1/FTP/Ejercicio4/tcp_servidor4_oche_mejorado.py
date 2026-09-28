import sys
import socket
import time

# Creación del socket de escucha
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# Podríamos haber omitido los parámetros, pues por defecto `socket()` en python
# crea un socket de tipo TCP

puerto = int(sys.argv[1])
# Asignarle puerto
s.bind(("localhost", puerto))

# Ponerlo en modo pasivo
s.listen(5)  # Máximo de clientes en la cola de espera al accept()

def recibe_mensaje(socket):
    buffer = []
    while True:
        mensaje = socket.recv(1)
        if not mensaje:
            return None # cliente desconectado
        buffer.append(mensaje)

        if len(buffer) >= 2 and buffer[-2] == b"\r" and buffer[-1] == b"\n":
            break
    return b"".join(buffer)
    

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    time.sleep(1)
    print("Nuevo cliente conectado desde %s, %d" % origen)
    continuar = True
    # Bucle de atención al cliente conectado
    while continuar:
       # Primero recibir el mensaje del cliente
        mensaje = recibe_mensaje(sd)
        #mensaje = sd.recv(1)  # Nunca enviará más de 80 bytes, aunque tal vez sí menos
        if not mensaje:
            sd.close()
            break
        mensaje = str(mensaje, "utf8") # Convertir los bytes a caracteres

        print(mensaje)

        # Segundo, quitarle el "fin de línea" que son sus 2 últimos caracteres
        linea = mensaje[:-2]  # slice desde el principio hasta el final -2

        # Tercero, darle la vuelta
        linea = linea[::-1]

        # Finalmente, enviarle la respuesta con un fin de línea añadido
        # Observa la transformación en bytes para enviarlo
        sd.sendall(bytes(linea+"\r\n", "utf8"))
