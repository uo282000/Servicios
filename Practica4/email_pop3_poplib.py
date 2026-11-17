import poplib
import getpass

server = "pop.gmail.com"
username = input("Usuario (Gmail): ")
password = getpass.getpass("Contraseña de aplicación: ")

# Instanciar objeto POP3_SSL y activar depuración
pop3_mail = poplib.POP3_SSL(server)
pop3_mail.set_debuglevel(2)

# Autenticación
pop3_mail.user(username)
pop3_mail.pass_(password)

# Obtener número de mensajes con stat() -> devuelve (num_mensajes, tamaño_total)
num_mensajes, _ = pop3_mail.stat()
print(f"\nMensajes disponibles: {num_mensajes}")

if num_mensajes > 0:
    # Recuperar el primer mensaje: devuelve (respuesta, lista_lineas, octetos)
    respuesta, lineas, octetos = pop3_mail.retr(1)
    print("\n--- Contenido crudo devuelto por poplib.retr(1) ---")
    for linea in lineas:
        print(linea)

pop3_mail.quit()