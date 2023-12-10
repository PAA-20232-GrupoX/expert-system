from graph import *

SKIPPED = None


class QuestionManager:
    def __init__(self):
        self.questions = []
        self.index = 0
        self.already_questioned = {}

        self.current_question = ""
        self.not_equation = False
        self.not_question = False

    def __add_question(self, stack):
        nodes, index = stack[-1]
        rule = nodes[index][0]
        self.index = 0

        match = re.match("\*\((.*)", rule)
        if match:
            self.questions = match.groups()[0].split(";")
            self.not_equation = True
            return
        self.questions = rule.split(";")
        self.not_equation = False

    def next_question(self, stack):
        if len(self.questions) == 0 or self.index >= len(self.questions):
            self.__add_question(stack)

        question = self.questions[self.index]

        if question[0] == "*":
            real_question = question[1:]
            self.not_question = True
            self.current_question = real_question
            if real_question not in self.already_questioned:
                return real_question

        else:
            self.not_question = False
            self.current_question = question
            if question not in self.already_questioned:
                return question

        return SKIPPED

    def answer_question(self, answer):
        if self.not_question:
            if answer == "s":
                answer = "n"
            else:
                answer = "s"

        self.index += 1
        if self.not_equation:
            if answer == "n":
                return "s"

            if self.index >= len(self.questions):
                return "n"

        else:
            if answer == "n":
                return "n"

            if self.index >= len(self.questions):
                return "s"

        return "l"

    def iterate_node(self, answer):
        if answer == "ns":
            return "ns"

        if answer == SKIPPED:
            if self.already_questioned[self.current_question]:
                return self.answer_question("s")
            return self.answer_question("n")

        if answer == "s":
            self.already_questioned[self.current_question] = True
        else:
            self.already_questioned[self.current_question] = False
        return self.answer_question(answer)


# Migrated to graph
def receive_from_answer():
    return input()


# Migrated to graph
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


def send_dict_dict(dict):
    return dict


def send_metadata(metadata):
    return metadata


if __name__ == "__main__":
    ################ Começo Inicialização

    # Local do arquivo
    file_path = "teste1.txt"

    with open(file_path, "r", encoding="utf8") as f:
        file_lines = f.readlines()

    # all_symptoms = read_symptoms_lines(file_lines)
    preprocess = PreProcess(file_path)
    preprocess.execute()

    all_symptoms = preprocess.all_symptoms

    # reversed_graph = read_entry(file_lines, all_symptoms)
    reversed_graph = read_entry(preprocess.lines, all_symptoms)
    back_propagate(reversed_graph)

    final_graph = reverse_graph(reversed_graph)
    stack = [[sorted(final_graph[""], key=lambda x: -x[1]), 0]]

    ################ Fim inicialização

    print(f"Dicionario mandado: {send_dict_dict(preprocess.name_conversion)}")

    qm = QuestionManager()

    while True:
        print()
        while True:
            question = qm.next_question(stack)
            if question != SKIPPED:
                send_question(question, preprocess)     # Send question
                answer = receive_from_answer()          # Receive answer
            else:
                answer = SKIPPED

            full_answer = qm.iterate_node(answer)

            if full_answer != "l":
                break

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
                print(f"Logo vc tem {preprocess.name_conversion[int(result)]}!")
            break

