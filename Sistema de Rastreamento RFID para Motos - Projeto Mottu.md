# Sistema de Rastreamento RFID para Motos - Projeto Mottu

![Banner do Projeto](https://i.imgur.com/placeholder.jpg)

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Desafio](#desafio)
- [Solução Proposta](#solução-proposta)
- [Arquitetura](#arquitetura)
- [Componentes](#componentes)
- [Simulação no Wokwi](#simulação-no-wokwi)
- [Dashboard](#dashboard)
- [Instalação e Configuração](#instalação-e-configuração)
- [Uso](#uso)
- [Expansão para Ambiente Real](#expansão-para-ambiente-real)
- [Contribuições](#contribuições)
- [Licença](#licença)

## 🔍 Visão Geral

Este projeto implementa um sistema de rastreamento de motos utilizando tecnologia RFID (Identificação por Radiofrequência), desenvolvido para o Challenge 2025 da Mottu. O sistema permite identificar e mapear a localização de motos dentro dos pátios da empresa, fornecendo visualização em tempo real através de um dashboard interativo.

## 🎯 Desafio

A Mottu enfrenta o desafio de gerenciar frotas de motos em pátios de múltiplas filiais. Atualmente, a localização das motos dentro desses pátios é controlada manualmente, gerando imprecisões e impactando a eficiência operacional. Com mais de 100 filiais espalhadas por diferentes regiões, é fundamental aprimorar o processo de monitoramento e gestão das motos.

**Objetivos:**
- Identificar com precisão a localização das motos dentro dos pátios
- Fornecer visualização em tempo real da disposição das motos
- Criar uma solução escalável para implementação em todas as filiais
- Integrar com sensores IoT das motos para informações adicionais

## 💡 Solução Proposta

Nossa solução utiliza etiquetas RFID fixadas nas motos e leitores RFID estrategicamente posicionados nos pátios. Quando uma moto passa próxima a um leitor, o sistema registra sua localização e atualiza o dashboard em tempo real.

**Benefícios:**
- **Precisão alta**: Sem necessidade de câmeras ou visão computacional
- **Baixo custo operacional**: Após implantação inicial
- **Automação**: Atualização de posições sem intervenção humana
- **Escalabilidade**: Facilmente adaptável para 100+ filiais

## 🏗️ Arquitetura

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
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │     │                 │
│  Frontend       │◀────│  API Backend    │◀────│  Processamento  │◀────│  Banco de Dados │
│  (Mapa do Pátio)│     │  (Node.js)      │     │  (Análise/IA)   │     │  (Oracle)       │
│                 │     │                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

O fluxo de dados ocorre da seguinte forma:
1. Etiquetas RFID nas motos são lidas pelos leitores RFID
2. Os leitores enviam os dados para o Gateway IoT
3. O Gateway processa e envia os dados para a plataforma Cloud via MQTT
4. Os dados são processados, armazenados no banco Oracle e disponibilizados via API
5. O dashboard frontend exibe a localização das motos em tempo real

## 🔧 Componentes

### Hardware
- **Etiquetas RFID**: Tags UHF passivas resistentes para veículos
- **Leitores RFID**: Leitores fixos UHF (como Impinj Speedway) ou leitores USB portáteis
- **Gateway IoT**: Dispositivos edge com capacidade de processamento local

### Software
- **Backend**: API em Node.js
- **Banco de Dados**: Oracle (requisito do challenge)
- **Frontend**: Dashboard em ReactJS
- **Comunicação**: Protocolo MQTT para transmissão de dados em tempo real

## 💻 Simulação no Wokwi

Para fins de demonstração e desenvolvimento, criamos duas versões de simulação no Wokwi:

### Versão Completa (requer assinatura Wokwi)
- Utiliza ESP32 com módulo RFID MFRC522
- Implementa comunicação MQTT com broker público
- Simula leitura de tags RFID e envio de dados para dashboard

### Versão Simplificada (sem necessidade de assinatura)
- Utiliza Arduino UNO com botões para simular leituras RFID
- Exibe dados no monitor serial
- Demonstra o conceito sem dependências externas

#### Arquivos da Simulação
- `rfid_esp32_wokwi.ino`: Código da versão completa para ESP32
- `rfid_simulado_simples.ino`: Código da versão simplificada para Arduino UNO

## 📊 Dashboard

O sistema inclui duas opções de dashboard para visualização em tempo real:

### Dashboard Node-RED
- Fluxo completo para Node-RED
- Visualização de tabela de leituras, gráficos e mapa do pátio
- Conexão via MQTT com o simulador ou hardware real

### Dashboard Web Standalone
- Interface web em HTML/CSS/JavaScript
- Conexão direta ao broker MQTT
- Visualização responsiva para desktop e dispositivos móveis

#### Funcionalidades do Dashboard
- Mapa interativo do pátio com posição das motos
- Tabela de histórico de leituras
- Gráficos estatísticos (status das motos, leituras por localização)
- Alertas visuais para eventos importantes

## 🚀 Instalação e Configuração

### Simulação no Wokwi

#### Versão Simplificada (Arduino UNO)
1. Acesse [Wokwi](https://wokwi.com/new/arduino-uno) e crie um novo projeto Arduino UNO
2. Copie o código do arquivo `rfid_simulado_simples.ino`
3. Configure o diagrama com 4 botões (pinos 2-5) e 1 LED (pino 13)
4. Inicie a simulação e teste usando os botões ou o monitor serial

#### Versão Completa (ESP32 + MFRC522)
1. Acesse [Wokwi](https://wokwi.com/new/esp32) e crie um novo projeto ESP32
2. Copie o código do arquivo `rfid_esp32_wokwi.ino`
3. Configure o diagrama conforme o arquivo `diagram.json`
4. Adicione as bibliotecas necessárias no arquivo `libraries.txt`
5. Inicie a simulação e teste usando o console do navegador para simular tags RFID

### Dashboard

#### Dashboard Node-RED
1. Instale o Node-RED:
   ```bash
   npm install -g --unsafe-perm node-red
   ```
2. Instale os nós adicionais:
   ```bash
   npm install -g node-red-dashboard
   npm install -g node-red-contrib-mqtt-broker
   npm install -g node-red-contrib-aedes
   ```
3. Inicie o Node-RED:
   ```bash
   node-red
   ```
4. Acesse a interface do Node-RED em http://localhost:1880
5. Importe o fluxo JSON do arquivo `mqtt_dashboard_config.md`
6. Clique em "Deploy" para ativar o fluxo
7. Acesse o dashboard em http://localhost:1880/ui

#### Dashboard Web
1. Salve o código HTML do arquivo `dashboard_implementation.md` como `index.html`
2. Abra o arquivo em um navegador web
3. Verifique se o dashboard se conecta ao broker MQTT

## 📝 Uso

### Simulação de Leituras RFID

#### Versão Simplificada
- Clique nos botões 1-4 para simular diferentes tags RFID
- Ou digite números 1-4 no monitor serial e pressione Enter
- Observe as informações da moto no monitor serial

#### Versão Completa
- Use o console do navegador para simular tags RFID:
  ```javascript
  const rfid = wokwi.pins.rfid1;
  rfid.simulateTag({ uid: [0x04, 0xA5, 0xB9, 0xC2] });
  ```
- Observe os dados sendo enviados via MQTT
- Verifique a atualização em tempo real no dashboard

### Dashboard
- Visualize a posição das motos no mapa do pátio
- Consulte o histórico de leituras na tabela
- Analise as estatísticas nos gráficos
- Filtre as informações conforme necessário

## 🌐 Expansão para Ambiente Real

Para implementar este sistema em um ambiente real, seriam necessários os seguintes passos:

1. **Hardware Físico**:
   - Adquirir etiquetas RFID UHF para as motos
   - Instalar leitores RFID fixos nas entradas, saídas e pontos estratégicos
   - Configurar gateways IoT para processamento local e comunicação

2. **Infraestrutura de Rede**:
   - Estabelecer rede WiFi ou Ethernet para os leitores
   - Configurar VPN para comunicação segura com a nuvem
   - Implementar redundância para garantir operação contínua

3. **Backend e Cloud**:
   - Configurar broker MQTT privado com autenticação
   - Implementar API Node.js completa com autenticação
   - Configurar banco de dados Oracle para armazenamento persistente

4. **Segurança**:
   - Implementar autenticação e autorização em todos os níveis
   - Criptografar dados em trânsito e em repouso
   - Estabelecer políticas de backup e recuperação

5. **Expansão Gradual**:
   - Iniciar com projeto piloto em uma filial
   - Validar e ajustar conforme necessário
   - Expandir para demais filiais com base nas lições aprendidas

## 👥 Contribuições

Este projeto foi desenvolvido como parte do Challenge 2025 da Mottu. Contribuições são bem-vindas através de pull requests. Para mudanças maiores, por favor abra uma issue primeiro para discutir o que você gostaria de mudar.

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

---

Desenvolvido para o Challenge 2025 da Mottu | 2º Ano - Análise e Desenvolvimento de Sistemas
