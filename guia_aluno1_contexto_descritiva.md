# 🎓 Guia Completo do Aluno 1 — Contextualização + Análise Descritiva (Slides 1 e 2)

> **Objetivo deste documento:** Permitir que você, Aluno 1, domine com segurança absoluta a abertura da apresentação do grupo. Você é o responsável por situar a banca no problema, explicar a origem dos dados do TSE e apresentar o diagnóstico das 4 variáveis que alimentarão os algoritmos de Machine Learning.

---

# PARTE 1 — SLIDE 1: CONTEXTUALIZAÇÃO DO TRABALHO (~1.5 min)

---

## 1.1 Objetivo do Trabalho e Pergunta de Negócio

### A Narrativa Central
Na abertura, evite começar diretamente listando números soltos. Comece contando **qual problema o grupo se propôs a resolver**:

> *"Em uma eleição para o Congresso Nacional, os candidatos competem em condições de igualdade ou existem abismos estruturais de recursos e perfil? Nosso objetivo é investigar se os candidatos a Deputado Federal no Nordeste se dividem em grupos socioeconômicos bem definidos ou se formam um continuum homogêneo."*

### O Problema sob a ótica de Machine Learning
- O aprendizado utilizado é **Não Supervisionado** (*Unsupervised Learning*).
- **Por que não supervisionado?** Porque os dados do TSE **não possuem um rótulo pré-definido** dizendo quem pertence a qual "tipo" de candidatura. O algoritmo precisa encontrar essa estrutura latente sozinho, a partir da geometria e das relações estatísticas das variáveis.
- **O Pipeline Completo:**
  1. Análise Descritiva e Diagnóstico de Distribuição (sua parte - Aluno 1)
  2. Particionamento Hierárquico por Bisecting K-Means (Aluno 2)
  3. Caracterização Sociodemográfica e Nomeação dos Arquétipos (Aluno 3)
  4. Validação por Regras de Associação e Detecção de Casos Atípicos (Aluno 4)

---

## 1.2 A População Analisada e a Base do TSE

### Delimitação Exata da População
- **População:** Todos os **2.189 candidatos a Deputado Federal** registrados no Tribunal Superior Eleitoral (TSE) para as Eleições de 2026.
- **Recorte Geográfico:** Os **9 estados da Região Nordeste** do Brasil:
  - Alagoas (AL)
  - Bahia (BA)
  - Ceará (CE)
  - Maranhão (MA)
  - Paraíba (PB)
  - Pernambuco (PE)
  - Piauí (PI)
  - Rio Grande do Norte (RN)
  - Sergipe (SE)
- **Cargo:** Deputado Federal (câmara baixa do legislativo federal, eleição proporcional de lista aberta).

### As Fontes de Dados e o Pré-Processamento (Notebook 00)
Para construir a base final, o grupo realizou o cruzamento relacional de três tabelas oficiais do Portal de Dados Abertos do TSE (`dadosabertos.tse.jus.br`):
1. **Consulta Candidatos (`consulta_cand`):** Atributos cadastrais e demográficos (Nome, CPF, Data de Nascimento/Idade, Gênero, Grau de Instrução, Ocupação Declarada, Estado Civil, Cor/Raça, Partido e UF).
2. **Declaração de Bens (`bem_candidato`):** Cada linha é um item patrimonial declarado pelo candidato (imóveis, veículos, aplicações financeiras, dinheiro em espécie). O grupo agrupou e somou esses valores por candidato (`Total_Bens`).
3. **Prestação de Contas Eleitorais (`despesas_contratadas`):** Registro contábil das despesas financeiras formalmente contratadas durante a campanha eleitoral. O grupo consolidou essas despesas no atributo `Total_Despesas_Contratadas`.

**Chave de Ligação:** O cruzamento foi realizado via `SQ_CANDIDATO` (código sequencial único do candidato no TSE).

---

# PARTE 2 — SLIDE 2: ANÁLISE DESCRITIVA DAS 4 VARIÁVEIS (~2.5 min)

---

## 2.1 Por que essas 4 Variáveis Foram Escolhidas?

O grupo selecionou **4 variáveis quantitativas fundamentais** para atuar como *drivers* (motoras) da clusterização. Elas representam os dois grandes pilares da viabilidade eleitoral:
1. **Capital Humano e Pessoal:** `IDADE` e `ANOS_ESTUDO`
2. **Capital Econômico e Político:** `Total_Bens` (patrimônio próprio) e `Total_Despesas_Contratadas` (mobilização de campanha)

> 💡 **Conceito Chave:** Deixamos variáveis como Gênero, Raça, Partido e Ocupação **fora** da clusterização propositalmente! Elas foram reservadas para a etapa de **perfilamento sociodemográfico** (Aluno 3), permitindo validar se os grupos econômicos formados refletiam ou não clivagens sociais reais sem causar distorções na distância euclidiana.

---

## 2.2 Tabela Geral de Estatísticas Descritivas (Tenha na Ponta da Língua)

