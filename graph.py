from collections import deque
from read_rules_file import *
from preprocess import *

# A mudar:
#     O grafo é salvado como final_graph (linha 191), ainda falta criar o JSON
# a partir do grafo (dica DFS)
#
# OBS:
# "" é o nó inicial e "!" é o nó terminal. As respostas são "s", "n" e "ns".
# Há dois arquivos de teste (teste1 e teste2), se quiser mudar mude em linha 188


def back_propagate(reversed_graph):

    queue = deque()
    queue.append("!")

    while queue:
        node = queue.popleft()
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
        return pop_stack(stack)

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


# # Receive "s", "n" or "ns"
# def receive_answer():
#     while True:
#         answer = input()
#         if answer in ("s", "n", "ns"):
#             return answer
#
# def check_question(question, already_questioned, preprocess):
#     if question[0] == "*":
#         real_question = question[1:]
#
#         if real_question in already_questioned:
#             if already_questioned[real_question]:
#                 return "n"
#             else:
#                 return "s"
#
#         else:
#             send_question(real_question, preprocess)
#             answer = receive_answer()  # **************
#             if answer == "s":
#                 already_questioned[real_question] = True
#                 return "n"
#             if answer == "n":
#                 already_questioned[real_question] = False
#                 return "s"
#
#             return "ns"
#
#     else:
#         if question in already_questioned:
#             if already_questioned[question]:
#                 return "s"
#             else:
#                 return "n"
#
#         send_question(question, preprocess)
#         answer = receive_answer()
#         if answer == "s":
#             already_questioned[question] = True
#             return "s"
#         if answer == "n":
#             already_questioned[question] = False
#             return "n"
#
#     return "ns"


# def check_question_unitary(stack, already_questioned, preprocess):
#     nodes, index = stack[-1]
#     rule = nodes[index][0]
#
#     match = re.match("\*\((.*)", rule)
#     if match:
#         for question in match.groups()[0].split(";"):
#             answer = check_question(question, already_questioned, preprocess)
#             if answer == "s":
#                 return "n"
#             if answer == "ns":
#                 return "ns"
#         return "n"
#
#     for question in rule.split(";"):
#         answer = check_question(question, already_questioned, preprocess)
#         if answer in ("n", "ns"):
#             return answer
#     return "s"


def graphviz_debug(graph):
    buffer = []

    for u in graph:
        for v in graph[u]:
            if u != "":
                buffer.append(f"\"{u}\" -- \"{v[0]}\" [label={v[1]}]")
            else:
                buffer.append(f"\"i\" -- \"{v[0]}\" [label={v[1]}]")

    return "\n".join(buffer)


def graphviz_debug_pp(graph, pp):
    names = pp.name_conversion
    with open("graphviz.txt", "w", encoding="utf8") as f:
        for u in graph:
            for v in graph[u]:
                if u != "":
                    try:
                        f.write(f"\"{names[int(u)]}({u})\" -- ")
                    except Exception:
                        f.write(f"\"{u}\" -- ")

                    try:
                        f.write(f"\"{names[int(v[0])]}({v[0]})\" [label={v[1]}]")
                    except Exception:
                        f.write(f"\"{v[0]}\" [label={v[1]}]")

                    f.write("\n")

                else:
                    f.write(f"\"i\" -- ")
                    try:
                        f.write(f"\"{names[int(v[0])]}({v[0]})\" [label={v[1]}]")
                    except Exception:
                        f.write(f"\"{v[0]}\" [label={v[1]}]")
                    f.write("\n")


def remove_node(node, graph):
    # graph[node].clear()
    reversed_graph = reverse_graph(graph)
    reversed_graph.pop(node)
    graph.clear()
    graph.update(reverse_graph(reversed_graph))


def change_probability(new_prop, edge, graph):
    old_prob = 0
    for i in range(len(graph[edge[0]])):
        val = graph[edge[0]][i]
        if val[0] == edge[1]:
            old_prob = val[1]
            graph[edge[0]][i][1] = new_prop

    increment = new_prop-old_prob
    reversed_graph = reverse_graph(graph)

    queue = deque()
    queue.append(edge[0])

    for i in range(len(reversed_graph[edge[0]])):
        reversed_graph[edge[0]][i][1] += increment

    while queue:
        node = queue.popleft()
        for edges in reversed_graph[node]:
            next_edge = edges[0]

            queue.append(next_edge)

            inner_edges = reversed_graph[next_edge]

            for i in range(len(inner_edges)):
                inner_edges[i][1] += increment

    graph.clear()
    graph.update(reverse_graph(reversed_graph))


if __name__ == "__main__":
    file_path = "teste1.txt"

    with open(file_path, "r", encoding="utf8") as f:
        file_lines = f.readlines()
    preprocess = PreProcess(file_path)
    preprocess.execute()

    all_symptoms = preprocess.all_symptoms

    reversed_graph = read_entry(preprocess.lines, all_symptoms)

    back_propagate(reversed_graph)
    final_graph = reverse_graph(reversed_graph)

    stack = [[sorted(final_graph[""], key=lambda x: -x[1]), 0]]

    print(final_graph)
    # graphviz_debug(final_graph)

    # change_probability(0.2, ("2", "!"), final_graph)
    remove_node("1;4", final_graph)

    graphviz_debug_pp(final_graph, preprocess)
    print(all_symptoms)
    print(preprocess.name_conversion)
    print()

    # already_questioned = {}
    #
    # for i in preprocess.lines:
    #     print(i)
    #
    # # print("***************", rule_to_set("11;8", all_symptoms))
    #
    # res = None
    # while True:
    #     for i in stack:
    #         print(i)
    #     # answer = check_question(stack)
    #     # answer = check_question_unitary_pp(stack, already_questioned, preprocess)
    #     answer = check_question_unitary(stack, already_questioned, preprocess)
    #     res = iterate_stack(answer, final_graph, stack)
    #     for i in stack:
    #         print(i)
    #     print("--------")
    #
    #     if res:
    #         if res == "?":
    #             print("Erro logico: Negou sintomas de mais")
    #         else:
    #             print(f"Logo vc tem {preprocess.name_conversion[int(res)]}!")
    #         break
