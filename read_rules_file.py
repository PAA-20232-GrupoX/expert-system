import re
from collections import defaultdict


def read_symptoms_lines(file_lines):
    res = set()
    for line in file_lines:
        for symp in re.findall("“S\s*((?:(?:\w|\*|-)*\s*)*)”", line):
            res.add(symp)

    return res


def combine_symptoms(symptoms):
    aux = symptoms.split(";")

    for i in range(len(aux)):
        match = re.match("\s*(NOT|)\s*“(?:S|C)\s*((?:(?:\w|\*|-)*\s*)*)”", aux[i]).groups()
        if match[0] == "NOT":
            aux[i] = "*" + match[1]
        else:
            aux[i] = match[1]

    return ";".join(sorted(aux))


def read_new_command(line):
    match_total = re.match("“(?:S|C)\s*((?:(?:\w|\*|-)*\s*)*)”,\s*(NOT|)\s*\((.*)\),\s*([0-9.]+)",
                           line)
    match = match_total.groups()
    if match[1] == "":
        return match[0], combine_symptoms(match[2]), float(match[3])

    return match[0], "*("+combine_symptoms(match[2]),  float(match[3])


def question_to_set(question, symptoms_set):
    aux_set = set()
    if question[0] == "*":
        aux_set.add(question[1:])
        return symptoms_set.difference(aux_set)
    aux_set.add(question)
    return aux_set


def rule_to_set(rule, symptoms_set):
    match = re.match("\*\((.*)", rule)

    result_set = set()
    if match:
        for question in match.groups()[0].split(";"):
            result_set = result_set.union(question_to_set(question, symptoms_set))
        return symptoms_set.difference(result_set)

    for question in rule.split(";"):
        result_set = result_set.union(question_to_set(question, symptoms_set))

    return result_set


def read_entry(lines, all_symptoms):
    all_nodes = set().union(all_symptoms)

    reversed_graph = defaultdict(list)
    has_child = set()
    has_parent = set()

    for line in lines:
        c, s, prob = read_new_command(line)

        # add node to all nodes
        all_nodes.add(c)
        all_nodes.add(s)

        # append in the graphs
        reversed_graph[c].append([s, prob])
        has_child.add(s)
        has_parent.add(c)

    all_nodes = sorted(list(all_nodes), key=len)
    # all_nodes = list(all_nodes)
    all_nodes_set = [rule_to_set(i, all_symptoms) for i in all_nodes]

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
            reversed_graph[node].append(["", 0.0])
        if node not in has_child:
            reversed_graph["!"].append([node, 0.0])

    return reversed_graph
