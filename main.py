import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from graph import Graph

politicianColumns = ["Congressman", "Party", "Votes"]
graphColumns = ["Congressman1", "Congressman2", "Votes"]

G = Graph()

date = int(input("Digite uma data entre 2002 e 2023: "))
while not (2002 <= date <= 2023):
    date = int(input("Digite uma data valida: "))

datasetPolitician = pd.read_csv(f"dataset/politicians{date}.csv",  delimiter=";", header=None, names=politicianColumns)
datasetGraph = pd.read_csv(f"dataset/graph{date}.csv", delimiter=";", header=None, names=graphColumns)

parties = input("Digite os nomes dos partidos separados por espaços: ").upper()
list_of_parties = parties.split()

for party in list_of_parties:
    if party not in datasetPolitician["Party"].values:
        print(f"O partido {party} não foi encontrado e será removido da lista")
        list_of_parties.remove(party)

for index, data in datasetPolitician.iterrows():
    G.add_node(data["Congressman"], data["Party"], data["Votes"])

for index, row in datasetGraph.iterrows():
    congressman1 = row["Congressman1"]
    congressman2 = row["Congressman2"]

    if congressman1 in G.adj_list and congressman2 in G.adj_list:
        G.add_edge(congressman1, congressman2, row["Votes"])



threshold_value = float(input("Digite o valor do threshold entre 0.1 a 1.0: "))

filtered_graph =  G.filter(list_of_parties)
normalized_graph = G.normalize_edges(filtered_graph)
threshold_graph = G.threshold(normalized_graph, threshold_value)
inversion_graph = G.invert_weights(threshold_graph)

#inicialização da plotagem de gráfico
nx_graph = nx.Graph()
for node, data in inversion_graph.adj_list.items():
    for neighbor, weight in data.items():
        nx_graph.add_edge(node, neighbor, weight=weight)

betweenness_centrality = nx.betweenness_centrality(nx_graph)
nodes = list(betweenness_centrality.keys()) 
centralities = list(betweenness_centrality.values()) 

nodes_sorted, centralities_sorted = zip(*sorted(zip(nodes, centralities), key=lambda x: x[1]))

plt.figure(figsize=(10, 6))
plt.bar(nodes_sorted, centralities_sorted, width=0.8) 
plt.xlabel("Deputados")
plt.ylabel("Centralidade")
plt.title("Centralidade dos Deputados (Ordem Crescente)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("betweenness_centrality.png")
plt.show()

#inicialização do heatmap

deputados = list(normalized_graph.adj_list.keys())

correlation_matrix = np.zeros((len(deputados), len(deputados)))

for i, deputado1 in enumerate(deputados):
    for j, deputado2 in enumerate(deputados):
        if i != j:  
            if deputado2 in normalized_graph.adj_list[deputado1]:
                correlation_matrix[i, j] = normalized_graph.adj_list[deputado1][deputado2]
            else:
                correlation_matrix[i, j] = 0

correlation_df = pd.DataFrame(correlation_matrix, index=deputados, columns=deputados)


plt.figure(figsize=(12, 8))
sns.set(font_scale=0.6)  
sns.heatmap(correlation_df, annot=False, cmap="coolwarm", fmt=".2f", linewidths=.5, xticklabels=True, yticklabels=True)
plt.title("Mapa de Calor de Correlação entre Deputados")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("correlation_heatmap.png")
plt.show()
