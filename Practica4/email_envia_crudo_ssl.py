import socket
import sys
import ssl
import base64
import getpass
import email.message
import email.utils

def RecvReply(sock, codigo):
    respuesta = sock.recv(1024)
    print("Servidor:", respuesta.decode("utf-8", errors="ignore").strip())
    if respuesta[:3] != codigo:
        print(f"Error: se esperaba {codigo} y se recibió {respuesta[:3]}")
        sys.exit()

# Configuración del servidor de Gmail
server = "smtp.gmail.com"
port = 587

# Solicitar credenciales (usa la contraseña de aplicación de Google)
username = input("Usuario: ")
password = getpass.getpass("Contraseña: ")

fromaddr = username
toaddr = input("Destinatario: ")
subject = "Prueba Ejercicio 11 SMTP con STARTTLS"
data = "Correo enviado desde Python usando sockets crudos, TLS y AUTH LOGIN."

# Construcción del mensaje estándar
mensaje = email.message.EmailMessage()
mensaje['To'] = toaddr
mensaje['From'] = fromaddr
mensaje['Subject'] = subject
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content(data)

binario = mensaje.as_bytes() + b"\r\n.\r\n"

# 1. Conexión TCP inicial (en claro)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
RecvReply(s, b"220")

# 2. Saludo extendido EHLO e inicio de STARTTLS
s.send(b"EHLO is-21\r\n")
RecvReply(s, b"250")

s.send(b"STARTTLS\r\n")
RecvReply(s, b"220")

# 3. Envolver el socket en un canal seguro SSL/TLS
context = ssl.create_default_context()
sc = context.wrap_socket(s, server_hostname=server)

# A partir de aquí todo va cifrado a través de 'sc'
# Conviene repetir EHLO tras negociar TLS
sc.send(b"EHLO is-21\r\n")
RecvReply(sc, b"250")

# 4. Autenticación AUTH LOGIN en Base64
sc.send(b"AUTH LOGIN\r\n")
RecvReply(sc, b"334")

sc.send(base64.b64encode(username.encode("ascii")) + b"\r\n")
RecvReply(sc, b"334")

sc.send(base64.b64encode(password.encode("utf8")) + b"\r\n")
RecvReply(sc, b"235")

# 5. Envío del correo por el canal cifrado
sc.send(f"MAIL From: <{fromaddr}>\r\n".encode("utf-8"))
RecvReply(sc, b"250")

sc.send(f"RCPT To: <{toaddr}>\r\n".encode("utf-8"))
RecvReply(sc, b"250")

sc.send(b"DATA\r\n")
RecvReply(sc, b"354")

sc.send(binario)
RecvReply(sc, b"250")

sc.send(b"QUIT\r\n")
RecvReply(sc, b"221")

sc.close()