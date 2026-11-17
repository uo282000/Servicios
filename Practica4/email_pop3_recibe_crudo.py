import socket
import ssl
import sys
import getpass
import email

# 1. Función para recibir y comprobar el código +OK
def RecvReply(sock):
    respuesta = sock.recv(1024)
    print("Servidor:", respuesta.decode("utf-8", errors="ignore").strip())
    if respuesta[:3] != b"+OK":
        print("Error en la respuesta del servidor POP3.")
        sys.exit()
    return respuesta

# 2. Configuración del servidor POP3 de Gmail
server = "pop.gmail.com"
port = 995

# 3. Pedir credenciales por teclado
username = input("Usuario (Gmail): ")
password = getpass.getpass("Contraseña de aplicación: ")

# 4. Crear socket TCP y envolverlo en SSL/TLS
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
context = ssl.create_default_context()
sc = context.wrap_socket(s, server_hostname=server)

# Leer el saludo inicial (+OK)
RecvReply(sc)

# 5. Autenticación con USER y PASS (estado AUTHORIZATION -> TRANSACTION)
sc.send(f"USER {username}\r\n".encode("utf-8"))
RecvReply(sc)

sc.send(f"PASS {password}\r\n".encode("utf-8"))
RecvReply(sc)

# 6. Consultar el número de mensajes disponibles con STAT
sc.send(b"STAT\r\n")
resp_stat = RecvReply(sc)

# La respuesta tiene formato: +OK NumMsg NumBytes
partes = resp_stat.split()
num_mensajes = int(partes[1])
print(f"Mensajes disponibles: {num_mensajes}")

if num_mensajes > 0:
    # 7. Leer el contenido completo del primer correo (hasta \r\n.\r\n)
    sc.send(b"RETR 1\r\n")
    datos_totales = b""
    while not datos_totales.endswith(b"\r\n.\r\n"):
        trozo = sc.recv(4096)
        if not trozo:
            break
        datos_totales += trozo

    if not datos_totales.startswith(b"+OK"):
        print("Error al descargar el mensaje 1.")
        sys.exit()

    # Quitamos la primera línea de estado (+OK ...) y el terminador final (\r\n.\r\n)
    _, cuerpo_crudo = datos_totales.split(b"\r\n", 1)
    cuerpo_crudo = cuerpo_crudo[:-5]

    # 8. Extraer cabeceras Subject y From e imprimirlas
    msg = email.message_from_bytes(cuerpo_crudo)
    print("\n--- Cabeceras del primer correo ---")
    print("From:", msg.get("From"))
    print("Subject:", msg.get("Subject"))

# Cerrar sesión POP3 (estado UPDATE)
sc.send(b"QUIT\r\n")
RecvReply(sc)
sc.close()