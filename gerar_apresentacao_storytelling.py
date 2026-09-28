import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Cores do Tema Storytelling Executivo ───────────────────────────────────────
NAVY = RGBColor(20, 42, 74)         # #142a4a - Azul Escuro Nobre (Títulos)
BLUE_ACCENT = RGBColor(37, 99, 235) # #2563eb - Azul Royal Vibrante
GOLD = RGBColor(217, 119, 6)        # #d97706 - Ouro Âmbar de Destaque
LIGHT_BG = RGBColor(248, 250, 252)  # #f8fafc - Fundo Clean Off-White
WHITE = RGBColor(255, 255, 255)
DARK_TEXT = RGBColor(30, 41, 59)    # #1e293b - Texto Principal Escuro
MUTED_TEXT = RGBColor(100, 116, 139)# #64748b - Texto Secundário
CARD_BG = RGBColor(255, 255, 255)   # Branco puro para cards em cima do light_bg
BORDER_COLOR = RGBColor(226, 232, 240)

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

def add_story_header(slide, category_text, headline_text):
    # Top accent line
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = BLUE_ACCENT
    top_bar.line.fill.background()

    # Category / Breadcrumb
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.28), Inches(11.5), Inches(0.3))
    p_cat = tb_cat.text_frame.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = BLUE_ACCENT

    # Main Storytelling Headline
    tb_head = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.8), Inches(0.75))
    tf_h = tb_head.text_frame
    tf_h.word_wrap = True
    p_head = tf_h.paragraphs[0]
    p_head.text = headline_text
    p_head.font.size = Pt(21)
    p_head.font.bold = True
    p_head.font.color.rgb = NAVY

def add_card_box(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COLOR):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
    else:
        card.line.fill.background()
    return card

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 0: CAPA DA APRESENTAÇÃO
# ═══════════════════════════════════════════════════════════════════════════════
slide0 = prs.slides.add_slide(blank_layout)
set_slide_background(slide0, NAVY)

bar0 = slide0.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.15))
bar0.fill.solid()
bar0.fill.fore_color.rgb = GOLD
bar0.line.fill.background()

tag_inst = slide0.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(4.8), Inches(0.45))
tag_inst.fill.solid()
tag_inst.fill.fore_color.rgb = RGBColor(30, 58, 102)
tag_inst.line.fill.background()
p_ti = tag_inst.text_frame.paragraphs[0]
p_ti.text = "SENAC • PÓS-GRADUAÇÃO EM CIÊNCIA DE DADOS"
p_ti.font.size = Pt(10)
p_ti.font.bold = True
p_ti.font.color.rgb = RGBColor(226, 232, 240)
p_ti.alignment = PP_ALIGN.CENTER

tb0_title = slide0.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(11.3), Inches(2.2))
tf0_title = tb0_title.text_frame
tf0_title.word_wrap = True

p0_1 = tf0_title.paragraphs[0]
p0_1.text = "Anatomia de uma Eleição Federal"
p0_1.font.size = Pt(38)
p0_1.font.bold = True
p0_1.font.color.rgb = WHITE

p0_2 = tf0_title.add_paragraph()
p0_2.text = "O que os dados do TSE revelam sobre patrimônio, poder e o impacto das cotas no Nordeste"
p0_2.font.size = Pt(22)
p0_2.font.color.rgb = RGBColor(191, 219, 254)

tb0_pipe = slide0.shapes.add_textbox(Inches(1.0), Inches(4.2), Inches(11.3), Inches(0.6))
p0_p = tb0_pipe.text_frame.paragraphs[0]
p0_p.text = "Estudo Descritivo e Não Supervisionado: Análise Exploratória • Bisecting K-Means • Regras de Associação • Detecção de Anomalias"
p0_p.font.size = Pt(12)
p0_p.font.color.rgb = RGBColor(203, 213, 225)

card_autores = slide0.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.9), Inches(11.3), Inches(1.8))
card_autores.fill.solid()
card_autores.fill.fore_color.rgb = RGBColor(15, 32, 57)
card_autores.line.color.rgb = RGBColor(59, 130, 246)
card_autores.line.width = Pt(1)

tf_ca = card_autores.text_frame
tf_ca.margin_left = Inches(0.4)
tf_ca.margin_top = Inches(0.25)
p_ca_t = tf_ca.paragraphs[0]
p_ca_t.text = "PROJETO APLICADO DE MINERAÇÃO DE DADOS — GRUPO 4"
p_ca_t.font.size = Pt(11)
p_ca_t.font.bold = True
p_ca_t.font.color.rgb = GOLD

