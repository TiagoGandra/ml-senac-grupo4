# Mineração de Dados Eleitorais 2026

Projeto de disciplina: da análise descritiva à detecção de anomalias, usando dados reais e abertos do TSE (Eleições 2026).

## Resumo da pesquisa

**Escopo:** candidatos a **Deputado Federal** nos **9 estados do Nordeste** (MA, PI, CE, RN, PB, PE, AL, SE, BA) nas Eleições 2026 — **2.224 candidaturas**, com base no cadastro de candidatos, bens declarados e prestação de contas de campanha do TSE.

**Clusters:** o K-Means (k = 4, validado por Silhouette, Davies-Bouldin e Bisecting K-Means) agrupa os candidatos por 4 variáveis: idade, escolaridade, patrimônio declarado e despesas contratadas de campanha. Os 4 arquétipos encontrados são:

| Cluster | Perfil | Candidatos |
|---|---|---|
| **Estruturados** | patrimônio alto + campanha cara | 1.142 (51,3%) |
| **Financiados** | sem patrimônio, mas com campanha financiada | 453 (20,4%) |
| **Base Simbólica** | patrimônio ≈ 0 e despesas ≈ 0 | 370 (16,6%) |
| **Patrimônio Sem Campanha** | patrimônio relevante, campanha inativa | 259 (11,6%) |

> As letras A–D do K-Means são fixadas **pelo perfil** (A = Base Simbólica, B = Estruturados, C = Financiados, D = Patrimônio Sem Campanha), então não mudam entre execuções.

**Resultado do 1º turno:** com o resultado oficial do TSE (`DS_SIT_TOT_TURNO`), a Fase 5 testa se o cluster se associa a ser eleito. Foram **150 eleitos (6,7%)**. Quase todos os eleitos são **Estruturados** (149 de 150; taxa de eleição de 13,0%), enquanto Financiados (0,2%), Base Simbólica (0%) e Patrimônio Sem Campanha (0%) praticamente não elegem ninguém — ter patrimônio e campanha estruturada andam juntos com ser eleito, mas isso é associação, não causalidade.

## Estrutura do projeto

| Fase | Notebook | O que faz |
|---|---|---|
| 0 | `00_preparacao_dados.ipynb` | Lê os zips do TSE (baixados manualmente para `dados/`), filtra por cargo/UF, limpa e salva um dataset pronto em `dados/` |
| 1 | `01_analise_descritiva.ipynb` | Exploração ampla e sem viés: distribuições, outliers, proporções e dispersão de todas as variáveis relevantes (candidatos e bens) |
| 2 | `02_clusterizacao.ipynb` | K-Means, DBSCAN, hierárquico (hclust) e Bisecting K-Means; batismo dos 4 clusters |
| 3 | `03_regras_associacao.ipynb` | Regras de associação (Apriori) |
| 4 | `04_deteccao_anomalias.ipynb` | Detecção de anomalias |
| 5 | `05_associacao_clusters_resultado.ipynb` | Associação entre clusters e resultado nas urnas |
| Extra | `extra_despesas.ipynb` | Análise de Despesas Eleitorais (Pagas e Contratadas), Clusterização com Radar e Regras Socioprofissionais |
| Consolidado | `candidatos_nordeste_2026.ipynb` | Pipeline completo do Nordeste em um só notebook |

Cada fase parte do resultado da anterior — todas leem/escrevem em `dados/`, então não é preciso repetir a Fase 0 dentro de cada notebook. **Ordem de execução:** 00 → 02 → 03 → 04 → 05 (a Fase 2 grava os clusters no CSV de `dados/`, usado pelas seguintes).

### Professor x alunos

O professor publica a análise **nível Brasil**, cargo **Governador**. Os alunos replicam o mesmo pipeline em **Senador ou Deputado Federal**, recortado pela **UF** do seu trabalho. A única coisa que muda é a célula de configuração no topo da Fase 0:

```python
CARGO = "GOVERNADOR"   # ou "SENADOR", "DEPUTADO FEDERAL"
UF = None                # None = Brasil inteiro; ou a sigla da UF, ex.: "SP", "BA", "PE"
ANO_ELEICAO = 2026
```

## Dados do TSE

O download automático pelo CDN do TSE é bloqueado por um firewall (Akamai) que rejeita requisições que não vêm de um navegador de verdade — acontece tanto no Colab quanto localmente, em qualquer rede, e não é intermitente (tentar de novo não resolve).

Por isso os zips oficiais (`consulta_cand_2026_pos_eleicao.zip`, com o resultado do 1º turno, e `bem_candidato_2026.zip`) ficam **versionados dentro de `dados/`** — quem clonar o repositório já recebe tudo, sem precisar baixar nada manualmente. A Fase 0 só confere se os arquivos estão no lugar certo antes de descompactar.

