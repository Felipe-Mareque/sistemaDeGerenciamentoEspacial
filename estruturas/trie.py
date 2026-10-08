# Interface da Trie (implementação na Parte 2)
# Uso previsto: busca de planetas por prefixo do nome (autocompletar)
class Trie:

    # cria a raiz vazia e o contador de nós visitados (métrica instrumentada)
    def __init__(self):
        pass

    # recebe o nome de um planeta (str) e o insere caractere por caractere
    def inserir(self, palavra):
        pass

    # recebe um nome (str) e retorna True se ele existir na Trie, senão False
    def buscar(self, palavra):
        pass

    # recebe um prefixo (str) e retorna a lista de nomes que começam com ele
    def pesquisar_prefixo(self, prefixo):
        pass
