import socket
import sys

# 1. Función para recibir y comprobar el código de respuesta SMTP
def RecvReply(sock, codigo):
    respuesta = sock.recv(1024)
    print("Servidor:", respuesta.decode("utf-8", errors="ignore").strip())
    if respuesta[:3] != codigo:
        print(f"Error: se esperaba {codigo} y se recibió {respuesta[:3]}")
        sys.exit()

# 2. Variables de configuración
server = "relay.uniovi.es"
port = 25
fromaddr = "uo282000@uniovi.es"
toaddr = "uo282000@uniovi.es"
subject = "Prueba SMTP en crudo"
data = "Hola, este es un correo enviado directamente por sockets."

# 3. Conexión TCP con el servidor SMTP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))

# Saludo inicial del servidor (código 220)
RecvReply(s, b"220")

# 4. Diálogo SMTP paso a paso
s.send(b"HELO is-21\r\n")
RecvReply(s, b"250")

s.send(f"MAIL From: <{fromaddr}>\r\n".encode("utf-8"))
RecvReply(s, b"250")

s.send(f"RCPT To: <{toaddr}>\r\n".encode("utf-8"))
RecvReply(s, b"250")

s.send(b"DATA\r\n")
RecvReply(s, b"354")

# Cuerpo del mensaje con el formato del guion
message = """To: %s\r
From: %s\r
Subject: %s\r\n\r
%s\r
.\r
""" % (toaddr, fromaddr, subject, data)

s.send(message.encode("utf-8"))
RecvReply(s, b"250")

s.send(b"QUIT\r\n")
RecvReply(s, b"221")

s.close()