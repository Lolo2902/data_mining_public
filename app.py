import streamlit as st

from frontend.modeling.training import entrainer_modeles
from frontend.processing.data_manager import charger_donnees
from frontend.prediction.inputs_manager import construire_entree
from frontend.prediction.predict import predire
from frontend.visualisation.visualisation import description_zones


# Configuration de la page (titre de l'onglet, icone, layout)
st.set_page_config(
    page_title="Cinéma Art & Essai",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Chargement des données (mises en cache automatiquement)
df_cinema = charger_donnees()


# Titre principal de la page
st.title("Ce cinéma a-t-il un profil Art & Essai ?")
st.caption("Prédiction basée sur les données du CNC — Centre national du cinéma")


# Menu de navigation dans la barre latérale (2 pages)
page = st.sidebar.radio("Menu", ["Prédiction", "Statistiques descriptives"])


if page == "Prédiction":

    # Paramètres des modèles ML (modifiables par l'utilisateur)
    with st.expander("Paramètres des modèles ML", expanded=False):
        max_depth = st.slider(
            "Arbre de décision — profondeur maximale",
            min_value=1, max_value=20, value=4,
            help="Plus la profondeur est grande, plus l'arbre est complexe (risque de surapprentissage).",
        )
        n_estimators = st.slider(
            "Random Forest — nombre d'arbres",
            min_value=10, max_value=300, value=100, step=10,
            help="Plus il y a d'arbres, plus la forêt est robuste (mais plus lente à entrainer).",
        )

    # Entrainement des modèles avec les paramètres choisis
    arbre, foret, colonnes_modele, _ = entrainer_modeles(max_depth, n_estimators)

    st.divider()

    # Formulaire de saisie : une variable par caractéristique
    pdm_fr = st.slider("% films français", 0, 100, 40)
    pdm_us = st.slider("% films américains", 0, 100, 40)
    pdm_eu = st.slider("% films européens", 0, 100, 10)
    nb_films = st.slider("Nombre de films programmés", 0, 500, 100)
    nb_inedits = st.slider("Nombre de films inédits", 0, 300, 50)
    ecrans = st.slider("Nombre d'écrans", 1, 30, 3)
    fauteuils = st.slider("Nombre de fauteuils", 20, 8000, 500)
    population = st.number_input("Population de la commune", 0, 3000000, 10000)
    multiplexe = st.selectbox("Multiplexe ?", ["NON", "OUI"])

    # Zones : on affiche le libellé complet, on garde la première lettre pour le modèle
    zones = ["B - Banlieue", "C - Centre-ville", "I - Intermédiaire", "R - Rural"]
    zone_choisie = st.selectbox("Zone de la commune", zones)
    zone = zone_choisie[0]

    lancer = st.button("Lancer la prédiction", use_container_width=True)

    if lancer:
        # Préparer la ligne d'entrée et lancer les 2 modèles
        X_user = construire_entree(
            colonnes_modele,
            pdm_fr, pdm_us, pdm_eu, nb_films, nb_inedits,
            ecrans, fauteuils, population, multiplexe, zone,
        )
        pred_arbre, pred_foret, proba_arbre, proba_foret, idx_oui, resultats = predire(arbre, foret, X_user)

        # Probabilité Art & Essai selon chaque modèle
        proba_arbre_oui = float(proba_arbre[idx_oui])
        proba_foret_oui = float(proba_foret[idx_oui])

        st.write(f"**Arbre de décision** — probabilité Art & Essai : {proba_arbre_oui:.0%}")
        st.progress(proba_arbre_oui)

        st.write(f"**Random Forest** — probabilité Art & Essai : {proba_foret_oui:.0%}")
        st.progress(proba_foret_oui)

        st.divider()

        # Verdict final
        if pred_arbre == pred_foret and pred_arbre == "OUI":
            st.success("Verdict : profil Art & Essai confirmé par les 2 modèles")
        elif pred_arbre == pred_foret and pred_arbre == "NON":
            st.error("Verdict : ce cinéma n'a pas un profil Art & Essai")
        else:
            st.warning("Les 2 modèles sont en désaccord — résultat incertain")


elif page == "Statistiques descriptives":

    # Quelques chiffres clés
    st.subheader("Vue d'ensemble")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total cinémas", len(df_cinema))
    col2.metric("Art & Essai", f"{(df_cinema['ae'] == 'OUI').mean():.0%}")
    col3.metric("Multiplexes", f"{(df_cinema['multiplexe'] == 'OUI').mean():.0%}")

    # Tableau récap par zone
    st.subheader("Répartition des cinémas par zone")
    st.dataframe(description_zones(df_cinema), hide_index=True, use_container_width=True)

    # Stats descriptives sur les variables numériques
    st.subheader("Statistiques des variables numériques")
    colonnes_num = [
        'pdm_en_entrees_des_films_francais',
        'pdm_en_entrees_des_films_americains',
        'pdm_en_entrees_des_films_europeens',
        'nombre_de_films_programmes',
        'nombre_de_films_inedits',
        'ecrans',
        'fauteuils',
        'population_de_la_commune',
    ]
    st.dataframe(df_cinema[colonnes_num].describe().round(1), use_container_width=True)
