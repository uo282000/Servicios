import smtplib
import getpass
import email.message
import email.utils

# 1. Configuración del servidor y credenciales
server = "smtp.gmail.com"
port = 587

username = input("Usuario (Gmail): ")
password = getpass.getpass("Contraseña de aplicación: ")
toaddr = input("Destinatario: ")

# 2. Construcción del mensaje con email.message (sin añadir el punto final)
mensaje = email.message.EmailMessage()
mensaje['To'] = toaddr
mensaje['From'] = username
mensaje['Subject'] = "Prueba Ejercicio 12 con smtplib"
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content("Correo enviado usando la librería smtplib de Python.")

# 3. Instanciar SMTP, activar depuración, negociar TLS y autenticar
s = smtplib.SMTP(server, port)
s.set_debuglevel(1)
s.starttls()
s.login(username, password)

# 4. Enviar el mensaje en bytes y cerrar conexión
s.sendmail(username, toaddr, mensaje.as_bytes())
s.quit()