
import json
import time
import argparse
from pathlib import Path

import paho.mqtt.client as mqtt


# ==========================================
# CONFIGURAÇÕES DO PROJETO
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "dados"

BROKER_HOST = "localhost"
BROKER_PORT = 1883

# Deve ser igual à API Key configurada no IoT Agent
API_KEY = "vacinas"

INTERVALO = 5  # Segundos entre cada envio

# Faixa de temperatura utilizada na simulação
TEMP_MIN_NORMAL = 3.0
TEMP_MAX_NORMAL = 7.0
TEMP_MIN_CRITICA = 2.0
TEMP_MAX_CRITICA = 8.0


# ==========================================
# CLASSIFICAÇÃO DA TEMPERATURA
# ==========================================

def verificar_status(temperatura):

    if temperatura < TEMP_MIN_CRITICA or temperatura > TEMP_MAX_CRITICA:
        return "critico"

    elif temperatura < TEMP_MIN_NORMAL or temperatura > TEMP_MAX_NORMAL:
        return "atencao"

    return "normal"


# ==========================================
# LEITURA DOS ARQUIVOS JSON
# ==========================================

def carregar_dados(nome_arquivo):

    caminho = DATA_DIR / nome_arquivo

    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if not isinstance(dados, list):
            raise ValueError("O arquivo deve conter uma lista JSON.")

        return dados

    except FileNotFoundError:
        print(f"[ERRO] Arquivo não encontrado: {caminho}")
        raise SystemExit(1)

    except json.JSONDecodeError as erro:
        print(f"[ERRO] JSON inválido: {erro}")
        raise SystemExit(1)


# ==========================================
# CONEXÃO COM O MQTT
# ==========================================

def conectar_mqtt():

    cliente = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="simulador_vacinas"
    )

    try:
        print("[MQTT] Conectando ao broker...")

        cliente.connect(
            BROKER_HOST,
            BROKER_PORT,
            keepalive=60
        )

        cliente.loop_start()

        print("[MQTT] Conectado com sucesso!")

        return cliente

    except Exception as erro:
        print(f"[ERRO MQTT] Não foi possível conectar: {erro}")
        raise SystemExit(1)


# ==========================================
# ENVIO DOS DADOS
# ==========================================

def enviar_temperatura(cliente, registro):

    temperatura = float(registro["temperatura"])

    status = verificar_status(temperatura)

    sensor = registro["sensor"]

    # Tópico esperado pelo IoT Agent MQTT
    topico = f"/{API_KEY}/{sensor}/attrs"

    # Dados enviados ao IoT Agent
    mensagem = {
        "temperatura": temperatura,
        "umidade": float(registro["umidade"]),
        "status": status,
        "ubs": registro["ubs"],
        "refrigerador": registro["refrigerador"],
        "sensor": sensor,
        "data_hora": registro.get("data_hora", "")
    }

    payload = json.dumps(mensagem, ensure_ascii=False)

    try:
        resultado = cliente.publish(
            topico,
            payload,
            qos=1
        )

        resultado.wait_for_publish(timeout=10)

        if not resultado.is_published():
            print("[ERRO] A publicação não foi confirmada.")
            return

        print("\n====================================")
        print(f"UBS: {registro['ubs']}")
        print(f"Refrigerador: {registro['refrigerador']}")
        print(f"Sensor: {sensor}")
        print(f"Temperatura: {temperatura} °C")
        print(f"Umidade: {registro['umidade']}%")
        print(f"Status: {status.upper()}")
        print(f"Tópico: {topico}")
        print("Mensagem enviada com sucesso!")
        print("====================================")

    except Exception as erro:
        print(f"[ERRO] Falha no envio MQTT: {erro}")


# ==========================================
# EXECUÇÃO DO SIMULADOR
# ==========================================

def executar_simulador(nome_arquivo, intervalo, repetir):

    dados = carregar_dados(nome_arquivo)

    if not dados:
        print("[AVISO] Não existem registros para enviar.")
        return

    cliente = conectar_mqtt()

    print("\nSIMULADOR DE TEMPERATURA DE VACINAS")
    print(f"Total de registros: {len(dados)}")
    print(f"Intervalo: {intervalo} segundos")
    print(f"Repetição: {'Sim' if repetir else 'Não'}")

    try:

        while True:

            for registro in dados:

                enviar_temperatura(cliente, registro)

                time.sleep(intervalo)

            if not repetir:
                break

            print("\n[SIMULADOR] Reiniciando os registros...\n")

    except KeyboardInterrupt:
        print("\n[SIMULADOR] Execução interrompida.")

    finally:
        cliente.disconnect()
        cliente.loop_stop()
        print("[MQTT] Conexão encerrada.")


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Simulador MQTT de temperatura de vacinas"
    )

    parser.add_argument(
        "--arquivo",
        default="historico.json",
        choices=["historico.json", "temperaturas.json"],
        help="Arquivo JSON utilizado na simulação"
    )

    parser.add_argument(
        "--intervalo",
        type=int,
        default=INTERVALO,
        help="Intervalo entre os envios em segundos"
    )

    parser.add_argument(
        "--repetir",
        action="store_true",
        help="Repetir os registros continuamente"
    )

    args = parser.parse_args()

    if args.intervalo < 1:
        parser.error("O intervalo deve ser de pelo menos 1 segundo.")

    executar_simulador(
        args.arquivo,
        args.intervalo,
        args.repetir
    )
