# Arquitetura, Integrações e Fluxo de Dados — MotoConnect IoT

Este documento consolida a visão ponta a ponta da solução entregue no 3º sprint do Challenge Mottu. O objetivo é evidenciar o fluxo completo de dados (captura → backend → persistência → visualização), as integrações disponibilizadas para outras disciplinas (mobile, Java, .NET, Banco de Dados e DevOps) e os artefatos necessários para a entrega final.

## 1. Visão Geral da Arquitetura

```mermaid
graph LR
    subgraph Patio
        A[Etiquetas RFID nas motos]
        B[Leitores RFID / ESP32]
        C[Sensores adicionais (Bateria, DHT22)]
    end

    A --> B -->|MQTT/JSON| D((Broker HiveMQ))
    D -->|MQTT subscribe| E[Backend Flask]
    E -->|SQLite| F[(telemetry.db)]
    E -->|REST/JSON| G[Dashboard Web]
    E -->|REST/JSON| H[Mobile App]
    E -->|REST/JSON| I[Serviços Java/.NET]
    E -->|Logs| J[(telemetry_log.json)]
```

## 2. Fluxo de Dados Ponta a Ponta

1. **Captura (IoT / Visão Computacional):** O firmware `rfid_simulado_simples.ino` emula três sensores (RFID, bateria e DHT22) e dois atuadores (LED RGB e buzzer). Cada leitura é serializada em JSON e publicada no tópico `motoconnect/telemetry` do HiveMQ.
2. **Gateway/Backend (Flask + MQTT):** `app.py` assina o tópico, enriquece o payload com timestamp do servidor, calcula alertas em tempo real (bateria baixa, temperatura crítica, localização incorreta ou bloqueio ativo) e persiste os dados em duas camadas:
   - **Arquivo** `telemetry_log.json` (compatibilidade e auditoria)
   - **Banco de dados** `telemetry.db` (SQLite) para consultas estruturadas
3. **Persistência e APIs:** O backend expõe endpoints REST (`/api/status`, `/api/summary`, `/api/history`, `/api/motos/<tag_id>`, `/api/command`) consumidos pelo dashboard e por integrações externas.
4. **Visualização (Dashboard Web):** `rfid_dashboard.html` renderiza mapa do pátio, estado de cada moto, gráficos de status/localização, histórico e um painel dedicado a alertas em tempo real.
5. **Integrações Multidisciplinares:** APIs documentadas sustentam o consumo por aplicações mobile (React Native/Flutter), serviços Java/.NET e pipelines DevOps.

## 3. Componentes Entregues

| Componente | Descrição | Disciplina | Evidência |
|------------|-----------|------------|-----------|
| Firmware IoT (`rfid_simulado_simples.ino`) | Publica telemetria e executa comandos BLOCK/UNBLOCK (atuando em LEDs e buzzer). | IoT/Embarcados | Código + simulação Wokwi |
| Backend (`app.py`) | MQTT + REST, persistência em SQLite, geração de alertas, APIs para integrações. | Backend / DevOps | Scripts `start_backend.sh/.bat` |
| Banco de Dados (`telemetry.db`) | Tabela `telemetry` com índices por tag e timestamp. | Banco de Dados | Migração automática em `init_storage()` |
| Dashboard (`rfid_dashboard.html`) | Visualização em tempo real, painel de alertas, filtros e relatórios. | Frontend | Hospedado via Flask |
| Documentação (`README.md`, `GUIA_EXECUCAO.md`, `docs/ARQUITETURA_INTEGRACAO.md`) | Guia de execução, arquitetura e integração multidisciplinar. | Comunicação Técnica | Repositório Git |

## 4. Esquema do Banco de Dados (SQLite)

Tabela criada automaticamente pelo backend:

```sql
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
);
```

Índices criados para desempenho:

```sql
CREATE INDEX IF NOT EXISTS idx_telemetry_tag ON telemetry(tag_id);
CREATE INDEX IF NOT EXISTS idx_telemetry_server_ts ON telemetry(server_timestamp);
```

## 5. Catálogo de APIs REST

