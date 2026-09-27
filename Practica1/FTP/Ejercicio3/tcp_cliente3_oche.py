import sys
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

puerto = int(sys.argv[1])

s.connect(("localhost", puerto))

texto = b"ABCDE" #lo hacemos de tipo bytes con la b

for i in range(1,5):
    s.send(texto)

s.sendall(b"FINAL")
    