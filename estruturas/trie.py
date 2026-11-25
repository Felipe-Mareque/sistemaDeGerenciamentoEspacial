# Trie (árvore de prefixos) implementada do zero.
# Uso: busca de planetas por prefixo do nome (autocompletar).
#
# Decisões de implementação:
# - Sem dict/set: os filhos de cada nó ficam em uma lista simples, mantida em
#   ordem alfabética por inserção manual. Assim pesquisar_prefixo devolve os
#   nomes já ordenados, sem precisar de sorted().
# - Lista com busca linear em vez de vetor fixo de 26 posições: os nomes da
#   SWAPI têm espaços e maiúsculas ("Yavin IV", "Mon Cala"), então o alfabeto
#   não é fixo. Como cada nó tem poucos filhos, a busca linear é barata.
# - Sem diferenciar maiúsculas: os caracteres são guardados em minúsculo
#   ("tat" encontra "Tatooine"), e o nome original fica no nó final para exibição.


class _NoTrie:

    def __init__(self, caractere):
        self.caractere = caractere
        self.filhos = []            # lista de _NoTrie, em ordem alfabética
        self.fim_de_palavra = False
        self.palavra = None         # nome original (com maiúsculas), só no nó final


class Trie:

    # cria a raiz vazia e o contador de nós visitados (métrica instrumentada)
    def __init__(self):
        self.raiz = _NoTrie(None)
        self.quantidade = 0         # palavras distintas armazenadas
        self.total_nos = 1          # inclui a raiz
        self.nos_visitados = 0      # nós percorridos na última operação

    # recebe o nome de um planeta (str) e o insere caractere por caractere.
    # Retorna True se inseriu e False se a palavra já existia.
    def inserir(self, palavra):
        palavra_normalizada = self._normalizar(palavra)

        if palavra_normalizada == "":
            raise ValueError("Não é possível inserir uma palavra vazia.")

        self.nos_visitados = 0
        no = self.raiz

        for caractere in palavra_normalizada:
            filho = self._buscar_filho(no, caractere)

            if filho is None:
                filho = _NoTrie(caractere)
                self._adicionar_filho_ordenado(no, filho)
                self.total_nos += 1

            no = filho
            self.nos_visitados += 1

        if no.fim_de_palavra:
            return False

        no.fim_de_palavra = True
        no.palavra = palavra.strip()
        self.quantidade += 1
        return True

    # recebe um nome (str) e retorna True se ele existir na Trie, senão False
    def buscar(self, palavra):
        palavra_normalizada = self._normalizar(palavra)

        if palavra_normalizada == "":
            self.nos_visitados = 0
            return False

        no = self._descer(palavra_normalizada)
        return no is not None and no.fim_de_palavra

    # recebe um prefixo (str) e retorna a lista de nomes que começam com ele,
    # em ordem alfabética. Prefixo vazio retorna todos os nomes.
    def pesquisar_prefixo(self, prefixo):
        prefixo_normalizado = self._normalizar(prefixo)
        no = self._descer(prefixo_normalizado)

        resultados = []

        if no is not None:
            self._coletar(no, resultados)

        return resultados

    # ---------------- auxiliares internos ----------------

    def _normalizar(self, texto):
        if not isinstance(texto, str):
            raise TypeError("A Trie só aceita textos (str).")

        return texto.strip().lower()

    # percorre a Trie seguindo o texto; retorna o nó final ou None.
    # Reinicia e atualiza o contador de nós visitados.
    def _descer(self, texto):
        self.nos_visitados = 0
        no = self.raiz

        for caractere in texto:
            no = self._buscar_filho(no, caractere)

            if no is None:
                return None

            self.nos_visitados += 1

        return no

    # busca linear na lista de filhos (que é ordenada, então pode parar cedo)
    def _buscar_filho(self, no, caractere):
        for filho in no.filhos:
            if filho.caractere == caractere:
                return filho

            if filho.caractere > caractere:
                return None

        return None

    # insere o novo filho na posição que mantém a lista em ordem alfabética
    def _adicionar_filho_ordenado(self, no, novo):
        posicao = 0

        while posicao < len(no.filhos) and no.filhos[posicao].caractere < novo.caractere:
            posicao += 1

        no.filhos.insert(posicao, novo)

    # DFS em pré-ordem: como os filhos estão ordenados, os nomes saem em ordem
    # alfabética (uma palavra vem antes das que a estendem: "Tat" < "Tatooine")
    # (o nó de partida já foi contado em _descer; aqui contamos só os descendentes)
    def _coletar(self, no, resultados):
        if no.fim_de_palavra:
            resultados.append(no.palavra)

        for filho in no.filhos:
            self.nos_visitados += 1
            self._coletar(filho, resultados)
