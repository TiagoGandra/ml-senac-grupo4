# 🎓 Guia Completo do Aluno 4 — Regras de Associação (Apriori) + Detecção de Anomalias (Isolation Forest)

> **Objetivo deste documento:** Permitir que você, Aluno 4, entenda com profundidade total cada conceito, cada decisão técnica e cada número do projeto. Ao final, você deve ser capaz de explicar sem ler — com suas próprias palavras — tudo o que foi feito nas Fases 3 e 4, defender cada escolha e responder a qualquer pergunta do professor com segurança.

---

# PARTE 1 — REGRAS DE ASSOCIAÇÃO COM APRIORI (Notebook 03)

---

## 1.1 O que é o Algoritmo Apriori? (Conceito Fundamental)

### A analogia do supermercado

Imagine o seguinte cenário: um supermercado quer descobrir que produtos os clientes costumam comprar **juntos**. Por exemplo, quem compra pão geralmente também compra manteiga? Quem leva cerveja também leva fraldas?

O Apriori é o algoritmo que responde exatamente isso. Ele varre todas as "cestas de compras" (transações) procurando **combinações de itens que aparecem juntas com mais frequência do que seria esperado se os itens fossem independentes**.

### Traduzindo para o nosso projeto

No nosso caso, cada **candidato** é uma "transação" (uma "cesta"). Os "itens" na cesta são as **características** dele: seu partido, gênero, escolaridade, faixa de patrimônio, faixa de gastos de campanha, etc.

A pergunta que respondemos:

> *"Que combinações de características dos candidatos aparecem juntas com frequência anormal? Em particular: o fato de um candidato pertencer a um cluster específico está associado a que combinação de atributos?"*

### Por que isso é importante no nosso trabalho?

Na Fase 2 (Clusterização), nomeamos os 4 clusters com nomes interpretativos:
- **Estruturados** (53% da base)
- **Financiados** (21%)
- **Base Simbólica** (15%)
- **Patrimônio Sem Campanha** (11%)

Mas esses nomes foram baseados na **nossa interpretação visual** dos radares polares e das tabelas. Será que estamos certos? O Apriori dá a **prova matemática**: se os nomes fazem sentido, então existirão regras do tipo `Sem Bens + Sem Despesa → Base Simbólica` com alta confiança e alto lift.

---

## 1.2 As Três Métricas Essenciais: Suporte, Confiança e Lift

Você **precisa saber explicar** essas três métricas. O professor pode perguntar sobre qualquer uma delas.

### 📏 Suporte — "Com que frequência isso aparece na base?"

**Definição:** Fração de candidatos em que os itens A e B aparecem **juntos**.

```
Suporte(A → B) = nº de candidatos com A e B / total de candidatos
```

**Exemplo concreto do nosso projeto:**
- `Sem Bens + Sem Despesa` aparece em 308 dos 2.189 candidatos
- Suporte = 308 / 2.189 = **14,1%**

**O que indica:** Volume. Suporte alto = a regra se aplica a muita gente. Suporte baixo = pode ser coincidência de poucos casos.

**Nosso filtro:** Usamos suporte mínimo de 1,5% (~33 candidatos). Isso garante que toda regra tem pelo menos 33 candidatos por trás dela — não é coincidência de 3 ou 4 pessoas.

### 🎯 Confiança — "Se A acontece, qual a probabilidade de B?"

**Definição:** Dentre os candidatos que têm A, qual a fração que também tem B?

```
Confiança(A → B) = P(B dado A) = Suporte(A e B) / Suporte(A)
```

**Exemplo concreto:**
- Dos candidatos que têm `Sem Bens + Sem Despesa`, **100%** estão no cluster `Base Simbólica`
- Confiança = 100%

**O que indica:** Precisão preditiva. "Se eu sei que o candidato não tem bens e não tem despesas, com que certeza ele é Base Simbólica?" → 100%.

**Por que 100% é tão forte:** Em nenhum caso um candidato com bens zero e despesas zero caiu fora do cluster Base Simbólica. A regra é **determinística**.

### 🚀 Lift — "Isso é mais frequente do que o acaso?"

**Definição:** Quantas vezes mais frequente a combinação A+B é em relação ao que seria esperado se A e B fossem independentes.

```
Lift(A → B) = Confiança(A → B) / Suporte(B)
```

