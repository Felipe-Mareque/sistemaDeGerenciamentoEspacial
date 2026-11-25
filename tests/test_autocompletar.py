import json
import os
import unittest

from estruturas.tabela_hash import TabelaHash
from estruturas.trie import Trie
from servicos.autocompletar import (
    construir_trie,
    sugerir_nomes,
    resolver_nome,
    consultar_com_sugestoes
)

CAMINHO_DADOS = os.path.join(os.path.dirname(__file__), "..", "dados", "planetas.json")


class TestIntegracaoTrieHash(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(CAMINHO_DADOS, encoding="utf-8") as arquivo:
            cls.planetas = json.load(arquivo)

        cls.tabela = TabelaHash()

        for planeta in cls.planetas:
            cls.tabela.inserir(planeta)

        cls.trie = construir_trie(Trie(), cls.planetas)

    def test_mesmos_planetas_nas_duas_estruturas(self):
        self.assertEqual(self.trie.quantidade, self.tabela.quantidade)

        for nome in self.trie.pesquisar_prefixo(""):
            self.assertIsNotNone(self.tabela.buscar(nome))

    def test_consulta_nome_exato(self):
        planeta, sugestoes = consultar_com_sugestoes(self.tabela, self.trie, "Tatooine")
        self.assertEqual(planeta["nome"], "Tatooine")
        self.assertEqual(sugestoes, [])

    def test_consulta_sem_diferenciar_maiusculas(self):
        # a hash sozinha não acharia "tatooine"; a Trie corrige o nome
        self.assertIsNone(self.tabela.buscar("tatooine"))

        planeta, _ = consultar_com_sugestoes(self.tabela, self.trie, "  tatooine ")
        self.assertEqual(planeta["nome"], "Tatooine")

    def test_consulta_incompleta_sugere_nomes(self):
        planeta, sugestoes = consultar_com_sugestoes(self.tabela, self.trie, "Ta")
        self.assertIsNone(planeta)
        self.assertEqual(sugestoes, ["Tatooine"])

    def test_consulta_inexistente(self):
        planeta, sugestoes = consultar_com_sugestoes(self.tabela, self.trie, "Krypton")
        self.assertIsNone(planeta)
        self.assertEqual(sugestoes, [])

    def test_consulta_vazia(self):
        planeta, sugestoes = consultar_com_sugestoes(self.tabela, self.trie, "   ")
        self.assertIsNone(planeta)
        self.assertEqual(sugestoes, [])

    def test_resolver_nome(self):
        self.assertEqual(resolver_nome(self.trie, "yavin iv"), "Yavin IV")
        self.assertIsNone(resolver_nome(self.trie, "Yavin"))

    def test_sugerir_nomes(self):
        self.assertEqual(sugerir_nomes(self.trie, "ca"), ["Cato Neimoidia"])
        self.assertEqual(sugerir_nomes(self.trie, "Co"), ["Concord Dawn", "Corellia", "Coruscant"])


if __name__ == "__main__":
    unittest.main()
