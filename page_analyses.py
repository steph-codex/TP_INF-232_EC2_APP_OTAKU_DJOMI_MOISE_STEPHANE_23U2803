import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import os

DATA_FILE = "data/reponses.csv"
PLOTLY_THEME = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Rajdhani", color="#c8b0ff"), margin=dict(t=30, b=20, l=10, r=10))
COLORS = ["#b060ff","#3dffa0","#ff6bb0","#ffcc44","#60c8ff","#ff8c44","#c8ff44","#ff4444","#aa44ff","#44ffcc"]

st.markdown('<div style="font-family:Orbitron,monospace;font-size:1.5rem;font-weight:900;color:#fff;margin-bottom:0.3rem;">🔬 <span style="color:#3dffa0;">Analyses</span> Descriptives</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size:13px;color:rgba(200,180,255,0.5);letter-spacing:1px;margin-bottom:1.5rem;">Exploration approfondie · Corrélations · Tendances</div>', unsafe_allow_html=True)

if not os.path.exists(DATA_FILE):
    st.warning("⏳ Aucune donnée disponible. Collectez d'abord des réponses via l'accueil.")
    st.stop()

df = pd.read_csv(DATA_FILE)
if df.empty or len(df) < 2:
    st.warning("⏳ Pas encore assez de données (minimum 2 réponses).")
    st.stop()

# Filtres
with st.expander("🎛️ FILTRES"):
    fc1, fc2, fc3 = st.columns(3)
    with fc1: f_ville = st.selectbox("Ville", ["Toutes"] + sorted(df["ville"].dropna().unique().tolist()))
    with fc2: f_age = st.selectbox("Âge", ["Tous"] + sorted(df["age"].dropna().unique().tolist()))
    with fc3: f_genre = st.selectbox("Genre", ["Tous"] + sorted(df["genre"].dropna().unique().tolist()))

dff = df.copy()
if f_ville != "Toutes": dff = dff[dff["ville"] == f_ville]
if f_age != "Tous": dff = dff[dff["age"] == f_age]
if f_genre != "Tous": dff = dff[dff["genre"] == f_genre]
st.markdown(f'<div style="font-size:12px;color:rgba(61,255,160,0.7);margin-bottom:1rem;">✅ {len(dff)} réponse(s) analysée(s)</div>', unsafe_allow_html=True)

