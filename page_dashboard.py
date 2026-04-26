import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

DATA_FILE = "data/reponses.csv"
PLOTLY_THEME = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Rajdhani", color="#c8b0ff"), margin=dict(t=30, b=20, l=10, r=10))
COLORS = ["#b060ff","#3dffa0","#ff6bb0","#ffcc44","#60c8ff","#ff8c44","#c8ff44","#ff4444"]

st.markdown('<div style="font-family:Orbitron,monospace;font-size:1.5rem;font-weight:900;color:#fff;margin-bottom:0.3rem;">📊 Tableau de <span style="color:#b060ff;">Bord</span></div>', unsafe_allow_html=True)
st.markdown('<div style="font-size:13px;color:rgba(200,180,255,0.5);letter-spacing:1px;margin-bottom:1.5rem;">Vue d\'ensemble des données collectées en temps réel</div>', unsafe_allow_html=True)

if not os.path.exists(DATA_FILE):
    st.warning("⏳ Aucune donnée collectée. Soumettez des réponses via l'accueil.")
    st.stop()

df = pd.read_csv(DATA_FILE)
if df.empty:
    st.warning("⏳ Aucune donnée collectée pour l'instant.")
    st.stop()

# Métriques
c1, c2, c3, c4, c5 = st.columns(5)
metrics = [
    (len(df), "RÉPONSES TOTALES", "#b060ff"),
    (df["ville"].nunique(), "VILLES REPRÉSENTÉES", "#3dffa0"),
    (f"{round(df['note_communaute'].mean(),1)}/5", "NOTE MOY. COMMUNAUTÉ", "#ffcc44"),
    (f"{round(df['est_otaku'].isin(['Oui, totalement','Plutôt oui']).sum()/len(df)*100)}%", "SE DISENT OTAKU", "#b060ff"),
    (f"{round(df['stigmatise'].isin(['Oui, souvent','Oui, parfois']).sum()/len(df)*100)}%", "ONT ÉTÉ STIGMATISÉS", "#ff6b6b"),
]
for col, (val, label, color) in zip([c1,c2,c3,c4,c5], metrics):
    with col:
        st.markdown(f'<div class="metric-box"><div class="metric-num" style="color:{color};">{val}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Graphiques row 1
col1, col2, col3 = st.columns([1.2, 1.2, 1])
with col1:
    st.markdown('<div class="chart-card"><div class="chart-title">RÉPARTITION PAR GENRE</div>', unsafe_allow_html=True)
    gc = df["genre"].value_counts().reset_index(); gc.columns = ["Genre","Nombre"]
    fig = px.pie(gc, names="Genre", values="Nombre", color_discrete_sequence=COLORS, hole=0.5)
    fig.update_layout(**PLOTLY_THEME); fig.update_traces(textfont_color="#fff", textfont_size=13)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-card"><div class="chart-title">TRANCHE D\'ÂGE</div>', unsafe_allow_html=True)
    age_order = ["Moins de 15 ans","15–18 ans","19–24 ans","25–30 ans","31–40 ans","Plus de 40 ans"]
    ac = df["age"].value_counts().reindex(age_order, fill_value=0).reset_index(); ac.columns = ["Âge","Nombre"]
    fig2 = px.bar(ac, x="Âge", y="Nombre", color="Âge", color_discrete_sequence=COLORS)
    fig2.update_layout(**PLOTLY_THEME, showlegend=False); fig2.update_xaxes(tickangle=-30, tickfont_size=10)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="chart-card"><div class="chart-title">IDENTITÉ OTAKU</div>', unsafe_allow_html=True)
    oc = df["est_otaku"].value_counts().reset_index(); oc.columns = ["Statut","Nombre"]
    fig3 = px.pie(oc, names="Statut", values="Nombre", color_discrete_sequence=COLORS, hole=0.4)
    fig3.update_layout(**PLOTLY_THEME); fig3.update_traces(textfont_color="#fff", textfont_size=11)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Graphiques row 2
col4, col5 = st.columns([1.5, 1])
with col4:
    st.markdown('<div class="chart-card"><div class="chart-title">TOP VILLES</div>', unsafe_allow_html=True)
    vc = df["ville"].value_counts().head(8).reset_index(); vc.columns = ["Ville","Nombre"]
    fig4 = px.bar(vc, x="Nombre", y="Ville", orientation="h", color="Nombre", color_continuous_scale=["#3d00a0","#b060ff","#3dffa0"])
    fig4.update_layout(**PLOTLY_THEME, coloraxis_showscale=False)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="chart-card"><div class="chart-title">HEURES/SEMAINE</div>', unsafe_allow_html=True)
    ho = ["Moins de 2h","2–5h","6–10h","11–20h","Plus de 20h"]
    hc = df["heures_semaine"].value_counts().reindex(ho, fill_value=0).reset_index(); hc.columns = ["Heures","Nombre"]
    fig5 = px.funnel(hc, x="Nombre", y="Heures", color_discrete_sequence=["#b060ff"])
    fig5.update_layout(**PLOTLY_THEME)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Note communauté
st.markdown('<div class="chart-card"><div class="chart-title">NOTE D\'ORGANISATION DE LA COMMUNAUTÉ</div>', unsafe_allow_html=True)
col6, col7 = st.columns([2, 1])
with col6:
    nc = df["note_communaute"].value_counts().sort_index().reset_index(); nc.columns = ["Note","Nombre"]
    fig6 = px.bar(nc, x="Note", y="Nombre", color="Note", color_continuous_scale=["#ff4444","#ff8c44","#ffcc44","#3dffa0","#00cc77"])
    fig6.update_layout(**PLOTLY_THEME, coloraxis_showscale=False)
    st.plotly_chart(fig6, use_container_width=True)
with col7:
    avg = df["note_communaute"].mean()
    fig7 = go.Figure(go.Indicator(
        mode="gauge+number", value=avg, domain={"x":[0,1],"y":[0,1]},
        gauge={"axis":{"range":[1,5]},"bar":{"color":"#b060ff"},"bgcolor":"rgba(0,0,0,0)",
               "steps":[{"range":[1,2],"color":"rgba(255,68,68,0.2)"},{"range":[2,3],"color":"rgba(255,200,68,0.2)"},
                        {"range":[3,4],"color":"rgba(61,255,160,0.15)"},{"range":[4,5],"color":"rgba(61,255,160,0.3)"}]},
        number={"suffix":"/5","font":{"color":"#b060ff","size":36,"family":"Orbitron"}},
        title={"text":"Moyenne","font":{"color":"#c8b0ff","size":13}}
    ))
    fig7.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#c8b0ff"), height=200, margin=dict(t=20,b=10,l=10,r=10))
    st.plotly_chart(fig7, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Avenir
st.markdown('<div class="chart-card"><div class="chart-title">VISION DE L\'AVENIR</div>', unsafe_allow_html=True)
av = df["avenir_culture"].value_counts().reset_index(); av.columns = ["Vision","Nombre"]
fig8 = px.bar(av, x="Vision", y="Nombre", color="Vision", color_discrete_sequence=COLORS)
fig8.update_layout(**PLOTLY_THEME, showlegend=False)
st.plotly_chart(fig8, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.caption("🔄 Rafraîchis la page pour voir les nouvelles réponses")
