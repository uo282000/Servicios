import telnetlib
import time

HOST = "localhost"
USER = "uo282000"      # Cambia si tu usuario en la VM es otro
PASSWORD = "principe2002"  # Contraseña del usuario en la VM

# 1. Conexión y autenticación
tn = telnetlib.Telnet(HOST, 23)

tn.read_until(b"login: ")
tn.write(USER.encode("ascii") + b"\n")

tn.read_until(b"Password: ")
tn.write(PASSWORD.encode("ascii") + b"\n")

# 2. Esperar al prompt inicial
tn.read_until(b"$")

# 3. Comprobar si el proceso está corriendo
tn.write(b"ps -ef\n")

# 4. Capturar la salida hasta el siguiente prompt
salida = tn.read_until(b"$").decode("utf-8")

# 5. Evaluar si ya está en ejecución
if "udp_servidor3_con_ok.py" in salida:
    print("El servidor ya está en ejecución")
else:
    # 6. Lanzar en segundo plano con nohup
    print("El servidor no estaba en ejecución. Arrancando...")
    tn.write(b"nohup python3 /home/uo282000/Servicios/Practica3/udp_servidor3_con_ok.py &\n")
    
    # 7. Esperar a que arranque
    time.sleep(1)

# 8. Cerrar la sesión del shell remoto
tn.write(b"exit\n")

# 9. Recoger resto de salida para depuración
debug_salida = tn.read_all().decode("utf-8", errors="ignore")
print("--- Salida de depuración ---")
print(debug_salida)