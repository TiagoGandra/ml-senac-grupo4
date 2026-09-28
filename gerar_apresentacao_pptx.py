import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Cores do Tema ─────────────────────────────────────────────────────────────
NAVY = RGBColor(26, 54, 93)       # #1a365d - Títulos e cabeçalhos
BLUE = RGBColor(43, 108, 176)     # #2b6cb0 - Acentos e subtítulos
LIGHT_BG = RGBColor(248, 250, 252)# #f8fafc - Fundo dos slides
WHITE = RGBColor(255, 255, 255)
DARK = RGBColor(45, 55, 72)       # #2d3748 - Texto principal
MUTED = RGBColor(113, 128, 150)   # #718096 - Texto secundário
GOLD = RGBColor(214, 158, 46)     # #d69e2e - Destaque ouro
TAG_BG = RGBColor(235, 248, 255)  # #ebf8ff - Fundo da tag
CARD_BG = RGBColor(241, 245, 249) # #f1f5f9 - Fundo dos cards

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def set_slide_background(slide, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_header(slide, title_text, category_text, presenter_tag=None):
    # Top accent bar
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = BLUE
    top_bar.line.fill.background()

    # Category / Breadcrumb
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.25), Inches(8.5), Inches(0.3))
    p_cat = tb_cat.text_frame.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = BLUE

    # Main Title
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(8.5), Inches(0.6))
    p_title = tb_title.text_frame.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY

    # Presenter Tag Badge
    if presenter_tag:
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.8), Inches(0.35), Inches(2.7), Inches(0.55))
        badge.fill.solid()
        badge.fill.fore_color.rgb = TAG_BG
        badge.line.color.rgb = BLUE
        badge.line.width = Pt(1.2)
        tf_b = badge.text_frame
        tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_b = tf_b.paragraphs[0]
        p_b.text = presenter_tag
        p_b.font.size = Pt(11)
        p_b.font.bold = True
        p_b.font.color.rgb = NAVY
        p_b.alignment = PP_ALIGN.CENTER

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=None):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 0: CAPA DA APRESENTAÇÃO
# ═══════════════════════════════════════════════════════════════════════════════
slide0 = prs.slides.add_slide(blank_layout)
set_slide_background(slide0, NAVY)

# Top Gold Accent
bar0 = slide0.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.18))
bar0.fill.solid()
bar0.fill.fore_color.rgb = GOLD
bar0.line.fill.background()

# Tag Institucional
tag_inst = slide0.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(5.2), Inches(0.45))
tag_inst.fill.solid()
tag_inst.fill.fore_color.rgb = RGBColor(38, 77, 133)
tag_inst.line.fill.background()
p_ti = tag_inst.text_frame.paragraphs[0]
p_ti.text = "SENAC • PÓS-GRADUAÇÃO EM CIÊNCIA DE DADOS"
p_ti.font.size = Pt(10)
p_ti.font.bold = True
p_ti.font.color.rgb = RGBColor(226, 232, 240)
p_ti.alignment = PP_ALIGN.CENTER

# Título Principal
tb0_title = slide0.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(1.8))
tf0_title = tb0_title.text_frame
tf0_title.word_wrap = True
p0_1 = tf0_title.paragraphs[0]
p0_1.text = "Mineração de Dados Eleitorais"
p0_1.font.size = Pt(36)
p0_1.font.bold = True
p0_1.font.color.rgb = WHITE

p0_2 = tf0_title.add_paragraph()
p0_2.text = "Perfis e Arquétipos dos Candidatos a Deputado Federal no Nordeste (2026)"
p0_2.font.size = Pt(22)
p0_2.font.color.rgb = RGBColor(190, 227, 248)

# Descrição do Pipeline
tb0_pipe = slide0.shapes.add_textbox(Inches(1.0), Inches(3.8), Inches(11.3), Inches(0.8))
p0_p = tb0_pipe.text_frame.paragraphs[0]
p0_p.text = "Aprendizado Não Supervisionado: Análise Descritiva • Bisecting K-Means • Regras de Associação (Apriori) • Detecção de Anomalias (Isolation Forest)"
p0_p.font.size = Pt(12)
p0_p.font.color.rgb = RGBColor(203, 213, 225)

