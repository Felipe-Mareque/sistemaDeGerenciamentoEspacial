# Integração Trie + Tabela Hash.
# A Trie resolve o NOME (prefixo, sem diferenciar maiúsculas) e a Tabela Hash
# resolve o PLANETA a partir do nome exato. Os serviços usam só a interface
# pública das estruturas (inserir / buscar / pesquisar_prefixo).

from servicos.consultas import consultar_planeta


def construir_trie(trie, planetas):
    for planeta in planetas:
        trie.inserir(planeta["nome"])

    return trie


def sugerir_nomes(trie, prefixo):
    return trie.pesquisar_prefixo(prefixo)


# converte o que o usuário digitou ("tatooine", " Tatooine ") no nome exato
# cadastrado ("Tatooine"), ou None se não existir
def resolver_nome(trie, nome):
    if not trie.buscar(nome):
        return None

    alvo = nome.strip().lower()

    for candidato in trie.pesquisar_prefixo(nome):
        if candidato.lower() == alvo:
            return candidato

    return None


# consulta tolerante: tenta o nome digitado na hash; se não achar, usa a Trie
# para corrigir maiúsculas/espaços. Retorna (planeta, sugestoes).
def consultar_com_sugestoes(tabela, trie, nome):
    planeta = consultar_planeta(tabela, nome)

    if planeta is not None:
        return planeta, []

    nome_exato = resolver_nome(trie, nome)

    if nome_exato is not None:
        return consultar_planeta(tabela, nome_exato), []

    if nome.strip() == "":
        return None, []

    return None, sugerir_nomes(trie, nome)
