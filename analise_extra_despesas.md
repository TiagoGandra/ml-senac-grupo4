# Análise Crítica e Metodológica: `extra_despesas.ipynb`

> **Recorte do Estudo:** Candidatos a Deputado Federal no Nordeste — Eleições 2026 (TSE)  
> **Arquivo Analisado:** [`extra_despesas.ipynb`](extra_despesas.ipynb)  
> **Data da Avaliação:** Setembro / 2026  

---

## 1. Veredito Executivo

O notebook **`extra_despesas.ipynb`** é um trabalho de **altíssimo nível técnico, estatístico e analítico**. Ele expande com sucesso o pipeline original do projeto (Fases 0 a 3), incorporando os dados financeiros de prestação de contas eleitorais (despesas pagas e contratadas) como um novo eixo multidimensional.

O projeto não se limitou a aplicar algoritmos de Machine Learning de forma mecânica: houve um cuidado excepcional com a **engenharia de dados relacionais do TSE**, um **rigor matemático exemplar na validação de hiperparâmetros**, a construção de **visualizações customizadas de alto impacto (Radar polar)** e uma **interpretação sociológica e política aprofundada** dos resultados.

---

## 2. Pontos Fortes e Destaques Técnicos

### 2.1. Engenharia e Integração de Dados
- **Resolução do desafio relacional do TSE:** A tabela oficial de despesas pagas (`despesas_pagas_candidatos_2026_{UF}.csv`) não contém diretamente o `SQ_CANDIDATO`, identificando o lançador apenas por `SQ_PRESTADOR_CONTAS`. O notebook constrói um mapeamento relacional 1:1 rigoroso a partir de `despesas_contratadas` e faz a ponte perfeita com a tabela consolidada de candidatos. 
  > *Verificação:* 100% dos 3.296 prestadores de contas com despesas pagas no Nordeste foram mapeados sem perda de integridade referencial.
- **Processamento eficiente em memória:** Os arquivos dos 9 estados nordestinos (`AL`, `BA`, `CE`, `MA`, `PB`, `PE`, `PI`, `RN`, `SE`) são lidos e processados diretamente de dentro do arquivo compactado `dados/prestacao_de_contas_eleitorais_candidatos_2026.zip`, sem necessidade de extração prévia em disco.
- **Preservação de coorte sem viés de sobrevivência:** O uso de `LEFT JOIN` com a base consolidada de candidatos preserva exatamente a totalidade dos **2.189 candidatos a Deputado Federal do Nordeste**, imputando `0.0` para despesas de candidatos sem movimentação financeira registrada (em vez de descartá-los via `INNER JOIN`, o que falsearia a distribuição real da eleição).
- **Tratamento de escala e assimetria:** 
  - Aplicação de `np.log1p` para variáveis financeiras (`Total_Bens` e `Total_Despesas_Pagas`), amortecendo a extrema assimetria positiva e a cauda pesada dos dados eleitorais.
  - Mapeamento intervalar de escolaridade em anos de instrução (`ANOS_ESTUDO`, escala de 0 a 16 anos), tornando a distância euclidiana semanticamente significativa.
  - Normalização Min-Max no intervalo $[0, 1]$ para todos os drivers antes da clusterização.

---

### 2.2. Rigor Matemático e Escolha de $k$ (K-Means 4 Drivers)
A escolha do número de clusters no modelo de 4 variáveis (`IDADE`, `ANOS_ESTUDO`, `Total_Bens_Log`, `Total_Despesas_Log`) foi submetida a um diagnóstico formal em $k \in [2, 8]$ com quatro métricas complementares:

| $k$ | Inércia (WCSS) | Silhouette Score | Davies-Bouldin | Calinski-Harabasz |
| :---: | :---: | :---: | :---: | :---: |
| 2 | 422.77 | 0.412 | 1.094 | 1522.5 |
| 3 | 280.86 | 0.445 | 0.909 | 1697.6 |
| **4** | **205.13** | **0.491 (Pico)** | **0.831 (Mínimo)** | **1817.8 (Pico)** |
| 5 | 179.62 | 0.428 | 0.970 | 1572.1 |
| 6 | 159.69 | 0.387 | 1.082 | 1438.4 |

> **Destaque:** É raro encontrar uma concordância matemática tão categórica em dados reais: **todas as três métricas formais atingem seus pontos ótimos simultaneamente em $k=4$**.

---

### 2.3. Caracterização dos 4 Arquétipos Eleitorais Resultantes

A inclusão das despesas pagas revelou 4 perfis empiricamente consistentes no cenário político do Nordeste:

```
                  [ALTO PATRIMÔNIO]
                         ▲
                         │
      Cluster D          │         Cluster B
(Patrimônio Sem Campanha)│       (Estruturados)
      15,4% da base      │       48,6% da base
                         │
[SEM DESPESAS] ──────────┼──────────► [ALTAS DESPESAS]
                         │
      Cluster A          │         Cluster C
   (Base Simbólica)      │       (Financiados)
      17,4% da base      │       18,6% da base
                         │
                         ▼
                  [BAIXO PATRIMÔNIO]
```