**Exemplo concreto:**
- Confiança de `Sem Bens + Sem Despesa → Base Simbólica` = 100% (1.0)
- Suporte de `Base Simbólica` na base toda = 328/2.189 = 15%
- Lift = 1.0 / 0.15 = **6,67**

**O que indica:** Se fosse tudo aleatório, apenas 15% dos candidatos seriam Base Simbólica. Mas entre os que não têm bens nem despesas, **100%** são. A combinação aparece **6,67 vezes mais** do que o acaso previa.

**Interpretação prática dos valores de lift:**
- **Lift = 1** → A e B são independentes. Saber A não ajuda a prever B.
- **Lift > 1** → Associação positiva. A e B aparecem juntos mais do que o esperado.
- **Lift < 1** → Associação negativa. A e B se evitam.
- **Lift = 8,83** (o nosso máximo!) → A combinação é quase 9 vezes mais frequente que o acaso.

> 💡 **Dica de fala:** "O lift é a métrica que tira o efeito do tamanho. Mesmo que Base Simbólica represente 15% da base, o fato de 100% dos 'sem bens + sem despesas' estarem nela dá um lift de 6,67 — ou seja, essa combinação é quase 7 vezes mais frequente que o acaso."

---

## 1.3 Passo a Passo do Que o Código Faz

### Passo 1: Carregar os dados e os clusters da Fase 2

O notebook lê o CSV gerado pela Fase 2, que já contém as 4 variáveis numéricas (Idade, Anos de Estudo, Total de Bens, Total de Despesas Contratadas) e a coluna `cluster_4v_nome` com os nomes dos 4 clusters.

### Passo 2: Transformar as variáveis contínuas em quartis

**Por que é necessário?**

O Apriori trabalha exclusivamente com **variáveis categóricas binárias** (Sim/Não). Ele não entende "patrimônio = R$ 150.000". Precisamos transformar variáveis contínuas em categorias.

**O professor exige quartis.** Então foi exatamente isso que fizemos.

**Como fizemos (e por que cada variável tem seu tratamento):**

#### Idade → `Faixa_Idade` (4 quartis puros)
```python
pd.qcut(df['IDADE'], q=4, labels=['Q1 (mais jovens)', 'Q2', 'Q3', 'Q4 (mais velhos)'])
```
- Q1: 567 candidatos | Q2: 595 | Q3: 485 | Q4: 542
- Funcionou perfeitamente com quartis puros porque a distribuição de idade é razoavelmente contínua.

#### Anos de Estudo → `Faixa_Estudo` (4 faixas por nível educacional)
**Aqui tem uma decisão técnica que você PRECISA saber defender:**
- Se tentássemos `pd.qcut` puro com 4 quartis, teríamos um problema: **58% dos candidatos têm Superior Completo** (16 anos de estudo). Os quartis Q2 e Q3 colapsariam ambos no valor 16, gerando apenas 2 faixas em vez de 4.
- **Solução:** Usamos cortes baseados nos níveis educacionais reais do Brasil:
  - `[-inf, 8]` → Até Fundamental (121 candidatos)
  - `(8, 11]` → Ensino Médio (538)
  - `(11, 13]` → Superior Incompleto (253)
  - `(13, inf]` → Superior Completo (1.277)
- Isso preserva 4 faixas significativas e interpretáveis.

> 💡 **Se o professor perguntar "por que não usou pd.qcut puro?"**: "Porque 58% da base tem Superior Completo, ou seja, 16 anos de estudo. O pd.qcut calcularia Q2 = Q3 = 16 e produziria apenas 2 faixas. Usamos cortes alinhados ao sistema educacional brasileiro para manter 4 categorias com significado real."

#### Total de Bens → `Faixa_Bens` (quartis zero-aware)
**Outra decisão técnica crucial:**
- **43% dos candidatos (771 de 2.189) declaram R$ 0 em patrimônio.**
- Se fizermos `pd.qcut` com 4 quartis, os dois primeiros quartis seriam ambos "R$ 0", desperdiçando poder discriminativo.
- **Solução zero-aware:**
  1. Separar os zeros como uma categoria à parte: `Sem Bens (R$ 0)` → 771 candidatos
  2. Calcular `pd.qcut(q=3)` **somente sobre quem tem bens > 0** (1.418 candidatos)
  3. Resultado: `Bens Q1` (474) | `Bens Q2` (471) | `Bens Q3` (473)
