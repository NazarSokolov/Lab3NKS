import math

import itertools
#Знаходження шляхів і Psystem
graph = {
    "start": ["1", "2"],
    "1": ["3", "4"],
    "2": ["3", "5", "7"],
    "3": ["4", "5", "7"],
    "4": ["5", "6"],
    "5": ["6", "7"],
    "6": ["end"],
    "7": ["end"],
    "end": []
}


probabils = {"start": 0.0, "1": 0.91, "2": 0.16, "3": 0.03, "4": 0.91, "5": 0.06, "6": 0.44, "7": 0.08, "end": 0.0}


def paths(first_state, last_state, graph, curr_path = []):
    curr_path = curr_path + [first_state]
    all_paths = []
    if first_state == last_state:
        return [curr_path]
    if first_state not in graph:
        return []
    for i in graph[first_state]:
        if i not in curr_path:
            create_paths = paths(i, last_state, graph, curr_path)
            for j in create_paths:
                all_paths.append(j)
    return all_paths


all_paths = paths("start", "end", graph)

comb = []
full_list_comb = []
all_states = graph.keys()
for i in range(1, len(graph.keys()) + 1):
    comb.append(list(itertools.combinations(all_states, i)))
for j in comb:
    for i in j:
        full_list_comb.append(i)


all_system_states = []
for i in full_list_comb:
    for j in all_paths:
        if set(j).issubset(set(i)):
            all_system_states.append(i)
all_system_states = set(all_system_states)

allProbabils = []
string = ""
for i in all_system_states:
    probability = 1
    for k in graph.keys():
        if k in i and k !="end" and k !="start":
            string += "+    "
            probability *= probabils[k]
        elif k not in i and k !="end" and k !="start":
            string += "-    "
            probability *= 1 - probabils[k]
    string += str(round(probability, 6)) + "\n"
    allProbabils.append(probability)

#                   Лаболаторна робота 3
P = sum(allProbabils)

probs = [0.91, 0.16, 0.03, 0.91, 0.06, 0.44, 0.08]

P = round(P, 6)
T = 2501           # час
K1, K2 = 3, 3      # кратність

Q = 1 - P

Tsystem = round(-T/math.log1p(P-1))

def reservation_quality_criteria(Qr, Pr, Tr):
    Gq = round(Qr/Q, 6)
    Gp = round(Pr/P, 6)
    Gt = round(Tr/Tsystem,6)

    return Gq, Gp, Gt

def general_unloaded(q, K):
    qr = round(1/math.factorial(K+1) * q, 6)

    return qr

def separate_loaded(p, K):
    qr = round((1 - p) ** (K + 1), 6)

    return qr

def general_loaded(p, K):
    pr = round(1 - (1-p) ** (K + 1), 6)

    return pr

print("Psystem({}) = {}\nQsystem({}) = {}\nTsystem = {}".format(T, P, T, Q, Tsystem))


Preserved_system = separate_loaded(P, K1)
Qreserved_system = 1 - Preserved_system
Treserved_system = round(-T/math.log1p(Preserved_system-1))
print("Ймовірність відмови на час {} годин системи з роздільним навантаженням Кратність = {}\n"
      "Qreserved system({}) = {}\nДалі знайдемо ймовірність безвідмовної роботи і значення середнього наробітку\n"
      "Preserved system = {}\n"
      "Treserved system = {}".format(T, K1, T, Qreserved_system, Preserved_system, Treserved_system))

Gq, Gp, Gt = reservation_quality_criteria(Qreserved_system, Preserved_system, Treserved_system)
print("Розрахуємо виграш надійності протягом часу {} годин за ймовірностю відмов:\nGq = {}\n"
      "виграш надійності протягом часу {} годин за ймовірностю безвідмовної роботи:\nGp = {}\n"
      "виграш надійності за середнім часом безвідмовної роботи:\nGt = {}".format(T, Gq, T, Gp, Gt))

Qreserved = [[] for _ in range(len(probs))]
Preserved = dict()
for i in range(len(Qreserved)):
    Qreserved[i] = general_unloaded(1 - probs[i], K2)
    Preserved.update({str(i+1) : round(1 - Qreserved[i], 6)})

print("Ймовірність відмови та безвідмовної роботи кожного елемента системи при його ненавантаженому резервуванні "
      "Кратність = {}\nQreserved = {}\nPreserved = {}".format(K2, Qreserved, Preserved.values()))

allProbabils2 = []
for i in all_system_states:
    probability = 1
    for k in graph.keys():
        if k in i and k !="end" and k !="start":
            probability *= Preserved[k]
        elif k not in i and k !="end" and k !="start":
            probability *= 1 - Preserved[k]
    allProbabils2.append(probability)

Preserved_system = round(sum(allProbabils2), 6)

Qreserved_system = round(1 - Preserved_system, 6)

Treserved_system = round(-T/math.log1p(Preserved_system-1))

Gq, Gp, Gt = reservation_quality_criteria(Qreserved_system, Preserved_system, Treserved_system)

print("ймовірність безвідмовної роботи в цілому:\nPreserved system = {}\n"
      "ймовірність безвідмовної роботи\n"
      "Qreserved system = {}\n"
      "значення середнього наробітку\n"
      "Treserved system = {}\n"
      "виграш надійності протягом часу {} годин за ймовірностю відмов:\nGq = {}\n"
      "виграш надійності протягом часу {} годин за ймовірностю безвідмовної роботи:\nGp = {}\n"
      "виграш надійності за середнім часом безвідмовної роботи:\nGt = {}".format(Preserved_system, Qreserved_system, Treserved_system,
                                                                                 T, Gq, T, Gp, Gt))
