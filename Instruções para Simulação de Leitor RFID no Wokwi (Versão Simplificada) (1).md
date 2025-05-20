# Instruções para Simulação de Leitor RFID no Wokwi (Versão Simplificada)

Este documento contém instruções para configurar e executar a versão simplificada do simulador de leitor RFID no Wokwi, sem necessidade de bibliotecas externas ou assinatura premium.

## Configuração do Projeto no Wokwi

1. Acesse [Wokwi](https://wokwi.com/new/arduino-uno) e crie um novo projeto com Arduino UNO
2. Copie o código do arquivo `rfid_simulado_simples.ino` para o editor
3. Configure o diagrama conforme as instruções abaixo

### Configuração do Diagrama

Adicione os seguintes componentes ao diagrama:

1. **4 Botões** para simular as diferentes tags RFID:
   - Botão 1: Conectado ao pino 2
   - Botão 2: Conectado ao pino 3
   - Botão 3: Conectado ao pino 4
   - Botão 4: Conectado ao pino 5

2. **1 LED** para indicar a leitura:
   - Conectado ao pino 13 (LED integrado do Arduino)

Exemplo de configuração do `diagram.json`:

```json
{
  "version": 1,
  "author": "Mottu RFID Simulator",
  "editor": "wokwi",
  "parts": [
    { "type": "wokwi-arduino-uno", "id": "arduino", "top": 0, "left": 0, "attrs": {} },
    { "type": "wokwi-pushbutton", "id": "btn1", "top": 150, "left": 20, "attrs": { "color": "red" } },
    { "type": "wokwi-pushbutton", "id": "btn2", "top": 150, "left": 100, "attrs": { "color": "green" } },
    { "type": "wokwi-pushbutton", "id": "btn3", "top": 150, "left": 180, "attrs": { "color": "blue" } },
    { "type": "wokwi-pushbutton", "id": "btn4", "top": 150, "left": 260, "attrs": { "color": "yellow" } },
    { "type": "wokwi-led", "id": "led1", "top": 80, "left": 140, "attrs": { "color": "red" } }
  ],
  "connections": [
    [ "arduino:GND.1", "btn1:2.l", "black", [ "v0" ] ],
    [ "arduino:GND.1", "btn2:2.l", "black", [ "v0" ] ],
    [ "arduino:GND.1", "btn3:2.l", "black", [ "v0" ] ],
    [ "arduino:GND.1", "btn4:2.l", "black", [ "v0" ] ],
    [ "arduino:2", "btn1:1.l", "green", [ "v0" ] ],
    [ "arduino:3", "btn2:1.l", "green", [ "v0" ] ],
    [ "arduino:4", "btn3:1.l", "green", [ "v0" ] ],
    [ "arduino:5", "btn4:1.l", "green", [ "v0" ] ],
    [ "arduino:13", "led1:A", "red", [ "v0" ] ],
    [ "arduino:GND.1", "led1:C", "black", [ "v0" ] ]
  ]
}
```

## Como Usar o Simulador

Existem duas maneiras de simular a leitura de tags RFID:

### 1. Usando os Botões

Cada botão representa uma tag RFID diferente:
- **Botão 1 (pino 2)**: Simula a tag da Honda CG 160 (ID: 04A5B9C2)
- **Botão 2 (pino 3)**: Simula a tag da Yamaha Factor 150 (ID: 1A2B3C4D)
- **Botão 3 (pino 4)**: Simula a tag da Honda Biz 125 (ID: AABB1122)
- **Botão 4 (pino 5)**: Simula a tag da Suzuki Yes 125 (ID: 55667788)

Para simular uma leitura, basta clicar em um dos botões. O LED acenderá brevemente e as informações da moto correspondente serão exibidas no monitor serial.

### 2. Usando o Monitor Serial

Você também pode simular leituras digitando números no monitor serial:
- Digite **1** e pressione Enter: Simula a tag da Honda CG 160
- Digite **2** e pressione Enter: Simula a tag da Yamaha Factor 150
- Digite **3** e pressione Enter: Simula a tag da Honda Biz 125
- Digite **4** e pressione Enter: Simula a tag da Suzuki Yes 125

## Interpretando os Resultados

Quando uma leitura é simulada, o monitor serial exibirá:

1. **Informações da Moto**:
   - ID da Tag
   - Modelo
   - Placa
   - Status
   - Localização

2. **Formato JSON dos Dados**:
   - Uma representação em formato JSON dos dados que seriam enviados para o dashboard

Exemplo de saída:

```
=================================================
LEITURA RFID DETECTADA!
=================================================
ID da Tag: 04A5B9C2
Modelo: Honda CG 160
Placa: ABC1234
Status: Disponível
Localização: Patio A - Entrada
=================================================
Dados enviados para o dashboard
=================================================
Formato JSON dos dados:
{"tag_id":"04A5B9C2","modelo":"Honda CG 160","placa":"ABC1234","status":"Disponível","location":"Patio A - Entrada","reader_id":"READER_001","timestamp":12345}
=================================================
```

## Adaptação para Demonstração

Esta versão simplificada simula o conceito de leitura RFID e processamento dos dados, sem depender de bibliotecas externas. Em um cenário real:

1. O módulo RFID MFRC522 seria usado para ler tags físicas
2. O ESP32 ou Arduino com shield WiFi/Ethernet se conectaria a um broker MQTT
3. Os dados seriam enviados via MQTT para um dashboard em tempo real

Para fins de demonstração do conceito, esta simulação mostra:
- Como as tags RFID seriam identificadas
- Como as informações das motos seriam associadas às tags
- Como os dados seriam formatados para envio
- Como o sistema responderia a diferentes leituras

## Próximos Passos

Para uma demonstração mais completa (quando tiver acesso às bibliotecas):
1. Implementar o código completo com ESP32 e MFRC522
2. Configurar a comunicação MQTT
3. Integrar com o dashboard web ou Node-RED