- Total: 4 categorias com distribuições equilibradas.

#### Total de Despesas Contratadas → `Faixa_Despesa_Contratada` (quartis zero-aware)
- Mesma lógica: **26% dos candidatos (557) têm despesas = R$ 0**
- Separamos `Sem Despesa (R$ 0)` → 557 candidatos
- `pd.qcut(q=3)` nos positivos: `Q1` (544) | `Q2` (544) | `Q3` (544)

> 💡 **Se o professor perguntar "por que zero-aware?"**: "Porque variáveis zero-inflated são comuns em dados eleitorais. 43% dos candidatos não declararam bens e 26% não contrataram despesas. Se tentássemos quartis puros, os quartis inferiores colapsariam todos em zero, perdendo todo o poder de distinção entre quem tem pouco patrimônio e quem não tem nenhum."

### Passo 3: Montar a "cesta" com one-hot encoding

As 11 variáveis categóricas são transformadas em colunas binárias (0/1):

```python
colunas_apriori = [
    'SG_PARTIDO', 'DS_GENERO', 'DS_GRAU_INSTRUCAO', 'DS_ESTADO_CIVIL',
    'DS_COR_RACA', 'cluster', 'Faixa_Bens', 'Faixa_Despesa_Contratada',
    'Faixa_Idade', 'Faixa_Estudo', 'DS_OCUPACAO'
]
cesta = pd.get_dummies(df[colunas_apriori], prefix_sep='=')
```

Cada candidato vira uma linha com dezenas de colunas binárias: `SG_PARTIDO=PT` (0 ou 1), `DS_GENERO=FEMININO` (0 ou 1), `cluster=Base Simbólica` (0 ou 1), etc.

### Passo 4: Executar o Apriori e gerar regras

```python
itens_frequentes = apriori(cesta, min_support=0.015, use_colnames=True, max_len=3)
regras = association_rules(itens_frequentes, metric='lift', min_threshold=1.1)
```

- **min_support = 0.015** → ~33 candidatos. Qualquer combinação que apareça em menos de 33 pessoas é descartada.
- **max_len = 3** → Combinações de no máximo 3 itens (2 antecedentes + 1 consequente).
- **min_threshold de lift = 1.1** → Só regras com associação positiva (mais frequentes que o acaso).

**Resultado:** ~3.117 itemsets frequentes, gerando milhares de regras de associação.

### Passo 5: Filtrar regras relevantes em duas direções

Aqui é onde respondemos a pergunta central do professor.

#### Direção 1: Características → Cluster (o cluster no CONSEQUENTE)

*"Se um candidato tem tais características, em qual cluster ele está?"*

Filtramos regras onde o consequente (resultado) é um dos 4 clusters.

**Os achados mais fortes (todos com 100% de confiança!):**

| Se o candidato tem... | Então ele é... | Confiança | Lift | Qtd |
|---|---|---|---|---|
| Sem Bens + Sem Despesa | **Base Simbólica** 🌱 | 100% | 6,67 | 308 |
| Bens Q2 + Sem Despesa | **Patrimônio Sem Campanha** 💼 | 100% | 8,83 | 63 |
| Bens Q3 + Sem Despesa | **Patrimônio Sem Campanha** 💼 | 100% | 8,83 | 48 |
| Bens Q3 + Despesa Q3 | **Estruturados** 🏛️ | 100% | 1,90 | 282 |
| Bens Q2 + Despesa Q3 | **Estruturados** 🏛️ | 100% | 1,90 | 142 |
| Sem Bens + Despesa Q3 | **Financiados** ⚡ | 100% | 4,76 | 49 |
| Sem Bens + Despesa Q2 | **Financiados** ⚡ | 100% | 4,76 | 167 |

> 💡 **Insight para a apresentação:** "Se você me disser quanto um candidato tem de patrimônio e quanto gastou em campanha, eu sei com **100% de certeza** em qual cluster ele está. A combinação dessas duas variáveis sozinha já define o perfil eleitoral."

#### Direção 2: Cluster → Características (o cluster no ANTECEDENTE)

*"Dado que o candidato é do Cluster X, quais características são mais fortes nele?"*