# Card de Apresentadores
card_autores = slide0.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.8), Inches(11.3), Inches(1.8))
card_autores.fill.solid()
card_autores.fill.fore_color.rgb = RGBColor(20, 42, 73)
card_autores.line.color.rgb = RGBColor(43, 108, 176)
card_autores.line.width = Pt(1)

tf_ca = card_autores.text_frame
tf_ca.margin_left = Inches(0.4)
tf_ca.margin_top = Inches(0.2)
p_ca_t = tf_ca.paragraphs[0]
p_ca_t.text = "EQUIPE DE APRESENTAÇÃO (GRUPO 4):"
p_ca_t.font.size = Pt(11)
p_ca_t.font.bold = True
p_ca_t.font.color.rgb = GOLD

p_ca_1 = tf_ca.add_paragraph()
p_ca_1.text = "• Aluno 1: Contextualização e Análise Descritiva (Slides 1 e 2)           • Aluno 2: Bisecting K-Means e Defesa de K=4 (Slide 3)"
p_ca_1.font.size = Pt(11.5)
p_ca_1.font.color.rgb = WHITE

p_ca_2 = tf_ca.add_paragraph()
p_ca_2.text = "• Aluno 3: Caracterização dos 4 Arquétipos Eleitorais (Slide 4)           • Aluno 4: Apriori, Isolation Forest e Conclusões (Slides 5, 6 e 7)"
p_ca_2.font.size = Pt(11.5)
p_ca_2.font.color.rgb = WHITE


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1: CONTEXTUALIZAÇÃO DO TRABALHO (ALUNO 1)
# ═══════════════════════════════════════════════════════════════════════════════
slide1 = prs.slides.add_slide(blank_layout)
set_slide_background(slide1, LIGHT_BG)
add_header(slide1, "Contexto Eleitoral e Base de Dados do TSE", "1. Contextualização", "🎤 ALUNO 1 (~1.5 min)")

# Coluna da Esquerda (Texto & Cards)
tb1 = slide1.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.6), Inches(4.2))
tf1 = tb1.text_frame
tf1.word_wrap = True

def add_bullet(tf, title, body):
    p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
    p.text = f"• {title}: "
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = NAVY
    run = p.add_run()
    run.text = body
    run.font.bold = False
    run.font.size = Pt(11.5)
    run.font.color.rgb = DARK
    p.space_after = Pt(10)

add_bullet(tf1, "Objetivo Central", "Identificar a estrutura socioeconômica latente dos candidatos a Deputado Federal, testando se a disputa é homogênea ou polarizada em arquétipos eleitorais distintos.")
add_bullet(tf1, "População Analisada", "Universo completo de 2.189 candidaturas a Deputado Federal registradas no Tribunal Superior Eleitoral (TSE) para as Eleições 2026.")
add_bullet(tf1, "Recorte Geográfico", "Os 9 estados da Região Nordeste (AL, BA, CE, MA, PB, PE, PI, RN, SE) — uma região marcada por contrastes sociais e intensa disputa política.")
add_bullet(tf1, "Integração das Bases do TSE", "Cruzamento relacional inédito de 3 bases oficiais via SQ_CANDIDATO: (1) Dados Cadastrais/Demográficos, (2) Declaração de Bens e (3) Prestação de Contas Eleitorais.")

# Card de Defesa no Rodapé
card_def1 = add_card(slide1, Inches(0.8), Inches(5.7), Inches(5.6), Inches(1.2), CARD_BG, BLUE)
tf_d1 = card_def1.text_frame
tf_d1.margin_left = Inches(0.2)
tf_d1.margin_top = Inches(0.12)
p_d1_t = tf_d1.paragraphs[0]
p_d1_t.text = "🛡️ Ponto-Chave de Defesa:"
p_d1_t.font.bold = True
p_d1_t.font.size = Pt(10.5)
p_d1_t.font.color.rgb = BLUE
p_d1_b = tf_d1.add_paragraph()
p_d1_b.text = "Trata-se de Aprendizado Não Supervisionado: o TSE não rotula 'tipos de candidatos'. O pipeline de algoritmos foi desenhado para descobrir esses agrupamentos empiricamente a partir dos dados."
p_d1_b.font.size = Pt(9.5)
p_d1_b.font.color.rgb = DARK

