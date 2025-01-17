import sys
from collections import defaultdict
import json

def reducer():
    """
    Detecta SYN Flood verificando pacotes SYN não seguidos de ACK.
    Detecta ACK Flood verificando pacotes ACK sem SYN anteriormente.
    Detecta Port Scanning verificando a quantidade de tentativa de acesso a portas.
    """
    syn_ack_count = defaultdict(lambda: {'SYN': 0, 'ACK': 0})
    scan_port_counts = defaultdict(list)

    for line in sys.stdin:
        # Remove espaços em branco.
        line = line.strip()

        if line:
            # Divide a linha com base na tabulação '\t' para obter a chave (source_ip|destination_ip|destination_port) e o valor
            key, value = line.split('\t')
            if key.startswith('port_scan'):       
                # Adiciona a porta ao conjunto correspondente
                scan_port_counts[key].append(int(value))

            if key.startswith('syn_ack_flood'):
                # Processa os dados mapeados (ACK e SYN)
                packet_type, count = value
                if packet_type == 'ACK':
                    syn_ack_count[key]['ACK'] += count
                elif packet_type == 'SYN':
                    syn_ack_count[key]['SYN'] += count
                
                # Verifica SYNs sem ACKs
                syn_count = syn_ack_count[key]['SYN']
                ack_count = syn_ack_count[key]['ACK']

    anomalies = []

    # Identifica SYNs sem ACKs
    # se n tiver resposta do cliente e aquela chave tenha mandado mais de 100 syn, consideraremos um padrao anomalo
    # print("Possível SYN Flood detectado para" + {key} + ":" +{syn_count}+ " pacotes SYN sem ACK.")
    if syn_count > 100 and ack_count == 0:  # Limite arbitrário para SYN Flood
        anomalies.append({
            "type": "SYN Flood",
            "key": key,
            "syn_packets": syn_count,
            "ack_packets": ack_count
        })

    # Identifica ACKs sem SYN
    # se n tiver resposta do cliente e aquela chave tenha mandado mais de 100 ack, consideraremos um padrao anomalo
    # print("Possível ACK Flood detectado para " + {key} + ":" + {ack_count} + " pacotes ACK sem SYN.")
    if ack_count > 100 and syn_count == 0:  # Limite arbitrário para ACK Flood
        anomalies.append({
            "type": "ACK Flood",
            "key": key,
            "syn_packets": syn_count,
            "ack_packets": ack_count
        })

    # print(f"Port scanning detectado para {key} com {len(scan_port_counts)} portas: {scan_port_counts.items()}")
    if len(scan_port_counts) > 5:
        anomalies.append({
            "type": "Port Scanning",
            "key": key,
            "ports": scan_port_counts.items()
        })

    for anomaly in anomalies:
        print(json.dumps(anomaly))