Esta tabela resume todo o seu segundo slide:

| Variável | Média | Mediana | Desvio-Padrão | Mínimo | Máximo | Comportamento Estatístico |
|---|---|---|---|---|---|---|
| **IDADE** | 48,1 anos | 48,0 anos | 11,4 anos | 21 anos | 81 anos | Simétrica, quase normal |
| **ANOS_ESTUDO** | 13,8 anos | 16,0 anos | 3,1 anos | 1 ano | 16 anos | Alta concentração no topo (Superior) |
| **Total_Bens** | R$ 1.050.412 | R$ 85.000 | R$ 3.245.190 | R$ 0 | R$ 48.330.000 | Assimetria extrema, **43% zeros** |
| **Total_Despesas_Contratadas** | R$ 442.180 | R$ 35.800 | R$ 785.420 | R$ 0 | R$ 3.320.000 | Bimodal, **26% zeros**, cauda pesada |

---

## 2.3 Diagnóstico Detalhado Variável por Variável

### 1. IDADE (Anos)
- **Média:** 48,1 anos | **Mediana:** 48,0 anos (média e mediana praticamente idênticas!).
- **Distribuição:** Forma de sino (quase gaussiana), variando de 21 anos (idade mínima legal para Deputado Federal no Brasil) até 81 anos.
- **Interpretação:** A política nordestina não é polarizada por extremos etários. O grosso dos concorrentes está na maturidade profissional (entre 38 e 58 anos). Não há necessidade de transformações matemáticas nessa variável.

### 2. ANOS_ESTUDO (Tempo de Instrução)
- **Como foi criada:** O TSE fornece graus de instrução nominais. Para alimentar algoritmos baseados em distância euclidiana, mapeamos os níveis para anos formais de escolaridade:
  - *Lê e Escreve:* 1 ano
  - *Ensino Fundamental Incompleto:* 4 anos | *Completo:* 8 anos
  - *Ensino Médio Incompleto:* 9 anos | *Completo:* 11 anos
  - *Ensino Superior Incompleto:* 13 anos | *Completo:* 16 anos
- **Distribuição:** Forte assimetria à esquerda.
- **O Dado Alarmante:** **58% dos candidatos possuem Ensino Superior Completo (16 anos)**.
- **Interpretação:** Enquanto na população geral do Nordeste a taxa de ensino superior é inferior a 15%, entre os candidatos ela chega a quase 60%. O registro de candidatura já opera como um filtro social elitista.

### 3. TOTAL_BENS (Patrimônio Declarado)
- **A Discrepância Brutal:** Média de **R$ 1,05 milhão**, contra uma Mediana de apenas **R$ 85 mil**!
- **O Fenômeno dos Zeros (*Zero-Inflated*):** **43% dos candidatos (941 de 2.189) declararam patrimônio exatamente igual a R$ 0,00!**
- **O Topo da Pirâmide:** No extremo oposto, candidatos declaram dezenas de milhões (como a candidata mais rica, com R$ 48,3 milhões).
- **Tratamento:** Impossível utilizar os valores brutos em reais no K-Means, pois poucos milionários puxariam os centróides para o infinito. Aplicamos a transformação logarítmica:
  $$\text{Total\_Bens\_Log} = \log(1 + \text{Total\_Bens})$$

### 4. TOTAL_DESPESAS_CONTRATADAS (Gastos de Campanha)
- **Média:** R$ 442 mil | **Mediana:** R$ 35,8 mil.
- **O Fenômeno dos Zeros:** **26% dos candidatos (569 de 2.189) contrataram R$ 0,00 em despesas!**
- **Interpretação Política:** Um quarto dos candidatos são puramente **candidaturas cartoriais / de legenda** (existem no papel para cumprir cota partidária, mas não confeccionaram um santinho nem fizeram um ato de rua).
- **Bimodalidade:** Os dados se dividem claramente entre:
  1. Quem não gastou nada ou valores simbólicos (< R$ 5.000);
  2. Quem recebeu grandes aportes do Fundo Eleitoral (FEFC) e gastou entre R$ 500 mil e o teto legal de R$ 3,32 milhões.
- **Tratamento:** Transformação $\log(1 + \text{Despesas})$.

---

## 2.4 As Relações Bivariadas Relevantes (Cruzar Informações)

No Slide 2, para demonstrar domínio analítico avançado, comente estes cruzamentos do notebook 01:
1. **Patrimônio vs. Despesas (Correlação Fraca a Moderada):**
   - A correlação entre Bens (log) e Despesas (log) é de apenas **+0,38**.
   - **Por que isso é fascinante?** Mostra que ter dinheiro próprio no bolso **não significa automaticamente** fazer campanha rica! Existem ricos que não gastam nada (o que virará o *Cluster Patrimônio Sem Campanha*), e existem candidatos sem patrimônio que gastam milhões viabilizados por fundo partidário (o que virará o *Cluster Financiados*).