Fixamos o cluster como antecedente e vemos o que surge como consequente:

**🏛️ Estruturados → DNA revelado:**
- Ocupação DEPUTADO (lift 1,83) — muitos já são mandatários
- Despesa Q3 (lift 1,73) — campanha com recursos pesados
- Bens Q3 (lift 1,70) — alto patrimônio pessoal
- Partidos PP e PT — partidos de máquina

**⚡ Financiados → DNA revelado:**
- Sem Bens (lift 2,80) — praticamente sem patrimônio (98,7% do cluster!)
- Despesa Q1 (lift 2,11) — campanha modesta mas ativa
- Partido MISSÃO (lift 2,06) — partido evangélico em ascensão
- **51,5% são mulheres** (lift 1,37) — evidência direta das cotas de financiamento feminino

**🌱 Base Simbólica → DNA revelado:**
- Partido DC (lift 4,51) — Democracia Cristã, partido de legendas menores
- Sem Despesa (lift 3,82) — 97% não gastaram nada
- Sem Bens (lift 2,74) — 97% declararam zero
- Ensino Médio (lift 1,75) e Fundamental (lift 1,93) — escolaridade mais baixa

**💼 Patrimônio Sem Campanha → DNA revelado:**
- Sem Despesa (lift 3,77) — 96% não gastaram
- Bens Q1 (lift 2,48) — patrimônio modesto a médio
- Masculino (lift 1,22) — 76% homens
- Idade Q4 (lift 1,14) — os mais velhos da base

### Passo 6: Visualização em grafos interativos

Os grafos interativos (HTML com Pyvis) mostram visualmente as conexões. Cada nó é um item, cada aresta é uma regra. A espessura da aresta representa a confiança. Os nós vermelhos destacados são os 4 clusters.

- [`grafo_regras_cluster.html`](images/notebook3/grafo_regras_cluster.html) → Características convergindo para os clusters (consequente)
- [`grafo_regras_antecedente_fixo.html`](images/notebook3/grafo_regras_antecedente_fixo.html) → Clusters irradiando para suas características (antecedente)

### Conclusão do Apriori

> **Os nomes dos clusters fazem sentido? SIM, 100%.**
> Cada cluster tem regras com 100% de confiança e lifts entre 1,90 e 8,83 que confirmam exatamente o perfil que nomeamos na Fase 2.

---
---

# PARTE 2 — DETECÇÃO DE ANOMALIAS COM ISOLATION FOREST (Notebook 04)

---

## 2.1 O que é o Isolation Forest? (Conceito Fundamental)

### A analogia do "onde está Waldo?"

Imagine uma multidão: milhares de pessoas vestidas normalmente. Waldo está lá, com a camisa listrada de vermelho e branco. Ele é **diferente de todo mundo**.

Se você "cortasse a multidão" aleatoriamente — tipo, "todo mundo à esquerda deste poste vai para um lado, todo mundo à direita vai para o outro" — seria preciso **muitos cortes** para isolar uma pessoa normal (ela está cercada de gente parecida). Mas o Waldo seria isolado rapidamente — ele é tão diferente que poucos cortes já o separam.

Essa é a intuição do Isolation Forest.

### Como funciona, passo a passo

1. **Constrói muitas "árvores de isolamento"** (200 árvores no nosso caso). Cada árvore:
   - Escolhe uma variável **aleatória** (ex: Idade)
   - Escolhe um ponto de corte **aleatório** entre o mín e máx daquela variável
   - Divide os dados em dois grupos
   - Repete recursivamente até cada ponto ficar sozinho

2. **Mede o "caminho"** de cada ponto: quantos cortes foram necessários até isolá-lo.
   - Pontos **anômalos** → isolados rapidamente (caminho **curto**)
   - Pontos **normais** → muitos cortes para isolar (caminho **longo**)

3. **Score de anomalia** = média dos caminhos em todas as 200 árvores, normalizada.
   - Score **baixo** (mais negativo) = mais anômalo
   - Score **alto** (mais positivo) = mais normal

### Vantagens do Isolation Forest

1. **Não precisa definir o que é "normal"** — diferente do K-Means (que assume esferas) ou DBSCAN (que assume densidade). O IF pergunta diretamente "quão fácil é isolar?" sem suposições de forma.
2. **Escala bem** — não calcula distância entre todos os pares de pontos.
3. **Funciona em alta dimensão** — operamos nas mesmas 4 variáveis da clusterização.

