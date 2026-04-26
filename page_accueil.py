import streamlit as st
import pandas as pd
import os
from datetime import datetime

DATA_FILE = "data/reponses.csv"
os.makedirs("data", exist_ok=True)

COLUMNS = [
    "timestamp","genre","age","ville","niveau",
    "est_otaku","annees_otaku","decouverte","profil_otaku",
    "genres_preferes","heures_semaine","plateformes",
    "famille_accepte","stigmatise","influences","evenement_cmr",
    "note_communaute","avenir_culture","depense_mensuelle",
    "conception_libre","email_contact"
]

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=COLUMNS)

def save_response(row: dict):
    df = load_data()
    new_row = pd.DataFrame([row])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

st.markdown("""
<div class="hero-banner">
    <div class="badge">INF 232 — EC2 — COLLECTE DE DONNÉES</div>
    <div class="hero-title">Culture <span>Otaku</span> au <span class="green">Cameroun</span></div>
    <div class="hero-sub">Formulaire de collecte · Analyse descriptive · Étude communautaire</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='font-family:Orbitron,monospace; font-size:14px; color:#c8b0ff; letter-spacing:2px; margin-bottom:1rem;'>
    📝 FORMULAIRE DE COLLECTE
</div>
""", unsafe_allow_html=True)

with st.form("otaku_form", clear_on_submit=True):
    st.markdown('<div class="section-card"><div class="section-head">01 — PROFIL DU RÉPONDANT</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        genre = st.selectbox("Genre *", ["", "Homme", "Femme", "Autre / Préfère ne pas préciser"])
        age = st.selectbox("Tranche d'âge *", ["", "Moins de 15 ans", "15–18 ans", "19–24 ans", "25–30 ans", "31–40 ans", "Plus de 40 ans"])
    with c2:
        ville = st.selectbox("Ville *", ["", "Yaoundé", "Douala", "Bafoussam", "Garoua", "Maroua", "Bamenda", "Ngaoundéré", "Bertoua", "Kribi", "Autre"])
        niveau = st.selectbox("Niveau d'études", ["", "Collège / Lycée", "Licence / BTS (en cours)", "Licence / BTS (obtenu)", "Master (en cours ou obtenu)", "Doctorat", "Autre"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-head">02 — IDENTITÉ OTAKU</div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        est_otaku = st.selectbox("Te considères-tu comme otaku ? *", ["", "Oui, totalement", "Plutôt oui", "Je consomme mais sans me revendiquer", "Non, pas du tout"])
        annees_otaku = st.selectbox("Depuis combien d'années ?", ["", "Moins d'1 an", "1–3 ans", "4–6 ans", "7–10 ans", "Plus de 10 ans"])
    with c4:
        decouverte = st.selectbox("Comment as-tu découvert l'anime ? *", ["", "À la télé (Cartoon Network, Club Dorothée…)", "Par des amis / famille", "Sur Internet (YouTube, TikTok…)", "Via les réseaux sociaux", "Autre"])
        profil_otaku = st.selectbox("Comment tu te définis ?", ["", "Casual (de temps en temps)", "Hardcore (très actif)", "Cosplayeur/Cosplayeuse", "Créateur de contenu", "Collectionneur"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-head">03 — CONSOMMATION DE CONTENU</div>', unsafe_allow_html=True)
    genres_options = ["Shonen (Naruto, DBZ, AOT…)", "Seinen (Tokyo Ghoul, Vinland Saga…)", "Isekai (Re:Zero, SAO…)", "Shojo / Romance", "Slice of Life", "Mecha / SF", "Horreur / Thriller", "Sport (Haikyuu, Kuroko…)"]
    genres_preferes = st.multiselect("Genres préférés (plusieurs choix possibles)", genres_options)
    c5, c6 = st.columns(2)
    with c5:
        heures = st.selectbox("Heures/semaine consacrées à l'anime/manga *", ["", "Moins de 2h", "2–5h", "6–10h", "11–20h", "Plus de 20h"])
    with c6:
        depense = st.selectbox("Dépenses mensuelles liées à l'otaku culture", ["", "0 FCFA (rien)", "1–2 000 FCFA", "2–5 000 FCFA", "5–15 000 FCFA", "Plus de 15 000 FCFA"])
    plat_options = ["Crunchyroll", "Netflix", "YouTube", "Telegram (groupes)", "Téléchargement direct", "Manga papier", "App manga (Manga Plus…)"]
    plateformes = st.multiselect("Plateformes utilisées (plusieurs choix)", plat_options)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-head">04 — IMPACT SOCIAL & PERSONNEL</div>', unsafe_allow_html=True)
    c7, c8 = st.columns(2)
    with c7:
        famille = st.selectbox("Ta famille accepte ta passion ? *", ["", "Oui, totalement", "Partiellement (ils tolèrent)", "Non, ils désapprouvent", "Ils ne savent pas"])
        stigma = st.selectbox("As-tu déjà été stigmatisé(e) ? *", ["", "Oui, souvent", "Oui, parfois", "Rarement", "Non, jamais"])
    with c8:
        evenement = st.selectbox("As-tu participé à un événement otaku au Cameroun ?", ["", "Oui, plusieurs fois", "Oui, une fois", "Non mais j'aimerais", "Non, pas intéressé(e)", "Je ne savais pas que ça existait"])
    influ_options = ["Orientation professionnelle / études", "Cercle social (amis via l'anime)", "Apprentissage du japonais", "Créativité (dessin, musique…)", "Valeurs et vision de la vie", "Aucune influence particulière"]
    influences = st.multiselect("La culture otaku a-t-elle influencé ta vie ? (plusieurs choix)", influ_options)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-head">05 — PERCEPTION & AVENIR</div>', unsafe_allow_html=True)
    note_comm = st.slider("Organisation de la communauté otaku camerounaise (1 = très désorganisée → 5 = très bien organisée) *", 1, 5, 3)
    avenir = st.selectbox("Quel avenir pour la culture otaku au Cameroun ? *", ["", "Elle va croître fortement", "Elle va rester stable", "Elle va décliner", "Je ne sais pas"])
    conception = st.text_area("En quelques mots, comment tu conçois le fait d'être otaku au Cameroun ?", placeholder="Exprime-toi librement…", height=100)
    email_contact = st.text_input("Ton email (facultatif — pour recevoir les résultats)", placeholder="toi@mail.com")
    st.markdown('</div>', unsafe_allow_html=True)

    submitted = st.form_submit_button("⛩️ SOUMETTRE MA RÉPONSE", use_container_width=True)

if submitted:
    errors = []
    if not genre: errors.append("Genre")
    if not age: errors.append("Âge")
    if not ville: errors.append("Ville")
    if not est_otaku: errors.append("Identité otaku")
    if not decouverte: errors.append("Mode de découverte")
    if not heures: errors.append("Heures/semaine")
    if not famille: errors.append("Acceptation familiale")
    if not stigma: errors.append("Stigmatisation")
    if not avenir: errors.append("Vision de l'avenir")
    if errors:
        st.error("⚠️ Champs obligatoires manquants : " + " · ".join(errors))
    else:
        row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "genre": genre, "age": age, "ville": ville, "niveau": niveau,
            "est_otaku": est_otaku, "annees_otaku": annees_otaku,
            "decouverte": decouverte, "profil_otaku": profil_otaku,
            "genres_preferes": ", ".join(genres_preferes),
            "heures_semaine": heures, "plateformes": ", ".join(plateformes),
            "famille_accepte": famille, "stigmatise": stigma,
            "influences": ", ".join(influences), "evenement_cmr": evenement,
            "note_communaute": note_comm, "avenir_culture": avenir,
            "depense_mensuelle": depense,
            "conception_libre": conception, "email_contact": email_contact
        }
        save_response(row)
        st.success("⛩️ Arigatou gozaimasu ! Ta réponse a été enregistrée.")
        st.balloons()