p_ca_1 = tf_ca.add_paragraph()
p_ca_1.text = "Integrantes: Aluno 1 • Aluno 2 • Aluno 3 • Aluno 4"
p_ca_1.font.size = Pt(13)
p_ca_1.font.bold = True
p_ca_1.font.color.rgb = WHITE

p_ca_2 = tf_ca.add_paragraph()
p_ca_2.text = "Candidatos a Deputado Federal nos 9 Estados do Nordeste (Eleições 2026)"
p_ca_2.font.size = Pt(11.5)
p_ca_2.font.color.rgb = RGBColor(203, 213, 225)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1: O CENÁRIO DA DISPUTA
# ═══════════════════════════════════════════════════════════════════════════════
slide1 = prs.slides.add_slide(blank_layout)
set_slide_background(slide1, LIGHT_BG)
add_story_header(slide1, "1. O Ponto de Partida", "O Cenário da Disputa: Quem Busca Representar o Nordeste em Brasília?")

card1 = add_card_box(slide1, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.5))
tf1 = card1.text_frame
tf1.margin_left = Inches(0.35)
tf1.margin_right = Inches(0.35)
tf1.margin_top = Inches(0.35)
tf1.word_wrap = True

def add_narrative_point(tf, title, body, space_after=14):
    p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
    p.text = f"{title}\n"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = NAVY
    run = p.add_run()
    run.text = body
    run.font.bold = False
    run.font.size = Pt(11)
    run.font.color.rgb = DARK_TEXT
    p.space_after = Pt(space_after)

add_narrative_point(tf1, "🎯 A Pergunta Central de Negócio", 
                    "Em uma disputa pelas vagas de Deputado Federal, os concorrentes partem de condições de disputa homogêneas ou existem abismos estruturais de recursos pré-determinando a viabilidade eleitoral?")

add_narrative_point(tf1, "👥 A População sob Observação", 
                    "O universo completo de 2.189 candidatos distribuídos pelos 9 estados do Nordeste — uma região marcada por grande densidade populacional e fortes clivagens socioeconômicas.")

add_narrative_point(tf1, "🔗 A Integração Tridimensional dos Dados", 
                    "Cruzamos três dimensões da vida pública registradas no TSE: quem o candidato é (perfil cadastral), quanto ele possui acumulado (declaração de bens) e quanta energia financeira ele colocou em movimento (prestação de contas).")

add_narrative_point(tf1, "💡 A Abordagem por Descoberta", 
                    "Como o TSE não rotula candidatos por categorias, utilizamos Aprendizado Não Supervisionado para que os padrões latentes emergissem diretamente da geometria das variáveis.", space_after=0)

img1_path = 'images/imagens_apresentacao/slide1_01_candidatos_por_uf.png'
if os.path.exists(img1_path):
    slide1.shapes.add_picture(img1_path, Inches(6.8), Inches(1.4), width=Inches(5.7))


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2: O RETRATO DESCRITIVO
# ═══════════════════════════════════════════════════════════════════════════════
slide2 = prs.slides.add_slide(blank_layout)
set_slide_background(slide2, LIGHT_BG)
add_story_header(slide2, "2. A Realidade dos Candidatos", "O Abismo Inicial: Elitização Escolar, Patrimônio Concentrado e Campanhas Silenciosas")

card2 = add_card_box(slide2, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5))
tf2 = card2.text_frame
tf2.margin_left = Inches(0.35)
tf2.margin_right = Inches(0.35)
tf2.margin_top = Inches(0.35)
tf2.word_wrap = True

add_narrative_point(tf2, "🎓 Barreira Educacional Elitizada", 
                    "58,3% dos concorrentes possuem Ensino Superior Completo. Uma barreira invisível de entrada que não reflete a escolaridade da população geral do Nordeste.")

add_narrative_point(tf2, "💰 O Abismo Patrimonial (43% de Zeros)", 
                    "43% dos candidatos não declararam um único centavo em bens (R$ 0). A mediana geral é de apenas R$ 85 mil, mas a média chega a R$ 1,05 milhão — impulsionada por milionários no topo da pirâmide.")

add_narrative_point(tf2, "🔇 Campanhas Silenciosas (26% de Zeros)", 
                    "Mais de um quarto dos postulantes (26%) registraram R$ 0 em despesas contratadas. São candidaturas de preenchimento formal de chapa, sem mobilização real de campanha.")

