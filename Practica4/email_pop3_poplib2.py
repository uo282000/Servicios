import poplib
import getpass
import email
import email.header

def imprime_resumen_mensaje(msg_bytes):
    # Parsear los bytes recibidos y construir con ellos un objeto EmailMessage
    msg = email.message_from_bytes(msg_bytes)

    # Extraemos las cabeceras "From" y "Subject"
    remite = msg.get("From", "<desconocido>")
    asunto = msg.get("Subject", "<sin asunto>")

    # Decodificar si contienen caracteres Unicode / no-ASCII
    remite = email.header.make_header(email.header.decode_header(remite))
    asunto = email.header.make_header(email.header.decode_header(asunto))

    # Extraemos el cuerpo
    cuerpo = msg.get_payload()

    # Si es multi-part, nos quedamos con el primer elemento
    if type(cuerpo) == list:
        parte_1 = cuerpo[0].get_payload()
        cuerpo = "---Multipart. Parte 1\n" + str(parte_1)

    print("From:", remite)
    print("Subject:", asunto)
    print(str(cuerpo)[:500])
    if len(str(cuerpo)) > 500:
        print("...[omitido]")
    print("-" * 80)

server = "pop.gmail.com"
username = input("Usuario (Gmail): ")
password = getpass.getpass("Contraseña de aplicación: ")

pop3_mail = poplib.POP3_SSL(server)
pop3_mail.user(username)
pop3_mail.pass_(password)

num_mensajes, _ = pop3_mail.stat()

for i in range(1, num_mensajes + 1):
    _, lineas, _ = pop3_mail.retr(i)
    # Concatenar la lista de líneas en un único objeto bytes separado por \r\n
    msg_bytes = b"\r\n".join(lineas)
    imprime_resumen_mensaje(msg_bytes)

pop3_mail.quit()