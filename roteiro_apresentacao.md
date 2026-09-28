# 🎓 Roteiro Completo da Apresentação
## Análise de Candidatos a Deputado Federal — Nordeste 2026 (TSE)

> **Tempo total**: 15-20 minutos  
> **Grupo**: 4 integrantes  
> **Narrativa**: Contexto → Dados → Descritiva → Escolha de K → Clusters → Caracterização e nomeação → Regras de associação → Validação dos perfis → Anomalias → Conclusões

---

## 📌 Divisão por Apresentador

| Apresentador | Bloco | Seções | Tempo Estimado |
|---|---|---|---|
| **Aluno 1** | Slides 1-2 | Contextualização + Análise Descritiva | ~4 min |
| **Aluno 2** | Slide 3 | Bisecting K-Means (escolha de K) | ~4 min |
| **Aluno 3** | Slide 4 | Caracterização dos Clusters + Nomeação | ~4 min |
| **Aluno 4** | Slides 5-6-7 | Apriori + Isolation Forest + Conclusão | ~5-7 min |

---

# 🎤 ALUNO 1 — Contextualização + Análise Descritiva (~4 min)

---

## Slide 1: Contextualização do Trabalho (~1.5 min)

### 🖼️ O que mostrar
- Slide com título do trabalho, nomes do grupo e mapa do Nordeste destacado

### 💬 Script de fala

> "Nosso trabalho analisa o perfil dos **2.189 candidatos a Deputado Federal no Nordeste** nas eleições de 2026, utilizando dados oficiais do **Tribunal Superior Eleitoral (TSE)**.
>
> A região analisada compreende os **9 estados do Nordeste**: Alagoas, Bahia, Ceará, Maranhão, Paraíba, Pernambuco, Piauí, Rio Grande do Norte e Sergipe.
>
> A base de dados do TSE integra informações cadastrais dos candidatos — como idade, gênero, raça, profissão e escolaridade — com dados financeiros: o **patrimônio pessoal declarado** (bens totais) e as **despesas de campanha contratadas**.
>
> O objetivo do trabalho é aplicar técnicas de **aprendizado não supervisionado** — clusterização, regras de associação e detecção de anomalias — para identificar **perfis eleitorais distintos**, validar esses perfis com regras empíricas e encontrar candidatos com comportamento atípico."

### 🛡️ Se o professor perguntar:
- **"Por que o Nordeste?"** → "Foi a região designada ao nosso grupo."
- **"De onde vêm os dados?"** → "Portal de Dados Abertos do TSE (dadosabertos.tse.jus.br). A base já vem pré-processada com junção de candidaturas, bens declarados e prestações de contas."

---

## Slide 2: Análise Descritiva das 4 Variáveis (~2.5 min)

### 🖼️ O que mostrar
1. **Histogramas das 4 Variáveis da Clusterização** — do notebook `01_analise_descritiva.ipynb` (Seção 3):
   - **Grid Unificado 2x2:** `images/imagens_apresentacao/slide2_01_distribuicao_4_drivers_grid.png` (ou `images/notebook1/02_distribuicao_4_drivers_clusterizacao.png`)
   - **Histogramas Individuais Separados:**
     - Idade: `images/imagens_apresentacao/slide2_02_hist_idade.png`
     - Grau de Instrução (Tempo de Estudo): `images/imagens_apresentacao/slide2_03_hist_grau_instrucao.png`
     - Patrimônio Declarado (log): `images/imagens_apresentacao/slide2_04_hist_total_bens_log.png`
     - Despesas Contratadas (log): `images/imagens_apresentacao/slide2_05_hist_total_despesas_log.png`
2. **Boxplots de Outliers** — `images/imagens_apresentacao/slide2_06_boxplots_outliers.png`
3. **Distribuição Bimodal de Despesas** — `images/imagens_apresentacao/slide2_07_distribuicao_despesas_log.png`
3. **Tabela de estatísticas descritivas** (pode montar um slide com estes números):

