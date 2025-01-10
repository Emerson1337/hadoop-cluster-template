import sys

def mapper():
    for line in sys.stdin:
        line_array = line.split(',')
        packet = {
            "timestamp": line_array[0],
            "source_ip": line_array[1],
            "source_port": line_array[2],
            "destination_ip": line_array[3],
            "destination_port": line_array[4],
            "flag": line_array[5],
            "sequence_number": line_array[6],
            "acknowledgment_number": line_array[7],
            "window_size": line_array[8],
            "options": line_array[9],
            "payload_length": line_array[10]
        }
        
        """
        Emite a chave como source_ip e destination_port com o flag SYN.
        """
        if packet['flag'] == 'SYN':
            key = "syn_ack_flood|{}|{}|{}".format(packet['source_ip'], packet['destination_ip'], packet['destination_port'])
            yield key, ('SYN', 1)

        """
        Emite a chave como source_ip e destination_port com a flag ACK.
        """
        if packet['flag'] == 'ACK':
            key = "syn_ack_flood|{}|{}|{}".format(packet['source_ip'], packet['destination_ip'], packet['destination_port'])
            yield key, ('ACK', 1)

        """
        Emite a chave como source_ip e destination_port para contar varreduras.
        """
        key = "port_scan|{}|{}".format(packet['source_ip'], packet['destination_ip'])
        yield key, packet['destination_port']


## Possivel execucao:
# hadoop jar /path/to/hadoop-streaming.jar \
#   -input /hdfs/caminho/do/arquivo.csv \
#   -output /hdfs/caminho/da/saida \
#   -mapper /path/to/mapper.py \
#   -reducer /path/to/reducer.py

# kubectl run hadoop-streaming --image=seu-docker-image-com-hadoop-python \
#   --env="HADOOP_HOME=/path/to/hadoop" \
#   --command -- /bin/bash -c "
#     hadoop jar /path/to/hadoop-streaming.jar \
#       -input /hdfs/caminho/do/arquivo.csv \
#       -output /hdfs/caminho/da/saida \
#       -mapper /path/to/mapper.py \
#       -reducer /path/to/reducer.py