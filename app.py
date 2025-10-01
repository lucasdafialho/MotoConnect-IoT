from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import paho.mqtt.client as mqtt
import json
import threading
import time
import os

app = Flask(__name__)
CORS(app)

moto_status = {}
log_file = 'telemetry_log.json'

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC_TELEMETRY = "motoconnect/telemetry"
MQTT_TOPIC_COMMAND_PREFIX = "motoconnect/commands/"

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao Broker MQTT com resultado: {rc}")
    client.subscribe(MQTT_TOPIC_TELEMETRY)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        tag_id = data.get('tag_id')

        if tag_id:
            print(f"Telemetria recebida de {tag_id}: {data}")
            data['server_timestamp'] = time.time()
            moto_status[tag_id] = data
            with open(log_file, 'a') as f:
                f.write(json.dumps(data) + '\n')

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

def mqtt_loop():
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()

@app.route('/api/status', methods=['GET'])
def get_status():
    sorted_status = sorted(moto_status.values(), key=lambda x: x['server_timestamp'], reverse=True)
    return jsonify(sorted_status)

@app.route('/api/command', methods=['POST'])
def send_command():
    data = request.json
    tag_id = data.get('tag_id')
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
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                history = [json.loads(line) for line in f.readlines()]
            return jsonify(history[-100:])
        return jsonify([])
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    mqtt_thread = threading.Thread(target=mqtt_loop)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    
    app.run(host='0.0.0.0', port=5000)