| Variável | Média | Mediana | Mín | Máx | Observação-chave |
|---|---|---|---|---|---|
| **Idade** | 48,1 anos | 48 anos | 21 | 81 | Distribuição simétrica |
| **Anos de Estudo** | 13,8 anos | 16 anos | 1 | 16 | 58% têm Superior Completo |
| **Total de Bens** | R$ 1,05M | R$ 85k | R$ 0 | R$ 48,3M | **43% declararam R$ 0** |
| **Despesas Contratadas** | R$ 442k | R$ 35,8k | R$ 0 | R$ 3,32M | **26% com R$ 0** |

### 💬 Script de fala

> "Antes de aplicar qualquer algoritmo, precisamos entender os dados. As **4 variáveis que usaremos na clusterização** são: idade, anos de estudo, total de bens declarados e total de despesas de campanha contratadas.
>
> A **idade** tem distribuição simétrica com média de 48 anos — o cenário político nordestino não é dominado por jovens nem por idosos.
>
> A **escolaridade** é fortemente concentrada no topo: 58% dos candidatos têm ensino superior completo. Isso reflete uma barreira de entrada na política institucional.
>
> Já o **patrimônio** apresenta uma assimetria brutal: **43% dos candidatos declararam R$ 0 em bens**. A mediana é de apenas R$ 85 mil, mas a média é de R$ 1 milhão — puxada por uma elite financeira.
>
> As **despesas de campanha** mostram um padrão bimodal: **26% não registraram nenhum gasto** — são candidaturas que provavelmente não se ativaram — enquanto outra parcela recebeu investimentos substanciais dos fundos partidário e eleitoral.
>
> A observação dos zeros é crucial: são candidatos reais que existem no sistema eleitoral, mas com perfis financeiros radicalmente diferentes. Essa heterogeneidade vai ser determinante na formação dos clusters."

### 🛡️ Se o professor perguntar:
- **"Por que usaram log?"** → "As variáveis financeiras têm distribuição extremamente assimétrica (média >> mediana). A transformação log(1+x) estabiliza a variância e permite que o algoritmo de clusterização não seja dominado por poucos outliers milionários."
- **"O que é zero-inflated?"** → "É quando uma proporção grande dos dados tem valor exatamente zero. No nosso caso, 43% de bens zerados e 26% de despesas zeradas. Isso cria uma bimodalidade que precisa ser tratada com cuidado."
- **"ANOS_ESTUDO existia na base original?"** → "Não. O TSE fornece o grau de instrução como texto (ex.: 'Ensino Superior Completo'). Nós criamos a variável numérica ANOS_ESTUDO mapeando cada grau para o número de anos correspondente (ex.: Superior Completo = 16, Ensino Médio = 11, Fundamental = 8), para poder usar na clusterização."

---

# 🎤 ALUNO 2 — Clusterização com Bisecting K-Means (~4 min)

---

## Slide 3: Escolha de K e Bisecting K-Means (~4 min)

### 🖼️ O que mostrar (do notebook `02_clusterizacao.ipynb`)
1. **Gráfico de Cotovelo + Curva de Silhueta** — seção V3.1
2. **Tabela de métricas por K** (montar no slide):

| K | Silhouette | Davies-Bouldin | Calinski-Harabasz |
|---|---|---|---|
| 2 | 0.446 | 1.219 | 1.391 |
| 3 | 0.380 | 1.048 | 1.701 |
| **4** | **0.488** ★ | **0.844** ★ | **2.429** ★ |
| 5 | 0.435 | 0.932 | 2.115 |
| 6 | 0.395 | 0.924 | 1.990 |

3. **Árvore de divisão do Bisecting K-Means** — seção V3.2
4. **Gráfico de barras K-Means vs Bisecting** — seção V3.2.1

### 💬 Script de fala