1. **🏛️ Cluster B — Candidatos Estruturados (48,6% / 1.063 candidatos):**
   - Maior escolaridade média (14,6 anos), maior patrimônio declarado (mediana de R$ 380 mil) e despesa média paga massiva de R$ 330 mil (contratada de R$ 496 mil).
   - Representa as máquinas eleitorais estabelecidas e incumbentes.
2. **🚀 Cluster C — Candidaturas Financiadas / Emergentes (18,6% / 407 candidatos):**
   - Patrimônio pessoal mediano de R$ 0,00, porém com despesa média paga expressiva de ~R$ 105 mil (viabilizada pelo Fundo Eleitoral partidário — FEFC).
   - Perfil mais jovem (média 45 anos) e alta representatividade feminina (53,8%).
3. **💼 Cluster D — Patrimônio Declarado Sem Campanha (15,4% / 338 candidatos):**
   - Patrimônio mediano considerável (R$ 155 mil), mas desembolso pago médio irrisório (R$ 6,50).
   - Representa a "elite de papel" ou candidaturas de reserva/apoio que não foram para a disputa real de rua.
4. **🌱 Cluster A — Candidaturas Simbólicas / Base (17,4% / 381 candidatos):**
   - Sem patrimônio pessoal declarado e despesas pagas praticamente nulas (R$ 0,80), com a menor escolaridade média (12 anos).
   - Representa a militância orgânica ou candidatos de composição de chapa/cota.

---

### 2.4. Visualização Multidimensional em Gráficos de Radar
- O notebook constrói manualmente funções em coordenadas polares (`plot_radar`) com fechamento de polígono, eixos percentuais padronizados $[0, 1]$ e preenchimento translúcido.
- A exibição do radar integrado (visão geral dos 4 perfis sobrepostos) combinada com o grid 2x2 individual permite diagnosticar visualmente o "formato" geométrico de cada arquétipo em segundos.

---

### 2.5. A Matriz de Transição (Fase 2 vs. Fase Extra)
Um dos maiores diferenciais analíticos do notebook é a **Seção 8**, onde o modelo de 3 variáveis da Fase 2 (`IDADE`, `ANOS_ESTUDO`, `Total_Bens_Log`) é cruzado diretamente com o novo modelo de 4 variáveis com Despesas Pagas. O cruzamento revelou fenômenos políticos marcantes:
- **Cisão da "Base Popular":** 59,2% permaneceram no Cluster A (sem verba), enquanto 40,8% migraram para o Cluster C (viabilizados por recursos partidários).
- **Cisão dos "Diplomados":** 40,1% ficaram no Cluster A (diplomados sem patrimônio e sem verba), enquanto 59,9% migraram para o Cluster C com campanhas ativas.
- **Desmistificação da "Elite":** 80,6% dos candidatos com patrimônio alto de fato colocaram grande volume financeiro na campanha (Cluster B), mas **19,4% eram "Elite de Papel"** (Cluster D), com bens declarados, mas sem movimentação financeira de campanha.

---

### 2.6. Regras de Associação Socioprofissionais (Apriori + PyVis)
- **Substituição da sigla partidária pela ocupação:** Em vez de repetir partidos políticos, o notebook utilizou a ocupação declarada (`DS_OCUPACAO`), revelando relações socioprofissionais inéditas.
- **Parametrização calibrada:** Suporte mínimo de 1,5% (~33 candidatos), permitindo capturar profissões de alta relevância eleitoral (como `DEPUTADO`, `ADVOGADO`, `EMPRESÁRIO`, `MÉDICO`) que possuem suporte individual menor.
- **Balanceamento de regras por cluster:** Seleção das Top 8 regras de cada um dos 4 clusters individualmente, evitando que o Cluster Estruturados (por ser majoritário e ter maior Lift bruto) monopolizasse toda a saída analítica.
- **Descobertas empíricas fortes:**
  - `DS_OCUPACAO=DEPUTADO → Cluster=Estruturados` com **Confiança = 95,3%** e **Lift = 1.96**.
  - `DS_GENERO=FEMININO + DS_ESTADO_CIVIL=SOLTEIRO(A) → Cluster=Financiados` com **Lift = 1.98**.
- **Grafos interativos com PyVis:** Geração dos arquivos HTML interativos (`grafo_regras_cluster_despesas.html` e `grafo_regras_antecedente_fixo_despesas.html`), permitindo navegação dinâmica pelos nós e arestas.

---

## 3. Pontos de Atenção e Oportunidades de Melhoria

Apesar da excelência geral, existem aspectos técnicos e conceituais que podem ser refinados:

