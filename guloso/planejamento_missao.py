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