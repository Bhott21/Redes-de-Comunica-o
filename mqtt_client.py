import psutil
import json
from Crypto.Cipher import AES
import base64
import os
import paho.mqtt.client as mqtt
import time
import ssl

# Configurações
MQTT_BROKER = "maqiatto.com"
MQTT_PORT = 1883  # Use 8883 para SSL
TOPIC_COMANDO = "bernardohrocha21@gmail.com/redes1/comando"
TOPIC_RESPOSTA = "bernardohrocha21@gmail.com/redes1/resposta"
MQTT_USER = "bernardohrocha21@gmail.com"
MQTT_PASS = "SenhaDificil"

# Criptografia
SECRET_KEY = b"1234567890abcdef"
IV = os.urandom(16)

def encrypt_message(message: str) -> str:
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    padded_message = message + (16 - len(message) % 16) * " "
    encrypted_bytes = cipher.encrypt(padded_message.encode('utf-8'))
    return base64.b64encode(IV + encrypted_bytes).decode('utf-8')

def get_system_info():
    """Coleta informações detalhadas do sistema"""
    return {
        'cpu': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent,
        'processes': [p.info for p in psutil.process_iter(['pid', 'name', 'cpu_percent'])],
        'timestamp': time.time()
    }

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("✅ Conectado ao broker!")
        client.subscribe(TOPIC_COMANDO, qos=1)
        print(f"👂 Aguardando comandos em: {TOPIC_COMANDO}")
    else:
        print(f"❌ Falha na conexão. Código: {rc}")

def on_message(client, userdata, msg):
    if msg.topic == TOPIC_COMANDO:
        try:
            comando = msg.payload.decode()
            if comando == "SOLICITAR_DADOS":
                print("📩 Recebida solicitação de dados...")
                data = get_system_info()
                encrypted_data = encrypt_message(json.dumps(data))
                client.publish(TOPIC_RESPOSTA, encrypted_data, qos=1)
                print("📤 Dados enviados para o servidor")
        except Exception as e:
            print(f"⚠️ Erro ao processar comando: {str(e)}")

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    
    # Configuração SSL (descomente se usar porta 8883)
    # client.tls_set(tls_version=ssl.PROTOCOL_TLS)
    # client.tls_insecure_set(True)
    
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print("🔌 Cliente pronto para receber solicitações")
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n🛑 Cliente encerrado")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()