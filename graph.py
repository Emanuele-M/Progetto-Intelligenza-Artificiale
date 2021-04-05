import pandas as pd
import numpy as np
import math

class Graph:
    def __init__(self, nodes = None):
        if nodes == None:
            nodes = []
        self.nodes = nodes

    def addNode(self, node):
        if node not in self.nodes:
                self.nodes.append(node)

    def addEdge(self, node1, node2): # aggiunge un arco se non aggiunge cicli
        if node1 and node2 in self.nodes:
            node2.parents.append(node1)
            node1.children.append(node2)


    def removeEdge(self, node1, node2): #rimuove un arco
        if node1 and node2 in self.nodes:
            if node1 in node2.parents:
                node2.parents.remove(node1)
                node1.children.remove(node2)
            elif node1 in node2.children:
                node2.children.remove(node1)
                node1.parents.remove(node2)

    def reverseEdge(self, node1, node2):# inverte il verso di un arco se non aggiunge cicli
        if node1 and node2 in self.nodes:
            if node1 in node2.parents:
                self.addEdge(node2, node1)
                self.removeEdge(node1, node2)
            elif node1 in node2.children:
                self.addEdge(node1, node2)
                self.removeEdge(node2, node1)

    def isCyclic(self, node): # controlla la presenza di cicli a partire da un nodo visitando i suoi vicini
        node.visited = True
        for neighbour in node.children:
            if neighbour.visited == False:
                if self.isCyclic(neighbour) == True:
                    return True
            else:
                return True
        return False

    def get_node(self, name): #funzione di appoggio, necessaria onde evitare che i nodi considerati nelle funzioni in change_graph non siano quelli del grafo originale
        names = []
        node = 0
        for i in range(len(self.nodes)):
            if self.nodes[i].name == name:
                node = self.nodes[i]
        return node

class Node:
    def __init__(self, name, parents = None, children = None, values = None):
        self.name = str(name)
        if parents == None:
            parents = []
        self.parents = parents
        if children == None:
            children = []
        self.children = []
        self.values = values
        self.value = None
        self.visited = False
        self.parentCombos = None

    def setParentCombos(self, df):
        self.parentCombos = df

    def updateCombos(self, df): #aggiorna il database che tiene traccia delle combinazioni dei nodi genitori di quello interessato. Utile per individuare gli N_ij
        parent = []
        combos = pd.DataFrame()
        if self.parents != []:
            for i in self.parents:
                if i is not parent:
                    parent.append(i.name)
            combos = df.value_counts(parent).reset_index(name = 'counts')
        self.setParentCombos(combos)

    def nodeCombos(self, df): #realizza un database che permette di tracciare le combinazioni distinte di valori del nodo e dei suoi genitori, necessaria per individuare gli N_ijk
        nodes = []
        combos = pd.DataFrame()
        for i in self.parents:
            if i is not nodes:
                nodes.append(i.name)
        nodes.append(self.name)
        combos = df.value_counts(nodes).reset_index(name = 'counts')
        return combos