> "Para a clusterização, utilizamos o **Bisecting K-Means** conforme orientado, e testamos valores de K de 2 a 8.
>
> Avaliamos cada K com **três métricas formais**:
> - O **Coeficiente de Silhueta**, que mede a qualidade da separação entre clusters — quanto maior, melhor.
> - O **Índice Davies-Bouldin**, que mede a sobreposição entre clusters — quanto menor, melhor.
> - O **Calinski-Harabasz**, que mede a razão entre a dispersão inter-cluster e intra-cluster — quanto maior, melhor.
>
> **K = 4 é o ótimo indiscutível nas três métricas**: Silhueta máxima de **0,488**, Davies-Bouldin mínimo de **0,844** e Calinski-Harabasz máximo de **2.429**.
>
> O **método do cotovelo** confirma: a inércia cai de forma acentuada até K=3 e K=4, estabilizando depois.
>
> O **Bisecting K-Means** opera de forma *top-down*: começa com todos os 2.189 candidatos em um único grupo e vai dividindo o cluster de maior inércia em cada nível. Na prática, as divisões foram:
> - Nível 1: a raiz se dividiu em 2 grupos (1.034 e 1.155 candidatos);
> - Nível 2: o grupo de 1.034 se dividiu em 573 e 461;
> - Nível 3: o grupo de 573 se dividiu em 326 e 247.
>
> Os tamanhos finais (1.155, 461, 326, 247) são **praticamente idênticos** aos do K-Means padrão (1.153, 460, 328, 248). Essa **convergência estrutural** entre dois algoritmos independentes valida que K=4 não é um artefato de um método específico.
>
> A silhueta do Bisecting (0,485) é virtualmente igual à do K-Means (0,488). Escolhemos **K=4** com confiança total."

### 🛡️ Se o professor perguntar:
- **"Por que não K=3 ou K=5?"** → "K=3 tem silhueta menor (0,380) e Davies-Bouldin pior (1,048). K=5 piora em todas as métricas. K=4 é pico simultâneo nos 3 indicadores."
- **"Qual a diferença entre K-Means e Bisecting?"** → "O K-Means particiona todos os pontos simultaneamente; o Bisecting é hierárquico e divisivo — divide de cima pra baixo. O fato de ambos convergirem para a mesma partição mostra que a estrutura de 4 clusters é intrínseca aos dados."
- **"E o método do cotovelo sozinho?"** → "O cotovelo tem interpretação visual subjetiva — por isso complementamos com métricas objetivas (Silhueta, DB, CH) que apontam unânime para K=4."

---

# 🎤 ALUNO 3 — Caracterização e Nomeação dos Clusters (~4 min)

---

## Slide 4: Perfis dos Clusters + Nomeação (~4 min)

### 🖼️ O que mostrar (do notebook `02_clusterizacao.ipynb`)
1. **Gráfico de Radar Polar** — seção V3.3 (sobreposição dos 4 clusters nos 4 eixos)
2. **Ficha técnica com medianas** (montar no slide):

| Cluster | n | Mediana Bens | Mediana Despesas | Mediana Idade | Escolaridade | % Mulheres |
|---|---|---|---|---|---|---|
| **🏛️ Estruturados** | 1.153 (52,7%) | R$ 400k | R$ 159k | 49 anos | Superior | 27,6% |
| **⚡ Financiados** | 460 (21,0%) | R$ 0 | R$ 33,6k | 44 anos | Superior | **51,5%** |
| **🌱 Base Simbólica** | 328 (15,0%) | R$ 0 | R$ 0 | 46 anos | Médio | 50,3% |
| **💼 Patr. Sem Campanha** | 248 (11,3%) | R$ 140k | R$ 0 | 55 anos | Médio/Superior | 24,2% |

3. **Heatmap de Z-Score** — seção V3.4 (desvios padronizados de cada cluster)
4. **Heatmap de Ocupações** — seção V3.4 (Top 10 profissões por cluster)

### 💬 Script de fala

