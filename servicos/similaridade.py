def planetas_com_clima_similar(tabela, planetas, nome):
    referencia = tabela.buscar(nome)

    if referencia is None:
        return []

    climas_referencia = referencia["clima"].split(", ")
    resultados = []

    for planeta in planetas:
        if planeta["nome"] == nome:
            continue

        for clima in planeta["clima"].split(", "):
            if clima in climas_referencia:
                resultados.append(planeta)
                break

    return resultados
