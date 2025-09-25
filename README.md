# Sistema de Rastreamento RFID para Motos - Projeto Mottu

![Banner do Projeto](MotoConnect.png)

## Índice

- [Visão Geral](#visão-geral)
- [Desafio](#desafio)
- [Solução Proposta](#solução-proposta)
- [Arquitetura](#arquitetura)
- [Componentes](#componentes)
- [Simulação no Wokwi](#simulação-no-wokwi)
- [Dashboard](#dashboard)
- [Instalação e Configuração](#instalação-e-configuração)
- [Uso](#uso)
- [Contribuições](#contribuições)
- [Licença](#licença)

## Visão Geral

Este projeto implementa um sistema de rastreamento de motos utilizando tecnologia RFID (Identificação por Radiofrequência), desenvolvido para o Challenge 2025 da Mottu. O sistema permite identificar e mapear a localização de motos dentro dos pátios da empresa, fornecendo visualização em tempo real através de um dashboard interativo.

## Desafio

A Mottu enfrenta o desafio de gerenciar frotas de motos em pátios de múltiplas filiais. Atualmente, a localização das motos dentro desses pátios é controlada manualmente, gerando imprecisões e impactando a eficiência operacional. Com mais de 100 filiais espalhadas por diferentes regiões, é fundamental aprimorar o processo de monitoramento e gestão das motos.

**Objetivos:**
- Identificar com precisão a localização das motos dentro dos pátios
- Fornecer visualização em tempo real da disposição das motos
- Criar uma solução escalável para implementação em todas as filiais
- Integrar com sensores IoT das motos para informações adicionais

## Solução Proposta

Nossa solução utiliza etiquetas RFID fixadas nas motos e leitores RFID estrategicamente posicionados nos pátios. Quando uma moto passa próxima a um leitor, o sistema registra sua localização e atualiza o dashboard em tempo real.

**Benefícios:**
- **Precisão alta**: Sem necessidade de câmeras ou visão computacional
- **Baixo custo operacional**: Após implantação inicial
- **Automação**: Atualização de posições sem intervenção humana
- **Escalabilidade**: Facilmente adaptável para 100+ filiais

## Arquitetura

O sistema segue uma arquitetura IoT moderna, com os seguintes componentes:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │     │                 │
│  Etiquetas RFID │────▶│  Leitores RFID  │────▶│  Gateway IoT    │────▶│  Cloud Platform │
│  (nas motos)    │     │  (nos pátios)   │     │  (Edge Device)  │     │                 │
│                 │     │                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                                                  │
                                                                                  │
                                                                                  ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Frontend       │◀────│  API Backend    │◀────│  Registro       │
│  (Mapa do Pátio)│     │  (Flask/Python) │     │  (JSON Lines)   │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

O fluxo de dados ocorre da seguinte forma:
1. Etiquetas RFID nas motos são lidas pelos leitores RFID
2. Os leitores enviam os dados para o Gateway IoT
3. O Gateway processa e envia os dados para a plataforma Cloud
4. Os dados são processados, armazenados e disponibilizados via API
5. O dashboard frontend exibe a localização das motos em tempo real

## Componentes

### Hardware/Dispositivos
- **Etiquetas RFID**: Tags passivas para identificação das motos
- **Leitores/Simuladores WiFi**: ESP32/ESP8266 (ou Wokwi) enviando telemetria via MQTT
- **Gateway IoT**: Incorporado no próprio dispositivo (publica MQTT diretamente)

### Software
- **Backend (Flask/Python)**: Assina telemetria via MQTT, persiste histórico e expõe API REST
- **Simulador IoT (ESP32/ESP8266)**: Publica leituras periódicas e recebe comandos MQTT
- **Dashboard Web**: Interface HTML/CSS/JavaScript que consome a API `/api/status`

## Simulação/Execução dos Dispositivos IoT

Você pode executar 3 simuladores ESP32/ESP8266 em paralelo (Wokwi ou físico). Use `rfid_simulado_simples.ino` como base e altere:

- `MQTT_CLIENT_ID`: valor único por instância, ex.: `motoconnect-sim-01`, `-02`, `-03`
- `reader_id`: diferencie cada dispositivo, ex.: `READER_001`, `READER_002`, `READER_003`

Isso permite cumprir o requisito de 3 dispositivos IoT simultâneos e comandos por tópico `motoconnect/commands/<tag_id>`.

## Dashboard

O sistema inclui um dashboard web para visualização quase em tempo real (polling a cada 3s):

### Dashboard Web
- Interface web em HTML/CSS/JavaScript (`rfid_dashboard.html`)
- Visualização responsiva para desktop e dispositivos móveis
- Consome `GET /api/status` do backend Flask

#### Funcionalidades do Dashboard
- Mapa interativo do pátio com posição das motos
- Tabela de histórico de leituras
- Gráficos estatísticos (status das motos, leituras por localização)
- Alertas visuais para eventos importantes

## Instalação e Configuração (Backend Flask)

1. Requisitos: Python 3.10+
2. Dentro de `MotoConnect-IoT/`, crie e ative um ambiente virtual
   - Windows PowerShell: `python -m venv .venv && .\.venv\Scripts\Activate.ps1`
3. Instale dependências: `pip install -r requirements.txt`
4. Execute o backend: `python app.py`
5. Backend disponível em `http://localhost:5000`

### Executar o Dashboard
1. Abra `rfid_dashboard.html` no navegador
2. Garanta que `API_URL` aponta para `http://localhost:5000/api/status`

### Executar 3 simuladores (Wokwi)
1. Acesse `https://wokwi.com/` e crie 3 projetos ESP32
2. Cole o conteúdo de `rfid_simulado_simples.ino` em cada projeto
3. Altere `MQTT_CLIENT_ID` e `reader_id` em cada um
4. Inicie as simulações em paralelo; verifique leituras no dashboard

### Dashboard Web

1. Abra o arquivo `rfid_dashboard.html` em um navegador web
2. Para uma experiência completa, você precisará conectar o dashboard ao simulador (isso está além do escopo desta demonstração)

## Uso

### Operação
- Inicie o backend Flask
- Inicie 3 simuladores IoT com IDs únicos
- Abra o dashboard; verifique contadores, mapa e tabela atualizando

### Formato dos Dados

Formato JSON publicado em `motoconnect/telemetry` e armazenado em `telemetry_log.json` (JSON Lines):

```json
{
  "tag_id": "04A5B9C2",
  "modelo": "Honda CG 160",
  "placa": "ABC1234",
  "status": "Disponível",
  "location": "Patio A - Entrada",
  "reader_id": "READER_001",
  "timestamp": 12345
}
```

### Endpoints
- `GET /api/status`: retorna última leitura por `tag_id` ordenada por `server_timestamp`
- `POST /api/command` body: `{ "tag_id": "...", "command": "BLOCK|UNBLOCK" }` envia comando MQTT para `motoconnect/commands/<tag_id>`

## Testes Funcionais (Casos de Uso)

1. Moto desaparecida
   - Pare um simulador por 2 ciclos; verifique no dashboard que a moto deixa de atualizar (campo horário estaciona)
2. Moto no lugar errado
   - Force a `location` incorreta por 1 ciclo; o mapa exibirá a moto em área divergente
3. Bloqueio/Desbloqueio
   - Envie `POST /api/command` com `BLOCK` e depois `UNBLOCK`; no terminal do simulador verá o efeito de atuador

## Métricas de Performance (Evidências)

- Latência média: diferença `server_timestamp - timestamp` observada no backend
- Vazão: mensagens/min calculadas a partir do tamanho de `telemetry_log.json`
- Disponibilidade: proporção de leituras recebidas por dispositivo (3 simuladores) em 5 minutos

Inclua esses números no vídeo e no README conforme o seu ensaio.

## Contribuições

Este projeto foi desenvolvido como parte do Challenge 2025 da Mottu. Contribuições são bem-vindas através de pull requests. Para mudanças maiores, por favor abra uma issue primeiro para discutir o que você gostaria de mudar.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

---

Desenvolvido para o Challenge 2025 da Mottu | 2º Ano - Análise e Desenvolvimento de Sistemas