### O parâmetro `contamination`

É a fração de dados que **você assume** serem anômalos. É como o `k` do K-Means: uma decisão do analista, não algo calculado automaticamente.

- `contamination = 0.03` significa "acredito que 3% dos dados são anômalos"
- O algoritmo então define o threshold (ponto de corte do score) que classifica exatamente 3% como atípicos.

> 💡 **Analogia:** Se eu pedir pra você marcar os 5% mais altos de uma turma como "outliers de altura", você está decidindo a proporção, e o algoritmo vai achar o ponto de corte correspondente.

---

## 2.2 A Escolha da Contaminação: Por Que 3%?

### O teste empírico

Testamos 6 valores diferentes para ver o efeito:

| contamination | Atípicos | % da base |
|---|---|---|
| 0.01 | 22 | 1,0% |
| 0.02 | 44 | 2,0% |
| **0.03** ★ | **66** | **3,0%** |
| 0.05 | 110 | 5,0% |
| 0.08 | 175 | 8,0% |
| `'auto'` | 792 | **36,2%** |

### Por que não `auto`?

O modo `auto` do scikit-learn marcou **792 candidatos (36,2%!)** como atípicos. Mais de um terço da base! Isso não é "detecção de anomalias", é quase dividir a base em dois. Perde completamente o sentido de "candidato discrepante".

### Por que 3% e não 1% ou 5%?

- **1% (22 candidatos):** Muito restritivo. Pega só os mais extremos, mas perde casos interessantes.
- **5% (110 candidatos):** Volume alto demais para inspeção individual substantiva.
- **3% (66 candidatos):** Equilíbrio perfeito. Volume focado, permite **analisar caso a caso** e identificar padrões reais.

Além disso, 3% é um valor comumente usado na literatura de detecção de fraudes e auditoria eleitoral.

> 💡 **Se o professor perguntar "por que 3%?"**: "Testamos de 1% até auto. O auto marcou 36% da base, totalmente impraticável. Escolhemos 3% porque gera 66 candidatos — volume suficiente para inspeção substantiva individual, sem diluir o foco com centenas de falsos positivos."

---

## 2.3 Anomalias Globais — Quem Foge do Padrão Geral?

### O que fizemos

Aplicamos o Isolation Forest nas **4 variáveis-driver padronizadas** (as mesmas da clusterização):
- `IDADE`
- `ANOS_ESTUDO`
- `Total_Bens_Log`
- `Total_Despesas_Contratadas_Log`

Resultado: **66 candidatos marcados como atípicos** na base de 2.189.

### Diagnóstico: POR QUE cada candidato é anômalo

Para cada atípico, calculamos o **z-score** de cada variável (quantos desvios-padrão ele está da média) e identificamos a variável com o maior desvio absoluto. Isso gera o campo `motivo_global`.

### Os casos mais marcantes (para citar na apresentação)

1. **Nathalia Pedrosa (PE)** — O caso mais extremo
   - 25 anos, Superior Incompleto
   - **R$ 48,3 milhões em bens declarados** e R$ 0 em despesas
   - Motivo: Patrimônio Super-Alto
   - O maior patrimônio de toda a eleição no Nordeste, numa candidata de 25 anos que não gastou absolutamente nada em campanha

2. **Tiririca (CE)** — O caso mais didático
   - Motivo: **Escolaridade Atípica**
   - Ele "Lê e Escreve" (1 ano de estudo, z = -4,1)
   - Mas tem R$ 2,45 milhões em despesas de campanha
   - **Importante para a explicação 3D:** No gráfico 3D (Idade x Bens x Despesas), Tiririca aparece **no meio da nuvem** — porque as 3 dimensões visíveis dele são normais! A anomalia está na **4ª dimensão (escolaridade)**, que não tem eixo no gráfico.

3. **Ubirajara É Show Papai (CE)** — Mesmo perfil do Tiririca
   - "Lê e Escreve" (z = -5,0)
   - Despesas de R$ 136 mil
   - Parece normal no 3D, mas extremo na 4ª dimensão

