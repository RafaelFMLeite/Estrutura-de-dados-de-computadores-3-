import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from graph import Graph

#Organização das colunas dos arquivos csv
politicianColumns = ["Congressman", "Party", "Votes"]
graphColumns = ["Congressman1", "Congressman2", "Votes"]

#instância do grafo
G = Graph()

#input de datas para leitura dos arquivo csv
date = int(input("Digite uma data entre 2002 e 2023: "))
while not (2002 <= date <= 2023):
    date = int(input("Digite uma data válida: "))

#Criação do dataframe
datasetPolitician = pd.read_csv(f"dataset/politicians{date}.csv", delimiter=";", header=None, names=politicianColumns)
datasetGraph = pd.read_csv(f"dataset/graph{date}.csv", delimiter=";", header=None, names=graphColumns)

#Condicional para utilização do filtro de partidos
use_filter = input(str("Você gostaria de usaria de usar o filtro de partidos? digite sim ou não ")).upper()

if(use_filter == "SIM"):
    parties = input("Digite os nomes dos partidos separados por espaços: ").upper()
    list_of_parties = parties.split()

    for party in list_of_parties:
        if party not in datasetPolitician["Party"].values:
            print(f"O partido {party} não foi encontrado e será removido da lista")
            list_of_parties.remove(party)

elif(use_filter == "NAO" or use_filter == "NÃO"):
    list_of_parties = []

    for party in datasetPolitician["Party"].values:
        list_of_parties.append(party)

else:
    print("Comando não indentificado!")

#Eliminação das arestas com valor inferior ou igual threshold value
threshold_value = float(input("Digite o valor do threshold entre 0.1 a 1.0: "))
while not (0.1 <= threshold_value <= 1.0):
    threshold_value = input(float("Digite um valor valido: "))

#Iteração e preenchimento de todos os nós 
for index, data in datasetPolitician.iterrows():
    G.add_node(data["Congressman"], data["Party"], data["Votes"])

#Conexão entre um nó e outro
for index, row in datasetGraph.iterrows():
    congressman1 = row["Congressman1"]
    congressman2 = row["Congressman2"]

    if congressman1 in G.adj_list and congressman2 in G.adj_list:
        G.two_way_edges(congressman1, congressman2, row["Votes"])

filtered_graph = G.filter(list_of_parties)
normalized_graph = G.normalize_edges(filtered_graph)
threshold_graph = G.threshold(normalized_graph, threshold_value)
inversion_graph = G.invert_weights(threshold_graph)

#Transformando o grafo G para a lib networkX para utilizar as funções desejadas 
nx_graph = nx.Graph()

for node, data in inversion_graph.adj_list.items():
    for neighbor, weight in data.items():
        nx_graph.add_edge(node, neighbor, weight=weight)

#Obtenção da centralidade ofericida pela lib NetworkX
betweenness_centrality = nx.betweenness_centrality(nx_graph)
nodes = list(betweenness_centrality.keys())
centralities = list(betweenness_centrality.values())

# Inicialização da plotagem de gráfico
#Ordenação de forma crescente dos nós do grafo para plotagem do gráfico
nodes_sorted, centralities_sorted = zip(*sorted(zip(nodes, centralities), key=lambda x: x[1]))

#Plotagem do gráfico em barra feita pela lib matplotlib
plt.figure(figsize=(10, 6))
plt.bar(nodes_sorted, centralities_sorted, width=0.8)
plt.xlabel("Deputados")
plt.ylabel("Centralidade")
plt.title("Centralidade dos Deputados (Ordem Crescente)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("betweenness_centrality.png")
plt.show()

# Inicialização do heatmap
deputados = list(normalized_graph.adj_list.keys())

correlation_matrix = np.zeros((len(deputados), len(deputados)))

node_to_index = {node: index for index, node in enumerate(nodes_sorted)}

for i, deputado1 in enumerate(deputados):
    for j, deputado2 in enumerate(deputados):
        if i != j:
            if deputado2 in normalized_graph.adj_list[deputado1]:
                correlation_matrix[i, j] = normalized_graph.adj_list[deputado1][deputado2]

correlation_matrix += correlation_matrix.T - np.diag(correlation_matrix.diagonal())

correlation_df = pd.DataFrame(correlation_matrix, index=deputados, columns=deputados)

plt.figure(figsize=(12, 8))
sns.set(font_scale=0.6)
sns.heatmap(correlation_df, annot=False, cmap="coolwarm", fmt=".2f", linewidths=.5, xticklabels=True, yticklabels=True)
plt.title("Mapa de Calor de Correlação entre Deputados (Ordenado)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("correlation_heatmap.png")
plt.show()

