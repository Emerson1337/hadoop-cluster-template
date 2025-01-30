import socket
import threading
import time

HOST = "127.0.0.1"  # IP do servidor
PORT = 5500         # Porta do servidor

def send_request():
    for _ in range(100):  # Cada thread faz 100 requisições
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)  # Timeout de 2s para evitar travamentos
            s.connect((HOST, PORT))
            
            request = b"GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
            s.sendall(request)
            
            response = s.recv(1024)  # Captura resposta (opcional)
            print(response.decode(errors="ignore"))  

            s.close()
            time.sleep(0.05)  # Pequeno delay para evitar sobrecarga
        except Exception as e:
            print(f"Erro: {e}")

# Criar várias threads para simular muitas conexões simultâneas
threads = []
for _ in range(10):  # 10 threads x 100 requests = 1.000 requisições
    t = threading.Thread(target=send_request)
    t.start()
    threads.append(t)

# Espera todas as threads terminarem
for t in threads:
    t.join()

print("Todas as requisições foram enviadas!")
