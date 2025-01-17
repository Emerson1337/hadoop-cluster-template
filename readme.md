# Como configurar NODES e Master utilizando Kubernetes (minikube) para rodar HDFS Cluster (Hadoop)

![image](https://github.com/user-attachments/assets/53cab607-0a92-4dc1-84ee-d8c2673982de)

## Passo 1: Configurar MINIKUBE para que possamos gerenciar o Kubernetes localmente

```bash
minikube start --profile sparkhdfs --cpus 6 --memory 15360MB {MEMORIA_DISPONIVEL: pelo menos 15360MB} opcional: --driver virtualbox --no-vtx-check
```

## Passo 2: Baixar algumas imagens bases disponíveis na internet ([text](https://github.com/Gradiant/dockerized-hadoop)) para usar variáveis de ambiente e configurar algumas propriedades.

```bash
docker pull gradiant/hdfs-datanode # configurará data nodes, responsáveis pela leitura e escrita de dados.
docker pull gradiant/hdfs-namenode # será o master e coordenará os datanodes para que funcionem de maneira distribuída.
docker pull bitnami/spark:3.3.1 # será o framework utilizado para gerenciar o HDFS
```

## Passo 3: Configurar os containers no Kubernetes para que um trabalhe como master e outros como nodes

```bash
kubectl apply -f ./hdfs-configmap.yaml
kubectl apply -f ./sparkhdfs.yaml
```

## Passo 4: Adicionar redirecionamento de portas para os containers

```bash
kubectl port-forward svc/sparkhdfs-master-namenode 8080:8080 50070:50070
```

# Para visualizar e orquestrar os containers por meio de interface, rode o seguinte comando:

```bash
minikube dashboard --profile sparkhdfs
```

Um link será gerado e você poderá visualizar os nodes em execução.

# Acessando o Hadoop

Basta acessar:
http://localhost:50070

# Acessando o APACHE Spark

Basta acessar:
http://localhost:8080

- Hadoop dashboard
  ![image](https://github.com/user-attachments/assets/2e44bf61-371a-41e4-8523-24cee750c146)

- Spark rodando
  ![image](https://github.com/user-attachments/assets/50eabeee-b0f4-4bac-a444-75d9bcac2c25)

- Kubernets rodando
  ![image](https://github.com/user-attachments/assets/53cab607-0a92-4dc1-84ee-d8c2673982de)

# Uma vez configurado, para rodar novamente faça:

```bash
minikube start --profile sparkhdfs --cpus 6 --memory 15360MB {MEMORIA_DISPONIVEL: pelo menos 7846MB} {opcional: --driver virtualbox --no-vtx-check}
```

```bash
kubectl port-forward svc/sparkhdfs-master-namenode 8080:8080 50070:50070
```

```bash
minikube dashboard --profile sparkhdfs
```

# Para resetar toda a configuração

```bash
kubectl delete all --all
```
