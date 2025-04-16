# Redes-de-Comunica-o
Códigos Referentes a disciplina de Redes de Comunicação de Dados da UFSC de Joinville

# Sistema de Monitoramento via MQTT

## Descrição
Sistema que coleta e transmite dados de desempenho do computador (CPU, memória, processos) utilizando o protocolo MQTT com criptografia AES-256.

## Arquivos do Projeto
- mqtt_client.py - Cliente que coleta e envia os dados
- mqtt_server.py - Servidor que recebe e exibe os dados
- requirements.txt - Lista de dependências
- imagens/ - Pasta com prints do sistema em funcionamento

## Instalação
1. Instale o Python 3.8+
2. Baixe os arquivos do repositório
3. Instale as dependências com: pip install -r requirements.txt

## Como Usar
1. Execute o servidor primeiro: python mqtt_server.py
2. Em outro terminal, execute o cliente: python mqtt_client.py
3. Os dados serão exibidos no servidor automaticamente

## Configuração
Edite diretamente nos arquivos .py:
- MQTT_BROKER = "maqiatto.com"
- MQTT_USER = "seu_email@dominio.com"
- MQTT_PASS = "sua_senha"
- TOPIC = "seu_email@dominio.com/redes1"

## Segurança
O sistema utiliza:
- Criptografia AES-256 nos dados
- Autenticação no broker MQTT
- Tópicos privados com namespace

Desenvolvido por [Seu Nome] - 2023
