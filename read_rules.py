import json
import re

class RulesParser:
    def __init__(self, filename):
        self.filename = filename

    @staticmethod
    def parse_line(line):
        match = re.match(r'(.*), \((.*)\), ([0-9.]+)', line)
        if not match:
            return None

        identificador, condicoes, probabilidade = match.groups()
        probabilidade = float(probabilidade)
        identificador = identificador.strip()[2:]
        condicoes = condicoes.split(", ")
        expressao = RulesParser.parse_conditions(condicoes)

        return {
            "identificador": identificador,
            "expressao": expressao,
            "probabilidade": probabilidade
        }

    @staticmethod
    def parse_conditions(condicoes):
        expressao = {"tipo": "AND", "condicoes": []}
        for condicao in condicoes:
            condicao = condicao.strip()
            if "NOT" in condicao:
                valor = condicao.replace("NOT ", "")[2:]
                expressao["condicoes"].append({
                    "tipo": "NOT",
                    "condicao": {"tipo": "SINTOMA", "valor": valor}
                })
            else:
                valor = condicao[2:]
                expressao["condicoes"].append({
                    "tipo": "SINTOMA",
                    "valor": valor
                })
        return expressao

    def parse_txt_to_json(self):
        rules = []
        with open(self.filename, "r") as file:
            for line in file:
                parsed_line = self.parse_line(line)
                if parsed_line:
                    rules.append(parsed_line)

        with open('rules.json', 'w', encoding='utf-8') as json_file:
            json.dump(rules, json_file, indent=4, ensure_ascii=False)


parser = RulesParser("regras.txt")
parser.parse_txt_to_json()