# Imagem na Direita
img1_path = 'images/imagens_apresentacao/slide1_01_candidatos_por_uf.png'
if os.path.exists(img1_path):
    slide1.shapes.add_picture(img1_path, Inches(6.8), Inches(1.4), width=Inches(5.7))


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2: ANÁLISE DESCRITIVA DAS 4 VARIÁVEIS (ALUNO 1)
# ═══════════════════════════════════════════════════════════════════════════════
slide2 = prs.slides.add_slide(blank_layout)
set_slide_background(slide2, LIGHT_BG)
add_header(slide2, "Distribuição das 4 Variáveis da Clusterização", "2. Análise Descritiva", "🎤 ALUNO 1 (~2.5 min)")

# Coluna da Esquerda: Diagnóstico das 4 variáveis
tb2 = slide2.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.7), Inches(4.3))
tf2 = tb2.text_frame
tf2.word_wrap = True

add_bullet(tf2, "Idade (Média: 48,1 | Mediana: 48,0)", "Distribuição perfeitamente simétrica (gaussiana) variando de 21 a 81 anos. Mostra que o cenário político não é dominado por extremos etários.")
add_bullet(tf2, "Escolaridade / Anos de Estudo", "Barreira social explícita: 58,3% dos candidatos possuem Ensino Superior Completo (16 anos de estudo). Apenas 5% pararam no ensino fundamental.")
add_bullet(tf2, "Total de Bens (Média: R$ 1,05M | Mediana: R$ 85k)", "Assimetria extrema: 43% dos candidatos (941) declararam patrimônio ZERO! O topo atinge R$ 48,3 milhões. Exigiu transformação log1p(Bens).")
add_bullet(tf2, "Despesas Contratadas (Média: R$ 442k | Mediana: R$ 35,8k)", "Padrão bimodal (zero-inflated): 26% com despesa ZERO (candidaturas cartoriais de nominata), enquanto a elite atinge o teto legal de R$ 3,3M.")

# Card de Solução Técnica
card_def2 = add_card(slide2, Inches(0.8), Inches(5.8), Inches(5.7), Inches(1.15), CARD_BG, GOLD)
tf_d2 = card_def2.text_frame
tf_d2.margin_left = Inches(0.2)
tf_d2.margin_top = Inches(0.12)
p_d2_t = tf_d2.paragraphs[0]
p_d2_t.text = "⚙️ Solução Metodológica Implementada:"
p_d2_t.font.bold = True
p_d2_t.font.size = Pt(10.5)
p_d2_t.font.color.rgb = GOLD
p_d2_b = tf_d2.add_paragraph()
p_d2_b.text = "Aplicação de log(1 + x) em Bens e Despesas para conter outliers bilionários sem perder os zeros, e mapeamento de instrução para ANOS_ESTUDO (1 a 16 anos) para tratar como escala intervalar contínua."
p_d2_b.font.size = Pt(9.5)
p_d2_b.font.color.rgb = DARK

# Imagem 2x2 Grid dos 4 Drivers
img2_path = 'images/imagens_apresentacao/slide2_01_distribuicao_4_drivers_grid.png'
if os.path.exists(img2_path):
    slide2.shapes.add_picture(img2_path, Inches(6.8), Inches(1.35), width=Inches(5.75))


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3: BISECTING K-MEANS E ESCOLHA DE K=4 (ALUNO 2)
# ═══════════════════════════════════════════════════════════════════════════════
slide3 = prs.slides.add_slide(blank_layout)
set_slide_background(slide3, LIGHT_BG)
add_header(slide3, "Bisecting K-Means e a Defesa Matemática de K=4", "3. Clusterização", "🎤 ALUNO 2 (~4 min)")

# Coluna Esquerda
tb3 = slide3.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.6), Inches(4.3))
tf3 = tb3.text_frame
tf3.word_wrap = True