add_narrative_point(tf2, "⚖️ O Equilíbrio da Maturidade", 
                    "A idade média e mediana é de 48 anos com distribuição simétrica: o cenário da disputa federal é dominado pela maturidade profissional, sem polarização por jovens ou idosos.", space_after=0)

img2_path = 'images/imagens_apresentacao/slide2_01_distribuicao_4_drivers_grid.png'
if os.path.exists(img2_path):
    slide2.shapes.add_picture(img2_path, Inches(6.7), Inches(1.4), width=Inches(5.8))


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3: A ESTRUTURA DOS DADOS
# ═══════════════════════════════════════════════════════════════════════════════
slide3 = prs.slides.add_slide(blank_layout)
set_slide_background(slide3, LIGHT_BG)
add_story_header(slide3, "3. A Descoberta dos Grupos", "A Divisão Natural: A Geometria dos Dados Aponta com Clareza para 4 Perfis")

card3 = add_card_box(slide3, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5))
tf3 = card3.text_frame
tf3.margin_left = Inches(0.35)
tf3.margin_right = Inches(0.35)
tf3.margin_top = Inches(0.35)
tf3.word_wrap = True

add_narrative_point(tf3, "🌲 O Caminho Divisivo (Bisecting K-Means)", 
                    "Em vez de forçar cortes simultâneos, partimos de todos os 2.189 candidatos em um único bloco e bissectamos sucessivamente os grupos mais dispersos até encontrar o equilíbrio geométrico.")

add_narrative_point(tf3, "📊 O Consenso das Métricas em K=4", 
                    "Avaliamos de 2 a 8 grupos. K=4 atinge o pico global de Silhueta (0,488) e o mínimo de Davies-Bouldin (0,844), além de uma inflexão nítida no método do cotovelo.")

add_narrative_point(tf3, "🤝 Uma Verdade Intrínseca dos Dados", 
                    "Dois algoritmos com filosofias totalmente distintas — K-Means tradicional e Bisecting K-Means — convergiram exatamente para os mesmos grupos (diferença de apenas 2 candidatos em grupos de mais de mil!).")

add_narrative_point(tf3, "💡 A Lógica Revelada", 
                    "A política não se divide apenas em 'ricos e pobres'. A dinâmica real nasce do cruzamento entre capital próprio e capital de campanha em movimento.", space_after=0)

img3_path = 'images/imagens_apresentacao/slide3_01_cotovelo_silhouette_db_ch.png'
if os.path.exists(img3_path):
    slide3.shapes.add_picture(img3_path, Inches(6.7), Inches(1.4), width=Inches(5.8))


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4: OS 4 ARQUÉTIPOS ELEITORAIS (NOVO RADAR 2x2 QUADRANTES)
# ═══════════════════════════════════════════════════════════════════════════════
slide4 = prs.slides.add_slide(blank_layout)
set_slide_background(slide4, LIGHT_BG)
add_story_header(slide4, "4. Os Perfis Revelados", "Os 4 Arquétipos Eleitorais: Da Máquina Pesada ao Impacto Real das Cotas Femininas")

card4 = add_card_box(slide4, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5))
tf4 = card4.text_frame
tf4.margin_left = Inches(0.35)
tf4.margin_right = Inches(0.35)
tf4.margin_top = Inches(0.3)
tf4.word_wrap = True

add_narrative_point(tf4, "🏛️ Estruturados (52,7% da base | 1.153 cand.)", 
                    "A máquina eleitoral competitiva: mediana de R$ 400k em bens e R$ 159k em gastos. Reúne 100% dos Deputados Federais em exercício que tentam reeleição, além de médicos e empresários (72% homens).", space_after=11)

add_narrative_point(tf4, "⚡ Financiados (21,0% da base | 460 cand.)", 
                    "O achado social mais marcante da análise: ÚNICO grupo com MAIORIA FEMININA (51,5%)! Candidatas sem bens acumulados que ganharam viabilidade graças às cotas públicas de repasse do Fundo Eleitoral.", space_after=11)

add_narrative_point(tf4, "🌱 Base Simbólica (15,0% da base | 328 cand.)", 
                    "Candidaturas cartoriais de nominata: bens zero e gastos zero. Formada por estudantes (18,4%), agricultores e pequenos comerciantes (72% negros/pardos). Zero mandatos prévios.", space_after=11)

