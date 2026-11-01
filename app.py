import streamlit as st
import math
import threading
import hmac
from datetime import datetime

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
    "skill": "Identificação dos operadores",
    "level": "Fácil",
    "story": "O sistema de monitoramento do refúgio climático identificou três situações que precisam ser analisadas. Antes de iniciar os cálculos, você deve selecionar o operador matemático adequado para cada diagnóstico.",
    "question": "Associe cada situação ao operador matemático correspondente, na ordem apresentada:\n\nI. Determinar o sentido de maior aumento local da temperatura em uma região do abrigo.\n\nII. Verificar se o campo de vento apresenta expansão ou convergência local.\n\nIII. Identificar a tendência de circulação local do ar, como a formação de redemoinhos.",
    "kind": "choice",
    "options": [
        "Gradiente, divergente e rotacional",
        "Divergente, gradiente e rotacional",
        "Rotacional, divergente e gradiente",
        "Gradiente, rotacional e divergente"
    ],
    "answer": "Gradiente, divergente e rotacional",
    "explanation": "I. Gradiente: aplicado a um campo escalar, indica o sentido de maior aumento local da temperatura. II. Divergente: aplicado a um campo vetorial, mede a expansão ou convergência local do fluxo. III. Rotacional: aplicado a um campo vetorial, identifica a tendência local de rotação do campo.",
    "hint": "Lembre-se: o gradiente está associado à variação espacial de um campo escalar; divergente e rotacional são operadores aplicados a campos vetoriais."
    },
    {
        "title": "Rota de resfriamento",
        "skill": "Gradiente",
        "level": "Fácil",
        "story": "A equipe quer calcular a variação térmica em um ponto do abrigo antes de orientar a circulação de pessoas.",
        "question": "Se T(x, y) = x² + 3y, qual é ∇T no ponto (2, 1)? Digite as duas componentes separadas por vírgula.",
        "kind": "text",
        "answer": "(4,3)",
        "explanation": "∂T/∂x = 2x e ∂T/∂y = 3. No ponto (2, 1), ∇T = (4, 3).",
        "hint": "Calcule as derivadas parciais primeiro: ∂T/∂x = 2x e ∂T/∂y = 3.",
    },
    {
    "title": "Calibração térmica",
    "skill": "Gradiente",
    "level": "Intermediário",
    "story": "O sensor térmico do refúgio climático detectou uma região com variações significativas de temperatura. Para calibrar o alerta de risco, o sistema precisa calcular a intensidade da variação térmica no ponto monitorado.",
    "question": "A temperatura é modelada pelo campo escalar T(x,y) = (5/2)x² + 6y². No ponto (1,1), calcule o módulo do gradiente |∇T|. Qual valor deve ser enviado ao sistema de monitoramento?",
    "kind": "choice",
    "options": ["10", "13", "17", "25"],
    "answer": "13",
    "explanation": "Primeiro, calculamos o gradiente: ∇T = (5x, 12y). No ponto (1,1), temos ∇T = (5,12). Seu módulo é |∇T| = √(5² + 12²) = √169 = 13. Portanto, a intensidade da variação térmica é 13 unidades de temperatura por unidade de distância.",
    "hint": "Calcule primeiro as duas derivadas parciais de T(x,y). Depois, substitua x = 1 e y = 1 e utilize a fórmula do módulo de um vetor."
    },
    {
    "title": "O redemoinho invisível",
    "skill": "Rotacional",
    "level": "Intermediário",
    "story": "Os sensores detectaram uma possível formação de redemoinho na circulação do ar próximo à área verde do refúgio. O sistema precisa calcular o rotacional do campo de vento para verificar a intensidade e o sentido da tendência de rotação local.",
    "question": "O campo de vento é modelado por F(x,y) = ((x² + 1)(y + 1), (x + 2)/(y + 1)). Calcule o rotacional escalar no ponto (1,1), utilizando rot F = ∂Q/∂x − ∂P/∂y. Qual valor deve ser registrado?",
    "kind": "choice",
    "options": ["−1/2", "−1", "−3/2", "−5/2"],
    "answer": "−3/2",
    "explanation": "Temos P = (x² + 1)(y + 1) e Q = (x + 2)/(y + 1). Pela regra do produto, ∂P/∂y = x² + 1. Pela regra do quociente, ∂Q/∂x = 1/(y + 1). No ponto (1,1), obtemos ∂P/∂y = 2 e ∂Q/∂x = 1/2. Portanto, rot F = 1/2 − 2 = −3/2.",
    "hint": "Calcule ∂Q/∂x e ∂P/∂y separadamente. Atenção à ordem da subtração na fórmula do rotacional."
    },
    {
    "title": "O redemoinho invisível",
    "skill": "Rotacional",
    "level": "Intermediário",
    "story": "Um padrão de circulação parece estar se formando perto da parede verde do abrigo.",
    "question": "Em duas dimensões, para F = (P,Q), o rotacional escalar é ∂Q/∂x − ∂P/∂y. Se P = −sen(y²) e Q = sen(x²), qual é o rotacional no ponto (π, π/2)?",
    "kind": "choice",
    "options": [
    "2πcos(π²) − πcos(π²/4)",
    "2πcos(π²) + πcos(π²/4)",
    "πcos(π²) + 2πcos(π²/4)",
    "0"
    ],
    "answer": "2πcos(π²) + πcos(π²/4)",
    "explanation": "Aplicando a regra da cadeia: ∂Q/∂x = 2x·cos(x²) e ∂P/∂y = −2y·cos(y²). No ponto (π, π/2), temos ∂Q/∂x = 2πcos(π²) e ∂P/∂y = −πcos(π²/4). Portanto, rot F = 2πcos(π²) + πcos(π²/4).",
    "hint": "Lembre-se da regra da cadeia: a derivada de sen(u) é cos(u) multiplicada pela derivada de u."
    },
    {
    "title": "Calibração dos sensores",
    "skill": "Gradiente e derivadas parciais",
    "level": "Avançado",
    "story": "A calibração exige derivar expressões com termos quadráticos e mistos.",
    "question": "Um sensor térmico monitora a distribuição de temperatura T(x,y) = x²y + 3xy em uma região do abrigo. A equipe deseja identificar como a temperatura varia na direção do eixo x, mantendo a coordenada y fixa. Qual é o valor dessa componente no ponto (1,2)? Assinale o valor correto.",
    "kind": "choice",
    "options": ["7.5", "5", "10", "12.5"],
    "answer": "10",
    "explanation": "Como a temperatura é uma função escalar, utilizamos o gradiente. Sua componente na direção x é ∂T/∂x. Tratando y como constante, ∂T/∂x = 2xy + 3y. No ponto (1,2), temos 2·1·2 + 3·2 = 10.",
    "hint": "A temperatura é uma grandeza escalar. Para analisar sua variação espacial, utilize o gradiente e identifique a componente correspondente ao eixo x.",
    "accepted": ["10"],
    },
    {
        "title": "Diagnóstico do abrigo",
        "skill": "Divergente e rotacional",
        "level": "Avançado",
        "story": "O painel apresenta dois indicadores para o campo de vento: expansão local e tendência de rotação.",
        "question": "Considere F(x,y) = (−y, x). Qual par apresenta (divergência, rotacional), nessa ordem?",
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
    "story": "Dois sensores disputam prioridade de intervenção. A equipe precisa identificar a região em que a temperatura apresenta a maior intensidade de variação espacial local.",
    "question": "A distribuição de temperatura em uma região tridimensional do abrigo é representada por T(x,y,z) = 3x² + 4y² + 12z² + 2xy. No ponto (1,1,1), qual é a intensidade da variação espacial local máxima da temperatura? Considere que essa intensidade é expressa pelo módulo do vetor que indica a maior taxa de aumento da temperatura.",
    "kind": "choice",
    "options": ["11.5", "27.2", "20.4", "18.7"],
    "answer": "27.2",
    "explanation": "A intensidade da variação espacial local máxima é dada pelo módulo do gradiente. Calculando as derivadas parciais: ∂T/∂x = 6x + 2y, ∂T/∂y = 8y + 2x e ∂T/∂z = 24z. No ponto (1,1,1), ∇T = (8, 10, 24). Portanto, ||∇T|| = √(8² + 10² + 24²) = √740 ≈ 27,2.",
    "hint": "Primeiro, determine as três taxas de variação da temperatura em relação a x, y e z. Depois, calcule a norma euclidiana do vetor obtido."
    },
    {
    "title": "Análise forense ambiental",
    "skill": "Diagnóstico de erros",
    "level": "Desafio",
    "story": "Um relatório automático apresenta inconsistências na análise de um campo vetorial que representa o fluxo de ar em uma região tridimensional do abrigo. Você precisa auditar os cálculos antes que a equipe utilize os resultados.",
    "question": "O campo vetorial F(x,y,z) = (xy², xz², yz) foi analisado por um sistema automático, que informou divergência ∇·F = y² + 2xz + y e rotacional ∇×F = (z - 2xz, 0, 2xy - xz²). Considerando as definições de divergência e rotacional em três dimensões, qual alternativa apresenta os dois resultados corretos?",
    "kind": "choice",
    "options": [
    "∇·F = y² + 2xz + y; ∇×F = (z - 2xz, 0, z² - 2xy)",
    "∇·F = y² + y; ∇×F = (2xz - z, 0, 2xy - z²)",
    "∇·F = y² + y; ∇×F = (0, 0, 0)",
    "∇·F = y² + y; ∇×F = (z - 2xz, 0, z² - 2xy)"
    ],
    "answer": "∇·F = y² + y; ∇×F = (z - 2xz, 0, z² - 2xy)",
    "explanation": "Identificando P = xy², Q = xz² e R = yz, a divergência é ∂P/∂x + ∂Q/∂y + ∂R/∂z = y² + 0 + y = y² + y. O rotacional é (∂R/∂y - ∂Q/∂z, ∂P/∂z - ∂R/∂x, ∂Q/∂x - ∂P/∂y) = (z - 2xz, 0 - 0, z² - 2xy).",
    "hint": "Para a divergência, some as derivadas de cada componente em relação à sua própria variável. Para o rotacional, utilize o determinante com os vetores unitários e as componentes do campo."
    },
    {
    "title": "Protocolo de sobrevivência",
    "skill": "Desafio integrado",
    "level": "Chefe final",
    "story": "O sistema está quase restaurado. Você precisa interpretar os indicadores de um último campo vetorial de vento em uma região tridimensional do abrigo.",
    "question": "O campo vetorial F(x,y,z) = (xy + z², yz + x², xz + y²) representa o fluxo de ar na região monitorada. Para concluir o diagnóstico, é necessário calcular a divergência e o rotacional vetorial desse campo. Qual alternativa apresenta corretamente os dois resultados?",
    "kind": "choice",
    "options": [
    "∇·F = x + y + z; ∇×F = (y, z, x)",
    "∇·F = 2(x + y + z); ∇×F = (y, z, x)",
    "∇·F = x + y + z; ∇×F = (−y, −z, −x)",
    "∇·F = x + y + z; ∇×F = (0, 0, 0)"
    ],
    "answer": "∇·F = x + y + z; ∇×F = (y, z, x)",
    "explanation": "Identificando P = xy + z², Q = yz + x² e R = xz + y², a divergência é ∂P/∂x + ∂Q/∂y + ∂R/∂z = y + z + x = x + y + z. O rotacional é (∂R/∂y - ∂Q/∂z, ∂P/∂z - ∂R/∂x, ∂Q/∂x - ∂P/∂y) = (2y - y, 2z - z, 2x - x) = (y, z, x).",
    "hint": "Para a divergência, some as derivadas de cada componente em relação à sua própria variável. Para o rotacional, calcule as diferenças das derivadas cruzadas seguindo a ordem correta das componentes."
    },
]


