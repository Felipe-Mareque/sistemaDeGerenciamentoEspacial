from api.swapi import buscar_planetas
from modelos.planeta import Planeta
from servicos.armazenamento import salvar_planetas
from estruturas.tabela_hash import TabelaHash

planetas = buscar_planetas()

planetas_normalizados = []

for dados in planetas:
    planeta = Planeta.de_dicionario(dados)
    dados_normalizados = planeta.para_dicionario()

    planetas_normalizados.append(dados_normalizados)

salvar_planetas(planetas_normalizados, "dados/planetas.json")

tabela = TabelaHash()
print("buscando")
print(tabela._funcao_hash("Tatooine"))
print(tabela._funcao_hash("Naboo"))
print(tabela._funcao_hash("Hoth"))
print(tabela._funcao_hash("Coruscant"))
print("ok")