add_bullet(tf3, "O Algoritmo Bisecting K-Means", "Particionamento hierárquico divisivo (top-down). Começa com todos os 2.189 candidatos em 1 grupo e bissecta sucessivamente o cluster de maior inércia interna.")
add_bullet(tf3, "Pico Absoluto de Silhueta (0,488)", "K=4 alcança o máximo global de qualidade de separação entre clusters. K=3 (0,380) e K=5 (0,435) apresentam degradação geométrica acentuada.")
add_bullet(tf3, "Mínimo de Davies-Bouldin (0,844)", "K=4 atinge a menor sobreposição e maior compacidade entre grupos (menor é melhor; K=2 é 1,219 e K=3 é 1,048).")
add_bullet(tf3, "Pico de Calinski-Harabasz (2.429)", "Máxima razão de variância inter/intra cluster obtida na partição quádrupla.")
add_bullet(tf3, "Convergência K-Means vs Bisecting", "Convergência estrutural perfeita em K=4: 1.155, 461, 326, 247 vs 1.153, 460, 328, 248. Diferença de apenas 2 candidatos em grupos de mais de mil!")

# Card de Defesa
card_def3 = add_card(slide3, Inches(0.8), Inches(5.8), Inches(5.6), Inches(1.15), CARD_BG, BLUE)
tf_d3 = card_def3.text_frame
tf_d3.margin_left = Inches(0.2)
tf_d3.margin_top = Inches(0.12)
p_d3_t = tf_d3.paragraphs[0]
p_d3_t.text = "🛡️ Resposta Rápida para a Banca:"
p_d3_t.font.bold = True
p_d3_t.font.size = Pt(10.5)
p_d3_t.font.color.rgb = BLUE
p_d3_b = tf_d3.add_paragraph()
p_d3_b.text = "Por que não K=3? Porque K=3 funde ricos sem campanha com quem não tem nada. Por que não K=5? Porque K=5 apenas fragmenta os Estruturados sem ganho algum de silhueta. K=4 é o ótimo estatístico e sociológico."
p_d3_b.font.size = Pt(9.5)
p_d3_b.font.color.rgb = DARK

# Imagem Métricas Formais
img3_path = 'images/imagens_apresentacao/slide3_01_cotovelo_silhouette_db_ch.png'
if os.path.exists(img3_path):
    slide3.shapes.add_picture(img3_path, Inches(6.8), Inches(1.35), width=Inches(5.75))


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4: CARACTERIZAÇÃO DOS 4 ARQUÉTIPOS (ALUNO 3)
# ═══════════════════════════════════════════════════════════════════════════════
slide4 = prs.slides.add_slide(blank_layout)
set_slide_background(slide4, LIGHT_BG)
add_header(slide4, "Caracterização e Batismo dos 4 Arquétipos Eleitorais", "4. Perfis dos Clusters", "🎤 ALUNO 3 (~4 min)")

# Coluna Esquerda: Descrição dos 4 Nomes
tb4 = slide4.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.7), Inches(4.3))
tf4 = tb4.text_frame
tf4.word_wrap = True

add_bullet(tf4, "🏛️ Estruturados (52,7% | 1.153 cand.)", "Bens R$ 400k, Despesas R$ 159k. Máquina política de alta renda: 100% dos Deputados em exercício, médicos, vereadores e empresários. 72% homens, 43% brancos.")
add_bullet(tf4, "⚡ Financiados (21,0% | 460 cand.)", "Bens ZERO, Despesas R$ 33,6k (média R$ 122k). Único grupo com MAIORIA FEMININA (51,5%)! Prova direta das cotas de financiamento do Fundo Eleitoral feminino.")
add_bullet(tf4, "🌱 Base Simbólica (15,0% | 328 cand.)", "Bens ZERO, Despesas ZERO. Candidaturas cartoriais de nominata. Estudantes (18,4%), agricultores, pequenos comerciantes. 72% negros/pardos. 0% deputados.")
add_bullet(tf4, "💼 Patrimônio Sem Campanha (11,3% | 248 cand.)", "Bens R$ 140k (média R$ 819k), Despesas ZERO. Mais velhos (55 anos), 76% homens. Mais da metade (52,3%) são ADVOGADOS ou EMPRESÁRIOS que não gastaram.")

