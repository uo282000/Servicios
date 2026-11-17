#!/bin/bash
# Script de configuración automática para las Sesiones 3 y 4 en la MV de clase

echo "============================================================"
echo " 1. Actualizando repositorios e instalando paquetes..."
echo "============================================================"
sudo apt-get update
sudo apt-get install -y openssh-server telnetd openbsd-inetd python3-venv python3-pip dnsutils wget

echo ""
echo "============================================================"
echo " 2. Configurando servicios SSH y Telnet..."
echo "============================================================"
sudo systemctl enable --now ssh

if [ -f /etc/inetd.conf ]; then
    if ! grep -q "^telnet" /etc/inetd.conf; then
        echo "telnet stream tcp nowait root /usr/sbin/tcpd /usr/sbin/telnetd" | sudo tee -a /etc/inetd.conf > /dev/null
    fi
    sudo systemctl restart openbsd-inetd 2>/dev/null || sudo systemctl restart inetd 2>/dev/null
fi

echo ""
echo "============================================================"
echo " 3. Creando entornos virtuales de Python (paramiko y dns)..."
echo "============================================================"
python3 -m venv ~/paramikoenv
~/paramikoenv/bin/pip install --upgrade pip
~/paramikoenv/bin/pip install paramiko

python3 -m venv ~/dnsenv
~/dnsenv/bin/pip install --upgrade pip
~/dnsenv/bin/pip install dnspython

echo ""
echo "============================================================"
echo " 4. Preparando ficheros auxiliares y de prueba..."
echo "============================================================"
# Crear ficheros de prueba en HOME para listar/descargar por SSH y SFTP
echo "Fichero de prueba 1" > ~/prueba_sftp_1.txt
echo "Fichero de prueba 2" > ~/prueba_sftp_2.txt

# Descargar logoatc.gif en el directorio actual (y en Practica4 si existe)
wget -q http://www.atc.uniovi.es/estilo_atc/logoatc.gif -O ./logoatc.gif
if [ -d ~/Servicios/Practica4 ]; then
    cp ./logoatc.gif ~/Servicios/Practica4/logoatc.gif
fi

# Copiar el servidor UDP al HOME si existe en el repositorio actual (para Telnet Ej. 2)
UDP_FILE=$(find . -maxdepth 3 -name "udp_servidor3_con_ok.py" | head -n 1)
if [ -n "$UDP_FILE" ]; then
    cp "$UDP_FILE" ~/udp_servidor3_con_ok.py
    echo "[OK] Copiado $UDP_FILE a ~/udp_servidor3_con_ok.py"
fi

echo ""
echo "============================================================"
echo " 5. DATO CLAVE DE ESTA MÁQUINA VIRTUAL (SSH HOST KEY)"
echo "============================================================"
HOST_KEY=$(awk '{print $2}' /etc/ssh/ssh_host_ed25519_key.pub)
echo "Copia esta cadena Base64 y pégala en tus scripts seguros (Ej. 10, 12 y 13):"
echo ""
echo "b'$HOST_KEY'"
echo ""
echo "============================================================"
echo " ¡Configuración completada!"
echo "============================================================"