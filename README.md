# Crônicas do Espaço: Planejamento Algorítmico de Missões

Sistema de Gerenciamento e Planejamento de Missões Espaciais, Parte 1, ambientado no universo **Star Wars**.

O sistema consulta a SWAPI em tempo de execução, normaliza e salva os planetas localmente e os carrega em uma **Tabela Hash** implementada no projeto. Sobre esses dados ele oferece consulta, pesquisa, filtragem e o planejamento de uma missão por **estratégia gulosa**.

**Integrante:** Felipe Mareque (trabalho individual)

---

## Como executar

```bash
pip install -r requirements.txt
python main.py
```

Os dados são buscados na API sempre que o programa roda. Se a API estiver indisponível (sem internet, rede bloqueada ou servidor fora do ar), o programa avisa e usa os dados salvos na última execução, em `dados/planetas.json`.

Ao iniciar, o programa carrega os dados, mostra as métricas da Tabela Hash e abre um menu com as opções: consultar planeta, pesquisar por atributo, filtrar por população mínima, planetas com clima similar e planejar missão.

### Organização do projeto

```
sistemaEspacial/
├── main.py                      # fluxo principal da aplicação
├── api/swapi.py                 # módulo de aquisição (requisições HTTP)
├── modelos/planeta.py           # modelo Planeta + normalização dos dados
├── servicos/
│   ├── armazenamento.py         # persistência local em JSON
│   ├── consultas.py             # consulta por nome (usa a Tabela Hash)
│   ├── pesquisas.py             # pesquisa por atributo
│   ├── filtros.py               # listagem/filtragem
│   ├── similaridade.py          # operação adicional: planetas com clima similar
│   └── avaliacao.py             # cálculo de benefício e custo (guloso)
├── estruturas/
│   ├── tabela_hash.py           # estrutura implementada (Parte 1)
│   ├── trie.py                  # interface (Parte 2)
│   └── arvore_b.py              # interface (Parte 2)
├── guloso/planejamento_missao.py
└── dados/planetas.json          # dados normalizados salvos localmente
```

---

## 1. Fonte de dados

### API escolhida

| Item | Valor |
|---|---|
| Nome | SWAPI – The Star Wars API |
| Endereço | `https://swapi.dev/api` |
| Recurso utilizado | `planets` |
| Formato | JSON via HTTP GET, sem autenticação |
| Data da consulta | 08/10/2026 (o sistema repete a consulta a cada execução) |

### Justificativa da escolha

- A API é pública, gratuita, não exige chave e devolve JSON bem estruturado.
- O recurso `planets` tem 60 registros, o suficiente para gerar colisões e redimensionamentos na tabela hash e para que o problema guloso tenha escolhas de verdade.
- Cada planeta tem atributos numéricos (diâmetro, população, período orbital, água superficial) e textuais (clima, terreno). Os numéricos servem para calcular custo e benefício da missão. Os textuais servem para pesquisas e filtros.
- Como alguns valores aparecem como `"unknown"`, o tratamento e a normalização dos dados tiveram que ser feitos de verdade.

### Endpoints utilizados

| Endpoint | Uso |
|---|---|
| `GET /api/planets/` | Primeira página da listagem de planetas |
| `GET /api/planets/?page=N` | Páginas seguintes, seguindo o campo `next` |

### Nível de integração: Nível 1 (consumo dinâmico)

O módulo [api/swapi.py](api/swapi.py) faz as requisições HTTP **em tempo de execução** com a biblioteca `requests`. Ele percorre a paginação até `next` ser `null` e converte cada resposta com `resposta.json()`. Se o status for diferente de 200, uma exceção é lançada. Depois os dados são normalizados ([modelos/planeta.py](modelos/planeta.py)), salvos em [dados/planetas.json](dados/planetas.json) ([servicos/armazenamento.py](servicos/armazenamento.py)) e carregados na Tabela Hash.

As requisições têm um limite de tempo de 10 segundos. Se a API falhar, o sistema lê os dados do arquivo local salvo na última consulta bem-sucedida (`carregar_planetas()`). A API continua sendo a fonte principal, e o arquivo local é só uma alternativa de segurança.

### Exemplos de requisição

```
GET https://swapi.dev/api/planets/
```

```json
{
  "count": 60,
  "next": "https://swapi.dev/api/planets/?page=2",
  "previous": null,
  "results": [ { ... }, { ... } ]
}
```

```
GET https://swapi.dev/api/planets/1/
```

