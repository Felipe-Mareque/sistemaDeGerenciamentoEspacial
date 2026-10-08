# Interface da Árvore B (implementação na Parte 2)
# Uso previsto: índice ordenado por atributos numéricos (população, diâmetro)
class ArvoreB:

    # cria a raiz vazia e os contadores de splits e altura (métricas instrumentadas)
    def __init__(self):
        pass

    # recebe uma chave e a insere mantendo a ordem, fazendo split quando o nó encher
    def inserir(self, chave):
        pass

    # recebe uma chave e retorna o elemento encontrado, ou None se não existir
    def buscar(self, chave):
        pass

    # recebe uma chave e a remove da árvore, mantendo as propriedades da Árvore B
    def remover(self, chave):
        pass
