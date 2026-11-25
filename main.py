from api.swapi import buscar_planetas
from modelos.planeta import Planeta
from servicos.armazenamento import salvar_planetas, carregar_planetas
from estruturas.tabela_hash import TabelaHash
from estruturas.trie import Trie
from servicos.autocompletar import (
    construir_trie,
    sugerir_nomes,
    resolver_nome,
    consultar_com_sugestoes
)
from servicos.pesquisas import pesquisar_por_atributo
from servicos.filtros import filtrar_por_populacao_minima
from servicos.similaridade import planetas_com_clima_similar
from guloso.planejamento_missao import (
    preparar_candidatos,
    ordenar_candidatos,
    planejar_missao
)


try:
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

except Exception:
    # Se a API falhar, usa os dados salvos na última execução
    print("API indisponível. Usando dados locais salvos.")
    planetas_normalizados = carregar_planetas("dados/planetas.json")


def ler_inteiro(mensagem, minimo=None):
    # repete a pergunta até o usuário digitar um inteiro válido (>= minimo, se informado)
    while True:
        entrada = input(mensagem)

        try:
            valor = int(entrada)
        except ValueError:
            print("Entrada inválida: digite um número inteiro.")
            continue

        if minimo is not None and valor < minimo:
            print(f"Entrada inválida: o valor deve ser maior ou igual a {minimo}.")
            continue

        return valor


# Cria e carrega a Tabela Hash
tabela = TabelaHash()

for planeta in planetas_normalizados:
    tabela.inserir(planeta)


# Mostra as métricas da estrutura
print("Quantidade de planetas:", tabela.quantidade)
print("Capacidade da tabela:", tabela.capacidade)
print("Colisões:", tabela.colisoes)
print("Fator de carga:", tabela.fator_carga())


# Cria e carrega a Trie (índice de nomes para busca por prefixo)
trie = construir_trie(Trie(), planetas_normalizados)

print()
print("Nomes na Trie:", trie.quantidade)
print("Nós da Trie:", trie.total_nos)


# Menu
while True:
    print()
    print("1 - Consultar planeta")
    print("2 - Pesquisar por atributo")
    print("3 - Filtrar por população mínima")
    print("4 - Planetas com clima similar")
    print("5 - Planejar missão")
    print("6 - Autocompletar nome (busca por prefixo)")
    print("0 - Sair")

    opcao = input("Opção: ")
    print()

    match opcao:
        case "1":
            nome = input("Nome do planeta: ")

            planeta, sugestoes = consultar_com_sugestoes(tabela, trie, nome)

            if planeta is not None:
                print(planeta)
            elif sugestoes:
                print("Planeta não encontrado. Você quis dizer:")

                for sugestao in sugestoes:
                    print(" -", sugestao)
            else:
                print("Planeta não encontrado.")

        case "2":
            atributo = input("Atributo (ex: clima, terreno): ")
            valor = input("Valor: ")

            try:
                resultados = pesquisar_por_atributo(
                    planetas_normalizados,
                    atributo,
                    valor
                )
            except ValueError as erro:
                print(erro)
                continue

            for planeta in resultados:
                print(planeta["nome"])

        case "3":
            populacao_minima = ler_inteiro("População mínima: ", minimo=0)

            resultados = filtrar_por_populacao_minima(
                planetas_normalizados,
                populacao_minima
            )

            for planeta in resultados:
                print(planeta["nome"], "-", planeta["populacao"])

        case "4":
            nome = resolver_nome(trie, input("Nome do planeta: "))

            if nome is None:
                print("Planeta não encontrado.")
                continue

            resultados = planetas_com_clima_similar(
                tabela,
                planetas_normalizados,
                nome
            )

            if not resultados:
                print("Nenhum outro planeta com clima similar a", nome)

            for planeta in resultados:
                print(planeta["nome"], "-", planeta["clima"])

        case "5":
            orcamento = ler_inteiro("Orçamento: ", minimo=0)

            candidatos = preparar_candidatos(planetas_normalizados)
            candidatos = ordenar_candidatos(candidatos)

            selecionados, recurso_utilizado, recurso_restante, beneficio_total = planejar_missao(
                candidatos,
                orcamento
            )

            for candidato in selecionados:
                print(
                    candidato["planeta"]["nome"],
                    "- benefício:",
                    candidato["beneficio"],
                    "- custo:",
                    candidato["custo"],
                    "- razão:",
                    candidato["razao"]
                )

            print()
            print("Resumo da missão:")
            print("Orçamento:", orcamento)
            print("Recurso utilizado:", recurso_utilizado)
            print("Recurso restante:", recurso_restante)
            print("Benefício total:", beneficio_total)

        case "6":
            prefixo = input("Prefixo do nome: ")

            resultados = sugerir_nomes(trie, prefixo)

            if not resultados:
                print("Nenhum planeta começa com", repr(prefixo.strip()))

            for nome in resultados:
                print(nome)

            print()
            print("Encontrados:", len(resultados))
            print("Nós visitados na Trie:", trie.nos_visitados)

        case "0":
            break

        case _:
            print("Opção inválida")
