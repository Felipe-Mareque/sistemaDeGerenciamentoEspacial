from estruturas.tabela_hash import TabelaHash


tabela = TabelaHash()

for numero in range(1, 9):
    planeta = {"nome": f"Planeta {numero}"}

    tabela.inserir(planeta)

    print(
        f"Inserção {numero}: "
        f"quantidade={tabela.quantidade}, "
        f"capacidade={tabela.capacidade}, "
        f"fator={tabela.fator_carga()}"
    )