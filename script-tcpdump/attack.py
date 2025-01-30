import subprocess
import socket
import threading
import time
import csv
import os

HOST = "127.0.0.1"  # IP do servidor de destino
PORT = 5500         # Porta do servidor de destino
CAPTURE_TIME = 30   # Tempo total de captura

NUM_THREADS = 20     # Número de threads simultâneas
REQUESTS_PER_THREAD = 250  # Cada thread faz 250 requisições

def executar_por_tempo(tempo_maximo):
    """Executa um tempo de espera para permitir captura de pacotes."""
    time.sleep(tempo_maximo)

def send_request():
    """Simula múltiplas conexões TCP enviando requisições para o servidor."""
    for _ in range(REQUESTS_PER_THREAD):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((HOST, PORT))

            request = b"GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
            s.sendall(request)

            response = s.recv(1024)  
            print(response.decode(errors="ignore"))  

            s.close()
            time.sleep(0.05)  
        except Exception as e:
            print(f"Erro: {e}")

# Inicia a captura de pacotes com tcpdump
tcpdump = subprocess.Popen(['sudo', 'tcpdump', '-i', 'eth0', '-w', 'output.pcap'])

time.sleep(5)  

threads = []
for _ in range(NUM_THREADS):  
    t = threading.Thread(target=send_request)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

time.sleep(5)

# Finaliza o tcpdump corretamente com sudo
subprocess.run(['sudo', 'pkill', '-SIGTERM', 'tcpdump'])

print("Todas as requisições foram enviadas e a captura foi finalizada!")

# Processamento com tshark
with open("saida.csv", "w", newline='', encoding="utf-8") as saida_csv:
    tshark = subprocess.Popen([
        'tshark', '-r', 'output.pcap', '-T', 'fields',
        '-e', 'frame.time', '-e', 'ip.src', '-e', 'tcp.srcport',
        '-e', 'ip.dst', '-e', 'tcp.dstport', '-e', 'tcp.flags.str',
        '-e', 'tcp.seq', '-e', 'tcp.ack', '-e', 'tcp.window_size_value',
        '-e', 'tcp.options', '-e', 'tcp.len', '-t', 'ad', '-E', 'separator=,'
    ], stdout=saida_csv)

    tshark.wait()

arquivo_csv = 'saida.csv'
arquivo_temp = 'arquivo_temp.csv'

titulos = ['timestamp', 'source_ip', 'source_port', 'destination_ip', 'destination_port', 'flags',
           'sequence_number', 'acknowledgment_number', 'window_size', 'options', 'payload_length']

with open(arquivo_csv, 'r', newline='', encoding='utf-8') as arquivo_original, \
     open(arquivo_temp, 'w', newline='', encoding='utf-8') as arquivo_modificado:

    leitor = csv.reader(arquivo_original)
    escritor = csv.writer(arquivo_modificado)

    escritor.writerow(titulos)

    for linha in leitor:
        if len(linha) < 7:
            continue  

        linha[6] = ''.join(
            {'C': 'CWR/', 'E': 'ECE/', 'A': 'ACK/', 'P': 'PSH/', 'R': 'RST/',
             'S': 'SYN/', 'F': 'FIN/', 'U': 'URG/'}.get(c, c)
            for c in linha[5] if c != '·'
        ).rstrip('/')

        escritor.writerow(linha)

os.replace(arquivo_temp, arquivo_csv)

print("Processamento da captura finalizado! Os dados estão em 'saida.csv'.")
