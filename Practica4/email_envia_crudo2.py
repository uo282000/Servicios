import socket
import sys
import email.message
import email.utils

def RecvReply(sock, codigo):
    respuesta = sock.recv(1024)
    print("Servidor:", respuesta.decode("utf-8", errors="ignore").strip())
    if respuesta[:3] != codigo:
        print(f"Error: se esperaba {codigo} y se recibió {respuesta[:3]}")
        sys.exit()

# Variables de configuración
server = "relay.uniovi.es"
port = 25
fromaddr = "uo282000@uniovi.es"
toaddr = "uo282000@uniovi.es"
subject = "Prueba Ejercicio 8 con estándar RFC-5322"
data = "Hola, este correo está construido con email.message y tiene tildes: áéíóú."

# Construcción del mensaje cumpliendo el estándar
mensaje = email.message.EmailMessage()
mensaje['To'] = toaddr
mensaje['From'] = fromaddr
mensaje['Subject'] = subject
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content(data)

#Apartado opcional Apartado 3 ejercicio9
with open("logoatc.gif", "rb") as f:
    gif = f.read()
mensaje.add_attachment(gif, "image", "gif", filename="atc.gif")

# Convertimos a bytes y añadimos el terminador SMTP obligatorio en crudo
binario = mensaje.as_bytes() + b"\r\n.\r\n"

# Conexión TCP y diálogo SMTP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))

RecvReply(s, b"220")

s.send(b"HELO is-21\r\n")
RecvReply(s, b"250")

s.send(f"MAIL From: <{fromaddr}>\r\n".encode("utf-8"))
RecvReply(s, b"250")

s.send(f"RCPT To: <{toaddr}>\r\n".encode("utf-8"))
RecvReply(s, b"250")

s.send(b"DATA\r\n")
RecvReply(s, b"354")

# Enviamos el mensaje codificado
s.send(binario)
RecvReply(s, b"250")

s.send(b"QUIT\r\n")
RecvReply(s, b"221")

s.close()