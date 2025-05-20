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
│  Frontend       │◀────│  API Backend    │◀────│  Banco de Dados │
│  (Mapa do Pátio)│     │  (Node.js)      │     │                 │
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

### Hardware
- **Etiquetas RFID**: Tags passivas para identificação das motos
- **Leitores RFID**: Simulados por botões no projeto atual (Arduino UNO)
- **Gateway IoT**: Representado pelo Arduino no ambiente de simulação

### Software
- **Simulador**: Código Arduino para simular leituras RFID
- **Dashboard**: Interface web HTML/CSS/JavaScript para visualização de dados

## Simulação no Wokwi

Para fins de demonstração e desenvolvimento, criamos uma versão simplificada no Wokwi:

### Versão Simplificada
- Utiliza Arduino UNO com botões para simular leituras RFID
- Exibe dados no monitor serial
- Demonstra o conceito sem dependências externas

#### Arquivos da Simulação
- `rfid_simulado_simples.ino`: Código da versão simplificada para Arduino UNO
- `Instruções para Simulação de Leitor RFID no Wokwi (Versão Simplificada) (1).md`: Documentação detalhada

## Dashboard

O sistema inclui um dashboard web para visualização em tempo real:

### Dashboard Web
- Interface web em HTML/CSS/JavaScript (`rfid_dashboard.html`)
- Visualização responsiva para desktop e dispositivos móveis

#### Funcionalidades do Dashboard
- Mapa interativo do pátio com posição das motos
- Tabela de histórico de leituras
- Gráficos estatísticos (status das motos, leituras por localização)
- Alertas visuais para eventos importantes

## Instalação e Configuração

### Simulação no Wokwi

1. Acesse [Wokwi](https://wokwi.com/new/arduino-uno) e crie um novo projeto Arduino UNO
2. Copie o código do arquivo `rfid_simulado_simples.ino`
3. Configure o diagrama com 4 botões (pinos 2-5) e 1 LED (pino 13)
4. Inicie a simulação e teste usando os botões ou o monitor serial

Para detalhes completos de configuração, consulte o arquivo `Instruções para Simulação de Leitor RFID no Wokwi (Versão Simplificada) (1).md`.

### Dashboard Web

1. Abra o arquivo `rfid_dashboard.html` em um navegador web
2. Para uma experiência completa, você precisará conectar o dashboard ao simulador (isso está além do escopo desta demonstração)

## Uso

### Simulação de Leituras RFID

- Clique nos botões 1-4 para simular diferentes tags RFID
- Ou digite números 1-4 no monitor serial e pressione Enter
- Observe as informações da moto no monitor serial

### Formato dos Dados

Quando uma leitura é simulada, o seguinte formato JSON é gerado:

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

## Contribuições

Este projeto foi desenvolvido como parte do Challenge 2025 da Mottu. Contribuições são bem-vindas através de pull requests. Para mudanças maiores, por favor abra uma issue primeiro para discutir o que você gostaria de mudar.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

---

Desenvolvido para o Challenge 2025 da Mottu | 2º Ano - Análise e Desenvolvimento de Sistemas
