from api.swapi import buscar_planetas
from modelos.planeta import Planeta
from servicos.armazenamento import salvar_planetas

planetas = buscar_planetas()

planetas_normalizados = []

for dados in planetas:
    planeta = Planeta.de_dicionario(dados)
    dados_normalizados = planeta.para_dicionario()

    planetas_normalizados.append(dados_normalizados)

salvar_planetas(planetas_normalizados, "dados/planetas.json")