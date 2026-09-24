class Planeta:

    def __init__(
        self,
        id,
        nome,
        clima,
        terreno,
        populacao,
        diametro,
        gravidade,
        agua_superficial,
        periodo_rotacao,
        periodo_orbital
    ):
        self.id = id
        self.nome = nome
        self.clima = clima
        self.terreno = terreno
        self.populacao = populacao
        self.diametro = diametro
        self.gravidade = gravidade
        self.agua_superficial = agua_superficial
        self.periodo_rotacao = periodo_rotacao
        self.periodo_orbital = periodo_orbital

    @classmethod
    # de_dicionario → futuramente vai receber um dicionário da SWAPI e criar um Planeta a partir dele.
    def de_dicionario(cls, dados):
        nome = dados["name"]
        clima = dados["climate"]
        terreno = dados["terrain"]

        id = int(dados["url"].rstrip("/").split("/")[-1])
        # pega o elemento que representa o numero do planeta que está na url da api

        populacao = dados["population"]

        if populacao == "unknown":
            populacao = None
        else:
            populacao = int(populacao)

        diametro = dados["diameter"]

        if diametro == "unknown":
            diametro = None
        else:
            diametro = int(diametro)

        gravidade = dados["gravity"]

        if gravidade == "unknown" or gravidade == "N/A":
            gravidade = None

        agua_superficial = dados["surface_water"]

        if agua_superficial == "unknown":
            agua_superficial = None
        else:
            agua_superficial = float(agua_superficial)

        periodo_rotacao = dados["rotation_period"]

        if periodo_rotacao == "unknown":
            periodo_rotacao = None
        else:
            periodo_rotacao = int(periodo_rotacao)

        periodo_orbital = dados["orbital_period"]

        if periodo_orbital == "unknown":
            periodo_orbital = None
        else:
            periodo_orbital = int(periodo_orbital)

        return cls(
            id,
            nome,
            clima,
            terreno,
            populacao,
            diametro,
            gravidade,
            agua_superficial,
            periodo_rotacao,
            periodo_orbital
        )

    def para_dicionario(self):  # representação de um Planeta em formato JSON
        return {
            "id": self.id,
            "nome": self.nome,
            "clima": self.clima,
            "terreno": self.terreno,
            "populacao": self.populacao,
            "diametro": self.diametro,
            "gravidade": self.gravidade,
            "agua_superficial": self.agua_superficial,
            "periodo_rotacao": self.periodo_rotacao,
            "periodo_orbital": self.periodo_orbital
        }