from api.swapi import buscar_planetas
from modelos.planeta import Planeta

planetas = buscar_planetas()

dados = next(
    planeta for planeta in planetas
    if planeta["population"] == "unknown"
)

planeta = Planeta.de_dicionario(dados)

print("ID:", planeta.id)
print("Nome:", planeta.nome)
print("Clima:", planeta.clima)
print("Terreno:", planeta.terreno)
print("População:", planeta.populacao)
print("Diâmetro:", planeta.diametro)
print("Gravidade:", planeta.gravidade)
print("Água superficial:", planeta.agua_superficial)
print("Período de rotação:", planeta.periodo_rotacao)
print("Período orbital:", planeta.periodo_orbital)