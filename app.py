import streamlit as st

from frontend.modeling.training import entrainer_modeles
from frontend.ui.form import afficher_formulaire
from frontend.prediction.inputs_manager import construire_entree
from frontend.prediction.predict import predire
from frontend.visualisation.visualisation import description_zones



st.set_page_config(
    page_title="Cinéma Art & Essai",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("""
<style>
    /* Fond et texte général */
    .stApp { background-color: #1a1a2e; color: #e0e0e0; }

    /* Barre latérale */
    section[data-testid="stSidebar"] { background-color: #0f0f1e; }

    /* Titres en rose */
    h1, h2, h3 { color: #e94560; }

    /* Forcer le texte clair sur tous les labels (sinon il devient sombre au rerun) */
    label, p, span, .stMarkdown { color: #e0e0e0 !important; }

    /* Bouton */
    .stButton button {
        background-color: #e94560;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
    }
    .stButton button:hover { background-color: #c73650; }

    /* Valeurs min/max du slider : toujours affichées */
    [data-testid="stSliderTickBar"] { opacity: 1; }
</style>
""", unsafe_allow_html=True)



def afficher_proba(label, proba_oui):
    st.markdown(f"**{label}**")
    col_oui, col_non = st.columns(2)
    with col_oui:
        st.markdown("<p style='color:#e94560; font-size:0.9rem;'>Art & Essai</p>", unsafe_allow_html=True)
        st.progress(proba_oui)
        st.caption(f"{proba_oui:.1%}")
    with col_non:
        st.markdown("<p style='color:#888; font-size:0.9rem;'>Non Art & Essai</p>", unsafe_allow_html=True)
        st.progress(1 - proba_oui)
        st.caption(f"{1 - proba_oui:.1%}")


arbre, foret, colonnes_modele, df_cinema = entrainer_modeles()


st.title("Ce cinéma a-t-il un profil Art & Essai ?")
st.caption("Prédiction basée sur les données du CNC — Centre national du cinéma")


# Menu de navigation dans la barre latérale
page = st.sidebar.radio("Menu", ["Prédiction", "Statistiques descriptives"])


if page == "Prédiction":
    valeurs = afficher_formulaire()
    lancer = st.button("Lancer la prédiction", use_container_width=True)

    if lancer:
        X_user = construire_entree(colonnes_modele, **valeurs)
        pred_arbre, pred_foret, proba_arbre, proba_foret, idx_oui, resultats = predire(arbre, foret, X_user)

        # Barres de probabilité
        afficher_proba("Arbre de décision", proba_arbre[idx_oui])
        afficher_proba("Random Forest", proba_foret[idx_oui])

        st.divider()

        # Verdict
        if pred_arbre == pred_foret:
            if pred_arbre == "OUI":
                st.success("### Verdict : profil Art & Essai confirmé par les 2 modèles")
            else:
                st.error("### Verdict : ce cinéma n'a pas un profil Art & Essai")
        else:
            st.warning("### Les 2 modèles sont en désaccord — résultat incertain")

elif page == "Statistiques descriptives":
    st.subheader("Vue d'ensemble")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total cinémas", len(df_cinema))
    col2.metric("Art & Essai", f"{(df_cinema['ae'] == 'OUI').mean():.0%}")
    col3.metric("Multiplexes", f"{(df_cinema['multiplexe'] == 'OUI').mean():.0%}")

    st.subheader("Répartition des cinémas par zone")
    st.dataframe(description_zones(df_cinema), hide_index=True, use_container_width=True)

    st.subheader("Statistiques des variables numériques")
    st.dataframe(df_cinema[[
        'pdm_en_entrees_des_films_francais',
        'pdm_en_entrees_des_films_americains',
        'pdm_en_entrees_des_films_europeens',
        'nombre_de_films_programmes',
        'nombre_de_films_inedits',
        'ecrans',
        'fauteuils',
        'population_de_la_commune',
    ]].describe().round(1), use_container_width=True)
