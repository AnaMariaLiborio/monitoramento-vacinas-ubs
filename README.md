# monitoramento-vacinas-ubs
Projeto para monitoramento de temperatura 
# 🌡️ Monitoramento Inteligente da Temperatura de Vacinas nas UBS de Natal – RN

## 1. Sobre o projeto

O projeto consiste no desenvolvimento de uma solução baseada em Internet das Coisas (IoT) para monitorar a temperatura dos refrigeradores utilizados no armazenamento de vacinas nas Unidades Básicas de Saúde (UBS) de Natal – RN.

A solução utiliza componentes da plataforma FIWARE para receber, processar, armazenar e disponibilizar os dados de temperatura em tempo real.

O objetivo é facilitar o acompanhamento das condições de armazenamento, identificar possíveis alterações de temperatura e emitir alertas quando os valores estiverem fora dos limites estabelecidos.

**Observação:** os dados de temperatura utilizados inicialmente são fictícios e destinados exclusivamente à simulação e aos testes acadêmicos.

## 2. Objetivos

- Monitorar a temperatura dos refrigeradores de vacinas.
- Receber dados dos sensores por meio do protocolo MQTT.
- Integrar os dispositivos à plataforma FIWARE.
- Armazenar o histórico das temperaturas.
- Identificar temperaturas fora dos limites configurados.
- Gerar alertas para situações de risco.
- Disponibilizar informações em um dashboard.

## 3. Tecnologias utilizadas

| Tecnologia | Função |
|---|---|
| ESP32 | Microcontrolador responsável pela leitura dos sensores. |
| Sensor de temperatura | Realizar as medições nos refrigeradores. |
| MQTT | Protocolo de comunicação dos dispositivos. |
| Mosquitto | Broker MQTT. |
| IoT Agent MQTT | Integrar os dispositivos ao Orion. |
| Orion Context Broker | Gerenciar os dados em tempo real. |
| QuantumLeap | Registrar o histórico das medições. |
| CrateDB | Armazenar séries temporais. |
| Draco | Integrar, transformar e encaminhar dados. |
| MongoDB | Armazenamento de dados de contexto/configuração do ambiente. |
| Grafana | Visualizar os dados e acompanhar os alertas. |
| Docker | Executar e gerenciar os serviços. |

## 4. Arquitetura do sistema

Fluxo principal:

**ESP32 + Sensor → Mosquitto → IoT Agent MQTT → Orion → QuantumLeap → CrateDB → Grafana**

O Draco será utilizado como componente complementar para integração e transformação dos dados.

### Responsabilidade de cada componente

**IoT Agent MQTT**
- Receber as mensagens MQTT.
- Integrar os dispositivos à plataforma FIWARE.
- Encaminhar as informações ao Orion.

**Orion Context Broker**
- Gerenciar os dados recebidos.
- Atualizar as informações dos refrigeradores.
- Disponibilizar os dados para consulta.

**QuantumLeap**
- Registrar as alterações dos dados.
- Manter o histórico das temperaturas.
- Permitir consultas temporais.

**Draco**
- Integrar diferentes fontes de dados.
- Transformar informações.
- Encaminhar dados para sistemas externos.

**Grafana**
- Apresentar as temperaturas atuais.
- Exibir gráficos históricos.
- Mostrar a situação dos refrigeradores.
- Facilitar o acompanhamento dos alertas.

## 5. Dados fictícios para simulação

Foram criados dez refrigeradores distribuídos em cinco UBS fictícias de Natal.

| UBS | Refrigerador | Temperatura | Situação |
|---|---|---:|---|
| UBS Alecrim | REF-001 | 4,5 °C | Normal |
| UBS Alecrim | REF-002 | 5,2 °C | Normal |
| UBS Tirol | REF-003 | 7,4 °C | Atenção |
| UBS Tirol | REF-004 | 4,1 °C | Normal |
| UBS Cidade Nova | REF-005 | 8,6 °C | Crítico |
| UBS Cidade Nova | REF-006 | 5,0 °C | Normal |
| UBS Pajuçara | REF-007 | 2,5 °C | Atenção |
| UBS Pajuçara | REF-008 | 3,8 °C | Normal |
| UBS Lagoa Nova | REF-009 | 6,2 °C | Normal |
| UBS Lagoa Nova | REF-010 | 9,1 °C | Crítico |