add_narrative_point(tf4, "💼 Patrimônio Sem Campanha (11,3% | 248 cand.)", 
                    "O enigma da eleição: candidatos abastados (mediana de R$ 140k em bens) que não gastaram nada em campanha. Mais da metade (52,3%) são Advogados ou Empresários com média de 55 anos.", space_after=0)

# Imagem Radar Polar 2x2 (Quadrantes perfeitos e nítidos!)
img4_path = 'images/imagens_apresentacao/slide4_01_radar_polar_2x2.png'
if os.path.exists(img4_path):
    slide4.shapes.add_picture(img4_path, Inches(6.8), Inches(1.4), width=Inches(5.7))


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5: A VALIDAÇÃO DAS REGRAS (PAINEL LIMPO + CHAMADA GRAFO HTML AO VIVO)
# ═══════════════════════════════════════════════════════════════════════════════
slide5 = prs.slides.add_slide(blank_layout)
set_slide_background(slide5, LIGHT_BG)
add_story_header(slide5, "5. A Confirmação dos Fatos", "A Certeza dos Padrões: 100% de Confiança na Previsão dos 4 Arquétipos")

card5 = add_card_box(slide5, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5))
tf5 = card5.text_frame
tf5.margin_left = Inches(0.35)
tf5.margin_right = Inches(0.35)
tf5.margin_top = Inches(0.35)
tf5.word_wrap = True

add_narrative_point(tf5, "🎯 Previsibilidade Absoluta", 
                    "Ao minerar regras de associação cruzando as variáveis contínuas em quartis, o algoritmo Apriori alcançou 100% de confiança para prever o perfil do candidato a partir de seus atributos.")

add_narrative_point(tf5, "🔗 O Casamento entre Bens e Despesas", 
                    "• Sem Bens + Sem Despesa ➔ 100% Base Simbólica (Lift 6,67)\n• Bens Médios/Altos + Sem Despesa ➔ 100% Patr. Sem Campanha (Lift 8,83 — o maior da base!)\n• Bens Altos + Despesa Alta ➔ 100% Estruturados")

add_narrative_point(tf5, "🧬 O DNA de Cada Grupo Revelado", 
                    "A direção inversa revela a identidade natural de cada arquétipo: Estruturados atrai mandatos parlamentares; Financiados atrai o gênero feminino; e a Base Simbólica concentra legendas menores como a DC.")

add_narrative_point(tf5, "✅ Validação Definitiva", 
                    "Os 4 nomes dados aos clusters não são rótulos subjetivos: representam assinaturas estatísticas sólidas e matematicamente comprovadas.", space_after=0)

# Imagem Painel de Regras + Chamada de Demonstração do Grafo HTML ao Vivo
img5_path = 'images/imagens_apresentacao/slide5_painel_regras_apriori.png'
if os.path.exists(img5_path):
    slide5.shapes.add_picture(img5_path, Inches(6.8), Inches(1.4), width=Inches(5.7))


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6: OS CASOS EXTREMOS (2D LIMPO COM ANOTAÇÕES + DEMO 3D AO VIVO)
# ═══════════════════════════════════════════════════════════════════════════════
slide6 = prs.slides.add_slide(blank_layout)
set_slide_background(slide6, LIGHT_BG)
add_story_header(slide6, "6. As Exceções da Regra", "Os Casos Fora da Curva: Quem Desafia a Lógica Comum do Jogo Eleitoral?")

card6 = add_card_box(slide6, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5))
tf6 = card6.text_frame
tf6.margin_left = Inches(0.35)
tf6.margin_right = Inches(0.35)
tf6.margin_top = Inches(0.35)
tf6.word_wrap = True

add_narrative_point(tf6, "🔬 O Mecanismo do Isolation Forest", 
                    "O modelo isola anomalias por cortes aleatórios sucessivos no espaço multidimensional: pontos fáceis de isolar são discrepâncias graves; pontos cercados de vizinhos são a norma.")

add_narrative_point(tf6, "🌟 Os Casos Notórios Globais", 
                    "• Nathalia Pedrosa (PE): 25 anos, patrimônio recorde de R$ 48,3 milhões e R$ 0 gastos em campanha — a herdeira milionária sem campanha.\n• Tiririca (CE): 1 ano de instrução formal operando uma máquina de R$ 2,45 milhões em campanha.")

