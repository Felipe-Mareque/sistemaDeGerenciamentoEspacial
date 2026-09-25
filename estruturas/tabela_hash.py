class TabelaHash:

    def __init__(self, capacidade=11):
        self.capacidade = capacidade
        self.tabela = [None] * capacidade
        self.quantidade = 0
        self.colisoes = 0
        self.limite_fator_carga = 0.7

    def _funcao_hash(self, chave):
        valor = 0

        for caractere in chave:
            valor = valor * 31 + ord(caractere)

        return valor % self.capacidade

    def inserir(self, planeta):
        self._inserir(planeta)

        if self.fator_carga() >= self.limite_fator_carga:
            self._rehash()

    def _inserir(self, planeta, contar_colisao=True):
        chave = planeta["nome"]
        indice = self._funcao_hash(chave)

        while self.tabela[indice] is not None:
            if contar_colisao:
                self.colisoes += 1

            indice = (indice + 1) % self.capacidade

        self.tabela[indice] = planeta
        self.quantidade += 1

    def fator_carga(self):
        return self.quantidade / self.capacidade

    def _proxima_capacidade(self):
        candidato = self.capacidade * 2 + 1

        while True:
            eh_primo = True

            for divisor in range(2, int(candidato ** 0.5) + 1):
                if candidato % divisor == 0:
                    eh_primo = False
                    break

            if eh_primo:
                return candidato

            candidato += 2

    def _rehash(self):
        tabela_antiga = self.tabela

        self.capacidade = self._proxima_capacidade()
        self.tabela = [None] * self.capacidade
        self.quantidade = 0

        for planeta in tabela_antiga:
            if planeta is not None:
                self._inserir(planeta, False)