### 5.1. Critérios de classificação

Para a simulação, serão utilizados os seguintes parâmetros:

| Temperatura | Classificação |
|---|---|
| Entre 3 °C e 7 °C | Normal |
| Abaixo de 3 °C ou acima de 7 °C, mas dentro de 2 °C a 8 °C | Atenção |
| Abaixo de 2 °C ou acima de 8 °C | Crítico |

Os limites devem ser validados com os responsáveis técnicos antes de qualquer utilização operacional.

## 6. Exemplo de mensagem MQTT

Exemplo de dados enviados por um dispositivo:

```json
{
  "ubs": "UBS_CIDADE_NOVA",
  "refrigerador": "REF_005",
  "sensor": "SENSOR_005",
  "temperatura": 8.6,
  "umidade": 52,
  "status": "critico",
  "data_hora": "2026-11-13T10:30:00-03:00"
}
```

Os dados serão utilizados para testar a comunicação entre os dispositivos e os componentes FIWARE.

## 7. Histórico de temperatura

Exemplo de medições simuladas do refrigerador REF-001:

| Horário | Temperatura |
|---|---:|
| 06:00 | 4,2 °C |
| 07:00 | 4,4 °C |
| 08:00 | 4,5 °C |
| 09:00 | 4,7 °C |
| 10:00 | 5,0 °C |
| 11:00 | 5,3 °C |
| 12:00 | 5,6 °C |
| 13:00 | 5,4 °C |
| 14:00 | 5,1 °C |
| 15:00 | 4,9 °C |
| 16:00 | 4,6 °C |
| 17:00 | 4,4 °C |

## 8. Simulação de situações críticas

Também serão testadas situações em que o refrigerador apresenta alterações de temperatura.

| Horário | Temperatura | Situação |
|---|---:|---|
| 08:00 | 5,0 °C | Normal |
| 09:00 | 6,2 °C | Normal |
| 10:00 | 7,3 °C | Atenção |
| 11:00 | 8,2 °C | Crítico |
| 12:00 | 9,1 °C | Crítico |
| 13:00 | 8,5 °C | Crítico |
| 14:00 | 7,5 °C | Atenção |
| 15:00 | 6,0 °C | Normal |

## 9. Funcionalidades previstas

- [ ] Comunicação dos sensores via MQTT.
- [ ] Integração do IoT Agent MQTT com o Orion.
- [ ] Atualização das temperaturas em tempo real.
- [ ] Integração do QuantumLeap.
- [ ] Armazenamento histórico no CrateDB.
- [ ] Integração complementar com Draco.
- [ ] Desenvolvimento do dashboard no Grafana.
- [ ] Implementação de alertas de temperatura.
- [ ] Identificação de sensores sem comunicação.
- [ ] Geração de relatórios por UBS.

## 10. Etapas de desenvolvimento

1. Preparar o ambiente com Docker.
2. Configurar o broker Mosquitto.
3. Configurar o IoT Agent MQTT.
4. Integrar o IoT Agent ao Orion.
5. Configurar o QuantumLeap e o CrateDB.
6. Integrar o Draco.
7. Implementar os dados simulados.
8. Desenvolver o dashboard no Grafana.
9. Realizar testes de comunicação e alertas.

## 11. Considerações finais

A solução busca demonstrar como a Internet das Coisas e a plataforma FIWARE podem contribuir para a modernização dos serviços de saúde pública.

Com o monitoramento inteligente, será possível acompanhar as condições dos refrigeradores, identificar situações de risco e disponibilizar informações para apoiar a gestão da Rede de Frio.

**Projeto acadêmico – Cidades Inteligentes e Internet das Coisas (IoT).**

**Local de aplicação proposto:** Natal – Rio Grande do Norte.

**Importante:** os dados apresentados são fictícios e não representam medições reais ou condições de funcionamento de unidades de saúde.
