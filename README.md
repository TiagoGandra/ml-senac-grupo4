# Mineração de Dados Eleitorais 2026

Projeto de disciplina: da análise descritiva à detecção de anomalias, usando dados reais e abertos do TSE (Eleições 2026).

## Estrutura do projeto

| Fase | Notebook | O que faz |
|---|---|---|
| 0 | `00_preparacao_dados.ipynb` | Lê os zips do TSE (baixados manualmente para `dados/`), filtra por cargo/UF, limpa e salva um dataset pronto em `dados/` |
| 1 | `01_analise_descritiva.ipynb` | Exploração ampla e sem viés: distribuições, outliers, proporções e dispersão de todas as variáveis relevantes (candidatos e bens) |
| 2 | `02_clusterizacao.ipynb` | K-Means, DBSCAN, hierárquico (hclust) e Bisecting K-Means |
| 3 | `03_regras_associacao.ipynb` | Regras de associação (Apriori) |
| 4 | `04_deteccao_anomalias.ipynb` | Detecção de anomalias |

Cada fase parte do resultado da anterior — todas leem/escrevem em `dados/`, então não é preciso repetir a Fase 0 dentro de cada notebook.

### Cronograma de liberação

- ✅ **Fase 0 e Fase 1** — liberadas.
- ⏳ Fase 2 (clusterização) — em breve.
- ⏳ Fase 3 (regras de associação) — em breve.
- ⏳ Fase 4 (detecção de anomalias) — em breve.

### Professor x alunos

O professor publica a análise **nível Brasil**, cargo **Governador**. Os alunos replicam o mesmo pipeline em **Senador ou Deputado Federal**, recortado pela **UF** do seu trabalho. A única coisa que muda é a célula de configuração no topo da Fase 0:

```python
CARGO = "GOVERNADOR"   # ou "SENADOR", "DEPUTADO FEDERAL"
UF = None                # None = Brasil inteiro; ou a sigla da UF, ex.: "SP", "BA", "PE"
ANO_ELEICAO = 2026
```

## Dados do TSE

O download automático pelo CDN do TSE é bloqueado por um firewall (Akamai) que rejeita requisições que não vêm de um navegador de verdade — acontece tanto no Colab quanto localmente, em qualquer rede, e não é intermitente (tentar de novo não resolve).

Por isso os dois zips oficiais (`consulta_cand_2026.zip` e `bem_candidato_2026.zip`) ficam **versionados dentro de `dados/`** — quem clonar o repositório já recebe tudo, sem precisar baixar nada manualmente. A Fase 0 só confere se os arquivos estão no lugar certo antes de descompactar.

Se precisar atualizar para uma versão mais recente publicada pelo TSE:
1. Baixe pelo navegador:
   - `https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2026.zip`
   - `https://cdn.tse.jus.br/estatistica/sead/odsele/bem_candidato/bem_candidato_2026.zip`
2. Substitua os arquivos em `dados/` (mesmos nomes) e rode a Fase 0 de novo.
3. Confira o `DT_GERACAO`/`HH_GERACAO` que a Fase 0 imprime, e faça o commit do novo zip + do novo `dados/*.csv` juntos — assim quem der `git pull` sabe exatamente qual snapshot está usando.

## Sobre "congelar" a versão dos dados

O arquivo-fonte do TSE pode ser atualizado por eles a qualquer momento (novas candidaturas, correções, impugnações). Para não depender disso:

- Os zips baixados manualmente ficam parados em `dados/` — eles só mudam quando alguém baixar uma versão nova de propósito e sobrescrever.
- O que fica **versionado no repositório** é o resultado da Fase 0 (`dados/*.csv`), não o zip bruto do TSE. Esse CSV é a versão "congelada": todo mundo que der `git pull` usa exatamente os mesmos dados, mesmo que o TSE tenha atualizado o arquivo original depois. Atualizar é sempre um gesto intencional: baixar um zip novo, rodar a Fase 0 de novo e commitar o novo CSV por cima.
- O próprio arquivo do TSE carrega as colunas `DT_GERACAO`/`HH_GERACAO`, com o timestamp de quando eles geraram aquele extrato — a Fase 0 exibe esse valor, então dá pra sempre rastrear qual snapshot está em uso.

## Como rodar

### Google Colab (recomendado para os alunos)

Cada notebook tem um badge **Open in Colab** na primeira célula — é só clicar. Ou use os links diretos:

- [`00_preparacao_dados.ipynb`](https://colab.research.google.com/github/rglopesdf/mineracao-dados-eleitorais-2026/blob/main/00_preparacao_dados.ipynb)
- [`01_analise_descritiva.ipynb`](https://colab.research.google.com/github/rglopesdf/mineracao-dados-eleitorais-2026/blob/main/01_analise_descritiva.ipynb)
- [`02_clusterizacao.ipynb`](https://colab.research.google.com/github/rglopesdf/mineracao-dados-eleitorais-2026/blob/main/02_clusterizacao.ipynb)

> Enquanto o repositório estiver **privado**, esses links pedem login com uma conta GitHub que tenha acesso ao repo. Assim que ele virar público, funcionam pra qualquer aluno sem autenticação nenhuma.

O Colab já vem com quase todas as bibliotecas prontas; se algo faltar (normalmente só `mlxtend`, usado na Fase 3), rode no topo do notebook:

```python
!pip install -q -r requirements.txt
```

### Local, com VS Code

O ambiente virtual não é versionado (está no `.gitignore`) — cada membro cria o seu localmente a partir do `requirements.txt`.

#### 🐧 Linux / macOS

1. **Crie o ambiente virtual na raiz do projeto:**
   ```bash
   python3 -m venv .venv
   ```

2. **Ative o ambiente virtual e instale as dependências:**
   ```bash
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Registre o kernel Jupyter:**
   ```bash
   python -m ipykernel install --user --name=mineracao-eleitoral-2026 --display-name="Python (mineração eleitoral 2026)"
   ```

---

#### 🪟 Windows

1. **Crie o ambiente virtual na raiz do projeto:**
   ```powershell
   python -m venv .venv
   ```

2. **Ative o ambiente virtual e instale as dependências:**
   - No **PowerShell**:
     ```powershell
     # Se receber erro de execução de scripts, execute antes:
     # Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
     .venv\Scripts\Activate.ps1
     pip install -r requirements.txt
     ```
   - No **Prompt de Comando (CMD)**:
     ```cmd
     .venv\Scripts\activate.bat
     pip install -r requirements.txt
     ```

3. **Registre o kernel Jupyter:**
   ```powershell
   python -m ipykernel install --user --name=mineracao-eleitoral-2026 --display-name="Python (mineração eleitoral 2026)"
   ```

---

#### ⚙️ No VS Code

1. Abra a pasta do projeto no VS Code (`Arquivo > Abrir Pasta...` ou pelo terminal com `code .`).
2. Abra qualquer notebook (`.ipynb`).
3. No canto superior direito do notebook, clique no seletor de kernel (**Select Kernel**).
4. Selecione **Python Environments...** apontando para o `.venv` criado (ou em **Jupyter Kernel...** selecione **"Python (mineração eleitoral 2026)"**).

## Fonte dos dados

Portal de dados abertos do TSE — Consulta de Candidatos e Bens de Candidatos, Eleições 2026 (`https://cdn.tse.jus.br/estatistica/sead/odsele/`).
