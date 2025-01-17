## Para executar o MapReduce utilizando o cluster HADOOP, será necessário:

1 - Ter o cluster rodando e operante. Agora entre no master para gerenciar os nodes

```bash
kubectl exec -it sparkhdfs-master-namenode-0 -- bash

# Crie as pastas que utilizaremos
mkdir /tmp/input && mkdir /tmp/scripts

#Em seguida saia da maquina
exit
```

2 - Enviar o arquivo alvo de processamento para o cluster (o master em questão)

```bash
kubectl cp ./dataset/{file}.txt default/sparkhdfs-master-namenode-0:/tmp/input/{file}.txt
```

3 - Elabore o algoritmo MapReduce para processar o arquivo contendo os dados dentro do node (Master) e envie para o container

```bash
kubectl cp ./map-reducer/mapper.py default/sparkhdfs-master-namenode-0:/tmp/scripts/mapper.py
kubectl cp ./map-reducer/reducer.py default/sparkhdfs-master-namenode-0:/tmp/scripts/reducer.py
```

4 - Adentrar ao node master

```bash
kubectl exec -it sparkhdfs-master-namenode-0 -- bash
```

5 - Torne os scripts executáveis

```bash
chmod a+x /tmp/scripts/*.py
```

6 - Repasse todos os arquivos do container para o cluster

```bash
hdfs dfs -mkdir -p /tmp/input
hdfs dfs -put /tmp/input/*.csv /tmp/input/

hdfs dfs -mkdir -p /tmp/scripts
hdfs dfs -put /tmp/scripts/*.py /tmp/scripts/

hdfs dfs -ls /tmp/input

# Caso ja exista output
hdfs dfs -rm -r /tmp/output
```

7 - Executar o algoritmo no Hadoop

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.7.7.jar \
  -input /tmp/input/*.csv \
  -output /tmp/output/results \
  -mapper "python3 /tmp/scripts/mapper.py" \
  -reducer "python3 /tmp/scripts/reducer.py"
```

8 - Checar resultados

```bash
hdfs dfs -cat /tmp/output/results/part-00000
```
