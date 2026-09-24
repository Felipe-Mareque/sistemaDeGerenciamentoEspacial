import json


def salvar_planetas(planetas, caminho):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(planetas, arquivo, ensure_ascii=False, indent=4)