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

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    time.sleep(1)
    print("Nuevo cliente conectado desde %s, %d" % origen)
    continuar = True
    f = sd.makefile(encoding="utf8", newline="\n")
    # Bucle de atención al cliente conectado
    while continuar:
       # Primero recibir el mensaje con la longitud
        longitud = f.readline()

        if not longitud:
            f.close()
            sd.close()
            break

        tam = int(longitud)
       
        mensaje = f.read(tam)

        print(mensaje)

        # Tercero, darle la vuelta
        mensaje_reversa = mensaje[::-1]

        resp_bytes = bytes(mensaje_reversa, "utf8")
        cabecera = "%d\n" % len(resp_bytes)
        sd.sendall(bytes(cabecera, "utf8") + resp_bytes)
