def pesquisar_por_atributo(planetas, atributo, valor):
    resultados = []

    for planeta in planetas:
        if planeta[atributo] == valor:
            resultados.append(planeta)

    return resultados