from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

def send_next_symptom(stack, already_quest):
    nodes, index = stack[-1]
    string = nodes[index][0]
    for symptom in string.split(";"):
        if symptom not in already_quest:
            return symptom
    return "ended"

@app.get("/tree")
async def root():
    file_path = "teste1.txt"

    with open(file_path, "r", encoding="utf8") as f:
        file_lines = f.readlines()

    all_symptoms = read_symptoms_lines(file_lines)

    reversed_graph = read_entry(file_lines, all_symptoms)
    back_propagate(reversed_graph)

    final_graph = reverse_graph(reversed_graph)
    stack = [[sorted(final_graph[""], key=lambda x: -x[1]), 0]]

    already_questioned = {}

    # Aqui manda o próximo sintoma para gerar a pergunta *********************
    next_symptom = send_next_symptom(stack, already_questioned)
    # Aqui envia o grafo para o front ************************************
    return {"graph": final_graph, "stack": stack, "already_questioned": already_questioned, "next_symptom": next_symptom}

@app.post("/answer")
async def root(graph: dict, stack: list, already_questioned: dict, next_symptom: str, answer: str):
    if answer == "s":
        already_questioned[next_symptom] = True
    elif answer == "n":
        already_questioned[next_symptom] = False

    result = iterate_stack(answer, graph, stack)
    
    if result:
        return {"result": result, "stack": stack, "already_questioned": already_questioned, "next_symptom": next_symptom}
    
    next_symptom = send_next_symptom(stack, already_questioned)
    return {"result": False, "stack": stack, "already_questioned": already_questioned, "next_symptom": next_symptom}
    


