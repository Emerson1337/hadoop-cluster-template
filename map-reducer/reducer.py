#!/usr/bin/env python3
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
    scan_port_counts = defaultdict(set)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        try:
            # Divide a linha com base na tabulação '\t' para obter a chave (source_ip|destination_ip|destination_port) e o valor
            key, value = line.split('\t', 1)
            if key.startswith('port_scan'):
                scan_port_counts[key].add(int(value))
            elif key.startswith('syn_ack_flood'):
                packet_type, count = value.split('\t')
                count = int(count)
                if packet_type == 'ACK':
                    syn_ack_count[key]['ACK'] += count
                elif packet_type == 'SYN':
                    syn_ack_count[key]['SYN'] += count
        except ValueError:
            print(f"Malformed line: {line}", file=sys.stderr)

    anomalies = []

    for key, counts in syn_ack_count.items():
        syn_count = counts['SYN']
        ack_count = counts['ACK']

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
    for key, ports in scan_port_counts.items():
        if len(ports) > 100:
            anomalies.append({
                "type": "Port Scanning",
                "key": key,
                "port_count": len(ports),
                "ports": list(ports)
            })

    for anomaly in anomalies:
        print(f"{json.dumps(anomaly)}")

if __name__ == "__main__":
    reducer()