2. **Cota de Gênero:**
   - Em todos os estados nordestinos, a proporção de mulheres fica rigorosamente entre 31% e 34% (o mínimo legal obrigatório é 30%). No entanto, ao olharmos os gastos de campanha, as mulheres recebem desproporcionalmente menos recursos próprios, dependendo quase que exclusivamente de repasses públicos.

---

# PARTE 3 — SIMULAÇÃO DE PERGUNTAS DA BANCA (Defesa Blindada)

**P1: "Por que vocês aplicaram a transformação Log nas variáveis de Bens e Despesas?"**
> *Sua Resposta:* "Porque ambas possuem assimetria positiva extrema (*right-skewed*), onde a média é mais de dez vezes superior à mediana. No K-Means e Bisecting K-Means, a distância utilizada é a euclidiana. Se usássemos os valores brutos em reais, candidatos com dezenas de milhões de patrimônio distorceriam completamente os centróides, formando clusters unitários de outliers. O $\log(1+x)$ estabiliza a escala sem perder a ordem de grandeza, e o '+1' evita o problema matemático de calcular $\log(0)$ para os candidatos com bens ou despesas zerados."

**P2: "O que significa dizer que os dados são 'Zero-Inflated'?"**
> *Sua Resposta:* "Significa que há uma concentração excessiva e estrutural de valores exatamente iguais a zero — no nosso caso, 43% em bens e 26% em despesas. Esses zeros não são dados faltantes (*missing values*), são informações substantivas reais: cidadãos que não possuem patrimônio registrado e candidatos que não executaram atos financeiros de campanha. Reconhecer esse fenômeno foi determinante para entender por que mais adiante o Apriori precisou de quartis zero-aware."

**P3: "Por que criar a variável ANOS_ESTUDO em vez de usar o código original do TSE?"**
> *Sua Resposta:* "O código original do TSE é meramente administrativo e não reflete intervalos proporcionais (por exemplo, a distância entre Fundamental e Médio não é a mesma entre Médio e Superior). Além disso, o K-Means calcula distâncias geométricas e médias contínuas. Mapear o grau de instrução para anos formais de estudo (1 a 16 anos) transformou uma variável ordinal qualitativa em uma métrica intervalar contínua, permitindo que a geometria euclidiana operasse sem criar distorções artificiais."

**P4: "Por que vocês não colocaram Gênero, Raça e Partido logo na clusterização inicial?"**
> *Sua Resposta:* "Porque misturar variáveis contínuas padronizadas com variáveis categóricas 'one-hot encoded' (0 ou 1) em algoritmos de distância euclidiana causa a chamada 'maldição da dimensionalidade' e perda da interpretabilidade física dos centróides. Adotamos o padrão metodológico de separar variáveis *driver* (as 4 financeiras e de capacitação) para formar os grupos e usar as variáveis demográficas para *caracterizar e validar* os grupos formados."

---

# PARTE 4 — IMAGENS PRONTAS PARA O SEU BLOCO

No seu computador, todas as imagens foram organizadas com nomes intuitivos na pasta `images/imagens_apresentacao/`:

| Slide | O que colocar | Arquivo Principal (Grid) | Arquivos Separados Disponíveis |
|---|---|---|---|
| **Slide 1** | Mapa e Distribuição de Candidatos por Estado | `images/imagens_apresentacao/slide1_01_candidatos_por_uf.png` | — |
| **Slide 2 (Destaque)** | **Grid 2x2 das 4 Variáveis da Clusterização** | `images/imagens_apresentacao/slide2_01_distribuicao_4_drivers_grid.png` | `slide2_02_hist_idade.png`<br>`slide2_03_hist_grau_instrucao.png`<br>`slide2_04_hist_total_bens_log.png`<br>`slide2_05_hist_total_despesas_log.png` |
| **Slide 2** | Boxplots de Outliers por Variável | `images/imagens_apresentacao/slide2_06_boxplots_outliers.png` | — |
| **Slide 2** | Distribuição de Despesas em Escala Log | `images/imagens_apresentacao/slide2_07_distribuicao_despesas_log.png` | — |

---

# PARTE 5 — COLA RÁPIDA DE 60 SEGUNDOS (Memorize)

1. **População:** 2.189 candidatos a Deputado Federal nos 9 estados do Nordeste em 2026.
2. **Fontes:** TSE (Candidaturas + Bens Declarados + Despesas Contratadas consolidadas por nós).
3. **Idade:** Média e mediana de 48 anos, perfeitamente simétrica.
4. **Instrução:** Super-elitizada, 58% possuem Ensino Superior Completo (16 anos de estudo).
5. **Bens:** Média R$ 1M vs Mediana R$ 85 mil — **43% têm patrimônio ZERO**.
6. **Despesas:** Média R$ 442k vs Mediana R$ 35,8k — **26% têm despesas ZERO** (candidaturas cartoriais).
7. **Solução:** Aplicamos $\log(1+x)$ em bens e despesas para conter a assimetria e permitir que o K-Means agrupe padrões sem ser distorcido por milionários.
