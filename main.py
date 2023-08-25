import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from graph import Graph

# Organização das colunas dos arquivos csv
politicianColumns = ["Congressman", "Party", "Votes"]
graphColumns = ["Congressman1", "Congressman2", "Votes"]

# Instância do grafo
G = Graph()

# Input de datas para leitura dos arquivos CSV
date = int(input("Digite uma data entre 2002 e 2023: "))
while not (2002 <= date <= 2023):
    date = int(input("Digite uma data válida: "))

# Criação do dataframe
datasetPolitician = pd.read_csv(f"dataset/politicians{date}.csv", delimiter=";", header=None, names=politicianColumns)
datasetGraph = pd.read_csv(f"dataset/graph{date}.csv", delimiter=";", header=None, names=graphColumns)

# Condicional para utilização do filtro de partidos
use_filter = input(str("Você gostaria de usar o filtro de partidos? Digite sim ou não: ")).upper()

if use_filter == "SIM":
    parties = input("Digite os nomes dos partidos separados por espaços: ").upper()
    list_of_parties = parties.split()

    for party in list_of_parties:
        if party not in datasetPolitician["Party"].values:
            print(f"O partido {party} não foi encontrado e será removido da lista")
            list_of_parties.remove(party)

elif use_filter == "NAO" or use_filter == "NÃO":
    list_of_parties = []

    for party in datasetPolitician["Party"].values:
        list_of_parties.append(party)

else:
    print("Comando não identificado!")

# Eliminação das arestas com valor inferior ou igual ao threshold value
threshold_value = float(input("Digite o valor do threshold entre 0.1 a 0.9: "))
while not (0.1 <= threshold_value <= 0.9):
    threshold_value = float(input("Digite um valor válido: "))

# Iteração e preenchimento de todos os nós
for index, data in datasetPolitician.iterrows():
    G.add_node(data["Congressman"], data["Party"], data["Votes"])

# Conexão entre um nó e outro
for index, row in datasetGraph.iterrows():
    congressman1 = row["Congressman1"]
    congressman2 = row["Congressman2"]

    if congressman1 in G.adj_list and congressman2 in G.adj_list:
        G.two_way_edges(congressman1, congressman2, row["Votes"])

filtered_graph = G.filter(list_of_parties)
normalized_graph = G.normalize_edges(filtered_graph)
threshold_graph = G.threshold(normalized_graph, threshold_value)
inversion_graph = G.invert_weights(threshold_graph)

# Transformando o grafo G para a biblioteca NetworkX para utilizar as funções desejadas
nx_graph = nx.Graph()

for node, data in inversion_graph.adj_list.items():
    for neighbor, weight in data.items():
        nx_graph.add_edge(node, neighbor, weight=weight)

# Obtenção da centralidade oferecida pela biblioteca NetworkX
betweenness_centrality = nx.betweenness_centrality(nx_graph)
nodes = list(betweenness_centrality.keys())
centralities = list(betweenness_centrality.values())

# Inicialização da plotagem de gráfico
# Ordenação de forma crescente dos nós do grafo para plotagem do gráfico
nodes_sorted, centralities_sorted = zip(*sorted(zip(nodes, centralities), key=lambda x: x[1]))

# Plotagem do gráfico em barra feita pela biblioteca Matplotlib
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

# Seção adicionada para colorir nós comuns com base em seus partidos políticos
# Criar um dicionário de cores para cada partido político
party_colors = {}
for party in list_of_parties:
    party_colors[party] = sns.color_palette("Set2", len(list_of_parties))[list_of_parties.index(party)]

# Criar uma lista de nós a partir do grafo personalizado threshold_graph
nodes_threshold = list(threshold_graph.adj_list.keys())

# Atribuir cores com base nos partidos políticos dos nós
node_colors = [party_colors[datasetPolitician[datasetPolitician['Congressman'] == node]['Party'].values[0]] for node in nodes_threshold]


# Criar uma cópia do grafo thresholded em NetworkX
thresholded_nx_graph = nx.Graph()

# Adicionar nós e arestas ao grafo thresholded em NetworkX
for node, data in threshold_graph.adj_list.items():
    thresholded_nx_graph.add_node(node)
    for neighbor, weight in data.items():
        thresholded_nx_graph.add_edge(node, neighbor, weight=weight)

# Plotar o grafo thresholded com cores baseadas em partidos políticos
plt.figure(figsize=(12, 8))
spring_layout = nx.spring_layout(thresholded_nx_graph, seed=42)
nx.draw(thresholded_nx_graph, spring_layout, with_labels=True, node_size=100, font_size=8, node_color=node_colors)
plt.title("Grafo")
plt.tight_layout()
plt.show()
