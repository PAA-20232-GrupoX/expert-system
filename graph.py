from collections import defaultdict, deque

# A mudar:
#   Atualmente a entrada lê um arquivo simplicado (linha 35):
#       X, A, B, 0.5
#   Mas deveria ler o por meio do parse, ou seja, ler regras da forma
#       X , Not (A; Not B), 0.6
#
#     O grafo é salvado como final_graph (linha 191), ainda falta criar o JSON
# a partir do grafo (dica DFS)
#
#   Falta implementar os casos com o NOT
#
# OBS:
# "" é o nó inicial e "!" é o nó terminal. As respostas são "s", "n" e "ns".
# Há dois arquivos de teste (teste1 e teste2), se quiser mudar mude em linha 188


def string_to_set(string):
    if len(string):
        return set(string.split(";"))
    return set()


def read_entry(path):
    all_nodes = set()

    reversed_graph = defaultdict(list)
    has_child = set()
    has_parent = set()

    with open(path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            aux = line.split(", ")
            c, s, prob = aux[0], ";".join(sorted(aux[1:-1])), float(aux[-1])

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


def back_propagate(reversed_graph):
    visited_node = set()

    queue = deque()
    queue.append("!")

    while queue:
        node = queue.popleft()
        if node not in visited_node:
            visited_node.add(node)

            for edges in reversed_graph[node]:
                summed_val = edges[1]
                next_edge = edges[0]

                queue.append(next_edge)

                inner_edges = reversed_graph[next_edge]

                for i in range(len(inner_edges)):
                    inner_edges[i][1] += summed_val

    return reversed_graph


def reverse_graph(graph):
    new_graph = defaultdict(list)

    for older_node in graph:
        for node, val in graph[older_node]:
            new_graph[node].append([older_node, val])
    return new_graph


def pop_stack(stack):
    nodes, index = stack[-1]
    nodes_size = len(nodes)
    if nodes_size > 1:
        if index == nodes_size - 1:
            stack[-1][1] -= 1

        nodes.pop(index)
    else:
        if len(stack) == 1:
            return True
        stack.pop()
        pop_stack(stack)

    return False


def is_terminal_node(node, graph):
    return "!" == graph[node][0][0]


def iterate_stack(answer, graph, stack):
    if answer == "s":
        nodes, index = stack[-1]
        current_node = nodes[index][0]

        next_list = sorted(graph[current_node], key=lambda x: -x[1])
        stack.append([next_list, 0])

        current_node = next_list[0][0]

    elif answer == "n":
        if pop_stack(stack):
            return "?"

        nodes, index = stack[-1]
        current_node = nodes[index][0]

    elif answer == "ns":
        nodes, index = stack[-1]
        new_index = (index + 1) % len(nodes)
        stack[-1][1] = new_index

        current_node = nodes[new_index][0]

    if is_terminal_node(current_node, graph):
        return current_node

    return None


def check_question(stack):
    nodes, index = stack[-1]
    string = nodes[index][0]

    print(f'Vc tem {" e ".join(string.split(";"))}?')
    return input()


def check_question_unitary(stack, already_quest):
    nodes, index = stack[-1]
    string = nodes[index][0]

    for symptom in string.split(";"):
        if symptom not in already_quest:
            while True:
                print(f'Vc tem {symptom}?')
                aux_answer = input()

                if aux_answer == "s":
                    already_quest[symptom] = True
                    break
                elif aux_answer == "n":
                    already_quest[symptom] = False
                    return "n"
                elif aux_answer == "ns":
                    return "ns"
        else:
            if not already_quest[symptom]:
                return "n"
    return "s"


if __name__ == "__main__":
    reversed_graph = read_entry("teste1.txt")

    back_propagate(reversed_graph)
    final_graph = reverse_graph(reversed_graph)

    stack = [[sorted(final_graph[""], key=lambda x: -x[1]), 0]]

    print(final_graph)
    print()

    already_questioned = {}

    res = None
    while True:
        for i in stack:
            print(i)
        # answer = check_question(stack)
        answer = check_question_unitary(stack, already_questioned)
        res = iterate_stack(answer, final_graph, stack)
        for i in stack:
            print(i)
        print("--------")

        if res:
            print(f"Logo vc tem {res}!")
            break