> "Definido K=4, precisamos entender **quem são** esses grupos. Nomeamos provisoriamente como Clusters A, B, C e D e analisamos tanto as 4 variáveis quantitativas quanto variáveis categóricas como gênero, raça e profissão.
>
> **Cluster A — Estruturados (1.153 candidatos, 52,7%)**:
> É o maior grupo. Patrimônio mediano de R$ 400 mil, despesas de campanha de R$ 159 mil. Concentra **100% dos deputados** em exercício, advogados, médicos e vereadores. É a **máquina eleitoral institucional** — candidatos que combinam patrimônio pessoal com alto investimento em campanha. 72% homens, 43% brancos.
>
> **Cluster B — Base Simbólica (328 candidatos, 15%)**:
> Patrimônio zero, despesas zero. São candidaturas que existem formalmente mas **não se ativaram financeiramente**. Predominam estudantes, agricultores e profissões de subsistência. 72% negros/pardos, 50% mulheres. O partido DC concentra 4,5x mais candidatos aqui do que a média.
>
> **Cluster C — Financiados (460 candidatos, 21%)**:
> Patrimônio zero, mas com despesas medianas de R$ 33,6 mil. São candidatos **sem recursos próprios que receberam aportes dos partidos**. Destaque: **51,5% são mulheres** — evidência direta do impacto da política de cotas de financiamento feminino. 71% negros/pardos.
>
> **Cluster D — Patrimônio Sem Campanha (248 candidatos, 11,3%)**:
> O inverso dos Financiados: patrimônio mediano de R$ 140 mil, mas despesas **zeradas**. São candidatos com recursos próprios que **não investiram na campanha**. O grupo mais idoso (mediana 55 anos), com **21,5% de advogados** e **30,8% de empresários** — a maior taxa da eleição. 76% homens."

### 🛡️ Se o professor perguntar:
- **"Por que esses nomes?"** → "Cada nome sintetiza a combinação única de patrimônio + despesa que define o cluster. 'Estruturados' = tem tudo; 'Financiados' = não tem bens mas recebe campanha; 'Base Simbólica' = não tem nada (candidatura formal); 'Patrimônio Sem Campanha' = tem bens mas não gasta."
- **"E o gênero?"** → "O dado mais surpreendente é que o Cluster Financiados é o único com maioria feminina (51,5%), sugerindo que as políticas de cota de financiamento para candidatas estão direcionando recursos a mulheres sem patrimônio próprio."
- **"E a raça?"** → "Brancos são super-representados nos Estruturados (43% vs 27% na base geral). Pretos e pardos dominam a Base Simbólica (72%) e os Financiados (71%)."

---

# 🎤 ALUNO 4 — Regras de Associação + Anomalias + Conclusão (~5-7 min)

---

## Slide 5: Regras de Associação — Apriori (~2.5 min)

### 🖼️ O que mostrar (do notebook `03_regras_associacao.ipynb`)
1. **Tabela de variáveis utilizadas** (montar no slide):
   - Categóricas: `SG_PARTIDO`, `DS_GENERO`, `DS_GRAU_INSTRUCAO`, `DS_ESTADO_CIVIL`, `DS_COR_RACA`, `DS_OCUPACAO`
   - Contínuas em quartis: `Faixa_Idade` (4 quartis), `Faixa_Estudo` (4 faixas por grau de instrução), `Faixa_Bens` (quartis zero-aware), `Faixa_Despesa_Contratada` (quartis zero-aware)
   - Alvo: `cluster` (os 4 arquétipos)
2. **Tabela de regras com cluster no consequente** — Cell 19:

| Características → Cluster | Confiança | Lift | n |
|---|---|---|---|
| `Sem Bens + Sem Despesa → Base Simbólica` | **100%** | **6,67** | 308 |
| `Bens Q2 (médio) + Sem Despesa → Patrimônio Sem Campanha` | **100%** | **8,83** | 63 |
| `Bens Q3 (alto) + Sem Despesa → Patrimônio Sem Campanha` | **100%** | **8,83** | 48 |
| `Bens Q3 (alto) + Despesa Q3 (alta) → Estruturados` | **100%** | **1,90** | 282 |
| `Bens Q2 (médio) + Despesa Q3 (alta) → Estruturados` | **100%** | **1,90** | 142 |
| `Sem Bens + Despesa Q3 (alta) → Financiados` | **100%** | **4,76** | 49 |
| `Sem Bens + Despesa Q2 (média) → Financiados` | **100%** | **4,76** | 167 |

