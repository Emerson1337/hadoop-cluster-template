import subprocess
import time
import csv
import os

def executar_por_tempo(tempo_maximo):
    inicio = time.time()
    
    while time.time() - inicio < tempo_maximo:
        time.sleep(1)

tcpdump = subprocess.Popen('sudo tcpdump -i eth0 -w output.pcap', shell=True)

executar_por_tempo(30)

tcpdump.terminate()
tcpdump.wait()

tshark = subprocess.Popen('tshark -r output.pcap -T fields -e frame.time -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e tcp.flags.str -e tcp.seq -e tcp.ack -e tcp.window_size_value -e tcp.options -e tcp.len -E separator=, > saida.csv', shell=True)

executar_por_tempo(30)

tshark.terminate()
tshark.wait()

arquivo_csv = 'saida.csv'
arquivo_temp = 'arquivo_temp.csv'

titulos = ['Coluna1', 'Coluna2', 'Coluna3', 'Coluna4', 'Coluna5', 'Coluna6', 'Coluna7', 'Coluna8', 'Coluna9', 'Coluna10', 'Coluna11',] 

with open(arquivo_csv, 'r', newline='', encoding='utf-8') as arquivo_original, \
     open(arquivo_temp, 'w', newline='', encoding='utf-8') as arquivo_modificado:

    leitor = csv.reader(arquivo_original)
    escritor = csv.writer(arquivo_modificado)

    escritor.writerow(titulos)

    for linha in leitor:
        escritor.writerow(linha)

os.replace(arquivo_temp, arquivo_csv)