```json
{
  "name": "Tatooine",
  "rotation_period": "23",
  "orbital_period": "304",
  "diameter": "10465",
  "climate": "arid",
  "gravity": "1 standard",
  "terrain": "desert",
  "surface_water": "1",
  "population": "200000",
  "residents": ["https://swapi.dev/api/people/1/", "..."],
  "films": ["https://swapi.dev/api/films/1/", "..."],
  "created": "2014-12-09T13:50:49.641000Z",
  "edited": "2014-12-20T20:58:18.411000Z",
  "url": "https://swapi.dev/api/planets/1/"
}
```

### Estrutura dos dados obtidos

Todos os campos chegam da API como **texto**, inclusive os numéricos. Valores ausentes aparecem como `"unknown"` (e, na gravidade, também como `"N/A"`). Os campos `residents`, `films`, `created` e `edited` não são usados nesta parte e são descartados na normalização.

---

## 2. Modelagem

### Representação dos elementos

Cada planeta é representado pela classe `Planeta` ([modelos/planeta.py](modelos/planeta.py)):

- `Planeta.de_dicionario(dados)` converte o JSON bruto da API em um objeto e trata os tipos.
- `planeta.para_dicionario()` gera a representação normalizada (em português) que é salva em JSON e inserida na tabela.

### Atributos utilizados

| Atributo interno | Campo da API | Tipo | Tratamento |
|---|---|---|---|
| `id` | `url` | `int` | Extraído do final da URL (`.../planets/1/` → `1`) |
| `nome` | `name` | `str` | **Chave** da Tabela Hash |
| `clima` | `climate` | `str` | Mantido como texto |
| `terreno` | `terrain` | `str` | Mantido como texto |
| `populacao` | `population` | `int` ou `None` | `"unknown"` → `None` |
| `diametro` | `diameter` | `int` ou `None` | `"unknown"` → `None` |
| `gravidade` | `gravity` | `str` ou `None` | `"unknown"` / `"N/A"` → `None` |
| `agua_superficial` | `surface_water` | `float` ou `None` | `"unknown"` → `None` |
| `periodo_rotacao` | `rotation_period` | `int` ou `None` | `"unknown"` → `None` |
| `periodo_orbital` | `orbital_period` | `int` ou `None` | `"unknown"` → `None` |

### Operações implementadas

| Operação | Onde | Descrição |
|---|---|---|
| Aquisição | `api/swapi.py` → `buscar_planetas()` | Busca todas as páginas de planetas na SWAPI |
| Normalização | `modelos/planeta.py` | Converte tipos e trata valores desconhecidos |
| Armazenamento local | `servicos/armazenamento.py` → `salvar_planetas()` | Grava os planetas normalizados em `dados/planetas.json` |
| Consulta (6.1) | `servicos/consultas.py` → `consultar_planeta()` | Localiza um planeta pelo nome **usando a Tabela Hash** |
| Pesquisa (6.2) | `servicos/pesquisas.py` → `pesquisar_por_atributo()` | Retorna os planetas cujo atributo é igual ao valor informado (ex.: `clima == "arid"`) |
| Listagem/filtragem (6.3) | `servicos/filtros.py` → `filtrar_por_populacao_minima()` | Lista os planetas com população conhecida e maior ou igual a um mínimo |
| Operação adicional (6.4) | `servicos/similaridade.py` → `planetas_com_clima_similar()` | Lista os planetas que compartilham ao menos um clima com o planeta informado (ver justificativa abaixo) |
| Planejamento de missão (7) | `guloso/planejamento_missao.py` | Seleciona destinos por estratégia gulosa respeitando um orçamento |

### Operação adicional: planetas com clima similar

Depois de explorar um planeta, a agência quer saber quais outros destinos têm condições climáticas parecidas. Assim pode reaproveitar equipamentos e o treinamento da equipe em missões futuras.

A função busca o planeta de referência **na Tabela Hash** (O(1) esperado) e percorre a lista de planetas (O(n)). Ela devolve os que têm pelo menos um clima em comum. O campo `clima` é separado por vírgula, então planetas de clima misto também entram. Por exemplo, a partir de Tatooine (`arid`) o sistema encontra Geonosis (`temperate, arid`), que a pesquisa por igualdade exata não encontraria.

### Decisões de projeto

