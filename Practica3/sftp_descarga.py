import base64
import getpass
import os
from stat import S_ISDIR
import paramiko

# 1. Preparación del cliente SSH
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

# 3. Abrir canal SFTP
sftp = client.open_sftp()

carpeta_remota = '.'  # Directorio actual / home remoto
carpeta_local_descarga = './descargas_sftp'
os.makedirs(carpeta_local_descarga, exist_ok=True)

# 4. Listar y descargar solo los archivos que no sean directorios
for item in sftp.listdir(carpeta_remota):
  # Obtener metadatos del elemento remoto
  modo = sftp.stat(item).st_mode

  # S_ISDIR devuelve True si el elemento es una carpeta
  if not S_ISDIR(modo):
    ruta_local = os.path.join(carpeta_local_descarga, item)
    print(f'Descargando fichero: {item}...')
    sftp.get(item, ruta_local)
  else:
    print(f'Omitiendo directorio: {item}')

print('\nDescarga completada con éxito.')

# 5. Cierre
sftp.close()
client.close()