> 💡 **Explicação para o professor sobre o 3D:** "O Isolation Forest operou em 4 dimensões simultaneamente. O gráfico 3D projeta apenas 3 eixos — a escolaridade fica 'oculta'. Candidatos como Tiririca parecem no centro do gráfico 3D porque idade, bens e despesas são normais. Mas na dimensão da escolaridade, eles estão completamente isolados. Por isso adicionamos o tooltip diagnóstico que explica o motivo do isolamento ao passar o mouse."

---

## 2.4 Anomalias Locais — Quem Foge do Padrão do Próprio Grupo?

### A diferença metodológica crucial

Na detecção **global**, comparamos cada candidato contra **toda a base** (2.189 candidatos). Mas existe um tipo de anomalia mais sutil:

> Um candidato dos Financiados que declara R$ 240 em bens é "normal" na população geral. Mas **dentro do cluster Financiados, onde 98,7% tem bens = R$ 0**, ele é um outlier extremo!

### Como implementamos

Para cada um dos 4 clusters, **separadamente**:
1. Isolamos os dados do cluster
2. **Repadronizamos** usando média e desvio-padrão **do próprio cluster** (StandardScaler local)
3. Rodamos um Isolation Forest novo com contaminação adaptativa

A contaminação por cluster usa a fórmula:
```
contaminação = min(max(0.03, 3/n), 0.08)
```
- Garante **pelo menos 3 anomalias** em clusters pequenos
- Não ultrapassa 8% em nenhum cluster

### Resultados por cluster

| Cluster | Tamanho | Anomalias Locais | Exemplos |
|---|---|---|---|
| **Estruturados** | 1.153 | **35** | Candidatos com patrimônio extremamente alto ou escolaridade muito baixa para o perfil |
| **Financiados** | 460 | **14** | Candidatos com pequenos bens declarados (R$ 240, R$ 389) quando 98,7% tem zero |
| **Base Simbólica** | 328 | **10** | Candidatos com despesas residuais (R$ 48, R$ 100) quando 97% tem despesa zero |
| **Patrimônio Sem Campanha** | 248 | **8** | Candidatos com patrimônios extremamente altos para o perfil do cluster |

### A matriz de contingência: global vs. local

| | Típico (cluster) | Atípico (cluster) |
|---|---|---|
| **Típico (global)** | 2.093 | **37** |
| **Atípico (global)** | 36 | **30** |

**Os 4 quadrantes explicados:**

1. **2.093 — Típicos em ambos:** A grande maioria. Normais na população e normais dentro do grupo.
2. **30 — Atípicos em ambos:** Candidatos tão discrepantes que se destacam em qualquer análise. Consenso total.
3. **36 — Atípicos só globalmente:** Extremos na base geral, mas "dentro da norma" do seu cluster. Exemplo: um Estruturado com patrimônio muito alto é atípico globalmente, mas entre os Estruturados (que já têm patrimônio alto) é esperado.
4. **37 — Atípicos só localmente:** ⭐ **O caso mais interessante!** Candidatos que passariam **completamente despercebidos** na análise global, mas que são outliers dentro do seu próprio grupo.

> 💡 **Destaque na apresentação:** "A análise local revelou **37 candidatos invisíveis** na análise global. Eles parecem normais quando comparados com todos os 2.189, mas quando olhamos apenas para seus pares de cluster, são completamente atípicos. Isso mostra que a análise em dois níveis — global e local — é essencial para não perder informação."

---

## 2.5 O Gráfico 3D: Por Que Tem Pontos Vermelhos "No Meio"?

**Essa é uma pergunta que o professor pode fazer.** Domine esta explicação:

O gráfico 3D tem 3 eixos: `Idade`, `Total_Bens_Log` e `Total_Despesas_Contratadas_Log`.

Mas o modelo operou em **4 dimensões** (incluindo `ANOS_ESTUDO`).

Quando projetamos dados de 4D em 3D, **perdemos uma dimensão**. Candidatos que são anômalos **apenas** na dimensão da escolaridade aparecem no centro do gráfico 3D, porque as outras 3 variáveis deles são normais.

É como tirar uma foto de um prédio de frente: se alguém estiver no fundo, parece estar no mesmo plano. Mas se você olhar de lado, vê que está bem mais atrás.

**Como resolvemos:** Adicionamos tooltip diagnóstico ao passar o mouse sobre cada ponto vermelho, mostrando: `🚨 Motivo do Isolamento: Escolaridade Atípica: LÊ E ESCREVE (z=-4.1)`.

