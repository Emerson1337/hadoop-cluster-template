# -*- coding: utf-8 -*-
from functools import reduce
from collections import defaultdict
import csv
import json

# 2 tasks
# 1. Rodar o codigo dentro do hadoop paralelamente
# 2. Verificar como sera a leitura do arquivo csv e onde ele vai se encontrar e fazer o script para pegar os dados

def csv_mapper(csv_file_path):
    """
    Lê um arquivo CSV e mapeia os dados para o formato adequado para análise.
    """
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        mapped_data = []    
        
        for row in reader:
            print('row', row)
            # Criando o formato esperado pelo syn_flood_mapper
            mapped_data.append({
                "timestamp": row["timestamp"],
                "source_ip": row["source_ip"],
                "source_port": int(row["source_port"]),
                "destination_ip": row["destination_ip"],
                "destination_port": int(row["destination_port"]),
                "flag": row["flag"],
                "sequence": row["sequence"],
                "acknowledgment": int(row["acknowledgment"]),
                "window_size": int(row["window_size"]),
                "options": row["options"],
                "payload_length": int(row["payload_length"])
            })
    
    return mapped_data

# input data
data = [
  {
    "timestamp": "11:16:58.137040",
    "source_ip": "192.168.100.130",
    "source_port": 56285,
    "destination_ip": "ec2-184-72-135-61.compute-1.amazonaws.com",
    "destination_port": 27017,
    "flag": "SYN",
    "sequence": "1464:1647",
    "acknowledgment": 9321,
    "window_size": 2048,
    "options": "nop,nop,TS val 4179693498 ecr 2621059119",
    "payload_length": 183
  },
  {
    "timestamp": "11:16:58.172574",
    "source_ip": "ec2-184-72-135-61.compute-1.amazonaws.com",
    "source_port": 27017,
    "destination_ip": "192.168.100.130",
    "destination_port": 56183,
    "flag": "ACK",
    "sequence": "9320:10485",
    "acknowledgment": 1,
    "window_size": 501,
    "options": "nop,nop,TS val 2621069157 ecr 2526399357",
    "payload_length": 1165
  },
  {
    "timestamp": "11:16:58.172574",
    "source_ip": "ec2-184-72-135-61.compute-1.amazonaws.com",
    "source_port": 27017,
    "destination_ip": "192.168.100.130",
    "destination_port": 56183,
    "flag": "ACK",
    "sequence": "9320:10485",
    "acknowledgment": 1,
    "window_size": 501,
    "options": "nop,nop,TS val 2621069157 ecr 2526399357",
    "payload_length": 1165
  },
  {
    "timestamp": "11:16:58.172574",
    "source_ip": "ec2-184-72-135-61.compute-1.amazonaws.com",
    "source_port": 27017,
    "destination_ip": "192.168.100.130",
    "destination_port": 56183,
    "flag": "ACK",
    "sequence": "9320:10485",
    "acknowledgment": 1,
    "window_size": 501,
    "options": "nop,nop,TS val 2621069157 ecr 2526399357",
    "payload_length": 1165
  },
  {
    "timestamp": "11:16:58.172574",
    "source_ip": "ec2-184-72-135-61.compute-1.amazonaws.com",
    "source_port": 27017,
    "destination_ip": "192.168.100.130",
    "destination_port": 56183,
    "flag": "SYN",
    "sequence": "9320:10485",
    "acknowledgment": 1,
    "window_size": 501,
    "options": "nop,nop,TS val 2621069157 ecr 2526399357",
    "payload_length": 1165
  },
  {
    "timestamp": "11:16:58.172809",
    "source_ip": "192.168.100.130",
    "source_port": 56183,
    "destination_ip": "ec2-184-72-135-61.compute-1.amazonaws.com",
    "destination_port": 80,
    "flag": "ACK",
    "sequence": None,
    "acknowledgment": 10485,
    "window_size": 2048,
    "options": "nop,nop,TS val 2526409367 ecr 2621069157",
    "payload_length": 0
  },
  {
    "timestamp": "11:16:58.285959",
    "source_ip": "server-108-139-134-14.for50.r.cloudfront.net",
    "source_port": "https",
    "destination_ip": "192.168.100.130",
    "destination_port": 51103,
    "flag": "SYN",
    "sequence": "1680:1740",
    "acknowledgment": 1,
    "window_size": 753,
    "options": "nop,nop,TS val 2769873028 ecr 3608361957",
    "payload_length": 60
  },
    {
    "timestamp": "11:16:58.285959",
    "source_ip": "server-108-139-134-14.for50.r.cloudfront.net",
    "source_port": "https",
    "destination_ip": "192.168.100.130",
    "destination_port": 51103,
    "flag": "ACK",
    "sequence": "1680:1740",
    "acknowledgment": 1,
    "window_size": 753,
    "options": "nop,nop,TS val 2769873028 ecr 3608361957",
    "payload_length": 60
  }
]

def syn_flood_mapper(packet):
    """
    Emite a chave como source_ip e destination_ip com o flag SYN.
    """
    if packet['flag'] == 'SYN':
        key = "{}|{}|{}".format(packet['source_ip'], packet['destination_ip'], packet['destination_port'])
        yield key, 1

