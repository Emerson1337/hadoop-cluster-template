import subprocess
import time

def executar_por_tempo(tempo_maximo):
    inicio = time.time()
    
    while time.time() - inicio < tempo_maximo:
        time.sleep(1)

tcpdump = subprocess.Popen('sudo tcpdump -i eth0 -w output.pcap', shell=True)

executar_por_tempo(30)

tcpdump.terminate()
tcpdump.wait()

tshark = subprocess.Popen('tshark -r output.pcap -T fields -e frame.number -e ip.src -e ip.dst -E separator=";" > saida.csv', shell=True)

executar_por_tempo(30)

tshark.terminate()
tshark.wait()
