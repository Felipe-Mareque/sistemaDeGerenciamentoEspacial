def filtrar_por_populacao_minima(planetas, populacao_minima):
    resultados = []

    for planeta in planetas:
        if planeta["populacao"] is not None and planeta["populacao"] >= populacao_minima:
            resultados.append(planeta)

    return resultados