@st.cache_resource
def get_shared_registry():
    """Dados compartilhados entre sessões enquanto o processo do app estiver ativo."""
    return {"records": {}, "lock": threading.Lock()}


def save_student_result(status):
    """Registra a melhor pontuação por aluno/turma nesta execução do aplicativo."""
    if st.session_state.get("result_saved", False):
        return
    name = st.session_state.get("student_name", "").strip()
    turma = st.session_state.get("student_class", "").strip()
    if not name or not turma:
        return

    registry = get_shared_registry()
    key = (normalize(name), normalize(turma))
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with registry["lock"]:
        previous = registry["records"].get(key)
        score = int(st.session_state.points)
        completed = len(st.session_state.completed)
        if previous is None:
            registry["records"][key] = {
                "Aluno": name, "Turma": turma,
                "Melhor pontuação": score, "Fases concluídas": completed,
                "Situação": status, "Última participação": now, "Tentativas": 1,
            }
        else:
            previous["Tentativas"] += 1
            previous["Última participação"] = now
            if score > previous["Melhor pontuação"] or (
                score == previous["Melhor pontuação"] and completed > previous["Fases concluídas"]
            ):
                previous["Melhor pontuação"] = score
                previous["Fases concluídas"] = completed
                previous["Situação"] = status
    st.session_state.result_saved = True


