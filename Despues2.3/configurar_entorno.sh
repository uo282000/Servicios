#!/bin/bash

# Salir inmediatamente si algún comando falla
set -e

# Guardar la ruta actual del repositorio
REPO_DIR=$(pwd)

echo "=== 1. Instalando dependencias base (Prometheus y Node Exporter) ==="
sudo apt-get update
sudo apt-get install -y prometheus prometheus-node-exporter apt-transport-https software-properties-common wget

echo "=== 2. Instalando Grafana ==="
sudo mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt-get update
sudo apt-get install -y grafana

echo "=== 3. Descargando e instalando Alertmanager 0.29.0 ==="
cd /tmp
wget -q https://github.com/prometheus/alertmanager/releases/download/v0.29.0/alertmanager-0.29.0.linux-amd64.tar.gz
tar -xzf alertmanager-0.29.0.linux-amd64.tar.gz
sudo cp alertmanager-0.29.0.linux-amd64/alertmanager /usr/local/bin/
sudo cp alertmanager-0.29.0.linux-amd64/amtool /usr/local/bin/
sudo mkdir -p /etc/alertmanager /var/lib/alertmanager
cd "$REPO_DIR"

echo "=== 4. Copiando configuraciones desde el repositorio ==="
sudo cp configs/prometheus.yml /etc/prometheus/
sudo cp configs/alerts.yml /etc/prometheus/
sudo cp configs/alertmanager.service /etc/systemd/system/

# Ajustar permisos por seguridad
sudo chown root:root /etc/prometheus/prometheus.yml /etc/prometheus/alerts.yml /etc/systemd/system/alertmanager.service

echo "=== 5. Habilitando y reiniciando los 4 servicios ==="
sudo systemctl daemon-reload

# 1. Prometheus
sudo systemctl enable prometheus
sudo systemctl restart prometheus

# 2. Node Exporter
sudo systemctl enable prometheus-node-exporter
sudo systemctl restart prometheus-node-exporter

# 3. Alertmanager
sudo systemctl enable alertmanager
sudo systemctl restart alertmanager

# 4. Grafana
sudo systemctl enable grafana-server
sudo systemctl restart grafana-server

echo "=== 6. Preparando entorno Docker ==="
docker network create pruebas 2>/dev/null || true

echo "=== ¡Configuración completada con éxito! ==="
echo "Servicios activos: Prometheus (9090), Node Exporter (9100), Alertmanager (9093) y Grafana (3000)."