def ack_flood_mapper(packet):
    """
    Emite a chave como source_ip e conta pacotes ACK.
    """
    if packet['flag'] == 'ACK':
        key = "{}|{}|{}".format(packet['source_ip'], packet['destination_ip'], packet['destination_port'])
        yield key, 1

def port_scanning_mapper(packet):
    """
    Emite a chave como source_ip e destination_port para contar varreduras.
    """
    key = "{}|{}|{}".format(packet['source_ip'], packet['destination_ip'], packet['destination_port'])
    yield key, 1

def process_packets(packets):
    syn_data = []
    ack_data = []
    scan_data = []

    for packet in packets:
        # Mapeia pacotes para SYN Flood
        syn_data.extend(syn_flood_mapper(packet))
        
        # Mapeia pacotes para ACK Flood
        ack_data.extend(ack_flood_mapper(packet))
        
        # Mapeia pacotes para Port Scanning
        scan_data.extend(port_scanning_mapper(packet))

    return syn_data, ack_data, scan_data

# Aplicar os reducers
def analyze_traffic(syn_data, ack_data, scan_data):
    print("Analisando SYN Flood...")
    syn_flood_reducer(syn_data, ack_data)

    print("\nAnalisando ACK Flood...")
    ack_flood_reducer(ack_data, syn_data)

    print("\nAnalisando Port Scanning...")
    port_scanning_reducer(scan_data)

def syn_flood_reducer(syn_data, ack_data):
    """
    Detecta SYN Flood verificando pacotes SYN não seguidos de ACK.
    """
    syn_counts = defaultdict(int)
    ack_counts = defaultdict(int)

    # Contabiliza os pacotes SYN
    for key, count in syn_data:
        syn_counts[key] += count
    
    # Contabiliza os pacotes ACK
    for key, count in ack_data:
        ack_counts[key] += count
    
    # Verifica SYNs sem ACKs
    for key, syn_count in syn_counts.items():
        # busca ack com a combinacao de chave do syn para verificar se houve uma resposta do cliente.
        ack_count = ack_counts.get(key, 0)
        # se n tiver resposta do cliente e aquela chave tenha mandado mais de 100 syn, consideraremos um padrao anomalo
        if syn_count > 100 and ack_count == 0:  # Limite arbitrário para SYN Flood
            print("Possível SYN Flood detectado para" + {key} + ":" +{syn_count}+ " pacotes SYN sem ACK.")

# Função de redução para ACK Flood
def ack_flood_reducer(ack_data, syn_data):
    ack_counts = defaultdict(int)
    syn_counts = defaultdict(int)

    # Contabiliza pacotes ACK
    for key, count in ack_data:
        ack_counts[key] += count

    # Contabiliza pacotes SYN
    for key, count in syn_data:
        syn_counts[key] += count
    
    # Identifica ACKs sem SYN
    for key, ack_count in ack_counts.items():
        # busca syn com a combinacao de chave do ack para verificar se houve uma tentativa de comunicacao legitiva, ou apenas estao tentando consumir recursos do servidor com acks falsos.
        syn_count = syn_counts.get(key, 0)
        # se n tiver resposta do cliente e aquela chave tenha mandado mais de 100 ack, consideraremos um padrao anomalo
        if ack_count > 100 and syn_count == 0:  # Limite arbitrário para ACK Flood
            print("Possível ACK Flood detectado para " + {key} + ":" + {ack_count} + " pacotes ACK sem SYN.")

def port_scanning_reducer(mapped_data):
    # Usando defaultdict de dicionários para agrupar source_ip e destination_ip
    scan_counts = defaultdict(lambda: defaultdict(set))  # source_ip -> destination_ip -> set de ports

    # Processar os dados mapeados
    for key, _ in mapped_data:
        source_ip, destination_ip, destination_port = key.split('|')
        scan_counts[source_ip][destination_ip].add(destination_port)

    # Identificar IPs que estão escaneando muitas portas em um destino específico
    print('scan_counts.items()', scan_counts.items())
    for source_ip, destination_data in scan_counts.items():
        print('destination_data', destination_data)
        for destination_ip, ports in destination_data.items():
            # se estiver escaneando mais do que 5 portas, consideramos padrao anomalo.
            if len(ports) > 5:  # Limite arbitrário para detecção
                print("Possível Port Scanning detectado de " + {source_ip} + " para " + {destination_ip} + " : " + {len(ports)} + " portas escaneadas.")

csv_mapper('test.csv')
syn_data, ack_data, scan_data = process_packets(data)
analyze_traffic(syn_data, ack_data, scan_data)

# def reduce_traffic(mapped_data):
#   result = defaultdict(int)
#   for item in mapped_data:
#     result[item["key"]] += item["value"]
#   return dict(result)

# # Aplicação do MapReduce
# mapped_data = map_traffic(data)
# reduced_data = reduce_traffic(mapped_data)

# print("Map Result:", mapped_data)
# print("Reduce Result:", reduced_data)



# # map by count ocurrences creating an key-value pair
# def map_function(data):
#   return (data, 1)

# # Fase Reduce
# def reduce_function(key, values):
#   return (key, sum(values))

# # Create a list of count
# mapped = list(map(map_function, data))

# # Shuffle and Sort: Group by key
# group = defaultdict(list)
# for key, value in mapped:
#   group[key].append(value)

# print('group.items()', group.items())
# result = [reduce_function(k, v) for k, v in group.items()]

# print(result)