3. **Grafo interativo** — print/screenshot do `grafo_regras_cluster.html`
4. **Tabela de regras com cluster no antecedente** — Cell 23:

| Cluster → Característica | Confiança | Lift |
|---|---|---|
| `Estruturados → DS_OCUPACAO=DEPUTADO` | 7,2% | **1,83** |
| `Estruturados → Despesa Q3 (alta)` | 42,9% | **1,73** |
| `Estruturados → Bens Q3 (alto)` | 36,8% | **1,70** |
| `Financiados → Sem Bens` | 98,7% | **2,80** |
| `Financiados → Despesa Q1 (baixa)` | 52,4% | **2,11** |
| `Financiados → DS_GENERO=FEMININO` | 51,5% | **1,37** |
| `Base Simbólica → SG_PARTIDO=DC` | 14,0% | **4,51** |
| `Base Simbólica → Sem Despesa` | 97,3% | **3,82** |
| `Base Simbólica → Sem Bens` | 96,6% | **2,74** |
| `Patrimônio Sem Campanha → Sem Despesa` | 96,0% | **3,77** |
| `Patrimônio Sem Campanha → Bens Q1 (baixo)` | 53,6% | **2,48** |

5. **Grafo de antecedente fixo** — print/screenshot do `grafo_regras_antecedente_fixo.html`

### 💬 Script de fala

> "Na etapa de regras de associação, usamos o algoritmo **Apriori** para verificar se os nomes que demos aos clusters fazem sentido empírico.
>
> As **variáveis contínuas foram transformadas em quartis**: idade em 4 faixas iguais por quartis; escolaridade em 4 faixas baseadas nos graus de instrução reais; e patrimônio e despesas em **quartis zero-aware** — separamos os valores zerados como categoria própria e calculamos quartis sobre os valores positivos, já que 43% dos bens e 26% das despesas são zero.
>
> O Apriori minerou **126 mil regras** a partir de 8.231 itemsets frequentes. Filtramos para analisar as mais relevantes.
>
> **Direção 1: Características → Cluster**
>
> Todas as regras que apontam para os clusters têm **100% de confiança**:
> - Quem tem **sem bens E sem despesas** → 100% Base Simbólica (lift 6,67, 308 candidatos).
> - Quem tem **bens no quartil médio ou alto E sem despesas** → 100% Patrimônio Sem Campanha (lift 8,83 — o maior da base!).
> - Quem tem **bens Q2 ou Q3 E despesas Q3** → 100% Estruturados.
> - Quem tem **sem bens E despesas Q2 ou Q3** → 100% Financiados.
>
> Ou seja: se você me disser quanto um candidato declarou de patrimônio e quanto gastou, eu sei com 100% de certeza em qual cluster ele está.
>
> **Direção 2: Cluster → Características**
>
> Invertendo a análise, cada cluster revela seu DNA sociopolítico:
> - **Estruturados** → associados a Deputados (lift 1,83), partido PP, médicos e vereadores.
> - **Financiados** → associados a Sem Bens (lift 2,80), partido MISSÃO (lift 2,06) e **51,5% mulheres** (lift 1,37).
> - **Base Simbólica** → associados ao partido DC (lift 4,51), sem despesas (lift 3,82), e escolaridade até fundamental (lift 1,93).
> - **Patrimônio Sem Campanha** → associados a sem despesas (lift 3,77), bens Q1 e Q2, homens (76%).
>
> **Conclusão: os nomes confirmam.** As regras de associação validam matematicamente cada arquétipo."

### 🛡️ Se o professor perguntar:
- **"Por que não quartis puros para bens e despesas?"** → "Porque 43% dos candidatos declararam bens = R$ 0 e 26% têm despesas = R$ 0. Se usássemos pd.qcut puro com 4 faixas, os dois primeiros quartis colapsariam em zero, perdendo todo o poder discriminativo. A abordagem zero-aware separa os zeros como categoria semântica e calcula quartis sobre quem de fato possui valores positivos."
- **"O que é lift?"** → "Lift mede quantas vezes mais frequente a regra é em relação ao esperado se as variáveis fossem independentes. Lift = 8,83 significa que a combinação 'bens médios/altos + sem despesas' aparece 8,83 vezes mais frequentemente no Patrimônio Sem Campanha do que seria esperado por chance."
- **"O que significam essas regras na prática?"** → "Que os clusters NÃO são artefatos do algoritmo — são padrões reais. As combinações de atributos socioeconômicos dos candidatos se alinham perfeitamente aos perfis que nomeamos."

