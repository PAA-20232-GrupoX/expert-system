from graph import  *


def receive_from_answer():
    return input()


def send_next_symptom(stack, already_quest):
    nodes, index = stack[-1]
    string = nodes[index][0]
    for symptom in string.split(";"):
        if symptom not in already_quest:
            return symptom
    return "ended"


class MetaData:
    def __init__(self, result, stack):
        self.result = result
        self.stack = stack


def send_metadata(metadata):
    return metadata


if __name__ == "__main__":
    ################ Começo Inicialização

    # Local do arquivo
    file_path = "teste1.txt"

    with open(file_path, "r", encoding="utf8") as f:
        file_lines = f.readlines()

    all_symptoms = read_symptoms_lines(file_lines)

    reversed_graph = read_entry(file_lines, all_symptoms)
    back_propagate(reversed_graph)

    final_graph = reverse_graph(reversed_graph)
    stack = [[sorted(final_graph[""], key=lambda x: -x[1]), 0]]

    already_questioned = {}
    ################ Fim inicialização
    while True:

        # Aqui manda o próximo sintoma para gerar a pergunta *********************
        next_symptom = send_next_symptom(stack, already_questioned)

        if next_symptom == "ended":
            print("Erro logico: Negou sintomas de mais")
            break
        print(f'Vc tem {next_symptom}?')

        # Aqui recebe a resposta da pergunta ***************************************
        answer = receive_from_answer()

        print(f"Sintoma enviado: {next_symptom}?")
        print(f"Resposta recebida: {answer}")

        if answer == "s":
            already_questioned[next_symptom] = True
        elif answer == "n":
            already_questioned[next_symptom] = False

        result = iterate_stack(answer, final_graph, stack)

        metadata = MetaData(result, stack)

        # Aqui envia os metadados, possívelmente o possível resultado da predição **************
        # e o estado da pilha de execução
        send_metadata(metadata)
        print(f"Metadados enviados: {result} {stack}")

        if result:
            if result == "?":
                print("Erro logico: Negou sintomas de mais")
            else:
                print(f"Logo vc tem {result}!")
            break

