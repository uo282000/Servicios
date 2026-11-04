import paramiko
import time
import base64

client = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(b'AAAAC3NzaC1lZDI1NTE5AAAAIMFRAkz4HHVXhJv4C1dH0vfy7q8TWMGGbQqMRP8kJX35'))
client.get_host_keys().add('localhost', 'ssh-ed25519', key)
clave = str(input("Introduce la clave: "))
client.connect('localhost', username='uo282000', password=clave)
print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('ls')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
time.sleep(1)  # Dar tiempo a que se vacie el buffer
client.close()