Se precisar atualizar para uma versão mais recente publicada pelo TSE:
1. Baixe pelo navegador:
   - `https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2026.zip` (salve como `dados/consulta_cand_2026_pos_eleicao.zip` quando for a versão pós-eleição)
   - `https://cdn.tse.jus.br/estatistica/sead/odsele/bem_candidato/bem_candidato_2026.zip`
2. Substitua os arquivos em `dados/` (mesmos nomes) e rode a Fase 0 de novo.
> ⚠️ Use sempre o zip **pós-eleição**: a base antiga (`consulta_cand_2026.zip`, de agosto) não tem resultado e deixa `DS_SIT_TOT_TURNO` todo `#NULO`, o que quebra a Fase 5.

3. Confira o `DT_GERACAO`/`HH_GERACAO` que a Fase 0 imprime, e faça o commit do novo zip + do novo `dados/*.csv` juntos — assim quem der `git pull` sabe exatamente qual snapshot está usando.

### Prestação de Contas Eleitorais (Fase Extra)

Para a análise de despesas eleitorais na **Fase Extra (`extra_despesas.ipynb`)**, é necessária a base de prestação de contas de candidatos. Devido ao limite de tamanho de arquivos do GitHub (>100 MB), o arquivo `dados/prestacao_de_contas_eleitorais_candidatos_2026.zip` **não** é versionado diretamente no Git.

- **Fonte oficial para download:** [Portal de Dados Abertos do TSE — Prestação de Contas Eleitorais 2026](https://dadosabertos.tse.jus.br/dataset/prestacao-de-contas-eleitorais-2026)
- Salve o arquivo baixado como `dados/prestacao_de_contas_eleitorais_candidatos_2026.zip`.

## Sobre "congelar" a versão dos dados

O arquivo-fonte do TSE pode ser atualizado por eles a qualquer momento (novas candidaturas, correções, impugnações). Para não depender disso:

- Os zips baixados manualmente ficam parados em `dados/` — eles só mudam quando alguém baixar uma versão nova de propósito e sobrescrever.
- O que fica **versionado no repositório** é o resultado da Fase 0 (`dados/*.csv`), não o zip bruto do TSE. Esse CSV é a versão "congelada": todo mundo que der `git pull` usa exatamente os mesmos dados, mesmo que o TSE tenha atualizado o arquivo original depois. Atualizar é sempre um gesto intencional: baixar um zip novo, rodar a Fase 0 de novo e commitar o novo CSV por cima.
- O próprio arquivo do TSE carrega as colunas `DT_GERACAO`/`HH_GERACAO`, com o timestamp de quando eles geraram aquele extrato — a Fase 0 exibe esse valor, então dá pra sempre rastrear qual snapshot está em uso.

## Como rodar

### Local, com VS Code

**Pré-requisitos:** Python 3.10+ e a extensão **Jupyter** (e **Python**) instaladas no VS Code. O ambiente virtual não é versionado (está no `.gitignore`) — cada membro cria o seu a partir do `requirements.txt`.

1. **Clone e abra a pasta do projeto** no VS Code (`Arquivo > Abrir Pasta...` ou `code .` no terminal).
2. **Abra o terminal integrado** (`Ctrl+'`) na raiz do projeto e crie o ambiente:

   | | Linux / macOS | Windows (PowerShell) |
   |---|---|---|
   | Criar | `python3 -m venv .venv` | `python -m venv .venv` |
   | Ativar | `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |

   > No Windows, se der erro de execução de scripts: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`. No CMD, use `.venv\Scripts\activate.bat`.

3. **Instale as dependências** (com o ambiente ativado):
   ```bash
   pip install -r requirements.txt
   ```
4. **Selecione o kernel:** abra um notebook (`.ipynb`), clique em **Select Kernel** (canto superior direito) > **Python Environments...** e escolha o `.venv` do projeto. (Opcional: `python -m ipykernel install --user --name=mineracao-eleitoral-2026 --display-name="Python (mineração eleitoral 2026)"` para aparecer em **Jupyter Kernel...**.)
5. **Rode os notebooks na ordem** 00 → 02 → 03 → 04 → 05, com `Run All` em cada um. Os caminhos são relativos à raiz do projeto, então abra sempre a **pasta raiz** no VS Code.

**Dicas:**
- Antes de salvar um notebook que foi alterado fora do VS Code, recarregue-o do disco (`Arquivo > Reverter Arquivo`) para não sobrescrever mudanças.
- Rode a Fase 2 antes da 05: é ela que grava a coluna `cluster` no CSV.
- Para a Fase Extra, baixe a prestação de contas (seção acima).

## Fonte dos dados

Portal de dados abertos do TSE — Consulta de Candidatos e Bens de Candidatos, Eleições 2026 (`https://cdn.tse.jus.br/estatistica/sead/odsele/`).
