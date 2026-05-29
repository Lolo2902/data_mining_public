import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

    # Qualite des donnees
    st.subheader("Qualité des données")
    st.caption("Données officielles du CNC, mises à jour automatiquement via l'API data.culture.gouv.fr.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Cinémas", len(df_cinema))
    col2.metric("Variables", df_cinema.shape[1])
    col3.metric("Art & Essai", f"{(df_cinema['ae'] == 'OUI').mean():.0%}")
    col4.metric("Non Art & Essai", f"{(df_cinema['ae'] == 'NON').mean():.0%}")

    # Top 5 colonnes avec le plus de valeurs manquantes
    manquantes = df_cinema.isnull().sum().sort_values(ascending=False).head(5)
    manquantes = manquantes[manquantes > 0]
    if len(manquantes) > 0:
        st.markdown("**Valeurs manquantes principales :**")
        tableau_manquantes = pd.DataFrame({
            'Colonne': manquantes.index,
            'Nb manquantes': manquantes.values,
            '% du total': (manquantes.values / len(df_cinema) * 100).round(1),
        })
        st.dataframe(tableau_manquantes, hide_index=True, use_container_width=True)
        st.caption(
            "Les colonnes très incomplètes (programmateur, label_art_et_essai) "

        )

    st.divider()

    # Tableau récap par zone
    st.subheader("Répartition des cinémas par zone")
    st.dataframe(description_zones(df_cinema), hide_index=True, use_container_width=True)

    # Graphique : part de marche moyenne par profil (Art & Essai OUI / NON)
    st.subheader("Part de marché moyenne par profil")
    st.caption("Comparaison des parts de marché entre les cinémas Art & Essai et les autres.")


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

    # Heatmap des correlations entre variables numeriques
    st.subheader("Corrélations entre variables")
    st.caption("Plus la couleur est foncée, plus les 2 variables varient ensemble (1 = lien parfait, 0 = aucun lien).")

    st.markdown(
        "**Ce que la heatmap nous apprend :**\n"
        "- Les **grands cinémas (multiplexes)** programment plus de films américains et moins de français. "
        "Les **petits cinémas** font l'inverse.\n"
        "- **Population** : on pourrait penser qu'une grosse ville = gros cinéma, mais le lien est faible."
    )

    # Noms plus courts pour que le graphique soit lisible
    noms_courts = {
        'pdm_en_entrees_des_films_francais': 'PdM français',
        'pdm_en_entrees_des_films_americains': 'PdM américains',
        'pdm_en_entrees_des_films_europeens': 'PdM européens',
        'nombre_de_films_programmes': 'Nb films',
        'nombre_de_films_inedits': 'Nb inédits',
        'ecrans': 'Écrans',
        'fauteuils': 'Fauteuils',
        'population_de_la_commune': 'Population',
    }
    corr = df_cinema[colonnes_num].rename(columns=noms_courts).corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlBu_r", center=0, ax=ax)
    st.pyplot(fig)

    st.success(
        "**Conclusion — le cinéma Art & Essai typique ressemblerait à :**\n"
        "- Petit (peu d'écrans, peu de fauteuils)\n"
        "- Forte PdM française\n"
        "- Faible PdM américaine\n"
        "- Programme peut-être moins de films au total"
    )