add_narrative_point(tf6, "👁️ A 4ª Dimensão Oculta no Gráfico 3D", 
                    "Por que alguns atípicos parecem 'no meio' da nuvem 3D? Porque sua anomalia é educacional! No espaço visual 3D (Idade, Bens, Despesas) são comuns, mas na 4ª dimensão (Escolaridade) estão totalmente isolados.")

add_narrative_point(tf6, "🔍 37 Anomalias Invisíveis na Base Geral", 
                    "Ao rodar o modelo dentro de cada grupo, descobrimos 37 candidatos que parecem normais para o Nordeste inteiro, mas que quebram radicalmente o padrão de seus pares.", space_after=0)

# Imagem 2D com Destaque de Nomes e Chamada da Demo 3D ao Vivo
img6_path = 'images/imagens_apresentacao/slide6_anomalias_2d_destaque.png'
if os.path.exists(img6_path):
    slide6.shapes.add_picture(img6_path, Inches(6.8), Inches(1.4), width=Inches(5.7))


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7: A GRANDE CONCLUSÃO
# ═══════════════════════════════════════════════════════════════════════════════
slide7 = prs.slides.add_slide(blank_layout)
set_slide_background(slide7, LIGHT_BG)
add_story_header(slide7, "7. Síntese e Impacto", "O Que os Dados Ensinam: As Lições Estruturais da Eleição Nordestina")

card_left = add_card_box(slide7, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5))
tf_cl = card_left.text_frame
tf_cl.margin_left = Inches(0.35)
tf_cl.margin_right = Inches(0.35)
tf_cl.margin_top = Inches(0.35)
tf_cl.word_wrap = True

add_narrative_point(tf_cl, "✅ O Que Confirmou Expectativas", 
                    "A política de alta densidade no Nordeste continua sendo dominada por uma elite estabelecida (os Estruturados: mandatários, médicos e advogados com alto patrimônio e altas despesas). Além disso, confirmou-se que centenas de candidaturas existem unicamente no papel para fins burocráticos (a Base Simbólica).")

add_narrative_point(tf_cl, "⚡ O Que os Dados Trouxeram de Novo", 
                    "• O impacto real das cotas: As mulheres não estão na base simbólica, mas sim nos Financiados (51,5%), movimentando recursos públicos sem necessidade de capital próprio.\n• A elite inativa: 11% dos candidatos têm patrimônio substancial, mas optam por não investir um centavo na disputa.", space_after=0)

card_right = add_card_box(slide7, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5), bg_color=NAVY, border_color=None)
tf_cr = card_right.text_frame
tf_cr.margin_left = Inches(0.4)
tf_cr.margin_right = Inches(0.4)
tf_cr.margin_top = Inches(0.4)
tf_cr.word_wrap = True

p_crt = tf_cr.paragraphs[0]
p_crt.text = "A CONTRIBUIÇÃO CENTRAL DO ESTUDO"
p_crt.font.bold = True
p_crt.font.size = Pt(14)
p_crt.font.color.rgb = GOLD
p_crt.space_after = Pt(16)

def add_white_point(tf, title, body):
    p = tf.add_paragraph()
    p.text = f"{title}\n"
    p.font.bold = True
    p.font.size = Pt(12.5)
    p.font.color.rgb = WHITE
    run = p.add_run()
    run.text = body
    run.font.bold = False
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(226, 232, 240)
    p.space_after = Pt(14)

add_white_point(tf_cr, "1. Superação da Visão Simplista", 
                "A disputa eleitoral para Deputado Federal não é um bloco único nem uma simples oposição entre ricos e pobres: ela opera através de 4 engrenagens políticas distintas.")

add_white_point(tf_cr, "2. A Ciência de Dados a Serviço da Transparência", 
                "A combinação de clusterização hierárquica, regras de associação determinísticas e detecção de anomalias permitiu mapear os papéis funcionais e o uso dos recursos públicos.")

add_white_point(tf_cr, "3. Evidência Empírica para Políticas Públicas", 
                "O estudo prova empiricamente que as políticas de cota e financiamento público transformam diretamente o perfil dos atores que entram na arena da disputa democrática.")


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8: FECHAMENTO
# ═══════════════════════════════════════════════════════════════════════════════
slide8 = prs.slides.add_slide(blank_layout)
set_slide_background(slide8, NAVY)

bar8 = slide8.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.15))
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
print(f"🎉 Apresentação atualizada com sucesso: {output_pptx} ({size_mb:.2f} MB)")
