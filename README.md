# Sistema Especialista

Este é um sistema especialista que utiliza regras definidas em um arquivo de texto para realizar inferências sobre um conjunto de condições. O objetivo é avaliar a probabilidade de ocorrência de determinados eventos com base nas condições fornecidas.

## Instalação

Certifique-se de ter o Python instalado em seu ambiente. Para instalar as dependências necessárias, execute o seguinte comando:

```bash
pip install -r requirements.txt
```
## Utilização
Definir Regras:

As regras são definidas no arquivo de texto regras.txt. Cada linha segue o formato: identificador, (condicoes), probabilidade.
Executar o Parser:

Execute o script main.py para converter as regras do formato de texto para JSON. Isso criará o arquivo rules.json.
bash
Copy code
python main.py
## Analisar Condições:

Executar servidor:
```
uvicorn server:app --reload
```

Utilize as regras convertidas em JSON para realizar inferências sobre as condições específicas.
Estrutura do Projeto
main.py: Script principal para análise e conversão das regras.
regras.txt: Arquivo de entrada contendo as regras no formato de texto.
rules.json: Arquivo de saída com as regras convertidas para o formato JSON.
rules_parser.py: Módulo contendo a classe RulesParser para análise e conversão de regras.
