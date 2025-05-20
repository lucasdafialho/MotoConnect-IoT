#define BOTAO_TAG1 2
#define BOTAO_TAG2 3
#define BOTAO_TAG3 4
#define BOTAO_TAG4 5

#define LED_LEITURA 13

struct MotoInfo {
  String id;
  String modelo;
  String placa;
  String status;
  String localizacao;
};

MotoInfo motosDB[] = {
  {"04A5B9C2", "Honda CG 160", "ABC1234", "Disponível", "Patio A - Entrada"},
  {"1A2B3C4D", "Yamaha Factor 150", "XYZ5678", "Em manutenção", "Patio B - Manutenção"},
  {"AABB1122", "Honda Biz 125", "DEF9012", "Reservada", "Patio A - Entrada"},
  {"55667788", "Suzuki Yes 125", "GHI3456", "Disponível", "Patio C - Saída"}
};

unsigned long lastReadTime = 0;
const long readInterval = 2000;
String lastTagId = "";

String inputString = "";
boolean stringComplete = false;

void setup() {
  Serial.begin(9600);
  
  pinMode(BOTAO_TAG1, INPUT_PULLUP);
  pinMode(BOTAO_TAG2, INPUT_PULLUP);
  pinMode(BOTAO_TAG3, INPUT_PULLUP);
  pinMode(BOTAO_TAG4, INPUT_PULLUP);
  
  pinMode(LED_LEITURA, OUTPUT);
  
  Serial.println("=================================================");
  Serial.println("  SIMULADOR DE LEITOR RFID - PROJETO MOTTU");
  Serial.println("=================================================");
  Serial.println("Pressione os botões 2-5 para simular leituras RFID");
  Serial.println("Ou digite 1-4 no monitor serial e pressione Enter");
  Serial.println("=================================================");
  Serial.println("Motos cadastradas:");
  
  for (int i = 0; i < 4; i++) {
    Serial.print(i+1);
    Serial.print(". ID: ");
    Serial.print(motosDB[i].id);
    Serial.print(" | Modelo: ");
    Serial.print(motosDB[i].modelo);
    Serial.print(" | Placa: ");
    Serial.print(motosDB[i].placa);
    Serial.print(" | Status: ");
    Serial.println(motosDB[i].status);
  }
  
  Serial.println("=================================================");
  Serial.println("Aguardando leituras...");
}

void loop() {
  if (stringComplete) {
    processarEntradaSerial();
    inputString = "";
    stringComplete = false;
  }
  
  verificarBotoes();
  
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}

void verificarBotoes() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - lastReadTime >= readInterval) {
    if (digitalRead(BOTAO_TAG1) == LOW) {
      processarLeitura(0);
      lastReadTime = currentMillis;
    }
    else if (digitalRead(BOTAO_TAG2) == LOW) {
      processarLeitura(1);
      lastReadTime = currentMillis;
    }
    else if (digitalRead(BOTAO_TAG3) == LOW) {
      processarLeitura(2);
      lastReadTime = currentMillis;
    }
    else if (digitalRead(BOTAO_TAG4) == LOW) {
      processarLeitura(3);
      lastReadTime = currentMillis;
    }
  }
}

void processarEntradaSerial() {
  int tagNum = inputString.toInt();
  
  if (tagNum >= 1 && tagNum <= 4) {
    processarLeitura(tagNum - 1);
  } else {
    Serial.println("Entrada inválida. Digite um número de 1 a 4.");
  }
}

void processarLeitura(int index) {
  digitalWrite(LED_LEITURA, HIGH);
  
  MotoInfo moto = motosDB[index];
  
  Serial.println("\n=================================================");
  Serial.println("LEITURA RFID DETECTADA!");
  Serial.println("=================================================");
  Serial.print("ID da Tag: ");
  Serial.println(moto.id);
  Serial.print("Modelo: ");
  Serial.println(moto.modelo);
  Serial.print("Placa: ");
  Serial.println(moto.placa);
  Serial.print("Status: ");
  Serial.println(moto.status);
  Serial.print("Localização: ");
  Serial.println(moto.localizacao);
  Serial.println("=================================================");
  
  Serial.println("Dados enviados para o dashboard");
  Serial.println("=================================================");
  
  Serial.println("Formato JSON dos dados:");
  Serial.print("{\"tag_id\":\"");
  Serial.print(moto.id);
  Serial.print("\",\"modelo\":\"");
  Serial.print(moto.modelo);
  Serial.print("\",\"placa\":\"");
  Serial.print(moto.placa);
  Serial.print("\",\"status\":\"");
  Serial.print(moto.status);
  Serial.print("\",\"location\":\"");
  Serial.print(moto.localizacao);
  Serial.print("\",\"reader_id\":\"READER_001\",\"timestamp\":");
  Serial.print(millis());
  Serial.println("}");
  Serial.println("=================================================");
  
  delay(200);
  digitalWrite(LED_LEITURA, LOW);
}