# Card de Evolução V2 -> V3
card_def4 = add_card(slide4, Inches(0.8), Inches(5.8), Inches(5.7), Inches(1.15), CARD_BG, GOLD)
tf_d4 = card_def4.text_frame
tf_d4.margin_left = Inches(0.2)
tf_d4.margin_top = Inches(0.12)
p_d4_t = tf_d4.paragraphs[0]
p_d4_t.text = "🔄 O que a Matriz de Transição V2 ➔ V3 revelou?"
p_d4_t.font.bold = True
p_d4_t.font.size = Pt(10.5)
p_d4_t.font.color.rgb = GOLD
p_d4_b = tf_d4.add_paragraph()
p_d4_b.text = "Sem despesas, ricos e pobres eram blocos únicos. Com despesas, quem não tinha bens se dividiu entre Financiados e Base Simbólica, e ricos se dividiram entre campanha ativa e inativa."
p_d4_b.font.size = Pt(9.5)
p_d4_b.font.color.rgb = DARK

# Imagem Radar Polar 4D
img4_path = 'images/imagens_apresentacao/slide4_01_radar_polar_4_arquetipos.png'
if os.path.exists(img4_path):
    slide4.shapes.add_picture(img4_path, Inches(6.8), Inches(1.35), width=Inches(5.75))


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5: REGRAS DE ASSOCIAÇÃO - APRIORI (ALUNO 4)
# ═══════════════════════════════════════════════════════════════════════════════
slide5 = prs.slides.add_slide(blank_layout)
set_slide_background(slide5, LIGHT_BG)
add_header(slide5, "Regras de Associação Apriori: Validação dos Nomes", "5. Regras de Associação", "🎤 ALUNO 4 (~2.5 min)")

# Coluna Esquerda
tb5 = slide5.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.7), Inches(4.3))
tf5 = tb5.text_frame
tf5.word_wrap = True

add_bullet(tf5, "Discretização em Quartis", "Idade (4 quartis puros), Estudo (4 faixas por instrução) e Quartis Zero-Aware em Bens e Despesas (zeros separados como classe própria antes dos quartis positivos).")
add_bullet(tf5, "Direção 1: Características ➔ Cluster", "Confiança de 100% em todos os arquétipos:\n• Sem Bens + Sem Despesa ➔ Base Simbólica (Lift 6,67 | n=308)\n• Bens Q2/Q3 + Sem Despesa ➔ Patr. Sem Campanha (Lift 8,83)\n• Sem Bens + Despesa Q2/Q3 ➔ Financiados (Lift 4,76)\n• Bens Q2/Q3 + Despesa Q3 ➔ Estruturados (Lift 1,90)")
add_bullet(tf5, "Direção 2: Cluster ➔ Características (O DNA)", "Estruturados ➔ Deputados (lift 1,83) e PT/PP | Financiados ➔ Sem Bens (lift 2,80) e Mulheres (lift 1,37) | Base Simbólica ➔ DC (lift 4,51).")

# Card Conclusão Apriori
card_def5 = add_card(slide5, Inches(0.8), Inches(5.8), Inches(5.7), Inches(1.15), CARD_BG, BLUE)
tf_d5 = card_def5.text_frame
tf_d5.margin_left = Inches(0.2)
tf_d5.margin_top = Inches(0.12)
p_d5_t = tf_d5.paragraphs[0]
p_d5_t.text = "🎯 Resposta Central: Os Nomes Fazem Sentido?"
p_d5_t.font.bold = True
p_d5_t.font.size = Pt(10.5)
p_d5_t.font.color.rgb = BLUE
p_d5_b = tf_d5.add_paragraph()
p_d5_b.text = "SIM, com 100% de confiança matemática. Se você me der o patrimônio e a despesa do candidato, sabemos com certeza absoluta em qual cluster ele cai. Os clusters NÃO são artefatos do algoritmo."
p_d5_b.font.size = Pt(9.5)
p_d5_b.font.color.rgb = DARK

# Imagem Regras Consequente
img5_path = 'images/imagens_apresentacao/slide5_02_regras_cluster_consequente.png'
if os.path.exists(img5_path):
    slide5.shapes.add_picture(img5_path, Inches(6.8), Inches(1.35), width=Inches(5.75))


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6: DETECÇÃO DE ANOMALIAS - ISOLATION FOREST (ALUNO 4)
# ═══════════════════════════════════════════════════════════════════════════════
slide6 = prs.slides.add_slide(blank_layout)
set_slide_background(slide6, LIGHT_BG)
add_header(slide6, "Isolation Forest: Anomalias Globais e Locais", "6. Detecção de Anomalias", "🎤 ALUNO 4 (~2 min)")

