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

    # =============================================
    # ETAPE 1 : choisir les parametres et entrainer
    # =============================================
    st.subheader("Étape 1 — Paramètres des modèles")

    max_depth = st.slider(
        "Profondeur maximale de l'arbre de décision",
        min_value=1, max_value=20, value=4,
    )
    n_estimators = st.slider(
        "Nombre d'arbres dans la Random Forest",
        min_value=10, max_value=300, value=100, step=10,
    )

    entrainer = st.button("Entraîner les modèles", use_container_width=True)

    # Quand on clique sur le bouton, on entraine les modeles
    # et on les met en memoire (st.session_state) pour les reutiliser plus tard.
    if entrainer:
        arbre, foret, colonnes_modele, _ = entrainer_modeles(max_depth, n_estimators)
        st.session_state["arbre"] = arbre
        st.session_state["foret"] = foret
        st.session_state["colonnes_modele"] = colonnes_modele
        st.success(
            f"Modèles entraînés avec profondeur = {max_depth} et nb d'arbres = {n_estimators}"
        )

    st.divider()

    # =============================================
    # ETAPE 2 : remplir le formulaire et predire
    # =============================================
    st.subheader("Étape 2 — Caractéristiques du cinéma")

    # On affiche le formulaire seulement si les modeles ont deja ete entraines
    if "arbre" not in st.session_state:
        st.info("Réglez les paramètres ci-dessus puis cliquez sur **Entraîner les modèles** pour commencer.")
    else:
        pdm_fr = st.slider("% films français", 0, 100, 40)
        pdm_us = st.slider("% films américains", 0, 100, 40)
        pdm_eu = st.slider("% films européens", 0, 100, 10)
        nb_films = st.slider("Nombre de films programmés", 0, 500, 100)
        nb_inedits = st.slider("Nombre de films inédits", 0, 300, 50)
        ecrans = st.slider("Nombre d'écrans", 1, 30, 3)
        fauteuils = st.slider("Nombre de fauteuils", 20, 8000, 500)
        population = st.number_input("Population de la commune", 0, 3000000, 10000)
        multiplexe = st.selectbox("Multiplexe ?", ["NON", "OUI"])

        # Zones : on affiche le libelle complet, on garde la premiere lettre pour le modele
        zones = ["B - Banlieue", "C - Centre-ville", "I - Intermédiaire", "R - Rural"]
        zone_choisie = st.selectbox("Zone de la commune", zones)
        zone = zone_choisie[0]

        lancer = st.button("Lancer la prédiction", use_container_width=True)

        if lancer:
            # On recupere les modeles entraines plus tot
            arbre = st.session_state["arbre"]
            foret = st.session_state["foret"]
            colonnes_modele = st.session_state["colonnes_modele"]

            # Preparer la ligne d'entree et lancer les 2 modeles
            X_user = construire_entree(
                colonnes_modele,
                pdm_fr, pdm_us, pdm_eu, nb_films, nb_inedits,
                ecrans, fauteuils, population, multiplexe, zone,
            )
            pred_arbre, pred_foret, proba_arbre, proba_foret, idx_oui, resultats = predire(arbre, foret, X_user)

            # Probabilite Art & Essai selon chaque modele
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
