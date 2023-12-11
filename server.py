from typing import Tuple, List, Union
from types import UnionType
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import HTTPException
from graph import *


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SKIPPED = None
class ChangeProbabilityData(BaseModel):
    new_prop: float#nova probabilidade
    edge: Tuple[str, str]#  aresta que você deseja modificar
    stack: List[List[Union[List[Tuple[str, float]], int]]] #Cada sublista parece ter dois elementos: uma lista de tuplas representando nós do grafo e um índice


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

    def reset(self):
        self.questions = []
        self.index = 0
        self.already_questioned = {}

        self.current_question = ""
        self.not_equation = False
        self.not_question = False

    def next_question(self, stack):
        if len(self.questions) == 0:
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
                self.questions.clear()
                return "s"

            if self.index >= len(self.questions):
                self.questions.clear()
                return "n"

        else:
            if answer == "n":
                self.questions.clear()
                return "n"

            if self.index >= len(self.questions):
                self.questions.clear()
                return "s"

        return "l"

    def iterate_node(self, answer):
        if answer == "ns":
            self.questions.clear()
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


# Receive "s", "n" or "ns"
def receive_answer():
    while True:
        answer = input()
        if answer in ("s", "n", "ns"):
            return answer


# Must send "preprocess.name_conversion[int(question)]"
def send_question(question, preprocess):
    print(f"Vc tem {preprocess.name_conversion[int(question)]}?")


class MetaData:
    def __init__(self, result, stack):
        self.result = result
        self.stack = stack


def send_dict_dict(dict):
    return dict


def send_metadata(metadata):
    return metadata

qm = QuestionManager()
@app.get("/graph")
async def root():
    ################ Começo Inicialização

    # Local do arquivo
    file_path = "rules_sem_not.txt"

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

    ################ Fim inicialização
    return {"graph": final_graph, "nameConv": preprocess.name_conversion, "allSymptoms": all_symptoms }

@app.get("/tree")
async def root():
    ################ Começo Inicialização

    # Local do arquivo
    file_path = "rules_sem_not.txt"

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

    question = qm.next_question(stack)
    
    ################ Fim inicialização
    return {"graph": final_graph, "stack": stack, "next_symptom": question, "nameConv": preprocess.name_conversion, "allSymptoms": all_symptoms }

class AnswerData(BaseModel):
    graph: dict
    stack: list
    answer: str

@app.post("/answer")
async def root(data: AnswerData):
    full_answer = qm.iterate_node(data.answer)
    
    if full_answer == "l":
        while True:
            question = qm.next_question(data.stack)
            if question != SKIPPED:
                return {"result": False, "stack": data.stack, "next_symptom": question}
            
            answer = SKIPPED
            full_answer = qm.iterate_node(answer)
            
            if full_answer != "l":
                break
    
    result = iterate_stack(full_answer, data.graph, data.stack)

    if result:
        qm.reset()
        return {"result": result, "stack": data.stack, "next_symptom": None}

    
    while True:
        question = qm.next_question(data.stack)
        if question != SKIPPED:
            print(question, "2")
            return {"result": False, "stack": data.stack, "next_symptom": question}
        
        answer = SKIPPED
        full_answer = qm.iterate_node(answer)

@app.delete("/remove_node/{node_id}")
async def remove_node_endpoint(node_id: str):
    try:
        stack = [[sorted(final_graph[""], key=lambda x: -x[1]), 0]]  # Supondo uma stack inicial padrão
        remove_node(node_id, final_graph)
        
        # Obter próxima pergunta após remover o nó
        question = qm.next_question(stack)

        return {
            "message": f"Nó {node_id} removido com sucesso",
            "graph": final_graph,
            "stack": stack,
            "next_symptom": question
        }
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Nó {node_id} não encontrado no grafo")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.post("/change_probability")
async def change_probability_endpoint(data: ChangeProbabilityData):
    try:
        new_prop = data.new_prop #nova probabilidade
        edge = data.edge        #aresta que você deseja modificar
        stack = data.stack

        # Chama a função para modificar a probabilidade
        change_probability(new_prop, edge, final_graph)

        # Obtém a próxima pergunta após a modificação
        question = qm.next_question(stack)

        # Retorna a resposta com o novo grafo, stack e próxima pergunta
        return {
            "message": f"Probabilidade modificada com sucesso",
            "graph": final_graph,
            "stack": stack,
            "next_symptom": question
        }

    except KeyError:
        raise HTTPException(status_code=404, detail=f"Edge {edge} não encontrada no grafo")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

        
    

