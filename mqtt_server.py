import paho.mqtt.client as mqtt
from Crypto.Cipher import AES
import base64
import json
import time

# Configurações
MQTT_BROKER = "maqiatto.com"
MQTT_PORT = 1883
TOPIC_COMANDO = "bernardohrocha21@gmail.com/redes1/comando"
TOPIC_RESPOSTA = "bernardohrocha21@gmail.com/redes1/resposta"
MQTT_USER = "bernardohrocha21@gmail.com"
MQTT_PASS = "SenhaDificil"

SECRET_KEY = b"1234567890abcdef"

def decrypt_message(encrypted_message: str) -> str:
    encrypted_data = base64.b64decode(encrypted_message)
    IV = encrypted_data[:16]
    encrypted_bytes = encrypted_data[16:]
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    return cipher.decrypt(encrypted_bytes).decode('utf-8').rstrip()

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("✅ Servidor conectado!")
        client.subscribe(TOPIC_RESPOSTA, qos=1)
        print(f"👂 Ouvindo respostas em: {TOPIC_RESPOSTA}")
    else:
        print(f"❌ Falha na conexão. Código: {rc}")

def on_message(client, userdata, msg):
    if msg.topic == TOPIC_RESPOSTA:
        try:
            data = json.loads(decrypt_message(msg.payload.decode()))
            
            print("\n" + "="*50)
            print(f"📊 Dados recebidos - {time.ctime(data['timestamp'])}")
            print(f"🖥️  CPU: {data['cpu']}%")
            print(f"💾 Memória: {data['memory']}%")
            print(f"💽 Disco: {data['disk']}%")
            print(f"📋 Total de processos: {len(data['processes'])}")
            print("="*50)
            
            # Exibe os 10 processos mais intensos
            print("\n🔥 Processos:")
            for p in sorted(data['processes'], key=lambda x: x.get('cpu_percent', 0), reverse=True):
                print(f"{p['pid']}: {p['name']} ({p.get('cpu_percent', )}%)")
            
        except Exception as e:
            print(f"⚠️ Erro ao processar dados: {str(e)}")

def solicitar_dados(client):
    """Envia comando para solicitar dados"""
    client.publish(TOPIC_COMANDO, "SOLICITAR_DADOS", qos=1)
    print("\n📨 Solicitando dados do cliente...")

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
        client.loop_start()
        
        print("\nPressione:")
        print("1 - Solicitar dados agora")
        print("Q - Sair")
        
        while True:
            comando = input("\nOpção: ").strip().upper()
            
            if comando == '1':
                solicitar_dados(client)
            elif comando == 'Q':
                break
            else:
                print("Opção inválida")
                
    except KeyboardInterrupt:
        print("\n🛑 Servidor encerrado")
    finally:
        client.disconnect()
        client.loop_stop()

if __name__ == "__main__":
    print("🚀 Servidor de monitoramento por demanda")
    main()