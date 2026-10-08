def calcular_beneficio(planeta):
    beneficio = 0

    if planeta["populacao"] is not None:
        beneficio += 2

    if planeta["agua_superficial"] is not None:
        beneficio += 3

    if planeta["diametro"] is not None:
        beneficio += 1

    if planeta["gravidade"] is not None:
        beneficio += 1

    if planeta["periodo_orbital"] is not None:
        beneficio += 1

    return beneficio




def calcular_custo(planeta):
    custo = 1

    if planeta["periodo_orbital"] is None:
        custo += 1
    else:
        if planeta["periodo_orbital"] > 300:
            custo += 1

        if planeta["periodo_orbital"] > 500:
            custo += 1

    if planeta["diametro"] is None:
        custo += 1
    else:
        if planeta["diametro"] > 10000:
            custo += 1

        if planeta["diametro"] > 20000:
            custo += 1

    if planeta["agua_superficial"] is None:
        custo += 1

    if planeta["gravidade"] is None:
        custo += 1

    return custo