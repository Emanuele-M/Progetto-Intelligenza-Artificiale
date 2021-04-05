from graph import *
import copy
import sys

def score(graph, df): #implementazione della funzione di score secondo il procedimento di Cooper & Herskovitz
    s = 0
    tmp_score = 0
    for i in graph.nodes:
        combos = i.nodeCombos(df)
        i.updateCombos(df)
        if not i.parentCombos.empty:
            for j in i.parentCombos.index:
                p_combo = i.parentCombos.loc[[j]]
                p_combo = p_combo.drop(columns = 'counts')
                parents = list(p_combo)
                p_combo = list(p_combo.loc[j])
                p_comboCount = 0
                parents.append(i.name)
                for k in range(len(i.values)):
                    p_combo.append(i.values[k])
                    my_combo = combos[combos[parents] == p_combo].drop(columns = 'counts')
                    my_combo = my_combo.dropna()
                    if not my_combo.empty:
                        index = my_combo.index.values.astype(int)[0]
                        config = combos.loc[index, 'counts']
                        p_comboCount += config
                    else:
                        config = 0
                    num2 = math.gamma(1 + config)
                    den2 = math.gamma(1)
                    if tmp_score == 0:
                        tmp_score = num2 / den2
                    else:
                        tmp_score = tmp_score * num2 / den2
                    p_combo.remove(i.values[k])
                parents.remove(i.name)
                den1 = math.gamma(1 + p_comboCount)
                num1 = math.gamma(1)
                if tmp_score == 0:
                    tmp_score = num1 / den1
                else:
                    tmp_score = tmp_score * num1 / den1
        if s == 0:
            s = tmp_score
        else:
            s = s * tmp_score
            if s == 0:
                s = sys.float_info.min
    return s


def change_graph(graph: Graph): #restituisce tre diverse alterazioni per un grafo di partenza: g1 è il grafo a cui è stato aggiunto un arco, g2 quello a cui è stato rimosso, g3 quello a cui è stato invertito
    node1 = np.random.choice(graph.nodes)
    node2 = np.random.choice(graph.nodes)
    while node1 == node2:
        node2 = np.random.choice(graph.nodes)
    g1 = copy.deepcopy(graph)
    g2 = copy.deepcopy(graph)
    g3 = copy.deepcopy(graph)
    node1 = g1.get_node(node1.name)
    node2 = g1.get_node(node2.name)
    g1 = addEdge(g1, node1, node2)
    node1 = g2.get_node(node1.name)
    node2 = g2.get_node(node2.name)
    g2 = removeEdge(g2, node1, node2)
    node1 = g3.get_node(node1.name)
    node2 = g3.get_node(node2.name)
    g3 = reverseEdge(g3, node1, node2)
    return g1, g2, g3


def hill_climbing(graph, data, num_iter): #effettua una greedy hill climbing search per individuare il grafo con score maggiore. Sono permesse fino a 5 sidemoves per evitare di incorrere in un plateau
    max_side_moves = 5
    side_moves = 0
    s = score(graph, data)
    test_graph = graph
    iterator = 0
    while True:
        sc = 0
        scores = []
        new_graph = change_graph(test_graph)
        for i in range(len(new_graph)):
            sc = score(new_graph[i], data)
            scores.append(sc)
        scr = np.array(scores)
        smax = np.amax(scr)
        indmax = np.argmax(scr)
        if s < smax:
            s = smax
            test_graph = new_graph[indmax]
        elif s == smax and side_moves < max_side_moves:
            s = smax
            test_graph = new_graph[indmax]
            side_moves += 1
        else:
            iterator += 1
        if iterator > num_iter:
            break
    return test_graph

def addEdge(graph, node1, node2):
    g = copy.copy(graph)
    g.addEdge(node1, node2)
    if g.isCyclic(node1):
        g.removeEdge(node1, node2)
    return g

def removeEdge(graph, node1, node2):
    g = copy.copy(graph)
    g.removeEdge(node1, node2)
    return graph

def reverseEdge(graph, node1, node2):
    g = copy.copy(graph)
    g.reverseEdge(node1, node2)
    if g.isCyclic(node1) or g.isCyclic(node2):
        g.reverseEdge(node1, node2)
    return g

def random_graph_permutation(graph, num): #genera un DAG con struttura casuale con num archi
    for i in range(num):
        node1 = np.random.choice(graph.nodes)
        node2 = np.random.choice(graph.nodes)
        while node1 == node2 or node1 in node2.parents or node1 in node2.children:
            node2 = np.random.choice(graph.nodes)
        g = addEdge(graph, node1, node2)

    return g