import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from random import seed
import statistics
from collections import Counter

RUNS = 1000
nodes = pd.read_csv("subreddit_nodes.csv", index_col=0)
edges = pd.read_csv("subreddit_edges.csv", delimiter=';')

#Weighted graph
# G_weighted = nx.Graph()
# for index, row in nodes.iterrows():
#     G_weighted.add_node(index, name=row['Label'], category=row['Category'])

# for index, row in edges.iterrows():
#     G_weighted.add_edge(row['Source'], row['Target'], weight=row['Weight'])


# #print(f"Degrees are:${G.degree()}")


# #print(degrees)


# #Unweighted
G_unweighted = nx.Graph()
for index, row in nodes.iterrows():
    G_unweighted.add_node(index, name=row['Label'], category=row['Category'])

for index, row in edges.iterrows():
    G_unweighted.add_edge(row['Source'], row['Target'])

degrees = [val for (node,val) in G_unweighted.degree()]

    
def clusteringCoefficient(G, weight=None):  
    return nx.average_clustering(G, weight=weight)
    

#Random graph
def randomWeightedGraph(nodes, edges):
    G = nx.Graph()
    for index, row in nodes.iterrows():
        G.add_node(index, name=row['Label'], category=row['Category'])

    for index, row in edges.iterrows():
        random_weight = random.randint(1,100)
        G.add_edge(row['Source'], row['Target'], weight=random_weight)
    
    return G


def getWeights(g):
    avg = 0
    for item in g.edges.data():
        avg+=item[2]['weight']
    print(avg/len(g.edges.data()))

def getEigenvectorCentrality(G, weight=None):
    return nx.eigenvector_centrality(G, weight=weight)


    
def getAveragePathLength(G, weight=None):
    num_nodes = G.number_of_nodes()
    all_lengths = []
    
    for i in range(0, num_nodes):
        for j in range(0, num_nodes):
            try:
                if (i != j):
                    shortest_path = nx.shortest_path_length(G, source=i, target=j, weight=weight)
                    all_lengths.append(shortest_path)
            except:
                continue

    avg_shortest = statistics.mean(all_lengths)
    return avg_shortest


#Graph with edges randomized (degree preserved), unweighted graph

G_unweighted_random = nx.expected_degree_graph(degrees, selfloops=False)
#print(G.edges.data())
#print(nx.info(G_unweighted_random))

#print(nx.betweenness_centrality(G_unweighted_random))

#print()

clustering = []
path_length = []
degree_centrality = []
eigenvector_centrality = []
#for each node
all_nodes_betweeness = [0]*674
all_nodes_clustering = [0]*674
all_nodes_eigenvector = [0]*674

#Degree and eigen vector centrality are fixed
G = nx.expected_degree_graph(degrees, selfloops=False)
avg_degree_centrality = statistics.mean(nx.degree_centrality(G))
avg_eigenvector_centrality = statistics.mean(getEigenvectorCentrality(G))
nodes_clustering = nx.clustering(G)

shortest_path = nx.shortest_path_length(G_unweighted_random, source=0, target=0)

#print(nx.clustering(G))

for i in range(0, RUNS):
    G = nx.expected_degree_graph(degrees, selfloops=False)
    
    avg_clustering = clusteringCoefficient(G, "weight")
    avg_path = getAveragePathLength(G)  
    nodes_betweeness = nx.betweenness_centrality(G)
    nodes_clustering = nx.clustering(G)
    nodes_eigenvector = nx.eigenvector_centrality(G)

    clustering.append(avg_clustering)
    path_length.append(avg_path)  

    all_nodes_betweeness = [a + b for a, b in zip(all_nodes_betweeness, nodes_betweeness.values())]
    all_nodes_clustering = [a + b for a, b in zip(all_nodes_clustering, nodes_clustering.values())]
    all_nodes_eigenvector = [a + b for a, b in zip(all_nodes_eigenvector, nodes_eigenvector.values())]


f = lambda x: x/RUNS
all_nodes_betweeness  = [x/RUNS for x in all_nodes_betweeness]
all_nodes_clustering = [x/RUNS for x in all_nodes_clustering]
all_nodes_eigenvector = [x/RUNS for x in all_nodes_eigenvector]


avg_clustering = statistics.mean(clustering)
avg_path_length = statistics.mean(path_length)

std_clustering = statistics.stdev(clustering)
std_path_length = statistics.stdev(path_length)


