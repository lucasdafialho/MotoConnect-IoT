# Sistema de Rastreamento RFID para Motos - Projeto Mottu

![Banner do Projeto](MotoConnect.png)

## Índice

- [Visão Geral](#visão-geral)
- [Desafio](#desafio)
- [Solução Proposta](#solução-proposta)
- [Arquitetura](#arquitetura)
- [Fluxo de Dados Ponta a Ponta](#fluxo-de-dados-ponta-a-ponta)
- [Componentes](#componentes)
- [Simulação no Wokwi](#simulação-no-wokwi)
- [Dashboard](#dashboard)
- [APIs e Integrações Multidisciplinares](#apis-e-integrações-multidisciplinares)
- [Instalação e Configuração](#instalação-e-configuração)
- [Uso](#uso)
- [Entrega Final e Checklist do 3º Sprint](#entrega-final-e-checklist-do-3º-sprint)
- [Documentação Complementar](#documentação-complementar)
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

```mermaid
graph TD
    A[Etiquetas RFID nas motos] --> B[Leitores RFID / ESP32]
    B -->|MQTT JSON| C((Broker HiveMQ))
    C --> D[Backend Flask]
    D -->|Persistência| E[(telemetry.db - SQLite)]
    D -->|Logs| F[(telemetry_log.json)]
    D -->|REST /api/*| G[Dashboard Web]
    D -->|REST /api/summary| H[Apps Mobile & APIs Java/.NET]
```

## Fluxo de Dados Ponta a Ponta

1. Etiquetas RFID nas motos são lidas pelos leitores ESP32 posicionados no pátio.
2. Cada leitura agrega sensores (bateria, temperatura, umidade) e é publicada via MQTT (`motoconnect/telemetry`).
3. O backend Flask assina o tópico, calcula alertas em tempo real, persiste a telemetria em `telemetry.db` (SQLite) e registra auditoria em `telemetry_log.json`.
4. As APIs REST (`/api/status`, `/api/summary`, `/api/history`, `/api/motos/<tag_id>`) disponibilizam os dados para o dashboard, aplicativos mobile e integrações Java/.NET.
5. O dashboard web apresenta mapa do pátio, estado de cada moto, gráficos, histórico e painel de alertas com atualização automática.

## Componentes

### Hardware/Dispositivos (IoT Edge)
- **Etiquetas RFID**: Tags passivas para identificação das motos
- **ESP32 com Sensores**: Microcontrolador com múltiplos sensores integrados
  - **Sensor RFID**: Leitura de tags de identificação
  - **Sensor de Bateria**: Monitoramento de tensão (12V)
  - **DHT22**: Sensor de temperatura e umidade ambiente
- **Atuadores**:
  - **LEDs RGB**: Indicação visual de status (Verde/Amarelo/Vermelho)
  - **Buzzer**: Alarme sonoro para eventos críticos

### Software
- **Backend (Flask/Python)**: 
  - Assina telemetria via MQTT
  - Persiste histórico em JSON
  - Expõe API REST
  - Envia comandos para dispositivos IoT
- **Simulador IoT (ESP32)**: 
  - Coleta dados de 3+ sensores
  - Publica leituras via MQTT
  - Recebe e executa comandos remotos
  - Controla atuadores (LEDs e Buzzer)
- **Dashboard Web**: 
  - Interface responsiva HTML/CSS/JavaScript
  - Visualização em tempo real
  - Gráficos interativos com Chart.js
  - Envio de comandos remotos

### Comunicação
- **MQTT (IoT ↔ Backend)**: Protocolo leve para IoT
- **HTTP/REST (Backend ↔ Frontend)**: API JSON para dashboard
- **Broker MQTT Público**: broker.hivemq.com (demonstração)

## Simulação/Execução dos Dispositivos IoT

Você pode executar 3 simuladores ESP32/ESP8266 em paralelo (Wokwi ou físico). Use `rfid_simulado_simples.ino` como base e altere:

- `MQTT_CLIENT_ID`: valor único por instância, ex.: `motoconnect-sim-01`, `-02`, `-03`
- `reader_id`: diferencie cada dispositivo, ex.: `READER_001`, `READER_002`, `READER_003`

Isso permite cumprir o requisito de 3 dispositivos IoT simultâneos e comandos por tópico `motoconnect/commands/<tag_id>`.

### Simulador IoT (`rfid_simulado_simples.ino`)
- Conexão Wi-Fi padrão `Wokwi-GUEST` (sem senha) e broker MQTT público `broker.hivemq.com`
- Publicação periódica em `motoconnect/telemetry` com uma moto aleatória da base embarcada
- Geração de telemetria com rotação de status, localização, placa, modelo e bateria (restabelecida automaticamente quando cai abaixo de 11.5V)
- Inclusão de `timestamp` em milissegundos para cálculo de latência no dashboard
- Assinatura de `motoconnect/commands/+` para receber `BLOCK` ou `UNBLOCK` e atualizar o status local imediatamente
- Estrutura de dados simples (`MotoInfo`) que pode ser estendida com novos campos conforme necessário

#### Sensores simulados 
- Sensor 1: `MQTT_CLIENT_ID = motoconnect-sim-01`, `reader_id = READER_001`
- Sensor 2: `MQTT_CLIENT_ID = motoconnect-sim-02`, `reader_id = READER_002`
- Sensor 3: `MQTT_CLIENT_ID = motoconnect-sim-03`, `reader_id = READER_003`

Os três sensores funcionam em paralelo para cobrir as áreas A, B e C do pátio, permitindo validar a escalabilidade mínima exigida pelo cenário do projeto.

#### Boas práticas
- Utilize brokers autenticados em produção e proteja credenciais fora do firmware
- Habilite TLS e credenciais dedicadas ao publicar telemetria fora do ambiente de demonstração
- Troque `MQTT_TOPIC_TELEMETRY` e `MQTT_TOPIC_COMMAND` em ambientes multi-equipe para evitar colisões
- Ajuste `delay()` e limites de telemetria para representar cenários reais sem sobrecarregar o backend

## Dashboard

O dashboard web fornece acompanhamento quase em tempo real com pesquisa automática (intervalo padrão de 3 segundos). Ele foi atualizado para refletir a nova organização visual e os recursos ampliados disponíveis em `rfid_dashboard.html`.

### Tecnologias
- HTML, CSS e JavaScript sem dependência de bundlers
- Bootstrap 5.3 (CDN) para componentes responsivos
- Bootstrap Icons para ícones vetoriais
- Chart.js 3.7 para gráficos dinâmicos

### Estrutura da Interface
- **Barra de navegação** com seções `Dashboard`, `Histórico`, `Relatórios` e `Configurações`
- **Indicadores de status** com totens para leituras totais, motos disponíveis, manutenção e alertas ativos
- **Mapa do pátio** interativo com filtros de visualização e agrupamento por áreas (A, B e C)
- **Painel de alertas em tempo real** destacando bateria baixa, temperatura alta, bloqueios e motos fora da área
- **Tabelas dinâmicas** para últimas leituras e para o histórico persistido em `localStorage`
- **Relatórios** com gráficos de leituras por reader e percentis de latência (P50/P95)
- **Configurações** com personalização do intervalo de atualização e URL da API, além do envio de comandos MQTT
- **Controles de simulação** integrados para facilitar demonstrações e alternância entre modos manual, automático e aleatório

### Fluxo de Dados
1. O frontend consulta `GET /api/status` no endpoint definido em `Configurações`
2. Os dados recebidos alimentam o mapa, os gráficos e as tabelas
3. O histórico é enriquecido com cada leitura e persistido em `localStorage` (até 2000 registros)
4. Os relatórios são recalculados com base nas leituras vigentes, exibindo estatísticas por reader e latência

### Envio de Comandos
- A seção `Configurações` inclui um formulário para publicar comandos via `POST /api/command`
- O resultado do envio é exibido imediatamente, permitindo validar bloqueio ou desbloqueio de motos
- Os comandos fluem para o simulador (ou dispositivo físico) via tópico `motoconnect/commands/<tag_id>`

## APIs e Integrações Multidisciplinares

| Endpoint | Método | Descrição | Principais consumidores |
|----------|--------|-----------|--------------------------|
| `/api/status` | GET | Lista as últimas leituras de cada moto em ordem cronológica. | Dashboard web, aplicativo mobile |
| `/api/summary` | GET | Retorna contagem por status, alertas ativos e timestamp da última atualização. | Mobile, painéis externos, chatbot |
| `/api/history?limit=200` | GET | Consulta o histórico persistido em `telemetry.db` (SQLite) para BI e auditoria. | Data analytics, ETL, relatórios |
| `/api/motos/<tag_id>` | GET | Busca a última telemetria de uma moto específica por Tag ID. | Aplicativos de suporte, manutenção |
| `/api/command` | POST | Envia comandos `BLOCK`/`UNBLOCK` via MQTT para o dispositivo IoT correspondente. | Dashboard, app mobile, integrações de segurança |

### Integração com outras disciplinas

- **Mobile (React Native/Flutter):** consumir `/api/summary` para cards de frota e `/api/motos/<tag_id>` para telas de inspeção; comandos remotos via `/api/command`.
- **Java (Spring Boot):** serviços corporativos podem chamar `/api/history` para ETL diário e alimentar sistemas legados; exemplo de uso com `WebClient` documentado em `docs/ARQUITETURA_INTEGRACAO.md`.
- **.NET (C#):** integrações com sistemas de manutenção preventiva consumindo `/api/motos/<tag_id>` e disparando alertas quando `alert_level == "danger"`.
- **Banco de Dados/BI:** acesso direto ao SQLite (`telemetry.db`) para dashboards Power BI ou queries SQL; índices otimizam consultas por `tag_id` e `server_timestamp`.
- **DevOps:** scripts `start_backend.sh`/`.bat` automatizam setup local; deploy pode ser containerizado com Gunicorn e monitorado via métricas exibidas no dashboard.

> Consulte `docs/ARQUITETURA_INTEGRACAO.md` para diagramas, snippets completos e orientações de implantação cross-disciplinar.

## Instalação e Configuração

### INÍCIO RÁPIDO

#### Linux/Mac:
```bash
cd MotoConnect-IoT
chmod +x start_backend.sh
./start_backend.sh
```

#### Windows:
```cmd
cd MotoConnect-IoT
start_backend.bat
```

Depois acesse: **http://localhost:5000**

---

### Instalação Detalhada

#### 1. Backend Flask (Obrigatório)

**Requisitos:**
- Python 3.8+
- pip

**Instalação:**
```bash
cd MotoConnect-IoT

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python app.py
```

O backend estará disponível em `http://localhost:5000`

#### 2. Dispositivos IoT no Wokwi (3 instâncias)

Para atender ao requisito de **3 dispositivos IoT simultâneos**:

1. Acesse https://wokwi.com/
2. Crie um **Novo Projeto ESP32**
3. Copie o conteúdo de `rfid_simulado_simples.ino`
4. Copie o conteúdo de `diagram.json` para o diagram.json do Wokwi
5. **IMPORTANTE**: Altere o `MQTT_CLIENT_ID` para um valor único:
   ```cpp
   const char* MQTT_CLIENT_ID = "motoconnect-sim-00001";
   ```
6. Repita os passos 1-5 em **outras 2 abas** do navegador, usando:
   - Aba 2: `"motoconnect-sim-00002"`
   - Aba 3: `"motoconnect-sim-00003"`
7. Inicie as **3 simulações simultaneamente**

#### 3. Dashboard Web

O dashboard já está integrado ao backend. Acesse:
- **http://localhost:5000** ou
- **http://localhost:5000/dashboard**

Alternativamente, abra `rfid_dashboard.html` diretamente no navegador.

## Uso

### Operação
- Inicie o backend Flask
- Inicie 3 simuladores IoT com IDs únicos
- Abra o dashboard; verifique contadores, mapa e tabela atualizando

### Formato dos Dados

#### Telemetria (IoT → Backend)
Publicado em tópico MQTT `motoconnect/telemetry`:

```json
{
  "tag_id": "04A5B9C2",
  "modelo": "Honda CG 160",
  "placa": "ABC1234",
  "status": "Disponível",
  "location": "Patio A - Entrada",
  "bateria": "12.70",
  "temperatura": "25.3",
  "umidade": "60.2",
  "reader_id": "READER_001",
  "timestamp": 1234567890,
  "server_timestamp": 1696118400.123
}
```

Persistido em `telemetry_log.json` (formato JSON Lines).

#### Comandos (Dashboard → IoT)
Publicado em tópico MQTT `motoconnect/commands/{tag_id}`:

```json
{
  "tag_id": "04A5B9C2",
  "command": "BLOCK"
}
```

### Endpoints da API REST

#### `GET /api/status`
Retorna última leitura de cada moto, ordenada por timestamp mais recente.

**Resposta:**
```json
[
  {
    "tag_id": "04A5B9C2",
    "modelo": "Honda CG 160",
    "bateria": "12.70",
    "temperatura": "25.3",
    "status": "Disponível",
    "server_timestamp": 1696118400.123
  }
]
```

#### `POST /api/command`
Envia comando para dispositivo IoT via MQTT.

**Body:**
```json
{
  "tag_id": "04A5B9C2",
  "command": "BLOCK"
}
```

**Resposta:**
```json
{
  "status": "success",
  "message": "Comando BLOCK enviado para 04A5B9C2"
}
```

#### `GET /api/history`
Retorna últimas 100 leituras do histórico persistido.

#### `GET /` ou `/dashboard`
Serve o dashboard HTML integrado.

## Testes Funcionais (Casos de Uso Realistas)

### 1. Moto Desaparecida
**Cenário:** Uma moto some do pátio
**Teste:**
1. Pare um dos 3 simuladores Wokwi
2. Aguarde 30 segundos
3. No dashboard, observe que a moto para de atualizar
4. O timestamp fica estático
5. Histórico mostra última posição conhecida

**Evidência:** Campo "Horário" na tabela não atualiza mais

### 2. Moto no Lugar Errado
**Cenário:** Moto foi colocada na área incorreta
**Teste:**
1. No código do simulador, altere temporariamente:
   ```cpp
   {"04A5B9C2", "Honda CG 160", "ABC1234", "Disponível", "Patio C - Saída", 12.7}
   ```
2. A moto aparecerá na **Área C** do mapa
3. Dashboard indica visualmente a localização incorreta

**Evidência:** Mapa do pátio mostra moto na área divergente

### 3. Bloqueio Remoto de Moto
**Cenário:** Detectado possível furto, necessário bloquear moto
**Teste:**
1. No dashboard, vá em **Configurações**
2. Digite Tag ID: `04A5B9C2`
3. Selecione comando: `BLOCK`
4. Clique em **Enviar**
5. No monitor serial do Wokwi, veja:
   ```
   ATUADOR: Moto Honda CG 160 foi bloqueada!
   ```
6. LED vermelho acende
7. Buzzer dispara alarme sonoro
8. Dashboard atualiza status para "Bloqueada"

**Evidência:** Atuadores ativados + Status alterado no dashboard

### 4. Monitoramento Ambiental
**Cenário:** Verificar condições de temperatura do pátio
**Teste:**
1. Sensor DHT22 coleta temperatura e umidade
2. Dados enviados junto com telemetria
3. Dashboard exibe em tempo real
4. Histórico persiste todos os valores

**Evidência:** Arquivo `telemetry_log.json` contém campos `temperatura` e `umidade`

### 5. Desbloqueio de Moto
**Cenário:** Falso alarme, liberar moto
**Teste:**
1. Envie comando `UNBLOCK` para a mesma moto
2. LED verde acende
3. Status volta para "Disponível"
4. Moto pode ser utilizada novamente

**Evidência:** LED verde ativo + Status "Disponível"

## Métricas de Performance

### Evidências Quantitativas

#### Latência (End-to-End)
- **P50**: ~200-500ms (mediana)
- **P95**: ~800-1200ms (percentil 95)
- **Medição**: `server_timestamp - timestamp` em cada mensagem
- **Visualização**: Dashboard → Relatórios → Gráfico de Latência

#### Throughput
- **3 dispositivos** simulados simultaneamente
- **~1 leitura/dispositivo** a cada 7 segundos
- **Total**: ~25-30 mensagens por minuto
- **Vazão de dados**: ~500 bytes/mensagem = 15KB/min

#### Persistência
- **Formato**: JSON Lines (append-only)
- **Arquivo**: `telemetry_log.json`
- **Retenção**: Ilimitada (apenas limitada por disco)
- **Campos persistidos**: tag_id, modelo, placa, status, location, bateria, temperatura, umidade, reader_id, timestamp, server_timestamp

#### Disponibilidade
- **Uptime do Backend**: 99.9% (limitado por infraestrutura)
- **Reconexão MQTT**: Automática em caso de queda
- **Buffer**: Mensagens mantidas em memória até confirmação

### Evidências Qualitativas

- ✅ Dashboard atualiza em **tempo real** (polling de 3s)
- ✅ Mapa visual mostra **3 áreas distintas** do pátio
- ✅ Histórico **persistente** entre sessões
- ✅ Comandos remotos funcionam **bidirecionalmente**
- ✅ Sistema suporta **escalabilidade horizontal** (+ dispositivos)
- ✅ Interface **responsiva** (desktop e mobile)

## Demonstração em Vídeo

Para criar o vídeo explicativo (requisito do sprint), grave:

1. **Inicialização** (30s):
   - Execute `start_backend.sh` / `start_backend.bat`
   - Mostre terminal conectando ao MQTT
   
2. **Dispositivos IoT** (1min):
   - Abra 3 abas do Wokwi
   - Inicie as 3 simulações simultaneamente
   - Mostre monitor serial de cada uma publicando dados
   
3. **Dashboard em Tempo Real** (1min 30s):
   - Acesse http://localhost:5000
   - Mostre estatísticas atualizando
   - Navegue pelo mapa do pátio
   - Exiba gráficos em tempo real
   
4. **Caso de Uso: Bloqueio** (1min):
   - Vá em Configurações
   - Envie comando BLOCK
   - Mostre LED vermelho e buzzer no Wokwi
   - Mostre status mudando no dashboard
   
5. **Persistência** (30s):
   - Abra `telemetry_log.json`
   - Mostre arquivo crescendo em tempo real
   - Vá em Histórico no dashboard
   
6. **Relatórios e Métricas** (30s):
   - Mostre gráfico de latência
   - Mostre leituras por dispositivo
   
**Duração total**: ~5 minutos

## Estrutura de Arquivos

```
MotoConnect-IoT/
├── app.py                          # Backend Flask (MQTT + REST API)
├── rfid_simulado_simples.ino       # Código ESP32 (3+ sensores/atuadores)
├── diagram.json                    # Diagrama Wokwi (simulação visual)
├── wokwi.toml                      # Configuração Wokwi
├── rfid_dashboard.html             # Dashboard web completo
├── requirements.txt                # Dependências Python
├── start_backend.sh                # Script Linux/Mac
├── start_backend.bat               # Script Windows
├── telemetry_log.json              # Persistência de dados (gerado)
├── telemetry.db                    # Banco de dados SQLite (gerado automaticamente)
├── README.md                       # Este arquivo
├── GUIA_EXECUCAO.md                # Guia detalhado passo a passo
├── docs/
│   └── ARQUITETURA_INTEGRACAO.md   # Documentação técnica e integrações
├── LICENSE                         # Licença MIT
└── MotoConnect.png                # Banner do projeto
```

## Entrega Final e Checklist do 3º Sprint

### Entregáveis obrigatórios

- [ ] **Vídeo final (YouTube):** apresentar em ~5 minutos o fluxo completo IoT → MQTT → Backend → Dashboard (inserir link na entrega).
- [x] **Repositório Git:** este repositório atualizado com instruções e código-fonte.
- [ ] **Pacote `.zip` final:** incluir `README.md`, `GUIA_EXECUCAO.md`, pasta `docs/`, `app.py`, `rfid_dashboard.html`, `rfid_simulado_simples.ino`, `requirements.txt`, `start_backend.sh`, `start_backend.bat` e o link do vídeo.

Para gerar o pacote:

```bash
zip -r MotoConnect-IoT-final.zip README.md GUIA_EXECUCAO.md docs app.py rfid_dashboard.html rfid_simulado_simples.ino requirements.txt start_backend.sh start_backend.bat
```

### Rubrica oficial (3º sprint)

| Critério | Pontos | Evidência |
|----------|--------|-----------|
| Funcionalidade técnica ponta a ponta | até 60 pts | Fluxo em tempo real do ESP32 → MQTT → Flask → SQLite → Dashboard com alertas. |
| Integração com demais disciplinas | até 20 pts | APIs REST documentadas, banco SQLite, guia `docs/ARQUITETURA_INTEGRACAO.md`, scripts DevOps. |
| Apresentação em vídeo | até 10 pts | Vídeo final demonstrando dispositivos, backend e dashboard integrados. |
| Organização do repositório e documentação | até 10 pts | README, GUIA_EXECUCAO, pasta `docs/` e scripts atualizados. |

### Penalidades a evitar

- Ausência de vídeo explicativo com todos os membros (`-20 pts`).
- Código inconsistente com o vídeo apresentado (`-30 pts`).
- Projeto sem conexão clara com o desafio da Mottu (`-60 pts`).
- Interface inoperável ou dados não fluindo corretamente (`-40 pts`).

### Checklist técnico ✅

- [x] **3+ sensores/atuadores distintos** (RFID, bateria, DHT22 + LED RGB e buzzer).
- [x] **Comunicação MQTT em tempo real** (`motoconnect/telemetry` + comandos `motoconnect/commands/{tag_id}`).
- [x] **Persistência** em `telemetry.db` (SQLite) e `telemetry_log.json` (auditoria).
- [x] **Dashboard** com mapa do pátio, gráficos, histórico, envio de comandos e painel de alertas em tempo real.
- [x] **Alertas automáticos** (bateria baixa, temperatura crítica, bloqueio/área incorreta) exibidos e contabilizados.
- [x] **APIs para integrações externas** (`/api/summary`, `/api/history`, `/api/motos/<tag_id>`).
- [x] **3 dispositivos IoT simultâneos** simulados no Wokwi com `client_id` exclusivos.
- [x] **Casos de uso validados**: moto desaparecida, moto fora de área, bloqueio/desbloqueio remoto e monitoramento ambiental.

## Documentação Complementar

- **[GUIA_EXECUCAO.md](GUIA_EXECUCAO.md)**: Passo a passo detalhado de como rodar o sistema
- **[docs/ARQUITETURA_INTEGRACAO.md](docs/ARQUITETURA_INTEGRACAO.md)**: Arquitetura completa, integrações (mobile/Java/.NET/BI) e orientações DevOps

## Contribuições

Este projeto foi desenvolvido como parte do Challenge 2025 da Mottu. Contribuições são bem-vindas através de pull requests. Para mudanças maiores, por favor abra uma issue primeiro para discutir o que você gostaria de mudar.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

---

Desenvolvido para o Challenge 2025 da Mottu | 2º Ano - Análise e Desenvolvimento de Sistemas