| Endpoint | Método | Finalidade | Consumidores |
|----------|--------|------------|--------------|
| `/api/status` | GET | Lista em ordem cronológica as últimas leituras de cada moto (utilizado pelo dashboard). | Dashboard Web, Mobile |
| `/api/summary` | GET | Retorna total de motos, contagem por status, alertas ativos e timestamp da última atualização. | Mobile, Painéis externos |
| `/api/history?limit=200` | GET | Consulta histórico persistido no SQLite para análises avançadas ou exportação. | BI, Data Science |
| `/api/motos/<tag_id>` | GET | Detalha a última telemetria registrada para uma moto específica (lookup rápido). | Aplicativos de suporte, chatbot |
| `/api/command` | POST | Envia comandos BLOCK/UNBLOCK via MQTT (retorno JSON de sucesso/erro). | Dashboard, App Mobile |

## 6. Integração com Outras Disciplinas

### 6.1 Mobile App (React Native / Flutter)
- Consumir `/api/summary` para exibir contagem de motos disponíveis, em manutenção e alertas ativos.
- Consumir `/api/motos/<tag_id>` para mostrar detalhes da última leitura (status, bateria, temperatura) em telas de inspeção.
- Enviar bloqueios/desbloqueios utilizando `/api/command` (corpo `{ "tag_id": "04A5B9C2", "command": "BLOCK" }`).

### 6.2 Backend Java (Spring Boot)
```java
WebClient client = WebClient.create("http://localhost:5000");
SummaryResponse summary = client.get()
    .uri("/api/summary")
    .retrieve()
    .bodyToMono(SummaryResponse.class)
    .block();
```
- O serviço pode persistir dados adicionais em um banco relacional corporativo ou expor APIs GraphQL.
- Utilizar `/api/history` para job de ETL diário.

### 6.3 Serviços .NET (C#)
```csharp
using var http = new HttpClient { BaseAddress = new Uri("http://localhost:5000") };
var json = await http.GetStringAsync("/api/motos/04A5B9C2");
var moto = JsonSerializer.Deserialize<MotoStatus>(json);
```
- Integrar com sistemas de manutenção preventiva em .NET, disparando alertas via Teams/Outlook quando `alert_level == "danger"`.

### 6.4 Banco de Dados / BI
- `telemetry.db` pode ser consumido via Power BI, DBeaver ou scripts Python (`sqlite3`).
- Consulta rápida para métricas de utilização:
  ```sql
  SELECT status, COUNT(*)
  FROM telemetry
  WHERE server_timestamp >= strftime('%s','now','-1 day')
  GROUP BY status;
  ```

### 6.5 DevOps & Observabilidade
- Scripts `start_backend.sh` e `start_backend.bat` facilitam execução local e em pipelines CI.
- Deploy cloud: containerizar com Gunicorn + Nginx; broker MQTT pode ser um cluster EMQX gerenciado.
- Monitoramento: expor métricas básicas (latência calculada no dashboard) e logs estruturados.
- Segurança operacional: utilizar broker MQTT com TLS e credenciais isoladas, ajustando o backend Flask e o firmware para carregar certificados.

## 7. Entregáveis do 3º Sprint

| Entregável | Descrição |
|------------|-----------|
| Vídeo final (YouTube) | Apresentação de ~5 minutos demonstrando IoT + backend + dashboard em tempo real (link referenciado no README). |
| Repositório Git | Código-fonte completo, documentação e scripts. |
| Artefatos para zip | `README.md`, `GUIA_EXECUCAO.md`, pasta `docs/`, vídeo link e instruções de execução. |

## 8. Próximos Passos / Evoluções

- **Infraestrutura:** provisionar pipeline GitHub Actions com testes automatizados e empacotamento Docker.
- **Telemetria avançada:** adicionar cálculos de SLA de leitura e consumo energético.
- **Mobile offline:** armazenar resumo localmente para operação em pátios sem rede.
- **Integração corporativa:** publicar eventos em um barramento (Kafka/Azure Service Bus) consumido por sistemas de CRM.

---

> Este documento complementa o `README.md` e o `GUIA_EXECUCAO.md`, fornecendo uma visão consolidada das integrações e da maturidade técnica exigida na fase final do Challenge IoT da Mottu.