# Coluna Esquerda
tb6 = slide6.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.7), Inches(4.3))
tf6 = tb6.text_frame
tf6.word_wrap = True

add_bullet(tf6, "Justificativa da Contaminação = 3%", "Testamos de 1% a 8% e o modo auto. O modo auto sinalizou 36,2% (792 candidatos!) — excessivo. Fixamos 3% (66 casos atípicos) para inspeção individual substantiva.")
add_bullet(tf6, "Anomalias Globais Notórias", "• Nathalia Pedrosa (PE): 25 anos, R$ 48,3M em bens (o maior da eleição) e R$ 0 gastos.\n• Tiririca (CE): 'Lê e Escreve' (1 ano de estudo, z=-4,1) com R$ 2,45M em despesas.")
add_bullet(tf6, "Por que há pontos 'no meio' no gráfico 3D?", "O modelo operou em 4 dimensões! A 4ª dimensão (escolaridade) não tem eixo no gráfico 3D. Tiririca é perfeitamente normal em dinheiro e idade, mas extremo em escolaridade.")
add_bullet(tf6, "Anomalias Locais (Cluster): 37 Casos Invisíveis", "Candidatos atípicos apenas em relação aos seus pares de grupo (ex: Financiados com pequenos bens declarados quando 98,7% do grupo é zero).")

# Card Defesa Anomalias
card_def6 = add_card(slide6, Inches(0.8), Inches(5.8), Inches(5.7), Inches(1.15), CARD_BG, GOLD)
tf_d6 = card_def6.text_frame
tf_d6.margin_left = Inches(0.2)
tf_d6.margin_top = Inches(0.12)
p_d6_t = tf_d6.paragraphs[0]
p_d6_t.text = "💡 A Força da Análise em 2 Níveis:"
p_d6_t.font.bold = True
p_d6_t.font.size = Pt(10.5)
p_d6_t.font.color.rgb = GOLD
p_d6_b = tf_d6.add_paragraph()
p_d6_b.text = "A detecção global isola discrepâncias macroeconômicas. A detecção local por cluster revela 37 candidatos que passariam completamente despercebidos na análise da base inteira."
p_d6_b.font.size = Pt(9.5)
p_d6_b.font.color.rgb = DARK

# Imagem 3D Matplotlib
img6_path = 'images/imagens_apresentacao/slide6_02_grafico_3d_anomalias_png.png'
if os.path.exists(img6_path):
    slide6.shapes.add_picture(img6_path, Inches(6.8), Inches(1.35), width=Inches(5.75))


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7: CONCLUSÕES E APRENDIZADOS DOS DADOS (ALUNO 4)
# ═══════════════════════════════════════════════════════════════════════════════
slide7 = prs.slides.add_slide(blank_layout)
set_slide_background(slide7, LIGHT_BG)
add_header(slide7, "Síntese dos Achados e Contribuições do Estudo", "7. Conclusões", "🎤 ALUNO 4 (~1.5 min)")

# Coluna Esquerda: O que confirmou vs O que surpreendeu
card_c1 = add_card(slide7, Inches(0.8), Inches(1.4), Inches(5.6), Inches(2.6), WHITE, BLUE)
tf_c1 = card_c1.text_frame
tf_c1.margin_left = Inches(0.25)
tf_c1.margin_top = Inches(0.15)
p_c1_h = tf_c1.paragraphs[0]
p_c1_h.text = "✅ O QUE CONFIRMOU EXPECTATIVAS:"
p_c1_h.font.bold = True
p_c1_h.font.size = Pt(11)
p_c1_h.font.color.rgb = BLUE
p_c1_1 = tf_c1.add_paragraph()
p_c1_1.text = "• A hegemonia da máquina eleitoral: Estruturados combinam alto patrimônio pessoal com alto investimento partidário (100% dos deputados).\n• A existência de candidaturas de fachada/legenda: Base Simbólica reúne 15% dos concorrentes com zero bens e zero despesas."
p_c1_1.font.size = Pt(10.5)
p_c1_1.font.color.rgb = DARK

