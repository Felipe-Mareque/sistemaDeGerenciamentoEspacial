import requests

URL_BASE = "https://swapi.dev/api"


def buscar_planetas():
    url = f"{URL_BASE}/planets/"
    planetas = []

    while url is not None:
        resposta = requests.get(url)

        if resposta.status_code != 200:
            raise Exception(f"Erro ao consultar a SWAPI: {resposta.status_code}")

        dados = resposta.json()

        planetas.extend(dados["results"])

        url = dados["next"]

    return planetas