- **Normalizar antes de armazenar.** A conversão de tipos fica concentrada em um único ponto (`Planeta.de_dicionario`), e o resto do sistema já recebe números como números e ausências como `None`.
- **`None` em vez de `"unknown"`.** Assim filtros e cálculos não precisam comparar strings especiais e não correm o risco de converter `"unknown"` para número.
- **Chave = nome do planeta.** O nome é o identificador natural para o usuário e é único no conjunto da SWAPI.
- **Divisão em camadas** (`api`, `modelos`, `estruturas`, `servicos`, `guloso`). Cada módulo tem uma responsabilidade, e os serviços usam as estruturas só pelos métodos públicos (`inserir`, `buscar`), sem acessar detalhes internos.

---

## 3. Estrutura de dados: Tabela Hash

### Estrutura escolhida e justificativa

A operação central do sistema é **localizar um planeta pelo nome**. Ela aparece na consulta direta e também serve de base para as operações seguintes. Uma tabela hash faz busca e inserção em tempo **O(1) esperado**, o melhor possível para acesso por chave exata.

A Trie seria mais útil para busca por prefixo e a Árvore B para consultas por intervalo e percurso ordenado. Nenhuma das duas é o caso principal desta primeira parte, por isso as duas ficaram como interfaces para a Parte 2.

A implementação **não usa `dict`** nem outra estrutura nativa de alto nível. O armazenamento é uma lista Python de tamanho fixo (`[None] * capacidade`), usada como vetor.

### Detalhes da implementação ([estruturas/tabela_hash.py](estruturas/tabela_hash.py))

| Aspecto | Escolha |
|---|---|
| Função hash | Método de **Horner** com base 31: `h = h·31 + ord(c)` para cada caractere, e no fim `h mod capacidade` |
| Tratamento de colisões | **Endereçamento aberto com sondagem linear**: se a posição está ocupada, tenta `(i + 1) mod capacidade` |
| Capacidade inicial | 11 (primo) |
| Limite do fator de carga | 0,7. Ao atingir `n/m ≥ 0,7`, ocorre o rehash |
| Rehash | Nova capacidade = **primeiro primo ≥ 2m + 1**; todos os elementos são reinseridos |

Capacidade prima e base 31 espalham melhor as chaves. O limite de 0,7 evita os longos agrupamentos (*clusters*) da sondagem linear quando a tabela está quase cheia.

### Instrumentação

A própria estrutura mantém os contadores dentro do seu código:

- `colisoes`: incrementado **a cada posição ocupada encontrada** durante a sondagem, nas inserções do carregamento. As reinserções feitas pelo rehash não entram na conta, porque não são inserções de dados novos.
- `fator_carga()`: calculado na hora como `quantidade / capacidade`.

Saída real do carregamento dos 60 planetas:

```
Quantidade de planetas: 60
Capacidade da tabela: 97
Colisões: 85
Fator de carga: 0.6185567010309279
```

Durante o carregamento a tabela cresceu assim:

| Inserção que dispara o rehash | Fator de carga no momento | Capacidade antiga → nova | Elementos reinseridos |
|---|---|---|---|
| 8ª | 8/11 ≈ 0,727 | 11 → 23 | 8 |
| 17ª | 17/23 ≈ 0,739 | 23 → 47 | 17 |
| 33ª | 33/47 ≈ 0,702 | 47 → 97 | 33 |

As 85 colisões somam **todas** as sondagens extras feitas nas tabelas intermediárias (11, 23 e 47) e na final (97). Por isso o número passa da quantidade de planetas.

### Operações e complexidade

| Operação | Caso esperado | Pior caso |
|---|---|---|
| `inserir(planeta)` | O(1) amortizado | O(n) (rehash ou cluster longo) |
| `buscar(nome)` | O(1) | O(n) |
| `fator_carga()` | O(1) | O(1) |
| `_rehash()` | — | O(n) |

Com fator de carga α e hipótese de hash uniforme, a sondagem linear examina em média cerca de ½(1 + 1/(1−α)) posições numa busca bem-sucedida e ½(1 + 1/(1−α)²) numa malsucedida. Com α = 0,7, isso dá ≈ 2,2 e ≈ 6,1 posições. Com o α ≈ 0,62 final, dá ≈ 1,8 e ≈ 3,9.

### Integração com o sistema

Em [main.py](main.py), cada planeta normalizado é inserido com `tabela.inserir(planeta)`. A consulta `consultar_planeta(tabela, "Tatooine")` ([servicos/consultas.py](servicos/consultas.py)) delega para `tabela.buscar(nome)`. O serviço não conhece a função hash nem a forma de sondagem.

### Interfaces das estruturas da Parte 2

As outras duas estruturas têm só a interface definida. A implementação fica para a Parte 2.