card_c2 = add_card(slide7, Inches(0.8), Inches(4.2), Inches(5.6), Inches(2.8), WHITE, GOLD)
tf_c2 = card_c2.text_frame
tf_c2.margin_left = Inches(0.25)
tf_c2.margin_top = Inches(0.15)
p_c2_h = tf_c2.paragraphs[0]
p_c2_h.text = "⚡ O QUE FOI INESPERADO / NOVO:"
p_c2_h.font.bold = True
p_c2_h.font.size = Pt(11)
p_c2_h.font.color.rgb = GOLD
p_c2_1 = tf_c2.add_paragraph()
p_c2_1.text = "• Maioria feminina no Cluster Financiados (51,5%): Efeito empírico comprovado das cotas de financiamento para mulheres sem capital próprio.\n• O arquétipo Patrimônio Sem Campanha (11,3%): 52% são advogados e empresários abastados que registram candidatura mas não investem.\n• 37 anomalias exclusivamente locais capturadas pelo Isolation Forest."
p_c2_1.font.size = Pt(10.5)
p_c2_1.font.color.rgb = DARK

# Coluna Direita: Contribuição Geral
card_c3 = add_card(slide7, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.6), NAVY)
tf_c3 = card_c3.text_frame
tf_c3.margin_left = Inches(0.4)
tf_c3.margin_top = Inches(0.4)
p_c3_t = tf_c3.paragraphs[0]
p_c3_t.text = "A PRINCIPAL CONTRIBUIÇÃO:"
p_c3_t.font.bold = True
p_c3_t.font.size = Pt(14)
p_c3_t.font.color.rgb = GOLD

p_c3_b1 = tf_c3.add_paragraph()
p_c3_b1.text = "\nO estudo demonstrou que a disputa eleitoral para Deputado Federal no Nordeste NÃO se resume a 'ricos contra pobres'."
p_c3_b1.font.size = Pt(12.5)
p_c3_b1.font.color.rgb = WHITE

p_c3_b2 = tf_c3.add_paragraph()
p_c3_b2.text = "\nAo cruzar Patrimônio Pessoal com Despesas Contratadas, o Aprendizado Não Supervisionado revelou 4 engrenagens políticas perfeitamente delimitadas."
p_c3_b2.font.size = Pt(12)
p_c3_b2.font.color.rgb = RGBColor(226, 232, 240)

p_c3_b3 = tf_c3.add_paragraph()
p_c3_b3.text = "\nAs regras Apriori com 100% de confiança provam que os clusters são reais e matematicamente determinísticos."
p_c3_b3.font.size = Pt(12)
p_c3_b3.font.color.rgb = RGBColor(190, 227, 248)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8: ENCERRAMENTO E BANCA AVALIADORA
# ═══════════════════════════════════════════════════════════════════════════════
slide8 = prs.slides.add_slide(blank_layout)
set_slide_background(slide8, NAVY)

bar8 = slide8.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.18))
bar8.fill.solid()
bar8.fill.fore_color.rgb = GOLD
bar8.line.fill.background()

tb8 = slide8.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.3), Inches(3.0))
tf8 = tb8.text_frame
tf8.vertical_anchor = MSO_ANCHOR.MIDDLE

p8_1 = tf8.paragraphs[0]
p8_1.text = "Obrigado pela Atenção!"
p8_1.font.size = Pt(40)
p8_1.font.bold = True
p8_1.font.color.rgb = WHITE
p8_1.alignment = PP_ALIGN.CENTER

p8_2 = tf8.add_paragraph()
p8_2.text = "Mineração de Dados Eleitorais • Grupo 4 (Nordeste 2026)"
p8_2.font.size = Pt(18)
p8_2.font.color.rgb = GOLD
p8_2.alignment = PP_ALIGN.CENTER

p8_3 = tf8.add_paragraph()
p8_3.text = "\nEstamos à disposição da banca examinadora para perguntas e discussões."
p8_3.font.size = Pt(15)
p8_3.font.color.rgb = RGBColor(203, 213, 225)
p8_3.alignment = PP_ALIGN.CENTER

output_pptx = 'apresentacao_trabalho.pptx'
prs.save(output_pptx)
size_mb = os.path.getsize(output_pptx) / (1024 * 1024)
print(f"🎉 Apresentação salva com sucesso: {output_pptx} ({size_mb:.2f} MB)")
