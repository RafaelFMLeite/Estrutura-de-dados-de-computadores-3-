import pandas as pd
from graph import Graph

G = Graph()

columns_politician = ["Deputado", "Partido", "Voto"]
columns_graph = ["Deputado1", "Deputado2", "Votos"]

date = int(input("Digite uma data entre 2002 e 2023: "))
parties = input("Digite os partidos políticos separados por espaços: ").upper()
threshold_value = float(input("Digite um valor para o Threshold no intervalo de 0.1 até 0.9: "))

list_of_parties = parties.split()

while date > 2023 or date < 2002:
    date = int(input("Digite uma data válida, entre 2002 e 2023: "))

while threshold_value > 0.9 or threshold_value < 0.1:
    threshold_value = float(input("Digite um threshold válido: "))


datasetPoliticians = pd.read_csv(f"dataset/politicians{date}.csv", delimiter=";", header=None, names=columns_politician)
datasetGraph = pd.read_csv(f"dataset/graph{date}.csv", delimiter=";", header=None, names=columns_graph)

for index, row in datasetPoliticians.iterrows():
    G.add_node(row["Deputado"])
    G.add_party_to_a_node(row["Deputado"], row["Partido"])
    G.add_vote_to_a_node(row["Deputado"], row["Voto"])

for index, row in datasetGraph.iterrows():
    G.add_edge(row["Deputado1"], row["Deputado2"], row["Votos"])

filtered_graph = None

for list_p in list_of_parties:
    if list_p not in datasetPoliticians["Partido"].values:
        print(f"O partido {list_p} não existe no dataset.")
    else:
        if filtered_graph is None:
            filtered_graph = G.filter_party(list_p)
        else:
            filtered_graph = filtered_graph + G.filter_party(list_p)

filtered_graph.normalize_edges(filtered_graph)

thresholded_graph = filtered_graph.threshold(filtered_graph, threshold_value)
print(thresholded_graph)