**Trie** ([estruturas/trie.py](estruturas/trie.py)): busca de planetas por **prefixo do nome** (autocompletar).

| Método | Finalidade |
|---|---|
| `inserir(palavra)` | Insere o nome de um planeta |
| `buscar(palavra)` | Verifica se o nome existe |
| `pesquisar_prefixo(prefixo)` | Retorna os nomes que começam com o prefixo |

Métrica prevista: quantidade de nós visitados em cada busca ou pesquisa por prefixo.

**Árvore B** ([estruturas/arvore_b.py](estruturas/arvore_b.py)): indexação **ordenada** por atributos numéricos (população, diâmetro), para consultas por faixa.

| Método | Finalidade |
|---|---|
| `inserir(chave)` | Insere uma chave mantendo a ordem |
| `buscar(chave)` | Localiza uma chave |
| `remover(chave)` | Remove uma chave |

Métricas previstas: número total de *splits* e altura final da árvore após o carregamento.

---

## 4. Análise amortizada: rehash da Tabela Hash

### O problema

Uma inserção que dispara o rehash reinsere **todos** os n elementos e custa Θ(n). Analisando só o pior caso de cada operação, m inserções custariam O(m·n), ou seja, O(n²) para carregar n elementos. Esse limite é conservador demais: o rehash é raro, e o intervalo entre dois rehashes cresce junto com a tabela.

Abaixo, **custo real** = número de posicionamentos de elementos no vetor (1 por inserção comum, mais 1 por elemento reinserido no rehash).

### Método agregado (com os dados reais)

Ao carregar os 60 planetas aconteceram 3 rehashes, com 8 + 17 + 33 = **58 reinserções**. O custo total foi:

```
60 inserções + 58 reinserções = 118 posicionamentos  →  118 / 60 ≈ 1,97 por inserção
```

Em geral, como a capacidade pelo menos dobra a cada rehash, as reinserções formam uma série geométrica limitada por n:

```
n·(1 + 1/2 + 1/4 + ...) ≤ 2n  →  custo total ≤ n + 2n = 3n  →  O(1) amortizado por inserção
```

### Método contábil

Cada inserção recebe **3 créditos**:

- 1 crédito paga a própria inserção;
- 2 créditos ficam guardados no elemento para pagar reinserções futuras.

Logo depois de um rehash para a capacidade m', a tabela tem cerca de 0,7·m'/2 = 0,35·m' elementos, e nenhum crédito sobrando. O próximo rehash só acontece com 0,7·m' elementos, ou seja, depois de **0,35·m' inserções novas**, que juntam 2 × 0,35·m' = **0,7·m' créditos**. Isso é exatamente o custo de reinserir os 0,7·m' elementos. O saldo de créditos nunca fica negativo, então o custo amortizado de cada inserção é **3 = O(1)**.

### Método do potencial

Seja n o número de elementos, m a capacidade e

```
Φ = max(0, 2n − 0,7·m)
```