---

## Slide 6: Detecção de Anomalias — Isolation Forest (~2 min)

### 🖼️ O que mostrar (do notebook `04_deteccao_anomalias.ipynb`)
1. **Tabela de contaminação testada** — Cell 16:

| Contamination | Atípicos | % |
|---|---|---|
| 0.01 | 22 | 1,0% |
| 0.02 | 44 | 2,0% |
| **0.03** ★ | **66** | **3,0%** |
| 0.05 | 110 | 5,0% |
| auto | 792 | 36,2% |

2. **Tabela de top anomalias globais** — Cell 20 (mostrar 5-8 nomes mais interessantes)
3. **Gráfico 2D de dispersão** com anomalias destacadas — Cell 22
4. **Resumo anomalias por cluster** — Cell 26+:
   - Estruturados: 35 atípicos
   - Financiados: 14 atípicos
   - Base Simbólica: 10 atípicos
   - Patrimônio Sem Campanha: 8 atípicos

### 💬 Script de fala

> "Na última etapa, aplicamos o **Isolation Forest** para detectar candidatos com comportamento atípico. O Isolation Forest constrói árvores de isolamento aleatórias: quanto mais fácil é isolar um ponto do restante, mais anômalo ele é.
>
> **Valor de contaminação: 3% (0.03)**. Testamos de 1% a 8% e o modo 'auto' do scikit-learn. O modo auto sinalizou **36% da base** (792 candidatos!) — totalmente impraticável. Optamos por 3%, que identifica **66 candidatos atípicos** — um volume focado para auditoria individual.
>
> **Anomalias na população completa** — os casos mais extremos:
> - **Nathalia Pedrosa** (PE): 25 anos, Superior Incompleto, **R$ 48,3 milhões em bens** e R$ 0 de despesas. O maior patrimônio de toda a eleição no Nordeste, numa candidata de 25 anos que não gastou nada em campanha.
> - **Tiririca** (CE): candidato que *lê e escreve* (1 ano de estudo), mas com R$ 2,45 milhões em despesas. A anomalia dele é *educacional* — ele aparece no meio da nuvem 3D porque a dimensão que o torna atípico (escolaridade) não tem eixo visual no gráfico tridimensional.
>
> **Anomalias dentro de cada cluster** — candidatos que quebram a lógica do próprio grupo:
> - Nos **Financiados**: candidatos com pequenos bens declarados (R$ 240, R$ 389) quando 98,7% do grupo tem R$ 0. São desvios mínimos em valor absoluto, mas enormes em relação ao padrão do cluster (z-score > 9,0).
> - Na **Base Simbólica**: candidatos que registraram despesas residuais (R$ 48, R$ 100, R$ 390) quando 97% do grupo tem despesa zero.
> - **37 candidatos** são atípicos **somente dentro do seu cluster** — na análise global, passariam despercebidos."

### 🛡️ Se o professor perguntar:
- **"Por que 3% e não 5%?"** → "Com 5% teríamos 110 atípicos — volume alto que dilui o foco. Com 3% capturamos os 66 mais extremos, mantendo a inspeção substantiva e focada."
- **"Por que algumas anomalias aparecem no centro do gráfico 3D?"** → "Porque o Isolation Forest foi treinado em 4 dimensões, mas o gráfico 3D mostra apenas 3 eixos (Idade, Bens, Despesas). A 4ª dimensão — escolaridade — está oculta visualmente. Candidatos cujo isolamento é puramente educacional (como Tiririca, com escolaridade z=-4,1) projetam-se no centro da nuvem 3D. É por isso que adicionamos um tooltip diagnóstico que explica o motivo de cada anomalia."
- **"Qual a diferença entre anomalia global e por cluster?"** → "A global compara contra toda a base de 2.189 candidatos. A por cluster compara contra os pares do mesmo grupo. Um candidato dos Financiados com R$ 240 em bens é 'normal' na população geral, mas é um outlier extremo dentro do seu grupo onde 98,7% tem bens = R$ 0."