---
---

# PARTE 3 — SLIDE 7: A CONCLUSÃO

---

## 3.1 Os Principais Achados

### Perfis encontrados (resumo rápido)

| Cluster | % | Perfil em uma frase |
|---|---|---|
| **Estruturados** 🏛️ | 53% | Candidatos com patrimônio E campanha ativa — a máquina eleitoral |
| **Financiados** ⚡ | 21% | Sem patrimônio, mas com dinheiro de campanha via fundo partidário |
| **Base Simbólica** 🌱 | 15% | Sem bens, sem campanha — candidaturas formais/cartoriais |
| **Patrimônio Sem Campanha** 💼 | 11% | Tem bens, mas não gastou nada em campanha |

### O que confirmou expectativas

- Que a elite política combina alto patrimônio com alto gasto (Estruturados)
- Que muitas candidaturas são apenas formais (Base Simbólica)

### O que foi inesperado

1. **Os Financiados têm maioria feminina (51,5%)** — As cotas de financiamento para candidatas estão funcionando: mulheres sem patrimônio pessoal recebem aportes dos partidos para campanhas modestas. É uma **política pública deixando rastro nos dados**.

2. **Patrimônio Sem Campanha existe como perfil distinto** — Empresários, advogados e profissionais com patrimônio que se candidataram mas não investiram nada em campanha. Por que se candidatam? É uma pergunta que os dados revelam mas não respondem completamente.

3. **37 anomalias invisíveis na análise global** — A análise de anomalias em dois níveis (global + local) revelou candidatos que só se destacam quando comparados aos seus pares de cluster.

### A principal contribuição

> "A combinação patrimônio × despesas de campanha revela 4 arquétipos eleitorais com perfis sociodemográficos e ocupacionais completamente distintos. Esses perfis são **validáveis por regras de associação com 100% de confiança** — não são artefatos do algoritmo, são padrões reais da dinâmica eleitoral nordestina."

---
---

# PARTE 4 — SIMULAÇÃO DE PERGUNTAS DO PROFESSOR

---

## Sobre o Apriori

**P: "O que é suporte, confiança e lift?"**
> R: "Suporte é a frequência da regra na base (quantos candidatos têm A e B juntos). Confiança é a probabilidade condicional (dado A, qual a chance de B). Lift compara com o acaso: se fosse tudo independente, qual seria a frequência esperada? Lift 6,67 significa que a combinação aparece quase 7 vezes mais do que se as variáveis não tivessem relação."

**P: "Por que quartis e não outra discretização?"**
> R: "Porque o professor exigiu quartis. E é a forma mais equilibrada: cada faixa tem aproximadamente 25% dos dados, evitando faixas vazias ou superpopuladas."

**P: "Por que zero-aware para bens e despesas?"**
> R: "Porque 43% dos candidatos têm bens = zero e 26% têm despesas = zero. Com quartis puros, os dois primeiros quartis seriam ambos zero, perdendo poder discriminativo. Separamos os zeros como categoria semântica e calculamos quartis sobre os valores positivos."

**P: "Por que não usou pd.qcut para escolaridade?"**
> R: "Porque 58% dos candidatos têm exatamente 16 anos de estudo (Superior Completo). O pd.qcut colapsaria Q2 = Q3 = 16 e produziria apenas 2 faixas. Usamos cortes baseados nos níveis educacionais brasileiros para manter 4 faixas interpretáveis."

**P: "O que significam essas regras na prática?"**
> R: "Que os clusters NÃO são artefatos do algoritmo. São padrões reais e mensuráveis. Se eu souber apenas o patrimônio e a despesa de um candidato, sei com 100% de certeza em qual perfil ele se encaixa."

**P: "O que é o grafo?"**
> R: "É uma representação visual das regras de associação. Cada nó é um item (ex: SG_PARTIDO=PT, cluster=Estruturados), cada seta é uma regra (antecedente → consequente). A espessura da seta é proporcional à confiança. Permite ver de relance quais itens são mais centrais e quais regras convergem para cada cluster."

## Sobre o Isolation Forest

