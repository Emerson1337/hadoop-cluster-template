# Passo a passo para rodar containers contendo o hadoop cluster a gerenciá-los usando Kubernets.

## Passo 1: Configurar MINIKUBE para que possamos gerenciar o Kubernetes localmente

minikube start --profile sparkhdfs --cpus 6 --memory 7846MB {MEMORIA_DISPONIVEL: pelo menos 7846MB} {opcional: --driver virtualbox --no-vtx-check}

## Passo 2: Habilitar o SSH no perfil do MINIKUBE que acamos acabamos de criar e entrar na linha de comando do serviço

minikube ssh --profile sparkhdfs

## Passo 3: Baixar algumas imagens bases disponíveis na internet ([text](https://github.com/Gradiant/dockerized-hadoop)) para usar variáveis de ambiente e configurar algumas propriedades.

docker pull gradiant/hdfs-datanode -> configurará data nodes, responsáveis pela leitura e escrita de dados.
docker pull gradiant/hdfs-namenode -> será o master e coordenará os datanodes para que funcionem de maneira distribuída.
docker pull bitnami/spark:3.3.1 -> será o framework utilizado para gerenciar o HDFS

## Passo 3: Configurar os containers no Kubernetes para que um trabalhe como master e outros como nodes

kubectl apply -f ./hdfs-configmap.yaml
kubectl apply -f ./sparkhdfs.yaml

## Passo 4: Adicionar redirecionamento de portas para os containers

kubectl port-forward svc/sparkhdfs-master-namenode 8080:8080 50070:50070

# Para visualizar e orquestrar os containers por meio de interface, rode o seguinte comando:

minikube dashboard --profile sparkhdfs

Um link será gerado e você poderá visualizar os nodes em execução.

# Acessando o Hadoop

Basta acessar:
https://localhost:50070

# Acessando o APACHE Spark

Basta acessar:
http://localhost:8080

# Importando dados para o cluster

Para importar dados para o cluster, é necessário primeiramente enviar o set de dados.

> Testando para o dataset de exemplo neste repositório.

1. Confira se o HDFS está pronto e operante
   kubectl exec -it sparkhdfs-master-namenode-0 -- hdfs dfsadmin -safemode get

Você deve receber algo como:
`Safe mode is OFF`

2. Rode para enviar o csv a um dos nodes:
   kubectl exec -it sparkhdfs-master-namenode-0 -- hdfs dfsadmin -safemode get

3. Criei o diretorio para fazer upload do dado para o cluster.
   kubectl exec -it sparkhdfs-master-namenode-0 -- hdfs dfs -mkdir -p /user/hadoop/dataset

4. Envie o dado do NODE para o HDFS
   kubectl cp ./dataset/sample.csv default/sparkhdfs-worker-datanode-0:/tmp/sample.csv
