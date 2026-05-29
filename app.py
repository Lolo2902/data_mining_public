import streamlit as st
import pandas as pd

from frontend.modeling.training import entrainer_modeles
from frontend.processing.data_manager import charger_donnees
from frontend.prediction.inputs_manager import construire_entree
from frontend.prediction.predict import predire
from frontend.visualisation.visualisation import description_zones


st.set_page_config(
    page_title="Cinéma Art & Essai",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Chargement des données 
df_cinema = charger_donnees()


# Titre principal de la page
st.title("Ce cinéma a-t-il un profil Art & Essai ?")
st.caption("Prédiction basée sur les données du CNC — Centre national du cinéma")


# Menu de navigation 
page = st.sidebar.radio("Menu", ["Prédiction", "Statistiques descriptives"])


if page == "Prédiction":

    # Paramètres des modèles ML
    st.subheader("Paramètres des modèles")
    max_depth = st.slider("Profondeur maximale de l'arbre de décision", 1, 20, 4)
    n_estimators = st.slider("Nombre d'arbres dans la Random Forest", 10, 300, 100, step=10)

    st.divider()

    # Caractéristiques du cinéma à prédire
    st.subheader("Caractéristiques du cinéma")
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

    # Bouton pour lancer l'entrainement + la prediction
    lancer = st.button("Lancer la prédiction", use_container_width=True)

    if lancer:
        
        arbre, foret, colonnes_modele, _ = entrainer_modeles(max_depth, n_estimators)

       
        X_user = construire_entree(
            colonnes_modele,
            pdm_fr, pdm_us, pdm_eu, nb_films, nb_inedits,
            ecrans, fauteuils, population, multiplexe, zone,
        )
        pred_arbre, pred_foret, proba_arbre, proba_foret, idx_oui, resultats = predire(arbre, foret, X_user)

      
        proba_arbre_oui = float(proba_arbre[idx_oui])
        proba_foret_oui = float(proba_foret[idx_oui])

        st.write(f"**Arbre de décision** — probabilité Art & Essai : {proba_arbre_oui:.0%}")
        st.progress(proba_arbre_oui)

        st.write(f"**Random Forest** — probabilité Art & Essai : {proba_foret_oui:.0%}")
        st.progress(proba_foret_oui)

        st.divider()

    
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

    # Graphique : part de marche moyenne par profil (Art & Essai OUI / NON)
    st.subheader("Part de marché moyenne par profil")
    st.caption("Comparaison des parts de marché entre les cinémas Art & Essai et les autres.")

    # On separe les cinemas en 2 groupes
    cinemas_ae = df_cinema[df_cinema['ae'] == 'OUI']
    cinemas_non_ae = df_cinema[df_cinema['ae'] == 'NON']

    # On calcule la moyenne des parts de marche pour chaque groupe
    moyennes = pd.DataFrame({
        'Art & Essai': [
            cinemas_ae['pdm_en_entrees_des_films_francais'].mean(),
            cinemas_ae['pdm_en_entrees_des_films_americains'].mean(),
            cinemas_ae['pdm_en_entrees_des_films_europeens'].mean(),
        ],
        'Non Art & Essai': [
            cinemas_non_ae['pdm_en_entrees_des_films_francais'].mean(),
            cinemas_non_ae['pdm_en_entrees_des_films_americains'].mean(),
            cinemas_non_ae['pdm_en_entrees_des_films_europeens'].mean(),
        ],
    }, index=['Films français', 'Films américains', 'Films européens'])

    
    st.bar_chart(moyennes, color=["#e94560", "#d4af37"])

    # Stats descriptives 
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
