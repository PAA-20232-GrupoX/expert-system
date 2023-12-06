import re
from collections import defaultdict


def read_symptoms_lines(file_lines):
    res = set()
    for line in file_lines:
        for symp in re.findall("“S\s*((?:(?:\w|\*|-)*\s*)*)”", line):
            res.add(symp)

    return res


def combine_line(line, symptoms_set):
    res = set()
    for symptom in line.split(";"):
        match = re.match("\s*(NOT|)\s*“(?:S|C)\s*((?:(?:\w|\*|-)*\s*)*)”", symptom).groups()
        if match[0] == "NOT":
            aux_set = set()
            aux_set.add(match[1])
            res = res.union(symptoms_set.difference(aux_set))
        else:
            res.add(match[1])
    return res


def new_command(line, symptoms_set):

    match_total = re.match("“(?:S|C)\s*((?:(?:\w|\*|-)*\s*)*)”,\s*(NOT|)\s+\((.*)\),\s*([0-9.]+)",
                           line)
    if not match_total:
        print(line)
    match = match_total.groups()

    if match[1] == "NOT":
        res = symptoms_set.difference(combine_line(match[2], symptoms_set))
    else:
        res = combine_line(match[2], symptoms_set)

    return match[0], ";".join(sorted(list(res))), float(match[3])


def string_to_set(string):
    if len(string):
        return set(string.split(";"))
    return set()


def read_entry(lines, all_symptoms):
    all_nodes = set().union(all_symptoms)

    reversed_graph = defaultdict(list)
    has_child = set()
    has_parent = set()

    for line in lines:
        c, s, prob = new_command(line, all_symptoms)

        # add node to all nodes
        all_nodes.add(c)
        all_nodes.add(s)

        # append in the graphs
        reversed_graph[c].append([s, prob])
        has_child.add(s)
        has_parent.add(c)

    all_nodes = sorted(list(all_nodes), key=len)
    all_nodes_set = [string_to_set(i) for i in all_nodes]

    nodes_size = len(all_nodes)

    for i in range(nodes_size):
        for j in range(i+1, nodes_size):
            if all_nodes_set[i].issubset(all_nodes_set[j]):
                node_i = all_nodes[i]
                node_j = all_nodes[j]

                reversed_graph[node_j].append([node_i, 0.0])
                has_child.add(node_i)
                has_parent.add(node_j)

    for node in all_nodes:
        if node not in has_parent:
            reversed_graph[node].append(["", 0])
        if node not in has_child:
            reversed_graph["!"].append([node, 0])

    return reversed_graph
