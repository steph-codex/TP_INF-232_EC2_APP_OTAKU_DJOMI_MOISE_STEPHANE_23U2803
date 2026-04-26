import streamlit as st

st.set_page_config(
    page_title="Otaku Cameroun — INF 232 EC2",
    page_icon="⛩️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS GLOBAL (chargé une seule fois ici) ───────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background-color: #0a0a12;
    color: #e0d8ff;
}
.stApp { background-color: #0a0a12; }

section[data-testid="stSidebar"] {
    background: #0d0820 !important;
    border-right: 1px solid rgba(160,80,255,0.2);
}
section[data-testid="stSidebar"] * { color: #c8b0ff !important; }
section[data-testid="stSidebar"] a { color: #c8b0ff !important; text-decoration: none; }

/* Boutons */
.stButton > button {
    background: linear-gradient(135deg, #6a00cc, #3d00a0) !important;
    color: #fff !important;
    border: 1px solid rgba(180,100,255,0.4) !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    border-radius: 4px !important;
    box-shadow: 0 0 18px rgba(160,80,255,0.25) !important;
}
.stButton > button:hover {
    box-shadow: 0 0 28px rgba(160,80,255,0.5) !important;
}

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #13001f 0%, #0d0a2a 50%, #001a12 100%);
    border: 1px solid rgba(160,80,255,0.25);
    border-radius: 12px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 0 30px rgba(160,80,255,0.6);
    margin-bottom: 0.5rem;
}
.hero-title span { color: #b060ff; }
.hero-title .green { color: #3dffa0; }
.hero-sub { font-size: 1.1rem; color: rgba(200,180,255,0.7); letter-spacing: 2px; }
.badge {
    display: inline-block;
    font-family: 'Orbitron', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    color: #7fffb0;
    border: 1px solid rgba(127,255,176,0.4);
    padding: 4px 14px;
    border-radius: 2px;
    margin-bottom: 1rem;
}

/* Sections formulaire */
.section-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(160,80,255,0.18);
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
}
.section-head {
    font-family: 'Orbitron', monospace;
    font-size: 12px;
    color: #3dffa0;
    letter-spacing: 2px;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(160,80,255,0.15);
}

/* Métriques */
.metric-box {
    background: linear-gradient(135deg, rgba(160,80,255,0.1), rgba(61,255,160,0.05));
    border: 1px solid rgba(160,80,255,0.25);
    border-radius: 8px;
    padding: 1.2rem;
    text-align: center;
}
.metric-num { font-family: 'Orbitron', monospace; font-size: 2rem; font-weight: 900; color: #b060ff; }
.metric-label { font-size: 11px; color: rgba(200,180,255,0.6); letter-spacing: 1px; margin-top: 4px; }

/* Charts */
.chart-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(160,80,255,0.15);
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}
.chart-title {
    font-family: 'Orbitron', monospace;
    font-size: 11px;
    color: #3dffa0;
    letter-spacing: 2px;
    margin-bottom: 0.8rem;
}
.insight-box {
    background: rgba(61,255,160,0.06);
    border-left: 3px solid #3dffa0;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    margin-top: 0.8rem;
    font-size: 14px;
    color: rgba(200,255,220,0.85);
}

/* Inputs */
input, select, textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(160,80,255,0.25) !important;
    color: #e0d8ff !important;
    border-radius: 6px !important;
}
label { color: #c8b0ff !important; }
hr { border-color: rgba(160,80,255,0.15) !important; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR LOGO ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem;'>
        <div style='font-family:Orbitron,monospace; font-size:1.3rem; color:#b060ff; font-weight:900;'>⛩️ OTAKU CMR</div>
        <div style='font-size:10px; color:rgba(200,180,255,0.4); letter-spacing:2px; margin-top:4px;'>INF 232 — EC2</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    import pandas as pd, os
    DATA_FILE = "data/reponses.csv"
    n = len(pd.read_csv(DATA_FILE)) if os.path.exists(DATA_FILE) else 0
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:0.5rem;'>
        <div style='font-family:Orbitron,monospace; font-size:2rem; color:#3dffa0; font-weight:900;'>{n}</div>
        <div style='font-size:10px; color:rgba(180,255,180,0.5); letter-spacing:1px;'>RÉPONSES COLLECTÉES</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

# ── NAVIGATION OFFICIELLE ─────────────────────────────────────────────────────
accueil   = st.Page("page_accueil.py",   title="🏠 Accueil & Formulaire",   default=True)
dashboard = st.Page("page_dashboard.py", title="📊 Tableau de bord")
analyses  = st.Page("page_analyses.py",  title="🔬 Analyses descriptives")
donnees   = st.Page("page_donnees.py",   title="🗄️ Données brutes")

pg = st.navigation([accueil, dashboard, analyses, donnees])
pg.run()
