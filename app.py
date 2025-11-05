from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import paho.mqtt.client as mqtt
import json
import threading
import time
import os
import sqlite3
from datetime import datetime


app = Flask(__name__)
CORS(app)

moto_status = {}
log_file = 'telemetry_log.json'
DB_PATH = 'telemetry.db'

db_lock = threading.Lock()

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC_TELEMETRY = "motoconnect/telemetry"
MQTT_TOPIC_COMMAND_PREFIX = "motoconnect/commands/"

mqtt_client = mqtt.Client()


def init_storage():
    if not os.path.exists(log_file):
        with open(log_file, 'w'):
            pass

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag_id TEXT,
                reader_id TEXT,
                status TEXT,
                location TEXT,
                modelo TEXT,
                placa TEXT,
                bateria REAL,
                temperatura REAL,
                umidade REAL,
                server_timestamp REAL,
                device_timestamp REAL,
                alert_level TEXT,
                alerts TEXT,
                ingested_at TEXT
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_telemetry_tag ON telemetry(tag_id)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_telemetry_server_ts ON telemetry(server_timestamp)"
        )


def _to_float(value, default=None):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def calculate_alerts(data):
    alerts = []

    bateria = _to_float(data.get('bateria'))
    if bateria is not None and bateria < 12.0:
        alerts.append('Bateria baixa')

    temperatura = _to_float(data.get('temperatura'))
    if temperatura is not None and temperatura > 38:
        alerts.append('Temperatura acima do esperado')

    umidade = _to_float(data.get('umidade'))
    if umidade is not None and umidade < 20:
        alerts.append('Umidade ambiente crítica')

    status = (data.get('status') or '').strip()
    if status == 'Bloqueada':
        alerts.append('Moto bloqueada pelo painel')

    location = (data.get('location') or '').strip()
    if status == 'Disponível' and 'Manutenção' in location:
        alerts.append('Disponível na área de manutenção')

    if not alerts:
        return [], 'normal'

    critical_keywords = {'bloqueada', 'crítica', 'critica'}
    level = 'warning'
    if any(keyword in alert.lower() for alert in alerts for keyword in critical_keywords):
        level = 'danger'

    return alerts, level


def persist_to_db(record):
    alerts_json = json.dumps(record.get('alerts', []))
    with db_lock:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                """
                INSERT INTO telemetry (
                    tag_id, reader_id, status, location, modelo, placa,
                    bateria, temperatura, umidade, server_timestamp,
                    device_timestamp, alert_level, alerts, ingested_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.get('tag_id'),
                    record.get('reader_id'),
                    record.get('status'),
                    record.get('location'),
                    record.get('modelo'),
                    record.get('placa'),
                    _to_float(record.get('bateria')),
                    _to_float(record.get('temperatura')),
                    _to_float(record.get('umidade')),
                    record.get('server_timestamp'),
                    _to_float(record.get('timestamp')),
                    record.get('alert_level'),
                    alerts_json,
                    record.get('server_timestamp_iso'),
                ),
            )
            conn.commit()


def load_history(limit=100):
    with db_lock:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM telemetry ORDER BY server_timestamp DESC LIMIT ?",
                (limit,),
            ).fetchall()

    history = []
    for row in rows:
        item = dict(row)
        item['alerts'] = json.loads(item.get('alerts') or '[]')
        item['server_timestamp_iso'] = item.get('ingested_at')
        history.append(item)
    return history


def build_summary():
    status_counts = {}
    alert_items = []
    last_update = 0

    for moto in moto_status.values():
        status = moto.get('status', 'Desconhecido')
        status_counts[status] = status_counts.get(status, 0) + 1
        server_ts = moto.get('server_timestamp') or 0
        last_update = max(last_update, server_ts)

        alerts = moto.get('alerts') or []
        if alerts:
            alert_items.append(
                {
                    'tag_id': moto.get('tag_id'),
                    'modelo': moto.get('modelo'),
                    'status': status,
                    'location': moto.get('location'),
                    'alerts': alerts,
                    'alert_level': moto.get('alert_level', 'warning'),
                    'server_timestamp': server_ts,
                    'server_timestamp_iso': moto.get('server_timestamp_iso'),
                }
            )

    return {
        'total_motos': len(moto_status),
        'status_counts': status_counts,
        'alertas_ativos': alert_items,
        'ultimo_update': last_update,
        'ultimo_update_iso': datetime.utcfromtimestamp(last_update).isoformat() + 'Z'
        if last_update
        else None,
    }


init_storage()


def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao Broker MQTT com resultado: {rc}")
    client.subscribe(MQTT_TOPIC_TELEMETRY)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        tag_raw = data.get('tag_id')
        tag_id = str(tag_raw).upper() if tag_raw else None

        if tag_id:
            print(f"Telemetria recebida de {tag_id}: {data}")
            data['tag_id'] = tag_id
            server_timestamp = time.time()
            data['server_timestamp'] = server_timestamp
            data['server_timestamp_iso'] = (
                datetime.utcfromtimestamp(server_timestamp).isoformat() + 'Z'
            )

            alerts, level = calculate_alerts(data)
            data['alerts'] = alerts
            data['alert_level'] = level

            moto_status[tag_id] = data

            with open(log_file, 'a') as f:
                f.write(json.dumps(data) + '\n')

            persist_to_db(data)

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

def mqtt_loop():
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()

@app.route('/api/status', methods=['GET'])
def get_status():
    sorted_status = sorted(
        (dict(moto) for moto in moto_status.values()),
        key=lambda x: x.get('server_timestamp', 0),
        reverse=True,
    )
    return jsonify(sorted_status)


@app.route('/api/summary', methods=['GET'])
def get_summary():
    return jsonify(build_summary())


@app.route('/api/motos/<tag_id>', methods=['GET'])
def get_moto(tag_id):
    tag_id = str(tag_id).upper()
    moto = moto_status.get(tag_id)
    if not moto:
        with db_lock:
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                row = conn.execute(
                    "SELECT * FROM telemetry WHERE tag_id = ? ORDER BY server_timestamp DESC LIMIT 1",
                    (tag_id,),
                ).fetchone()
        if not row:
            return jsonify({"status": "error", "message": "Moto não encontrada"}), 404
        moto = dict(row)
        moto['alerts'] = json.loads(moto.get('alerts') or '[]')
        moto['server_timestamp_iso'] = moto.get('ingested_at')
    return jsonify(moto)

@app.route('/api/command', methods=['POST'])
def send_command():
    data = request.json
    tag_id = data.get('tag_id')
    if tag_id:
        tag_id = str(tag_id).upper()
    command = data.get('command')

    if not tag_id or not command:
        return jsonify({"status": "error", "message": "tag_id e command são obrigatórios"}), 400

    command_topic = f"{MQTT_TOPIC_COMMAND_PREFIX}{tag_id}"
    command_payload = json.dumps({"tag_id": tag_id, "command": command})
    
    try:
        mqtt_client.publish(command_topic, command_payload)
        print(f"Comando '{command}' enviado para a moto '{tag_id}' no tópico '{command_topic}'")
        return jsonify({"status": "success", "message": f"Comando {command} enviado para {tag_id}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/dashboard')
@app.route('/')
def dashboard():
    dashboard_path = os.path.join(os.path.dirname(__file__), 'rfid_dashboard.html')
    return send_file(dashboard_path)

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        limit = request.args.get('limit', default=100, type=int)
        limit = max(1, min(limit, 1000))
        history = load_history(limit)
        return jsonify(history)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    mqtt_thread = threading.Thread(target=mqtt_loop)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    
    app.run(host='0.0.0.0', port=5000)
