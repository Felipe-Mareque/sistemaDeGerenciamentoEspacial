class TabelaHash:

    def __init__(self, capacidade=11):
        self.capacidade = capacidade
        self.tabela = [None] * capacidade
        self.quantidade = 0
        self.colisoes = 0

    def _funcao_hash(self, chave):
        valor = 0

        for caractere in chave:
            valor = valor * 31 + ord(caractere)

        return valor % self.capacidade

    def inserir(self, planeta):
        chave = planeta["nome"]
        indice = self._funcao_hash(chave)

        while self.tabela[indice] is not None:
            self.colisoes += 1
            indice = (indice + 1) % self.capacidade

        self.tabela[indice] = planeta
        self.quantidade += 1


    def fator_carga(self):
        return self.quantidade / self.capacidade
