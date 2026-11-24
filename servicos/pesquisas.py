def _converter_valor(valor, referencia):
    # a entrada do usuário chega como str; converte para o tipo do atributo
    # (ex: populacao é int) antes de comparar. Retorna None se não for conversível.
    if referencia is None or isinstance(referencia, str):
        return valor

    try:
        return type(referencia)(valor)
    except (TypeError, ValueError):
        return None


def pesquisar_por_atributo(planetas, atributo, valor):
    resultados = []

    for planeta in planetas:
        if atributo not in planeta:
            raise ValueError(f"Atributo desconhecido: {atributo}")

        valor_convertido = _converter_valor(valor, planeta[atributo])

        if valor_convertido is not None and planeta[atributo] == valor_convertido:
            resultados.append(planeta)

    return resultados