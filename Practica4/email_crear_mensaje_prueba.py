import email.message, email.policy, email.utils

#codigo copiado del documento de la práctica
mensaje = email.message.EmailMessage()
mensaje['To'] = 'Desti Natario <destinatario@example.com>'
mensaje['From'] = 'Remi Tente <remitente@example.com>'
mensaje['Subject'] = 'Mensaje de prueba con tildes: áéíóú ñ'
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content("Esto es una prueba con acentos: camión, pingüino.")

binario = mensaje.as_bytes()
print(binario.decode("utf-8"))