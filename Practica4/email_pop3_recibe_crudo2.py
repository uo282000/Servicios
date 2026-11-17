import socket
import ssl
import sys
import getpass
import email

def RecvReply(sock):
    respuesta = sock.recv(1024)
    print("Servidor:", respuesta.decode("utf-8", errors="ignore").strip())
    if respuesta[:3] != b"+OK":
        print("Error en la respuesta del servidor POP3.")
        sys.exit()
    return respuesta

server = "pop.gmail.com"
port = 995

username = input("Usuario (Gmail): ")
password = getpass.getpass("Contraseña de aplicación: ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
context = ssl.create_default_context()
sc = context.wrap_socket(s, server_hostname=server)

RecvReply(sc)

sc.send(f"USER {username}\r\n".encode("utf-8"))
RecvReply(sc)

sc.send(f"PASS {password}\r\n".encode("utf-8"))
RecvReply(sc)

sc.send(b"STAT\r\n")
resp_stat = RecvReply(sc)

partes = resp_stat.split()
num_mensajes = int(partes[1])
print(f"Total de mensajes disponibles: {num_mensajes}\n")

# Iterar sobre todos los mensajes disponibles (del 1 al num_mensajes)
for i in range(1, num_mensajes + 1):
    sc.send(f"RETR {i}\r\n".encode("utf-8"))
    datos_totales = b""
    while not datos_totales.endswith(b"\r\n.\r\n"):
        trozo = sc.recv(4096)
        if not trozo:
            break
        datos_totales += trozo

    if not datos_totales.startswith(b"+OK"):
        print(f"Error al descargar el mensaje {i}.")
        sys.exit()

    _, cuerpo_crudo = datos_totales.split(b"\r\n", 1)
    cuerpo_crudo = cuerpo_crudo[:-5]

    msg = email.message_from_bytes(cuerpo_crudo)
    print(f"--- Mensaje {i} ---")
    print("From:", msg.get("From"))
    print("Subject:", msg.get("Subject"))

sc.send(b"QUIT\r\n")
RecvReply(sc)
sc.close()