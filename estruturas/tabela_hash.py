class TabelaHash:

    def __init__(self, capacidade=10):
        self.capacidade = capacidade
        self.tabela = [None] * capacidade
        self.quantidade = 0
        self.colisoes = 0

    def _funcao_hash(self, chave):
        valor = 0

        for caractere in chave:
            valor = valor * 31 + ord(caractere)

        return valor % self.capacidade