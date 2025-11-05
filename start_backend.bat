@echo off
echo =========================================
echo   MotoConnect IoT - Iniciando Backend
echo =========================================

if not exist "venv" (
    echo Criando ambiente virtual Python...
    python -m venv venv
)

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo Instalando dependencias...
pip install -q -r requirements.txt

echo.
echo Iniciando servidor Flask na porta 5000...
echo API disponivel em: http://localhost:5000/api/status
echo Dashboard em: http://localhost:5000/dashboard
echo Resumo operacional: http://localhost:5000/api/summary
echo Historico (JSON): http://localhost:5000/api/history?limit=200
echo.
echo Aguardando conexoes MQTT de dispositivos IoT...
echo Broker MQTT: broker.hivemq.com:1883
echo Topico de telemetria: motoconnect/telemetry
echo Banco de dados: telemetry.db (SQLite)
echo.
echo Pressione Ctrl+C para parar o servidor
echo =========================================

python app.py