- Logo após um rehash, n ≈ 0,35·m e **Φ ≈ 0**. Φ nunca é negativo.
- **Inserção comum:** custo real 1, ΔΦ ≤ 2, então custo amortizado ≤ **3**.
- **Inserção com rehash** (n chega a 0,7·m, e a capacidade passa a m' ≈ 2m): antes, Φ = 1,4m − 0,7m = 0,7m. Depois, Φ ≈ 2·(0,7m) − 0,7·(2m) = 0. Custo real = 1 + 0,7m e ΔΦ = −0,7m, então custo amortizado = 1 + 0,7m − 0,7m = **1**.

Nos dois casos o custo amortizado é constante. A soma dos custos amortizados limita a soma dos custos reais, então **n inserções custam O(n) no total**.

### Conclusão

O pior caso O(n) de uma inserção isolada é real, mas acontece só em ⌈log₂ n⌉ inserções de toda a sequência. O potencial acumulado pelas inserções baratas paga cada rehash. Numa sequência longa de requisições, o custo médio por inserção fica limitado por uma constante. No carregamento real foi ≈ 1,97 posicionamento por inserção.

---

## 5. Algoritmo guloso: Opção A (Planejamento e Triagem de Missões)

### Definição do problema

A agência tem um **orçamento limitado de recursos** (informado pelo usuário na opção 5 do menu). Cada planeta tem um **custo** de exploração e um **benefício** para a missão. O objetivo é escolher um conjunto de planetas cuja soma de custos não passe do orçamento e cuja soma de benefícios seja a maior possível. É uma variação do **problema da mochila 0/1**.

### Benefício: valor científico da informação disponível ([servicos/avaliacao.py](servicos/avaliacao.py))

| Critério | Pontos |
|---|---|
| População conhecida | +2 |
| Água superficial conhecida | +3 |
| Diâmetro conhecido | +1 |
| Gravidade conhecida | +1 |
| Período orbital conhecido | +1 |
| **Máximo** | **8** |

A água superficial vale mais porque indica potencial para sustentar vida e recursos. A população indica presença de civilização e infraestrutura.

### Custo: tamanho + distância orbital + risco por falta de informação

Custo-base 1, mais:

| Situação | Custo |
|---|---|
| Diâmetro > 10.000 | +1 |
| Diâmetro > 20.000 | +1 adicional |
| Diâmetro desconhecido | +1 |
| Período orbital > 300 | +1 |
| Período orbital > 500 | +1 adicional |
| Período orbital desconhecido | +1 |
| Água superficial desconhecida | +1 |
| Gravidade desconhecida | +1 |

Planetas maiores exigem mais recursos para serem explorados. Períodos orbitais longos indicam órbitas mais afastadas. Dados desconhecidos aumentam o risco operacional.

### Estratégia adotada

1. `preparar_candidatos`: calcula benefício, custo e a **razão benefício/custo** de cada planeta.
2. `ordenar_candidatos`: ordena os candidatos pela razão, da maior para a menor.
3. `planejar_missao`: percorre a lista ordenada e **escolhe cada candidato que ainda cabe no orçamento restante**, sem voltar atrás em nenhuma decisão.

Complexidade: O(n log n) para ordenar e O(n) para selecionar.

### Justificativa do critério

Escolher só pelo maior benefício favorece planetas caros que consomem o orçamento com poucos destinos. Escolher só pelo menor custo favorece planetas baratos de pouco valor. A razão benefício/custo mede **quanto retorno cada unidade de recurso gera**, que é o critério guloso clássico para mochila e o mais eficiente em média.

### Solução encontrada (orçamento = 15)

| Planeta | Benefício | Custo | Razão |
|---|---|---|---|
| Endor | 8 | 2 | 4,00 |
| Geonosis | 8 | 2 | 4,00 |
| Mustafar | 8 | 2 | 4,00 |
| Rodia | 8 | 2 | 4,00 |
| Sullust | 8 | 2 | 4,00 |
| Glee Anselm | 8 | 2 | 4,00 |
| Tatooine | 8 | 3 | 2,67 |

**Recurso utilizado:** 15 · **Recurso restante:** 0 · **Benefício total:** 56

Para comparar, calculamos a solução ótima por programação dinâmica. Com orçamento 15 o ótimo também é **56**, ou seja, aqui o guloso acertou.

### Limitações da estratégia

Para a mochila 0/1 o guloso **não garante a solução ótima**: ele não pode pegar frações de um planeta nem desfazer uma escolha. Isso acontece com os próprios dados da SWAPI. Com **orçamento = 16**:

| | Seleção | Custo | Benefício |
|---|---|---|---|
| **Guloso** | 6 planetas (8, 2) + Tatooine (8, 3) | 15 (sobra 1) | **56** |
| **Ótimo** | 6 planetas (8, 2) + Felucia (5, 2) + Toydaria (5, 2) | 16 | **58** |

Depois dos seis planetas de razão 4, o guloso escolhe Tatooine (razão 2,67), que tem razão maior que Felucia e Toydaria (2,5). Isso deixa 1 unidade de orçamento que nenhum candidato consegue usar. Duas escolhas de razão um pouco menor teriam aproveitado o orçamento inteiro. Testando orçamentos de 1 a 39, o mesmo problema aparece em 16, 19, 22, 25, 28, 31, 34 e 37, sempre com diferença de 2 pontos.

Outras limitações:

- **Empates:** muitos planetas têm a mesma razão (6 com razão 4,0 e 13 com 8/3). Entre empatados vale a ordem original, e o critério não diferencia esses planetas.
- **Critério discreto:** o benefício mede quanta informação existe sobre o planeta, não o seu valor real. Dois planetas com todos os dados conhecidos recebem o mesmo benefício.
- **Uma única restrição:** o modelo considera só o orçamento. Restrições extras (combustível, tempo, tripulação) fariam do problema uma mochila multidimensional, em que a razão simples funciona ainda pior.

A solução exata (programação dinâmica, O(n·W)) resolveria esses casos, mas o guloso é mais simples, roda em O(n log n) e, nestes dados, fica sempre a no máximo 2 pontos do ótimo.
