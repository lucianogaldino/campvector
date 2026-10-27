import streamlit as st
import math

# ============================================================
# OPERAÇÃO REFÚGIO — jogo de cálculo vetorial em Streamlit
# Execute com: streamlit run app.py
# ============================================================

st.set_page_config(
    page_title="Operação Refúgio",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Visual ----------
st.markdown(
    """
    <style>
    .stApp {
        background:
          radial-gradient(circle at 12% 8%, rgba(14,116,144,.20), transparent 28%),
          radial-gradient(circle at 90% 20%, rgba(30,64,175,.16), transparent 25%),
          #07111f;
        color: #e5eef8;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0c1b2d 0%, #091321 100%);
        border-right: 1px solid #1e3a52;
    }
    h1, h2, h3 { color: #e6f7ff !important; }
    p, li, label { color: #d5e3f0; }
    .hero {
        padding: 1.35rem 1.5rem;
        border: 1px solid #24506b;
        border-radius: 18px;
        background: linear-gradient(120deg, rgba(8,47,73,.88), rgba(15,23,42,.92));
        margin-bottom: 1rem;
    }
    .eyebrow {
        color: #67e8f9; font-size: .78rem; font-weight: 800;
        letter-spacing: .16em; text-transform: uppercase;
    }
    .metric-card {
        padding: .9rem 1rem; border: 1px solid #244258; border-radius: 14px;
        background: rgba(12, 30, 48, .82); min-height: 88px;
    }
    .metric-label { color: #91a9bc; font-size: .82rem; }
    .metric-value { color: #67e8f9; font-size: 1.65rem; font-weight: 800; }
    .mission-card {
        border: 1px solid #244258; background: rgba(10, 26, 43, .82);
        border-radius: 16px; padding: 1.1rem 1.2rem; margin: .55rem 0;
    }
    .small-muted { color: #9db3c6; font-size: .9rem; }
    .stButton > button {
        border-radius: 10px; border: 1px solid #2c819e;
        background: linear-gradient(90deg, #0e7490, #155e75);
        color: white; font-weight: 750; min-height: 2.8rem;
    }
    .stButton > button:hover { border-color: #67e8f9; color: white; }
    div[data-testid="stAlert"] { border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

PHASES = [
    {
        "title": "O alerta térmico",
        "skill": "Gradiente",
        "level": "Fácil",
        "story": "Um sensor registra o campo de temperatura T(x, y). O sistema precisa identificar o vetor que aponta para o maior aumento local da temperatura.",
        "question": "Em um ponto, o gradiente da temperatura é ∇T = (3, 4). Qual vetor indica o sentido de maior aumento local de T?",
        "kind": "choice",
        "options": ["(−3, −4)", "(3, 4)", "(4, 3)", "(−4, 3)"],
        "answer": "(3, 4)",
        "explanation": "O gradiente aponta para o sentido de maior aumento local do campo escalar. Como ∇T = (3, 4), esse é o vetor procurado.",
        "hint": "O gradiente aponta para o maior aumento local, não para a diminuição.",
    },
    {
        "title": "Rota de resfriamento",
        "skill": "Gradiente",
        "level": "Fácil",
        "story": "A equipe quer calcular a variação térmica em um ponto do abrigo antes de orientar a circulação de pessoas.",
        "question": "Se T(x, y) = x² + 3y, qual é ∇T no ponto (2, 1)? Digite as duas componentes separadas por vírgula.",
        "kind": "text",
        "answer": "4,3",
        "explanation": "∂T/∂x = 2x e ∂T/∂y = 3. No ponto (2, 1), ∇T = (4, 3).",
        "hint": "Calcule as derivadas parciais primeiro: ∂T/∂x = 2x e ∂T/∂y = 3.",
    },
    {
        "title": "Mapa das correntes de ar",
        "skill": "Campos vetoriais",
        "level": "Intermediário",
        "story": "O sensor de vento fornece um campo vetorial F(x,y) = (P,Q). A primeira componente descreve o fluxo horizontal e a segunda o vertical.",
        "question": "No campo F(x,y) = (2x, −y), quais são as componentes P e Q?",
        "kind": "choice",
        "options": ["P = −y e Q = 2x", "P = 2x e Q = −y", "P = 2 e Q = −1", "P = x² e Q = −y²"],
        "answer": "P = 2x e Q = −y",
        "explanation": "Por definição, F = (P,Q). Basta ler a primeira e a segunda componente do vetor, respectivamente.",
        "hint": "A primeira entrada do par é P; a segunda entrada é Q.",
    },
    {
        "title": "Fonte ou sumidouro?",
        "skill": "Divergente",
        "level": "Intermediário",
        "story": "O sistema procura regiões onde o fluxo de ar tende a se expandir ou convergir.",
        "question": "Para F(x,y) = (2x, −2y), calcule a divergência ∇·F.",
        "kind": "choice",
        "options": ["4", "0", "−4", "2x − 2y"],
        "answer": "0",
        "explanation": "∇·F = ∂P/∂x + ∂Q/∂y = 2 + (−2) = 0. Divergência nula não significa campo nulo nem ausência de movimento.",
        "hint": "Use ∇·F = ∂P/∂x + ∂Q/∂y.",
    },
    {
        "title": "O redemoinho invisível",
        "skill": "Rotacional",
        "level": "Intermediário",
        "story": "Um padrão de circulação parece estar se formando perto da parede verde do abrigo.",
        "question": "Em duas dimensões, para F = (P,Q), o rotacional escalar é ∂Q/∂x − ∂P/∂y. Se P = −y e Q = x, qual é o rotacional?",
        "kind": "choice",
        "options": ["0", "1", "−1", "2"],
        "answer": "2",
        "explanation": "∂Q/∂x = 1 e ∂P/∂y = −1. Portanto, rot F = 1 − (−1) = 2.",
        "hint": "Atenção ao sinal de ∂P/∂y: como P = −y, essa derivada vale −1.",
    },
    {
        "title": "Calibração dos sensores",
        "skill": "Derivadas parciais",
        "level": "Avançado",
        "story": "A calibração exige derivar expressões com termos quadráticos e mistos.",
        "question": "Se T(x,y) = x²y + 3xy, qual é ∂T/∂x no ponto (1,2)? Digite o valor numérico.",
        "kind": "text",
        "answer": "7",
        "explanation": "Tratando y como constante, ∂T/∂x = 2xy + 3y. Em (1,2), o valor é 2·1·2 + 3·2 = 10.",
        "hint": "Ao derivar em relação a x, trate y como constante.",
        "accepted": ["10"],
    },
    {
        "title": "Diagnóstico do abrigo",
        "skill": "Divergente e rotacional",
        "level": "Avançado",
        "story": "O painel apresenta dois indicadores para o campo de vento: expansão local e tendência de rotação.",
        "question": "Considere F(x,y) = (−y, x). Qual par apresenta (divergência, rotacional escalar), nessa ordem?",
        "kind": "choice",
        "options": ["(0, 2)", "(2, 0)", "(0, 0)", "(−2, 2)"],
        "answer": "(0, 2)",
        "explanation": "P = −y e Q = x. Divergência: ∂P/∂x + ∂Q/∂y = 0 + 0 = 0. Rotacional: ∂Q/∂x − ∂P/∂y = 1 − (−1) = 2.",
        "hint": "Calcule cada indicador separadamente. Divergência usa ∂P/∂x + ∂Q/∂y; rotacional usa ∂Q/∂x − ∂P/∂y.",
    },
    {
        "title": "Zona crítica",
        "skill": "Gradiente",
        "level": "Avançado",
        "story": "Dois sensores disputam prioridade de intervenção. O módulo do gradiente indica a intensidade da variação espacial local da temperatura.",
        "question": "Se ∇T = (6, 8), qual é o módulo do gradiente?",
        "kind": "choice",
        "options": ["10", "14", "48", "100"],
        "answer": "10",
        "explanation": "||∇T|| = √(6² + 8²) = √100 = 10.",
        "hint": "Use a norma euclidiana: √(componente₁² + componente₂²).",
    },
    {
        "title": "Análise forense ambiental",
        "skill": "Diagnóstico de erros",
        "level": "Desafio",
        "story": "Um relatório automático afirma que o campo F = (x², y²) tem divergência 2x + 2y e rotacional 2y − 2x. Você precisa auditar o diagnóstico.",
        "question": "Qual é a correção adequada para o rotacional escalar ∂Q/∂x − ∂P/∂y desse campo?",
        "kind": "choice",
        "options": ["2y − 2x", "0", "2x + 2y", "2x − 2y"],
        "answer": "0",
        "explanation": "P = x² e Q = y². Como Q não depende de x, ∂Q/∂x = 0; como P não depende de y, ∂P/∂y = 0. Logo, o rotacional é zero. A divergência 2x + 2y está correta.",
        "hint": "Derive Q em relação a x e P em relação a y. Observe quais variáveis aparecem em cada função.",
    },
    {
        "title": "Protocolo de sobrevivência",
        "skill": "Desafio integrado",
        "level": "Chefe final",
        "story": "O sistema está quase restaurado. Você precisa interpretar os indicadores de um último campo vetorial de vento.",
        "question": "Para F(x,y) = (x + y, x − y), qual é o par (divergência, rotacional escalar)?",
        "kind": "choice",
        "options": ["(0, 0)", "(2, 0)", "(0, 2)", "(2, −2)"],
        "answer": "(0, 0)",
        "explanation": "P = x + y e Q = x − y. Divergência = ∂P/∂x + ∂Q/∂y = 1 + (−1) = 0. Rotacional = ∂Q/∂x − ∂P/∂y = 1 − 1 = 0.",
        "hint": "Calcule as quatro derivadas parciais necessárias e só então forme os dois indicadores.",
    },
]

def normalize(value):
    value = str(value).strip().lower().replace(" ", "")
    value = value.replace("−", "-").replace("，", ",").replace(";", ",")
    return value

def is_correct(phase, submitted):
    accepted = phase.get("accepted", [phase["answer"]])
    candidate = normalize(submitted)
    return any(candidate == normalize(a) for a in accepted)

def reset_game():
    st.session_state.unlocked = 0
    st.session_state.completed = set()
    st.session_state.points = 0
    st.session_state.lives = 3
    st.session_state.results = {}
    st.session_state.hints_used = set()
    st.session_state.game_started = False
    st.session_state.game_over = False

if "unlocked" not in st.session_state:
    reset_game()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🌡️ OPERAÇÃO REFÚGIO")
    st.caption("CENTRAL DE MONITORAMENTO AMBIENTAL")
    st.markdown("---")
    if st.session_state.game_started:
        st.markdown(f"**Vidas:** {'❤️ ' * st.session_state.lives}{'🖤 ' * (3-st.session_state.lives)}")
        st.progress(len(st.session_state.completed) / len(PHASES), text=f"Progresso: {len(st.session_state.completed)}/{len(PHASES)}")
        st.markdown(f"**Pontos:** `{st.session_state.points}`")
        st.markdown("---")
        st.markdown("### Mapa de fases")
        for i, phase in enumerate(PHASES):
            if i in st.session_state.completed:
                status = "✅"
            elif i <= st.session_state.unlocked and not st.session_state.game_over:
                status = "🔓"
            else:
                status = "🔒"
            st.markdown(f"{status} **{i+1:02d}.** {phase['title']}")
    if st.button("↻ Reiniciar missão", use_container_width=True):
        reset_game()
        st.rerun()

# ---------- Header ----------
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">PROTOCOLO DE RESPOSTA CLIMÁTICA • SIMULAÇÃO INTERATIVA</div>
      <h1 style="margin:.35rem 0;">🌡️ Operação Refúgio</h1>
      <p style="font-size:1.08rem;margin-bottom:.2rem;">
        Recupere o sistema de monitoramento do refúgio climático usando cálculo vetorial.
      </p>
      <div class="small-muted">GRADIENTE · DIVERGÊNCIA · ROTACIONAL</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not st.session_state.game_started:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="metric-card"><div class="metric-label">MISSÕES</div><div class="metric-value">10 fases</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><div class="metric-label">RECURSOS</div><div class="metric-value">3 vidas</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><div class="metric-label">OBJETIVO</div><div class="metric-value">Restaurar</div></div>', unsafe_allow_html=True)
    st.markdown("### 📡 Briefing da missão")
    st.markdown(
        """
        Um refúgio climático urbano está com o painel de monitoramento comprometido.
        Os sensores de temperatura e vento continuam funcionando, mas o sistema não consegue
        interpretar corretamente os dados. Resolva as 10 fases para restaurar o diagnóstico.

        **Regras**
        - Cada fase concluída libera a próxima.
        - Você começa com **3 vidas**.
        - Uma resposta correta vale **100 pontos**; usar uma dica reduz o prêmio para **70 pontos**.
        - Ao errar, você recebe uma explicação e perde uma vida. Você pode tentar novamente enquanto tiver vidas.
        - Os campos são bidimensionais, salvo indicação contrária.
        """
    )
    st.info("Dica de estudo: gradiente é aplicado a campos escalares; divergência e rotacional são operadores aplicados a campos vetoriais.")
    if st.button("🚀 Iniciar missão", type="primary", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()
    st.stop()

if st.session_state.game_over:
    st.error("Missão encerrada: suas vidas acabaram. Reinicie para tentar novamente.")
    if st.button("Tentar novamente", type="primary"):
        reset_game()
        st.session_state.game_started = True
        st.rerun()
    st.stop()

if len(st.session_state.completed) == len(PHASES):
    st.balloons()
    st.success("MISSÃO CONCLUÍDA! O sistema de monitoramento do refúgio foi restaurado.")
    st.markdown(f"## Pontuação final: {st.session_state.points} pontos")
    st.markdown("### Relatório de desempenho")
    for skill in ["Gradiente", "Campos vetoriais", "Divergente", "Rotacional", "Derivadas parciais", "Divergente e rotacional", "Diagnóstico de erros", "Desafio integrado"]:
        count = sum(1 for i in st.session_state.completed if PHASES[i]["skill"] == skill)
        if count:
            st.write(f"- **{skill}:** {count} fase(s) concluída(s)")
    st.markdown("Você concluiu o protocolo de análise ambiental. Revise as explicações das fases para consolidar os conceitos.")
    if st.button("Jogar novamente", type="primary"):
        reset_game()
        st.session_state.game_started = True
        st.rerun()
    st.stop()

phase_index = st.session_state.unlocked
phase = PHASES[phase_index]

# Top metrics
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">FASE ATUAL</div><div class="metric-value">{phase_index+1:02d}/10</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">DIFICULDADE</div><div class="metric-value" style="font-size:1.2rem">{phase["level"]}</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">PONTOS</div><div class="metric-value">{st.session_state.points}</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">VIDAS</div><div class="metric-value">{"❤️" * st.session_state.lives}</div></div>', unsafe_allow_html=True)

st.progress((phase_index) / len(PHASES), text=f"Progresso da missão: {phase_index} de {len(PHASES)} fases concluídas")
st.markdown(f"## Fase {phase_index+1}: {phase['title']}")
st.caption(f"ÁREA DE TREINAMENTO: {phase['skill'].upper()}  •  NÍVEL: {phase['level'].upper()}")

st.markdown('<div class="mission-card">', unsafe_allow_html=True)
st.markdown("### 📍 Contexto")
st.write(phase["story"])
st.markdown("### 🧩 Desafio")
st.write(phase["question"])
st.markdown("</div>", unsafe_allow_html=True)

hint_key = phase_index
if hint_key not in st.session_state.hints_used:
    if st.button("💡 Solicitar dica (vale menos pontos)", key=f"hint_{phase_index}"):
        st.session_state.hints_used.add(hint_key)
        st.rerun()
if hint_key in st.session_state.hints_used:
    st.info(f"**Dica:** {phase['hint']}")

if phase["kind"] == "choice":
    submitted = st.radio(
        "Selecione sua resposta:",
        phase["options"],
        index=None,
        key=f"answer_{phase_index}",
    )
else:
    submitted = st.text_input(
        "Sua resposta:",
        placeholder="Digite o resultado (ex.: 4,3)",
        key=f"answer_{phase_index}",
    )

col_submit, col_space = st.columns([1, 2])
with col_submit:
    check = st.button("Validar resposta", type="primary", use_container_width=True, key=f"check_{phase_index}")

if check:
    if submitted is None or str(submitted).strip() == "":
        st.warning("Escolha ou digite uma resposta antes de validar.")
    elif is_correct(phase, submitted):
        if phase_index not in st.session_state.completed:
            earned = 70 if phase_index in st.session_state.hints_used else 100
            st.session_state.points += earned
            st.session_state.completed.add(phase_index)
            st.session_state.results[phase_index] = "correct"
        st.session_state.last_feedback = ("correct", phase_index)
        st.success("Resposta correta! " + phase["explanation"])
        st.session_state.unlocked = min(phase_index + 1, len(PHASES) - 1)
        if phase_index == len(PHASES) - 1:
            st.session_state.unlocked = len(PHASES)
        st.rerun()
    else:
        st.session_state.lives -= 1
        st.session_state.results[phase_index] = "incorrect"
        st.session_state.last_feedback = ("incorrect", phase_index)
        if st.session_state.lives <= 0:
            st.session_state.game_over = True
        st.rerun()

# Feedback after a rerun
feedback = st.session_state.get("last_feedback")
if feedback and feedback[1] == phase_index:
    if feedback[0] == "correct":
        st.success(f"Fase concluída! {phase['explanation']}")
        if phase_index < len(PHASES) - 1:
            if st.button("➡️ Avançar para a próxima fase", type="primary", use_container_width=True):
                st.session_state.unlocked = phase_index + 1
                st.session_state.last_feedback = None
                st.rerun()
        else:
            if st.button("🏁 Ver resultado final", type="primary", use_container_width=True):
                st.session_state.unlocked = len(PHASES) - 1
                st.session_state.last_feedback = None
                st.rerun()
    elif feedback[0] == "incorrect":
        st.error(f"Resposta incorreta. Vidas restantes: {st.session_state.lives}. Revise o conceito e tente novamente.")
        st.caption("A resposta será explicada quando você concluir a fase. Você também pode solicitar a dica acima.")

st.markdown("---")
st.markdown(
    '<div class="small-muted">OPERAÇÃO REFÚGIO • Simulação didática. Os modelos são simplificados para fins de aprendizagem e não representam uma previsão meteorológica real.</div>',
    unsafe_allow_html=True,
)
