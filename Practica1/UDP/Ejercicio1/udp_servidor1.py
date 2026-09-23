import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(("", int(sys.argv[1])))

while (True):
    datagrama, origen = s.recvfrom(1024) #recibe una dupla
    print("Hemos recibido esto: ", datagrama.decode("utf-8"))
    print("Desde el origen: ", origen)