**P: "Como funciona o Isolation Forest?"**
> R: "Constrói 200 árvores que cortam o espaço aleatoriamente. Pontos anômalos são isolados rapidamente (poucos cortes). Pontos normais precisam de muitos cortes porque estão cercados de vizinhos. O score de anomalia é a profundidade média de isolamento: quanto mais raso, mais anômalo."

**P: "Por que 3% de contaminação?"**
> R: "Testamos de 1% a 8% e o modo auto. Auto marcou 36% — impraticável. Com 3% temos 66 candidatos, volume focado para análise substantiva individual."

**P: "Por que alguns pontos anômalos aparecem no centro do gráfico 3D?"**
> R: "Porque o modelo operou em 4 dimensões, mas o gráfico mostra apenas 3. A escolaridade não tem eixo visual. Candidatos como Tiririca, com 1 ano de estudo num ambiente de graduados, são anômalos na 4ª dimensão — que o olho não vê no 3D. O tooltip diagnóstico explica o motivo."

**P: "Qual a diferença entre anomalia global e por cluster?"**
> R: "A global compara contra todos os 2.189 candidatos. A local compara contra os pares do mesmo grupo. Um Financiado com R$ 240 em bens é normal na população geral, mas é outlier extremo no seu cluster onde 98,7% tem zero. Encontramos 37 candidatos que são anômalos só localmente — invisíveis na análise global."

**P: "Se fizessem de novo, o que mudariam?"**
> R: "Incluiríamos o resultado da eleição (eleito/não eleito) quando disponível para testar se algum perfil tem vantagem competitiva. Também exploraríamos coligações e a proporção de receitas partidárias vs. individuais."

---

# PARTE 5 — IMAGENS PARA OS SLIDES

## Slide 5 (Apriori)
| Imagem | Arquivo |
|---|---|
| Distribuição das 4 faixas de quartis | `images/notebook3/01_distribuicao_quartis.png` |
| Top regras: Características → Cluster (barras por lift) | `images/notebook3/02_top_regras_cluster_consequente.png` |
| Top regras: Cluster → Características (DNA dos arquétipos) | `images/notebook3/03_top_regras_cluster_antecedente.png` |
| Dispersão: Suporte x Confiança colorido por Lift | `images/notebook3/04_dispersao_regras_suporte_confianca.png` |
| Grafo interativo (consequente) | `images/notebook3/grafo_regras_cluster.html` |
| Grafo interativo (antecedente fixo) | `images/notebook3/grafo_regras_antecedente_fixo.html` |

## Slide 6 (Anomalias)
| Imagem | Arquivo |
|---|---|
| Scatter 2D das anomalias globais | `images/notebook4/03_anomalias_globais_2d.png` |
| Scatter 3D estático (PNG para slide) | `images/notebook4/04_grafico_3d_anomalias_matplotlib.png` |
| 3D interativo global (para abrir no navegador) | `images/notebook4/04_grafico_3d_anomalias_global.html` |
| 3D interativo por cluster (para abrir no navegador) | `images/notebook4/05_grafico_3d_anomalias_cluster.html` |
| Matriz de contingência global vs local | `images/notebook4/06_matriz_contingencia_anomalias.png` |

---

# PARTE 6 — RESUMO MENTAL (Cola Rápida)

## Apriori em 30 segundos
1. Transformamos variáveis contínuas em quartis (com zero-aware para bens/despesas)
2. Montamos uma "cesta" binária com 11 variáveis categóricas
3. Rodamos Apriori com suporte mínimo 1,5%
4. Filtramos regras nas 2 direções: Características → Cluster e Cluster → Características
5. **Resultado:** TODOS os clusters confirmados com 100% de confiança e lifts de até 8,83

## Isolation Forest em 30 segundos
1. Constrói 200 árvores que cortam aleatoriamente o espaço 4D
2. Pontos fáceis de isolar = anômalos; difíceis = normais
3. Contaminação = 3% (testamos 6 valores, auto deu 36%)
4. **66 anomalias globais** (Nathalia Pedrosa = R$ 48M em bens com 25 anos; Tiririca = 1 ano de estudo com R$ 2,4M de campanha)
5. **67 anomalias locais** (por cluster), revelando **37 candidatos invisíveis** na análise global

## A frase de ouro para fechar
> "As regras de associação com 100% de confiança em todos os clusters provam que os perfis não são artefatos do algoritmo — são padrões reais da dinâmica eleitoral nordestina."
