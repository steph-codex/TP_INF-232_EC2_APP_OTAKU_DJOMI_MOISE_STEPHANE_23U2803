import streamlit as st
import pandas as pd
import os

DATA_FILE = "data/reponses.csv"

st.markdown('<div style="font-family:Orbitron,monospace;font-size:1.5rem;font-weight:900;color:#fff;margin-bottom:0.3rem;">🗄️ Données <span style="color:#ffcc44;">Brutes</span></div>', unsafe_allow_html=True)
st.markdown('<div style="font-size:13px;color:rgba(200,180,255,0.5);letter-spacing:1px;margin-bottom:1.5rem;">Toutes les réponses · Filtrage · Export CSV</div>', unsafe_allow_html=True)

if not os.path.exists(DATA_FILE):
    st.warning("⏳ Aucune donnée collectée pour l'instant.")
    st.stop()

df = pd.read_csv(DATA_FILE)
if df.empty:
    st.warning("⏳ Aucune réponse enregistrée.")
    st.stop()

# Métriques
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div style="background:rgba(160,80,255,0.08);border:1px solid rgba(160,80,255,0.25);border-radius:10px;padding:1rem;text-align:center;"><div style="font-family:Orbitron,monospace;font-size:2rem;color:#b060ff;">{len(df)}</div><div style="font-size:11px;color:rgba(200,180,255,0.5);letter-spacing:1px;">RÉPONSES</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div style="background:rgba(61,255,160,0.06);border:1px solid rgba(61,255,160,0.25);border-radius:10px;padding:1rem;text-align:center;"><div style="font-family:Orbitron,monospace;font-size:2rem;color:#3dffa0;">{len(df.columns)}</div><div style="font-size:11px;color:rgba(180,255,180,0.5);letter-spacing:1px;">VARIABLES</div></div>', unsafe_allow_html=True)
with c3:
    last = str(df["timestamp"].iloc[-1])[:16] if "timestamp" in df.columns else "–"
    st.markdown(f'<div style="background:rgba(255,200,68,0.06);border:1px solid rgba(255,200,68,0.25);border-radius:10px;padding:1rem;text-align:center;"><div style="font-family:Orbitron,monospace;font-size:1rem;color:#ffcc44;">{last}</div><div style="font-size:11px;color:rgba(255,200,68,0.5);letter-spacing:1px;">DERNIÈRE RÉPONSE</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Filtres
with st.expander("🎛️ FILTRES"):
    fc1, fc2 = st.columns(2)
    with fc1: f_ville = st.selectbox("Ville", ["Toutes"] + sorted(df["ville"].dropna().unique().tolist()))
    with fc2: f_genre = st.selectbox("Genre", ["Tous"] + sorted(df["genre"].dropna().unique().tolist()))

dff = df.copy()
if f_ville != "Toutes": dff = dff[dff["ville"] == f_ville]
if f_genre != "Tous": dff = dff[dff["genre"] == f_genre]

# Tableau résumé
cols_display = [c for c in ["timestamp","genre","age","ville","est_otaku","heures_semaine","famille_accepte","stigmatise","note_communaute","avenir_culture"] if c in dff.columns]
st.dataframe(dff[cols_display].reset_index(drop=True), use_container_width=True, height=400)

st.markdown("<br>", unsafe_allow_html=True)

# Export
csv = dff.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ TÉLÉCHARGER LES DONNÉES COMPLÈTES (CSV)", data=csv, file_name="otaku_cameroun_donnees.csv", mime="text/csv", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div style="font-family:Orbitron,monospace;font-size:11px;color:#3dffa0;letter-spacing:2px;margin-bottom:0.8rem;">TOUTES LES COLONNES</div>', unsafe_allow_html=True)
st.dataframe(dff.reset_index(drop=True), use_container_width=True, height=300)