print(f'Average clustering coefficient (unweighted): {avg_clustering}\n\
        Average path length (unweighted): {avg_path_length}\n\
        Degree centrality (unweighted):{avg_degree_centrality}\n\
        Average Eigenvector centrality (unweighted): {avg_eigenvector_centrality}\n\
        Standard deviation clustering coefficient (unweighted): {std_clustering}\n\
        Standard deviation path length (unweighted): {std_path_length}\n\
        Runs: {RUNS}\n\n'
    )

#Graph with fixed, original edges (degree preserved) but weights are randomized

clustering_weighted = []
path_length_weighted = []
eigenvector_centrality_weighted = []

all_nodes_betweeness_weighted =  [0]*674
all_nodes_clustering_weighted =  [0]*674
all_nodes_eigenvector_weighted =  [0]*674

for i in range(0, RUNS):
    G = randomWeightedGraph(nodes, edges)
    avg_clustering_weighted = clusteringCoefficient(G, "weight")
    avg_path = nx.average_shortest_path_length(G, weight="djikstra")
    avg_eigenvector_centrality = statistics.mean(getEigenvectorCentrality(G, "weight"))
    nodes_betweeness_weighted = nx.betweenness_centrality(G, weight="weight")
    nodes_clustering_weighted = nx.clustering(G, weight="weight")
    nodes_eigenvector_weighted = nx.eigenvector_centrality(G, weight="weight")

    clustering_weighted.append(avg_clustering)
    path_length_weighted.append(avg_path) 
    eigenvector_centrality_weighted.append(avg_eigenvector_centrality)   

    all_nodes_betweeness_weighted = [a + b for a, b in zip(all_nodes_betweeness_weighted, nodes_betweeness_weighted.values())]
    all_nodes_clustering_weighted = [a + b for a, b in zip(all_nodes_clustering_weighted, nodes_clustering_weighted.values())]
    all_nodes_eigenvector_weighted = [a + b for a, b in zip(all_nodes_eigenvector_weighted, nodes_eigenvector_weighted.values())]

all_nodes_betweeness_weighted  = [x/RUNS for x in all_nodes_betweeness_weighted]
all_nodes_clustering_weighted = [x/RUNS for x in all_nodes_clustering_weighted]
all_nodes_eigenvector_weighted = [x/RUNS for x in all_nodes_eigenvector_weighted]


avg_clustering_weighted = statistics.mean(clustering_weighted)
avg_path_length_weighted = statistics.mean(path_length_weighted)   
avg_eigenvector_centrality_weighted = statistics.mean(eigenvector_centrality_weighted)

std_clustering_weighted = statistics.stdev(clustering_weighted)
std_path_length_weighted = statistics.stdev(path_length_weighted)


print(f'Average clustering coefficient (weighted): {avg_clustering_weighted}\n\
        Average path length (weighted): {avg_path_length_weighted}\n\
        Average Eigenvector centrality (weighted): {avg_eigenvector_centrality_weighted}\n\
        Standard deviation clustering coefficient (weighted): {std_clustering_weighted}\n\
        Standard deviation path length (weighted): {std_path_length_weighted}\n\
        Runs: {RUNS}'
    )

print("-----------------------END")

#Create csv for all measurements
stats = pd.DataFrame(
    columns=['Graph type', 'Avg clustering coeff', 'Avg path length', 'Std clustering coeff', 'Std path length', 'Avg Degree centrality', 'Avg Eigenvector centrality'],
    data=[['Unweighted', avg_clustering, avg_path_length, std_clustering, std_path_length, avg_degree_centrality, avg_eigenvector_centrality], 
        ['Weighted', avg_clustering_weighted, avg_path_length_weighted, std_clustering_weighted, std_path_length_weighted, 'N/A', avg_eigenvector_centrality]]
    )

nodes['Clustering coefficient centrality unweighted']= pd.Series(all_nodes_clustering)
nodes['Betweeness centrality unweighted']= pd.Series(all_nodes_betweeness)
nodes['Eigenvector centrality unweighted']= pd.Series(all_nodes_eigenvector)


nodes['Clustering coefficient centrality weighted']= pd.Series(all_nodes_clustering_weighted)
nodes['Betweeness centrality weighted']= pd.Series(all_nodes_betweeness_weighted)
nodes['Eigenvector centrality weighted']= pd.Series(all_nodes_eigenvector_weighted)

#nodes['Clustering coeiff unweighted (each node)']= pd.Series(all_nodes_betweeness)
# nodes_stats = pd.DataFrame(columns=['Clustering coeiff (each node)'],
#                 data=[[all_nodes_betweeness]]
#             )

stats.to_csv('null-models-basic-stats.csv', sep=',')
nodes.to_csv("null-models-nodes-stats.csv", sep=',')