def teacher_area():
    """Área administrativa protegida por senha configurada nos Secrets."""
    with st.sidebar.expander("🔐 Área do professor"):
        try:
            expected_password = st.secrets["teacher"]["password"]
        except Exception:
            st.warning("Configure [teacher].password em Settings → Secrets.")
            return
        entered = st.text_input("Senha de acesso", type="password", key="teacher_password_input")
        if entered and hmac.compare_digest(str(entered), str(expected_password)):
            st.success("Acesso autorizado.")
            registry = get_shared_registry()
            with registry["lock"]:
                rows = sorted(
                    [dict(row) for row in registry["records"].values()],
                    key=lambda row: (-row["Melhor pontuação"], row["Aluno"].casefold())
                )
            st.markdown("**Participantes registrados nesta execução**")
            if rows:
                import pandas as pd
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
                csv_data = pd.DataFrame(rows).to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    "⬇️ Baixar resultados (CSV)", data=csv_data,
                    file_name="operacao_refugio_resultados.csv",
                    mime="text/csv", use_container_width=True,
                )
            else:
                st.info("Ainda não há participações registradas.")
        elif entered:
            st.error("Senha incorreta.")


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
    st.session_state.result_saved = False

if "unlocked" not in st.session_state:
    reset_game()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🌡️ OPERAÇÃO REFÚGIO")
    st.caption("CENTRAL DE MONITORAMENTO AMBIENTAL")
    teacher_area()
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
    st.markdown("### Identificação do participante")
    with st.form("student_identification"):
        student_name = st.text_input("Nome completo")
        student_class = st.text_input("Turma")
        start = st.form_submit_button("🚀 Iniciar missão", type="primary", use_container_width=True)
    if start:
        if not student_name.strip() or not student_class.strip():
            st.warning("Informe seu nome e sua turma para iniciar.")
        else:
            st.session_state.student_name = student_name.strip()
            st.session_state.student_class = student_class.strip()
            st.session_state.game_started = True
            st.rerun()
    st.stop()

if st.session_state.game_over:
    save_student_result("Não concluiu — sem vidas")
    st.error("Missão encerrada: suas vidas acabaram. Reinicie para tentar novamente.")
    if st.button("Tentar novamente", type="primary"):
        reset_game()
        st.session_state.game_started = True
        st.rerun()
    st.stop()

if len(st.session_state.completed) == len(PHASES):
    save_student_result("Concluiu")
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
st.caption(f"Participante: **{st.session_state.get('student_name', '')}** · Turma: **{st.session_state.get('student_class', '')}**")
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
        placeholder="Digite o resultado (ex.: -5,6)",
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
