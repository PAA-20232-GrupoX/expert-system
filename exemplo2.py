from graph import *


def send_graph(graph):
    return graph


if __name__ == "__main__":
    # Local do arquivo
    file_path = "teste1.txt"

    with open(file_path, "r", encoding="utf8") as f:
        file_lines = f.readlines()

    all_symptoms = read_symptoms_lines(file_lines)

    reversed_graph = read_entry(file_lines, all_symptoms)
    back_propagate(reversed_graph)

    final_graph = reverse_graph(reversed_graph)

    # Aqui envia o grafo para o front ************************************
    graph = send_graph(final_graph)
    print(f"Grafo enviado: \n{graph}]")

    # Visualização via graphviz:
    # Copiar e colar em https://dreampuf.github.io/GraphvizOnline
    print("\nColar no graphviz!\n")
    print("graph G {")
    print(graphviz_debug(final_graph))
    print("}")
