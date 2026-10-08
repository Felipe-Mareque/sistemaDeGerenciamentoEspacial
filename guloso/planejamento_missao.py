from servicos.avaliacao import calcular_beneficio, calcular_custo


def preparar_candidatos(planetas):
    candidatos = []

    for planeta in planetas:
        beneficio = calcular_beneficio(planeta)
        custo = calcular_custo(planeta)
        razao = beneficio / custo

        candidato = {
            "planeta": planeta,
            "beneficio": beneficio,
            "custo": custo,
            "razao": razao
        }

        candidatos.append(candidato)

    return candidatos



def ordenar_candidatos(candidatos):
    return sorted(
        candidatos,
        key=lambda candidato: candidato["razao"],
        reverse=True
    )


def planejar_missao(candidatos, orcamento):
    selecionados = []
    recurso_utilizado = 0
    beneficio_total = 0

    for candidato in candidatos:
        if recurso_utilizado + candidato["custo"] <= orcamento:
            selecionados.append(candidato)
            recurso_utilizado += candidato["custo"]
            beneficio_total += candidato["beneficio"]

    recurso_restante = orcamento - recurso_utilizado

    return selecionados, recurso_utilizado, recurso_restante, beneficio_total