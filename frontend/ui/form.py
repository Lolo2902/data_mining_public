import streamlit as st
from frontend.modeling.models_params import ZONES_LABELS

def afficher_formulaire():
    return {
        "pdm_fr": st.slider("% films francais", 0, 100, 40),
        "pdm_us": st.slider("% films americains", 0, 100, 40),
        "pdm_eu": st.slider("% films europeens", 0, 100, 10),
        "nb_films": st.slider("Nombre de films programmes", 0, 500, 100),
        "nb_inedits": st.slider("Nombre de films inedits", 0, 300, 50),
        "ecrans": st.slider("Nombre d'ecrans", 1, 30, 3),
        "fauteuils": st.slider("Nombre de fauteuils", 20, 8000, 500),
        "population": st.number_input("Population de la commune", 0, 3000000, 10000),
        "multiplexe": st.selectbox("Multiplexe ?", ["NON", "OUI"]),
        "zone": st.selectbox(
            "Zone de la commune",
            options=list(ZONES_LABELS.keys()),
            format_func=lambda x: ZONES_LABELS[x],
        ),
    }
