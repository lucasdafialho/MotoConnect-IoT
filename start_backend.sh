#!/bin/bash

echo "========================================="
echo "  MotoConnect IoT - Iniciando Backend"
echo "========================================="

if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual Python..."
    python3 -m venv venv
fi

echo "Ativando ambiente virtual..."
source venv/bin/activate

echo "Instalando dependências..."
pip install -q -r requirements.txt

echo ""
echo "Iniciando servidor Flask na porta 5000..."
echo "API disponível em: http://localhost:5000/api/status"
echo "Dashboard em: http://localhost:5000/dashboard"
echo "Resumo operacional: http://localhost:5000/api/summary"
echo "Histórico (JSON): http://localhost:5000/api/history?limit=200"
echo ""
echo "Aguardando conexões MQTT de dispositivos IoT..."
echo "Broker MQTT: broker.hivemq.com:1883"
echo "Tópico de telemetria: motoconnect/telemetry"
echo "Banco de dados: telemetry.db (SQLite)"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo "========================================="

python3 app.py