---

## Slide 7: Conclusão (~1.5 min)

### 🖼️ O que mostrar
- Slide-resumo com os 4 arquétipos e os achados principais

### 💬 Script de fala

> "Para concluir, nossos principais achados:
>
> **1. Identificamos 4 perfis eleitorais distintos no Nordeste:**
> - Os **Estruturados** (53%) — a máquina eleitoral consolidada com patrimônio e campanha ativa.
> - Os **Financiados** (21%) — candidatos sem patrimônio pessoal que recebem aportes dos partidos.
> - A **Base Simbólica** (15%) — candidaturas formais sem mobilização financeira.
> - O **Patrimônio Sem Campanha** (11%) — candidatos com bens que não investem em campanha.
>
> **2. O que confirmou nossas expectativas:**
> - Que a elite política tem alto patrimônio e alto gasto — os Estruturados.
> - Que muitas candidaturas são apenas formais, para preenchimento de nominata — a Base Simbólica.
>
> **3. O que foi inesperado:**
> - O **Cluster Financiados tem maioria feminina (51,5%)**. Isso é evidência direta de que as cotas de financiamento para candidatas estão redirecionando recursos a mulheres sem patrimônio próprio — uma política pública deixando rastro nos dados.
> - O **Cluster Patrimônio Sem Campanha**: empresários e advogados com bens declarados que não gastaram nada em campanha. Por que se candidatam? É uma pergunta que os dados revelam mas não respondem.
>
> **4. A principal contribuição:**
> As regras de associação com **100% de confiança** em todos os clusters mostram que os perfis não são artefatos do algoritmo — são padrões reais e interpretáveis da dinâmica eleitoral nordestina. E a detecção de anomalias revelou 37 candidatos que só são atípicos dentro do seu grupo — invisíveis na análise global, mas significativos quando comparados aos seus pares.
>
> Obrigado!"

### 🛡️ Se o professor perguntar:
- **"Qual a principal contribuição do trabalho?"** → "Mostrar que a combinação patrimônio × despesas de campanha revela 4 arquétipos eleitorais com perfis sociodemográficos e ocupacionais completamente distintos — e que esses perfis são validáveis por regras de associação com 100% de confiança."
- **"Se fizessem de novo, o que mudariam?"** → "Incluiríamos o resultado da eleição (eleito/não eleito) quando disponível para testar se algum perfil tem vantagem competitiva. Também exploraríamos variáveis como número do candidato na urna e coligações."

---

## 📋 Checklist Final Antes da Apresentação

- [ ] Verificar que todos os gráficos estão renderizados nos notebooks (recarregar abas)
- [ ] Preparar prints/screenshots dos gráficos-chave para os slides
- [ ] Cada aluno lê e ensaia seu bloco pelo menos 2x
- [ ] Testar se os grafos HTML (`grafo_regras_cluster.html` e `grafo_regras_antecedente_fixo.html`) abrem no navegador
- [ ] Preparar para perguntas cruzadas — o professor pode perguntar qualquer parte a qualquer aluno

---

## 📊 Mapa de Imagens Prontas para a Apresentação

Todas as imagens foram salvas em alta resolução (300 DPI) e organizadas por pasta para inserção direta nos slides:

| Slide | Tema / Gráfico | Arquivo Principal | Arquivo na Pasta de Apresentação |
|---|---|---|---|
| **Slide 1** | Síntese de Candidatos por Estado | `images/notebook0/01_candidatos_por_uf_preparados.png` | `images/imagens_apresentacao/slide1_01_candidatos_por_uf.png` |
| **Slide 2** | Grid das 4 Variáveis da Clusterização | `images/notebook1/02_distribuicao_4_drivers_clusterizacao.png` | `images/imagens_apresentacao/slide2_01_distribuicao_4_drivers_grid.png` |
| **Slide 2** | Histograma 1: Idade (Simétrica) | `images/notebook1/hist_01_idade.png` | `images/imagens_apresentacao/slide2_02_hist_idade.png` |
| **Slide 2** | Histograma 2: Grau de Instrução (58% Superior) | `images/notebook1/hist_02_grau_instrucao.png` | `images/imagens_apresentacao/slide2_03_hist_grau_instrucao.png` |
| **Slide 2** | Histograma 3: Bens em Log (43% com R$ 0) | `images/notebook1/hist_03_total_bens_log.png` | `images/imagens_apresentacao/slide2_04_hist_total_bens_log.png` |
| **Slide 2** | Histograma 4: Despesas em Log (26% com R$ 0) | `images/notebook1/hist_04_total_despesas_contratadas_log.png` | `images/imagens_apresentacao/slide2_05_hist_total_despesas_log.png` |
| **Slide 2** | Boxplots de Outliers por Variável | `images/notebook1/03_boxplots_variaveis_numericas.png` | `images/imagens_apresentacao/slide2_06_boxplots_outliers.png` |
| **Slide 2** | Distribuição de Despesas (log) Zoom | `images/notebook1/18_distribuicao_despesas_log.png` | `images/imagens_apresentacao/slide2_07_distribuicao_despesas_log.png` |
| **Slide 3** | Cotovelo, Silhueta, DB e CH ($k=4$) | `images/notebook2/17_v3_metricas_cotovelo_silhouette_db_ch.png` |
| **Slide 3** | Árvore e Queda de Inércia Bisecting | `images/notebook2/18_v3_bisecting_arvore_e_inercia.png` |
| **Slide 3** | Comparação K-Means vs Bisecting | `images/notebook2/19_v3_comparacao_silhouette_kmeans_vs_bisecting.png` |
| **Slide 4** | Radar Polar Multidimensional dos 4 Clusters | `images/notebook2/20_v3_radar_polar_multidimensional.png` |
| **Slide 4** | Top 10 Ocupações por Cluster (Heatmap) | `images/notebook2/24_v3_top10_ocupacoes_heatmap.png` |
| **Slide 4** | Assinatura de Desvio Z-Score | `images/notebook2/25_v3_assinatura_desvio_zscore.png` |
| **Slide 4** | Matriz de Transição V2 → V3 | `images/notebook2/26_v3_matriz_transicao_v2_vs_v3.png` |
| **Slide 5** | Distribuição dos Quartis das 4 Variáveis | `images/notebook3/01_distribuicao_quartis.png` |
| **Slide 5** | Top Regras: Características ➔ Cluster | `images/notebook3/02_top_regras_cluster_consequente.png` |
| **Slide 5** | Top Regras: Cluster ➔ Características (DNA) | `images/notebook3/03_top_regras_cluster_antecedente.png` |
| **Slide 5** | Grafo de Rede Interativo (Cluster) | `images/notebook3/grafo_regras_cluster.html` |
| **Slide 6** | Projeções 2D dos Candidatos Atípicos | `images/notebook4/03_anomalias_globais_2d.png` |
| **Slide 6** | Gráfico 3D das Anomalias (PNG Estático) | `images/notebook4/04_grafico_3d_anomalias_matplotlib.png` |
| **Slide 6** | Gráfico 3D Interativo Global (HTML) | `images/notebook4/04_grafico_3d_anomalias_global.html` |
| **Slide 6** | Gráfico 3D Interativo por Cluster (HTML) | `images/notebook4/05_grafico_3d_anomalias_cluster.html` |
| **Slide 6** | Matriz de Contingência (Global vs Local) | `images/notebook4/06_matriz_contingencia_anomalias.png` |

> 📦 **Pacotes ZIP para Download Direto:**
> - Todas as imagens unificadas: `images/todas_as_imagens.zip` (24,8 MB)
> - Por notebook: `images/notebook0.zip`, `images/notebook1.zip`, `images/notebook2.zip`, `images/notebook3.zip`, `images/notebook4.zip`
