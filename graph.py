from collections import deque
from read_rules_file import *

# A mudar:
#     O grafo é salvado como final_graph (linha 191), ainda falta criar o JSON
# a partir do grafo (dica DFS)
#
# OBS:
# "" é o nó inicial e "!" é o nó terminal. As respostas são "s", "n" e "ns".
# Há dois arquivos de teste (teste1 e teste2), se quiser mudar mude em linha 188


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
    file_path = "teste1.txt"

    with open(file_path, "r", encoding="utf8") as f:
        file_lines = f.readlines()

    all_symptoms = read_symptoms_lines(file_lines)

    reversed_graph = read_entry(file_lines, all_symptoms)

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
