import numpy as np

# Exemplo de modelos de ML
models = [
    {'name': 'Rede Convolucional', 'answers': {'imagens': 1, 'dados rotulados': 1, 'análise visual': 1}},
    
    {'name': 'Rede Neural Recorrente', 'answers': {'texto': 1, 'dados sequenciais': 1}},
    
    {'name': 'Máquina de Vetores de Suporte', 'answers': {'dados estruturados': 1, 'classificação binária': 1}},
    
    {'name': 'Árvore de Decisão', 'answers': {'dados categóricos': 1, 'dados rotulados': 1}},
    
    {'name': 'Floresta Aleatória', 'answers': {'dados estruturados': 1, 'dados com ruído': 1, 'dados rotulados': 1}},
    
    {'name': 'Boosting', 'answers': {'dados desbalanceados': 1, 'dados rotulados': 1}},
    
    {'name': 'Rede Neural Profunda', 'answers': {'dados de alta dimensão': 1, 'dados rotulados': 1}},
    
    {'name': 'K-Means', 'answers': {'dados não rotulados': 1, 'agrupamento': 1}},
    
    {'name': 'PCA', 'answers': {'redução de dimensionalidade': 1, 'dados contínuos': 1}},
    
    {'name': 'Regressão Logística', 'answers': {'dados estruturados': 1, 'dados rotulados': 1, 'classificação binária': 1}},
    
    {'name': 'Naive Bayes', 'answers': {'texto': 1, 'classificação rápida': 1}},
    
    {'name': 'KNN', 'answers': {'dados pouco complexos': 1, 'classificação multiclasse': 1}},
    
    {'name': 'Rede Generativa Adversarial', 'answers': {'imagens': 1, 'dados não rotulados': 1}},
    
    {'name': 'Autoencoder', 'answers': {'imagens': 1, 'redução de ruído': 1}},
    
    {'name': 'Regressão Linear', 'answers': {'dados contínuos': 1, 'relação linear': 1}},
    
    {'name': 'Regressão Polinomial', 'answers': {'dados contínuos': 1, 'relação não-linear': 1}},
    
    {'name': 'Rede LSTM', 'answers': {'texto': 1, 'dados sequenciais': 1}},
    
    {'name': 'Rede GRU', 'answers': {'dados sequenciais': 1, 'eficiência computacional': 1}},
    
    {'name': 'SOM (Mapas Auto-Organizáveis)', 'answers': {'dados multidimensionais': 1, 'dados não rotulados': 1}},
    
    {'name': 'Algoritmo Genético', 'answers': {'otimização de parâmetros': 1, 'ambientes dinâmicos': 1}}
]



def calculate_probabilities(questions_so_far, answers_so_far):
    probabilities = []
    for model in models:
        probabilities.append({
            'name': model['name'],
            'probability': calculate_model_probability(model, questions_so_far, answers_so_far)
        })

    return probabilities

def calculate_model_probability(model, questions_so_far, answers_so_far):
    # Prior uniforme para todos os modelos
    P_model = 1 / len(models)

    # Likelihood
    P_answers_given_model = 1
    P_answers_given_not_model = 1
    for question, answer in zip(questions_so_far, answers_so_far):
        P_answers_given_model *= 1 - \
            abs(answer - model_answer(model, question))

        P_answer_not_model = np.mean([1 - abs(answer - model_answer(not_model, question))
                                      for not_model in models
                                      if not_model['name'] != model['name']])
        P_answers_given_not_model *= P_answer_not_model

    # Evidence
    P_answers = P_model * P_answers_given_model + \
        (1 - P_model) * P_answers_given_not_model

    # Bayes Theorem
    P_model_given_answers = (
        P_answers_given_model * P_model) / P_answers

    return P_model_given_answers

def model_answer(model, question):
    if question in model['answers']:
        return model['answers'][question]
    return 0.5  # Padrão para incerteza ou falta de informação


def get_answers(models, k=5):
    # Contagem de frequência das características
    answer_count = {}
    for model in models:
        for answer in model['answers']:
            if answer in answer_count:
                answer_count[answer] += 1
            else:
                answer_count[answer] = 1

    # Classificação das características mais comuns
    sorted_answers = sorted(answer_count.items(), key=lambda x: x[1], reverse=True)
    # Retorna apenas as respostas (não a tupla inteira)
    return [answer[0] for answer in sorted_answers[:k]]



# Exemplo de uso
questions = get_answers(models)
answers = [1, 1, 0, 0, 0]  # Sim para ambas as perguntas

probabilities = calculate_probabilities(questions, answers)

print(probabilities)