### 3.1. Multicolinearidade no Modelo de 5 Variáveis (Seção 9)
- Na Seção 9, o notebook adiciona `Total_Despesas_Contratadas_Log` ao modelo de 4 variáveis.
- **Problema:** A correlação linear de Pearson entre `Total_Despesas_Pagas_Log` e `Total_Despesas_Contratadas_Log` é extremamente alta: **$r = 0,906$**.
- **Impacto no K-Means:** O K-Means calcula distâncias euclidianas no hiperplano de variáveis. Quando duas variáveis fortemente colineares entram juntas no cálculo, a dimensão "gastos de campanha" passa a ter, na prática, **peso duplicado** em relação à idade, escolaridade e bens.
- **Sugestão de evolução:** Em vez de usar duas somas financeiras em escala log, o 5º eixo ficaria matematicamente mais elegante se representasse uma **métrica de eficiência ou déficit**:
  $$\text{Taxa de Liquidação} = \frac{\text{Despesas Pagas}}{\text{Despesas Contratadas} + 1} \in [0, 1]$$
  ou o **Passivo em Aberto**:
  $$\text{Saldo a Pagar (Log)} = \log_{1p}(\max(0, \text{Contratadas} - \text{Pagas}))$$
  Isso eliminaria a redundância de volume e mediria diretamente a saúde financeira e a capacidade de quitação das campanhas.

### 3.2. Rótulos Arbitrários do K-Means entre Modelos
- No modelo de 4 variáveis:
  - Cluster B = *Estruturados*
  - Cluster C = *Financiados*
  - Cluster D = *Patrimônio Sem Campanha*
  - Cluster A = *Base Simbólica*
- No modelo de 5 variáveis:
  - Cluster A virou *Estruturados* (1.057 candidatos)
  - Cluster B virou *Base Simbólica* (374 candidatos)
- Como os rótulos alfabéticos do K-Means dependem da ordem de convergência dos centróides, ter letras trocadas entre `cluster` (4v) e `cluster_5v` pode gerar confusão para quem consome o CSV gerado. É recomendável priorizar sempre as colunas nominais explícitas (`cluster_4v_nome`).

### 3.3. Salvamento Duplicado do Dataset Consolidado
- Na **Célula 23**, o dataset é salvo em `dados/candidatos_DEPUTADO_FEDERAL_nordeste_2026_com_despesas.csv` (com 64 colunas).
- Na **Célula 39**, o mesmo caminho é sobrescrito com a versão final completa de 69 colunas (`df_merged_final`).
- O resultado em disco está correto e íntegro, mas a exportação da Célula 23 é redundante e pode ser removida ou unificada.

### 3.4. Distribuição Zero-Inflated (Bimodalidade dos Gastos)
- Cerca de **31,61%** dos candidatos possuem exatamente R$ 0,00 em despesas pagas registradas, e uma parcela substancial possui patrimônio declarado igual a R$ 0,00.
- A função $\log_{1p}(0) = 0$ mapeada no `MinMaxScaler` cria uma densa massa pontual no vértice zero. O K-Means separou bem os grupos justamente por conta dessa descontinuidade natural dos dados, mas vale registrar no texto uma breve nota metodológica sobre a natureza *zero-inflated* dos dados eleitorais.

---

## 4. Síntese Comparativa: 4 Variáveis vs. 5 Variáveis

| Dimensão | Modelo 4 Variáveis (Pagas) | Modelo 5 Variáveis (Pagas + Contratadas) |
| :--- | :--- | :--- |
| **Variáveis Utilizadas** | Idade, Anos Estudo, Bens (Log), Desp. Pagas (Log) | Idade, Anos Estudo, Bens (Log), Desp. Pagas (Log), Desp. Contratadas (Log) |
| **Silhouette Score ($k=4$)** | **0.491** | 0.449 |
| **Davies-Bouldin ($k=4$)** | **0.831** | 0.938 |
| **Calinski-Harabasz ($k=4$)** | **1817.8** | 1604.2 |
| **Interpretabilidade** | Máxima (eixos ortogonais e independentes) | Muito boa, porém com redundância entre os eixos financeiros ($r=0.906$) |
| **Recomendação** | **Modelo Principal (Mais Robusto)** | **Modelo Complementar de Diagnóstico de Liquidação** |

---

## 5. Conclusão Final

O notebook `extra_despesas.ipynb` cumpre com distinção todos os requisitos de um estudo de Ciência de Dados e Mineração de Dados no padrão de pós-graduação:
1. **Pergunta de negócio bem delineada e respondida.**
2. **Pipelines de dados defensivos e reprodutíveis.**
3. **Métricas estatísticas objetivas fundamentando as decisões de modelagem.**
4. **Visualizações sofisticadas que traduzem dados em inteligência acionável.**
5. **Insights sociopolíticos de alto valor analítico.**
