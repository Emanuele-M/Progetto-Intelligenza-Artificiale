
from graphScore import *
import pandas as pd
data =  pd.read_csv(r'C:\Users\kamae\Documents\simulationsachs2.dat', sep=",")
data = data[['Plcg', 'PIP3', 'PIP2', 'PKC', 'PKA', 'Raf', 'Jnk', 'P38', 'Mek', 'Erk', 'Akt']]
goalNodes = []
for i in data.columns:
    data2 = data.dropna()
    vals = data2[i].unique()
    goalNodes.append(Node(i, None, None, vals))
graph = Graph(goalNodes)
g2 = copy.deepcopy(graph)
g4 = copy.deepcopy(graph)

print("Test: struttura iniziale con archi casuali")
print("\n")
graph2 = random_graph_permutation(g2, 8)
for i in graph2.nodes:
    print ("Node: " + i.name)
    for j in i.parents:
        print (i.name + "'s Parents: " + j.name)
    for j in i.children:
        print(i.name + "'s Children: " + j.name)
print(str(score(graph2, data)))
print("\n")
print("---------------")
print("\n")

s = hill_climbing(graph2, data, 1000)
for i in s.nodes:
    print ("Node: " + i.name)
    for j in i.parents:
        print (i.name + "'s Parents: " + j.name)
    for j in i.children:
        print(i.name + "'s Children: " + j.name)
print(str(score(s, data)))



