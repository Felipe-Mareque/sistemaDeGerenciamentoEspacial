from api.swapi import buscar_planetas
from modelos.planeta import Planeta
from servicos.armazenamento import salvar_planetas
from estruturas.tabela_hash import TabelaHash
from servicos.consultas import consultar_planeta
from servicos.pesquisas import pesquisar_por_atributo
from servicos.filtros import filtrar_por_populacao_minima
from servicos.avaliacao import calcular_beneficio, calcular_custo
from guloso.planejamento_missao import preparar_candidatos, ordenar_candidatos


# Busca os planetas na SWAPI
planetas = buscar_planetas()

# Normaliza os dados recebidos da API
planetas_normalizados = []

for dados in planetas:
    planeta = Planeta.de_dicionario(dados)
    dados_normalizados = planeta.para_dicionario()

    planetas_normalizados.append(dados_normalizados)


# Salva os dados localmente
salvar_planetas(planetas_normalizados, "dados/planetas.json")


# Cria a Tabela Hash
tabela = TabelaHash()


# Carrega os planetas na Tabela Hash
for planeta in planetas_normalizados:
    tabela.inserir(planeta)


# Mostra as métricas da estrutura
print("Quantidade de planetas:", tabela.quantidade)
print("Capacidade da tabela:", tabela.capacidade)
print("Colisões:", tabela.colisoes)
print("Fator de carga:", tabela.fator_carga())

print()
print("Consulta por Tatooine:")
print(consultar_planeta(tabela, "Tatooine"))

print()
print("Consulta por planeta inexistente:")
print(consultar_planeta(tabela, "Planeta Inexistente"))

print()
print("Pesquisa por clima árido:")
resultados = pesquisar_por_atributo(
    planetas_normalizados,
    "clima",
    "arid"
)

for planeta in resultados:
    print(planeta["nome"])




print()
print("Planetas com população mínima de 100000:")

resultados = filtrar_por_populacao_minima(
    planetas_normalizados,
    100000
)

for planeta in resultados:
    print(planeta["nome"], "-", planeta["populacao"])


print()
print("Benefício dos planetas:")

for planeta in planetas_normalizados:
    beneficio = calcular_beneficio(planeta)
    print(planeta["nome"], "-", beneficio)



print()
print("Custo dos planetas:")
for planeta in planetas_normalizados:
    custo = calcular_custo(planeta)
    print(planeta["nome"], "-", custo)


print()
print("Candidatos ordenados:")

candidatos = preparar_candidatos(planetas_normalizados)
candidatos = ordenar_candidatos(candidatos)

for candidato in candidatos:
    print(
        candidato["planeta"]["nome"],
        "- benefício:",
        candidato["beneficio"],
        "- custo:",
        candidato["custo"],
        "- razão:",
        candidato["razao"]
    )