# Découverte & profils
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="chart-card"><div class="chart-title">MODE DE DÉCOUVERTE</div>', unsafe_allow_html=True)
    dec = dff["decouverte"].value_counts().reset_index(); dec.columns = ["Mode","Nombre"]
    fig = px.bar(dec, x="Nombre", y="Mode", orientation="h", color="Nombre", color_continuous_scale=["#3d00a0","#b060ff","#3dffa0"])
    fig.update_layout(**PLOTLY_THEME, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
    if len(dec) > 0:
        st.markdown(f'<div class="insight-box">💡 Découverte via <strong>{dec.iloc[0]["Mode"]}</strong> la plus fréquente.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-card"><div class="chart-title">PROFIL DANS LA COMMUNAUTÉ</div>', unsafe_allow_html=True)
    profil = dff["profil_otaku"].dropna().value_counts().reset_index(); profil.columns = ["Profil","Nombre"]
    fig2 = px.pie(profil, names="Profil", values="Nombre", color_discrete_sequence=COLORS, hole=0.45)
    fig2.update_layout(**PLOTLY_THEME); fig2.update_traces(textfont_color="#fff", textfont_size=12)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Genres anime
st.markdown('<div class="chart-card"><div class="chart-title">GENRES D\'ANIME LES PLUS POPULAIRES</div>', unsafe_allow_html=True)
all_genres = []
for val in dff["genres_preferes"].dropna():
    all_genres.extend([g.strip() for g in str(val).split(",") if g.strip()])
if all_genres:
    gdf = pd.DataFrame(Counter(all_genres).most_common(), columns=["Genre","Votes"])
    fig3 = px.bar(gdf, x="Genre", y="Votes", color="Votes", color_continuous_scale=["#3d00a0","#b060ff","#3dffa0"])
    fig3.update_layout(**PLOTLY_THEME, coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown(f'<div class="insight-box">🎌 Genre dominant : <strong>{gdf.iloc[0]["Genre"]}</strong></div>', unsafe_allow_html=True)
else:
    st.info("Pas encore de données sur les genres.")
st.markdown('</div>', unsafe_allow_html=True)

# Plateformes
st.markdown('<div class="chart-card"><div class="chart-title">PLATEFORMES DE CONSOMMATION</div>', unsafe_allow_html=True)
all_plat = []
for val in dff["plateformes"].dropna():
    all_plat.extend([p.strip() for p in str(val).split(",") if p.strip()])
if all_plat:
    pdf2 = pd.DataFrame(Counter(all_plat).most_common(), columns=["Plateforme","Utilisateurs"])
    cp1, cp2 = st.columns([2,1])
    with cp1:
        fig4 = px.bar(pdf2, x="Utilisateurs", y="Plateforme", orientation="h", color="Utilisateurs", color_continuous_scale=["#3d00a0","#b060ff","#3dffa0"])
        fig4.update_layout(**PLOTLY_THEME, coloraxis_showscale=False)
        st.plotly_chart(fig4, use_container_width=True)
    with cp2:
        fig5 = px.pie(pdf2.head(5), names="Plateforme", values="Utilisateurs", color_discrete_sequence=COLORS, hole=0.4)
        fig5.update_layout(**PLOTLY_THEME); fig5.update_traces(textfont_color="#fff", textfont_size=11)
        st.plotly_chart(fig5, use_container_width=True)
else:
    st.info("Pas encore de données sur les plateformes.")
st.markdown('</div>', unsafe_allow_html=True)

# Impact social
col3, col4 = st.columns(2)
with col3:
    st.markdown('<div class="chart-card"><div class="chart-title">ACCEPTATION FAMILIALE</div>', unsafe_allow_html=True)
    fam = dff["famille_accepte"].value_counts().reset_index(); fam.columns = ["Réponse","Nombre"]
    cmap = {"Oui, totalement":"#3dffa0","Partiellement (ils tolèrent)":"#ffcc44","Non, ils désapprouvent":"#ff4444","Ils ne savent pas":"#888"}
    fig6 = px.pie(fam, names="Réponse", values="Nombre", color="Réponse", color_discrete_map=cmap, hole=0.45)
    fig6.update_layout(**PLOTLY_THEME); fig6.update_traces(textfont_color="#fff", textfont_size=11)
    st.plotly_chart(fig6, use_container_width=True)
    pct = round(dff["famille_accepte"].eq("Oui, totalement").sum()/len(dff)*100) if len(dff)>0 else 0
    st.markdown(f'<div class="insight-box">👨‍👩‍👧 <strong>{pct}%</strong> ont une famille totalement acceptante.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="chart-card"><div class="chart-title">STIGMATISATION SOCIALE</div>', unsafe_allow_html=True)
    stig = dff["stigmatise"].value_counts().reset_index(); stig.columns = ["Réponse","Nombre"]
    scmap = {"Oui, souvent":"#ff4444","Oui, parfois":"#ff8c44","Rarement":"#ffcc44","Non, jamais":"#3dffa0"}
    fig7 = px.bar(stig, x="Réponse", y="Nombre", color="Réponse", color_discrete_map=scmap)
    fig7.update_layout(**PLOTLY_THEME, showlegend=False)
    st.plotly_chart(fig7, use_container_width=True)
    pct2 = round(dff["stigmatise"].isin(["Oui, souvent","Oui, parfois"]).sum()/len(dff)*100) if len(dff)>0 else 0
    st.markdown(f'<div class="insight-box">⚠️ <strong>{pct2}%</strong> ont subi de la stigmatisation.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Stats descriptives note
st.markdown('<div class="chart-card"><div class="chart-title">STATISTIQUES DESCRIPTIVES — NOTE COMMUNAUTÉ</div>', unsafe_allow_html=True)
notes = dff["note_communaute"].dropna()
if len(notes) > 0:
    cols_s = st.columns(5)
    stats = [("MOYENNE", round(notes.mean(),2),"#b060ff"), ("MÉDIANE", round(notes.median(),2),"#3dffa0"),
             ("ÉCART-TYPE", round(notes.std(),2),"#ffcc44"), ("MIN", int(notes.min()),"#ff6bb0"), ("MAX", int(notes.max()),"#60c8ff")]
    for col, (label, val, clr) in zip(cols_s, stats):
        with col:
            st.markdown(f'<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(160,80,255,0.2);border-radius:8px;padding:1rem;text-align:center;"><div style="font-family:Orbitron,monospace;font-size:1.5rem;font-weight:900;color:{clr};">{val}</div><div style="font-size:11px;color:rgba(200,180,255,0.5);letter-spacing:1px;margin-top:4px;">{label}</div></div>', unsafe_allow_html=True)
    fig9 = px.histogram(notes, nbins=5, color_discrete_sequence=["#b060ff"], labels={"value":"Note /5","count":"Nombre"})
    fig9.update_layout(**PLOTLY_THEME)
    st.plotly_chart(fig9, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Témoignages
conceptions = dff["conception_libre"].dropna().str.strip()
conceptions = conceptions[conceptions != ""]
if not conceptions.empty:
    st.markdown('<div class="chart-card"><div class="chart-title">TÉMOIGNAGES — ÊTRE OTAKU AU CAMEROUN</div>', unsafe_allow_html=True)
    for txt in conceptions.head(8):
        st.markdown(f'<div style="background:rgba(160,80,255,0.06);border-left:3px solid #b060ff;border-radius:0 8px 8px 0;padding:0.8rem 1rem;margin-bottom:0.6rem;font-size:14px;color:rgba(220,210,255,0.85);font-style:italic;">« {txt} »</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
