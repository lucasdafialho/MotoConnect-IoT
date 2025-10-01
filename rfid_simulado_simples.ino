#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHTesp.h>

const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASSWORD = "";

const char* MQTT_BROKER = "broker.hivemq.com";
const int MQTT_PORT = 1883;
const char* MQTT_CLIENT_ID = "motoconnect-sim-12345";

const char* MQTT_TOPIC_TELEMETRY = "motoconnect/telemetry";
const char* MQTT_TOPIC_COMMAND = "motoconnect/commands/+";

const int LED_GREEN = 23;
const int LED_YELLOW = 22;
const int LED_RED = 21;
const int BUZZER_PIN = 19;
const int DHT_PIN = 4;

WiFiClient espClient;
PubSubClient client(espClient);
DHTesp dht;

struct MotoInfo {
  String id;
  String modelo;
  String placa;
  String status;
  String localizacao;
  float bateria;
};

MotoInfo motosDB[] = {
  {"04A5B9C2", "Honda CG 160", "ABC1234", "Disponível", "Patio A - Entrada", 12.7},
  {"1A2B3C4D", "Yamaha Factor 150", "XYZ5678", "Em manutenção", "Patio B - Manutenção", 12.2},
  {"AABB1122", "Honda Biz 125", "DEF9012", "Disponível", "Patio A - Entrada", 12.5},
  {"55667788", "Suzuki Yes 125", "GHI3456", "Disponível", "Patio C - Saída", 11.9}
};

void setup_wifi() {
  Serial.println("Conectando ao WiFi...");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Conectado!");
}

void updateStatusLeds(String status) {
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_YELLOW, LOW);
  digitalWrite(LED_RED, LOW);
  
  if (status == "Disponível") {
    digitalWrite(LED_GREEN, HIGH);
  } else if (status == "Em manutenção") {
    digitalWrite(LED_YELLOW, HIGH);
  } else if (status == "Bloqueada") {
    digitalWrite(LED_RED, HIGH);
    tone(BUZZER_PIN, 1000, 200);
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Comando recebido no tópico: ");
  Serial.println(topic);

  StaticJsonDocument<128> doc;
  deserializeJson(doc, payload, length);

  const char* target_id = doc["tag_id"];
  const char* command = doc["command"];

  for (int i = 0; i < 4; i++) {
    if (motosDB[i].id == target_id) {
      if (strcmp(command, "BLOCK") == 0) {
        motosDB[i].status = "Bloqueada";
        Serial.print("ATUADOR: Moto ");
        Serial.print(motosDB[i].modelo);
        Serial.println(" foi bloqueada!");
        digitalWrite(LED_RED, HIGH);
        tone(BUZZER_PIN, 1000, 500);
      } else if (strcmp(command, "UNBLOCK") == 0) {
        motosDB[i].status = "Disponível";
        Serial.print("ATUADOR: Moto ");
        Serial.print(motosDB[i].modelo);
        Serial.println(" foi desbloqueada!");
        digitalWrite(LED_GREEN, HIGH);
      }
      updateStatusLeds(motosDB[i].status);
      break;
    }
  }
}

void reconnect_mqtt() {
  while (!client.connected()) {
    Serial.print("Conectando ao Broker MQTT...");
    if (client.connect(MQTT_CLIENT_ID)) {
      Serial.println(" Conectado!");
      client.subscribe(MQTT_TOPIC_COMMAND);
      Serial.print("Inscrito no tópico de comandos: ");
      Serial.println(MQTT_TOPIC_COMMAND);
    } else {
      Serial.print(" falhou, rc=");
      Serial.print(client.state());
      Serial.println(" tentando novamente em 5 segundos");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_YELLOW, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  
  dht.setup(DHT_PIN, DHTesp::DHT22);
  
  setup_wifi();
  client.setServer(MQTT_BROKER, MQTT_PORT);
  client.setCallback(callback);
  
  Serial.println("Sistema MotoConnect IoT Inicializado!");
  Serial.println("Sensores: RFID, Bateria, Temperatura/Umidade");
  Serial.println("Atuadores: LEDs (Status), Buzzer (Alarme)");
}

void loop() {
  if (!client.connected()) {
    reconnect_mqtt();
  }
  client.loop();

  int motoIndex = random(0, 4);
  MotoInfo moto = motosDB[motoIndex];

  moto.bateria -= random(0, 10) / 100.0;
  if (moto.bateria < 11.5) moto.bateria = 12.8;
  motosDB[motoIndex].bateria = moto.bateria;

  TempAndHumidity sensor_data = dht.getTempAndHumidity();
  float temperatura = sensor_data.temperature;
  float umidade = sensor_data.humidity;

  updateStatusLeds(moto.status);

  StaticJsonDocument<384> doc;
  doc["tag_id"] = moto.id;
  doc["modelo"] = moto.modelo;
  doc["placa"] = moto.placa;
  doc["status"] = moto.status;
  doc["location"] = moto.localizacao;
  doc["bateria"] = String(moto.bateria, 2);
  doc["temperatura"] = String(temperatura, 1);
  doc["umidade"] = String(umidade, 1);
  doc["reader_id"] = "READER_001";
  doc["timestamp"] = millis();

  char json_buffer[384];
  serializeJson(doc, json_buffer);

  client.publish(MQTT_TOPIC_TELEMETRY, json_buffer);

  Serial.println("\n==================================");
  Serial.println("LEITURA SIMULADA E ENVIADA VIA MQTT:");
  Serial.println(json_buffer);
  Serial.print("Sensores: RFID=");
  Serial.print(moto.id);
  Serial.print(" | Bateria=");
  Serial.print(moto.bateria);
  Serial.print("V | Temp=");
  Serial.print(temperatura);
  Serial.print("C | Umid=");
  Serial.print(umidade);
  Serial.println("%");
  Serial.println("==================================");

  delay(7000);
}
