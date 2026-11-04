import base64
import getpass
import paramiko

# 1. Configuración de SSH y clave conocida del host
client = paramiko.SSHClient()
key = paramiko.Ed25519Key(
    data=base64.b64decode(
        b'AAAAC3NzaC1lZDI1NTE5AAAAIMFRAkz4HHVXhJv4C1dH0vfy7q8TWMGGbQqMRP8kJX35'
    )
)
client.get_host_keys().add('localhost', 'ssh-ed25519', key)

# 2. Conectar
clave = getpass.getpass('Introduce la clave: ')
client.connect('localhost', username='uo282000', password=clave)
print('Conectado por SSH!')

# 3. Abrir la sesión SFTP
sftp = client.open_sftp()

# 4. Obtener y mostrar el listado del directorio home remoto
# Por defecto SFTP se posiciona en el home del usuario remoto
ficheros = sftp.listdir()

print('\nContenido de la carpeta remota:')
for nombre in ficheros:
  print(nombre)

# 5. Cerrar canales
sftp.close()
client.close()