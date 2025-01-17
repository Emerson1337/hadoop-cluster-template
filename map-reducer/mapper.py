#!/usr/bin/env python3
import sys

def mapper():
    for line in sys.stdin:
        line_array = line.strip().split(',')
        if len(line_array) < 11:
            continue
        
        packet = {
            "timestamp": line_array[0],
            "source_ip": line_array[1],
            "source_port": line_array[2] or '0',
            "destination_ip": line_array[3],
            "destination_port": line_array[4] or '0',
            "flag": line_array[5],
            "sequence_number": line_array[6] or '0',
            "acknowledgment_number": line_array[7] or '0',
            "window_size": line_array[8] or '0',
            "options": line_array[9] or '',
            "payload_length": line_array[10] or '0',
        }

        flag = packet['flag'].split('/')[0]

        """
        Emite a chave como source_ip e destination_port com o flag SYN.
        """
        if flag == 'SYN':
            key = f"syn_ack_flood|{packet['source_ip']}|{packet['destination_ip']}|{packet['destination_port']}"
            print(f"{key}\tSYN\t1")

        """
        Emite a chave como source_ip e destination_port com a flag ACK.
        """    
        if flag == 'ACK':
            key = f"syn_ack_flood|{packet['source_ip']}|{packet['destination_ip']}|{packet['destination_port']}"
            print(f"{key}\tACK\t1")

        """
        Emite a chave como source_ip e destination_port para contar varreduras.
        """
        key = f"port_scan|{packet['source_ip']}|{packet['destination_ip']}"
        print(f"{key}\t{packet['destination_port']}")

if __name__ == "__main__":
    mapper()
