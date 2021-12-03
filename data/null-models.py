import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from random import seed
import statistics

RUNS = 1000
nodes = pd.read_csv("subreddit_nodes.csv", index_col=0)
edges = pd.read_csv("subreddit_edges.csv", delimiter=';')

#Weighted graph
G_weighted = nx.Graph()
for index, row in nodes.iterrows():
    G_weighted.add_node(index, name=row['Label'], category=row['Category'])

for index, row in edges.iterrows():
    G_weighted.add_edge(row['Source'], row['Target'], weight=row['Weight'])


#print(f"Degrees are:${G.degree()}")

degrees = [val for (node,val) in G_weighted.degree()]
#print(degrees)


#Unweighted
G_unweighted = nx.Graph()
for index, row in nodes.iterrows():
    G_unweighted.add_node(index, name=row['Label'], category=row['Category'])

for index, row in edges.iterrows():
    G_unweighted.add_edge(row['Source'], row['Target'])

    
def clusteringCoefficient(G, weight=None):  
    return nx.average_clustering(G, weight=weight)
    

#Random graph
def randomWeightedGraph(nodes, edges):
    G = nx.Graph()
    for index, row in nodes.iterrows():
        G.add_node(index, name=row['Label'], category=row['Category'])

    for index, row in edges.iterrows():
        random_weight = random.randint(1,99)
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

clustering = []
path_length = []
degree_centrality = []
eigen_centrality = []


shortest_path = nx.shortest_path_length(G_unweighted_random, source=0, target=0)

for i in range(0, RUNS):
    G = nx.expected_degree_graph(degrees, selfloops=False)
    
    avg_clustering = clusteringCoefficient(G, "weight")
    avg_path = getAveragePathLength(G)
    avg_degree_centrality = statistics.mean(nx.degree_centrality(G))
    avg_eigenvector_centrality = statistics.mean(getEigenvectorCentrality(G))

    clustering.append(avg_clustering)
    path_length.append(avg_path)  
    degree_centrality.append(avg_degree_centrality)
    eigen_centrality.append(avg_eigenvector_centrality)

    
avg_clustering = statistics.mean(clustering)
avg_path_length = statistics.mean(path_length)
avg_degree_centrality = statistics.mean(avg_degree_centrality)
avg_eigenvector_centrality = statistics.mean(avg_eigenvector_centrality)

print(f'Average clustering coefficient (unweighted): {avg_clustering}\n\
        Average path length (unweighted): {avg_path_length}\n\
        Degree centrality (unweighted):{avg_degree_centrality}\
        Eigenvector centrality (unweighted): {avg_eigenvector_centrality}\
        Runs: {RUNS}\n\n'
    )

#Graph with fixed, original edges (degree preserved) but weights are randomized

clustering = []
path_length = []
degree_centrality = []
eigen_centrality = []

for i in range(0, RUNS):
    G = randomWeightedGraph(nodes, edges)
    avg_clustering = clusteringCoefficient(G, "weight")
    avg_path = getAveragePathLength(G, weight='weight')
    avg_eigenvector_centrality = statistics.mean(getEigenvectorCentrality(G, "weight"))
    
    clustering.append(avg_clustering)
    path_length.append(avg_path)    
    if (i%100 == 0):
        print(f"clustering:{avg_clustering} path length: {avg_path}")


avg_clustering = statistics.mean(clustering)
avg_path_length = statistics.mean(path_length)   
avg_eigenvector_centrality = statistics.mean(avg_eigenvector_centrality)

print(f'Average clustering coefficient (weighted): {avg_clustering}\n\
        Average path length (weighted): {avg_path_length}\n\
        Eigenvector centrality (weighted): {avg_eigenvector_centrality}\
        Runs: {RUNS}'
    )

