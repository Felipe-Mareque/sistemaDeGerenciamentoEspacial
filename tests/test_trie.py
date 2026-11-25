import json
import os
import random
import unittest

from estruturas.trie import Trie

CAMINHO_DADOS = os.path.join(os.path.dirname(__file__), "..", "dados", "planetas.json")


def carregar_nomes():
    with open(CAMINHO_DADOS, encoding="utf-8") as arquivo:
        return [planeta["nome"] for planeta in json.load(arquivo)]


# resultado esperado calculado por força bruta (busca linear), para comparação
def prefixo_forca_bruta(nomes, prefixo):
    alvo = prefixo.strip().lower()
    return sorted(
        (nome for nome in nomes if nome.lower().startswith(alvo)),
        key=str.lower
    )


class TestTrieCasosUsuais(unittest.TestCase):

    def setUp(self):
        self.trie = Trie()

        for nome in ["Tatooine", "Alderaan", "Naboo", "Yavin IV", "Hoth", "Haruun Kal"]:
            self.trie.inserir(nome)

    def test_busca_exata(self):
        self.assertTrue(self.trie.buscar("Tatooine"))
        self.assertTrue(self.trie.buscar("Yavin IV"))
        self.assertFalse(self.trie.buscar("Coruscant"))

    def test_prefixo_nao_e_palavra(self):
        # "Tat" é caminho na Trie, mas não foi inserido como palavra
        self.assertFalse(self.trie.buscar("Tat"))

    def test_ignora_maiusculas_e_espacos_nas_pontas(self):
        self.assertTrue(self.trie.buscar("tatooine"))
        self.assertTrue(self.trie.buscar("  HOTH "))
        self.assertEqual(self.trie.pesquisar_prefixo("tAt"), ["Tatooine"])

    def test_pesquisa_por_prefixo(self):
        self.assertEqual(self.trie.pesquisar_prefixo("H"), ["Haruun Kal", "Hoth"])
        self.assertEqual(self.trie.pesquisar_prefixo("yavin "), ["Yavin IV"])

    def test_resultado_preserva_nome_original(self):
        self.assertEqual(self.trie.pesquisar_prefixo("naboo"), ["Naboo"])

    def test_quantidade(self):
        self.assertEqual(self.trie.quantidade, 6)


class TestTrieCasosLimite(unittest.TestCase):

    def test_trie_vazia(self):
        trie = Trie()
        self.assertFalse(trie.buscar("Tatooine"))
        self.assertEqual(trie.pesquisar_prefixo("T"), [])
        self.assertEqual(trie.pesquisar_prefixo(""), [])
        self.assertEqual(trie.quantidade, 0)

    def test_prefixo_inexistente(self):
        trie = Trie()
        trie.inserir("Tatooine")
        self.assertEqual(trie.pesquisar_prefixo("Tz"), [])
        self.assertEqual(trie.pesquisar_prefixo("Tatooine Prime"), [])

    def test_prefixo_vazio_retorna_tudo_em_ordem(self):
        trie = Trie()

        for nome in ["Naboo", "Alderaan", "Hoth"]:
            trie.inserir(nome)

        self.assertEqual(trie.pesquisar_prefixo(""), ["Alderaan", "Hoth", "Naboo"])

    def test_ordem_independe_da_insercao(self):
        nomes = ["Hoth", "Endor", "Bespin", "Dagobah", "Alderaan"]
        trie_a, trie_b = Trie(), Trie()

        for nome in nomes:
            trie_a.inserir(nome)

        for nome in reversed(nomes):
            trie_b.inserir(nome)

        self.assertEqual(trie_a.pesquisar_prefixo(""), trie_b.pesquisar_prefixo(""))

    def test_palavra_prefixo_de_outra(self):
        trie = Trie()
        trie.inserir("Tatooine")
        trie.inserir("Tat")

        self.assertTrue(trie.buscar("Tat"))
        self.assertTrue(trie.buscar("Tatooine"))
        self.assertEqual(trie.pesquisar_prefixo("ta"), ["Tat", "Tatooine"])

    def test_duplicata_nao_e_inserida(self):
        trie = Trie()
        self.assertTrue(trie.inserir("Hoth"))
        nos_antes = trie.total_nos

        self.assertFalse(trie.inserir("Hoth"))
        self.assertFalse(trie.inserir("hoth"))  # mesma palavra sem diferenciar maiúsculas
        self.assertEqual(trie.quantidade, 1)
        self.assertEqual(trie.total_nos, nos_antes)
        self.assertEqual(trie.pesquisar_prefixo("h"), ["Hoth"])

    def test_entradas_invalidas(self):
        trie = Trie()

        with self.assertRaises(ValueError):
            trie.inserir("")

        with self.assertRaises(ValueError):
            trie.inserir("   ")

        with self.assertRaises(TypeError):
            trie.inserir(None)

        with self.assertRaises(TypeError):
            trie.buscar(42)

        with self.assertRaises(TypeError):
            trie.pesquisar_prefixo(None)

        self.assertFalse(trie.buscar(""))


class TestTrieMetricas(unittest.TestCase):

    def test_prefixos_compartilham_nos(self):
        trie = Trie()
        trie.inserir("ab")
        trie.inserir("ac")
        # raiz + 'a' + 'b' + 'c' (o 'a' é compartilhado)
        self.assertEqual(trie.total_nos, 4)

    def test_nos_visitados_na_busca(self):
        trie = Trie()
        trie.inserir("Tatooine")

        trie.buscar("Tatooine")
        self.assertEqual(trie.nos_visitados, 8)

        trie.buscar("Taz")  # para no 3º caractere: só 2 nós percorridos
        self.assertEqual(trie.nos_visitados, 2)

    def test_nos_visitados_no_prefixo(self):
        trie = Trie()
        trie.inserir("ab")
        trie.inserir("ac")

        trie.pesquisar_prefixo("a")
        # 1 nó na descida ('a') + 2 descendentes ('b', 'c')
        self.assertEqual(trie.nos_visitados, 3)


class TestTrieConsistencia(unittest.TestCase):

    def test_dados_reais_contra_forca_bruta(self):
        nomes = carregar_nomes()
        trie = Trie()

        for nome in nomes:
            trie.inserir(nome)

        self.assertEqual(trie.quantidade, len(nomes))

        for nome in nomes:
            self.assertTrue(trie.buscar(nome))

            for tamanho in range(0, len(nome) + 1):
                prefixo = nome[:tamanho]
                self.assertEqual(
                    trie.pesquisar_prefixo(prefixo),
                    prefixo_forca_bruta(nomes, prefixo),
                    f"prefixo {prefixo!r}"
                )

    def test_instancias_de_tamanhos_diferentes(self):
        gerador = random.Random(2026)

        for tamanho in [1, 10, 100, 2000]:
            palavras = set()

            while len(palavras) < tamanho:
                comprimento = gerador.randint(1, 8)
                palavras.add("".join(gerador.choice("abcde ") for _ in range(comprimento)).strip() or "a")

            palavras = list(palavras)
            trie = Trie()

            for palavra in palavras:
                trie.inserir(palavra)

            unicas = {p.strip().lower() for p in palavras}
            self.assertEqual(trie.quantidade, len(unicas))

            for prefixo in ["", "a", "ab", "c d", "eee", "zz"]:
                esperado = sorted({p.strip() for p in palavras if p.strip().lower().startswith(prefixo)}, key=str.lower)
                self.assertEqual(trie.pesquisar_prefixo(prefixo), esperado, f"n={tamanho} prefixo {prefixo!r}")


if __name__ == "__main__":
    unittest.main()
