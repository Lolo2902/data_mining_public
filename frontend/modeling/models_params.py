COLONNES_NUM = [
    'pdm_en_entrees_des_films_francais',
    'pdm_en_entrees_des_films_americains',
    'pdm_en_entrees_des_films_europeens',
    'nombre_de_films_programmes',
    'nombre_de_films_inedits',
    'ecrans',
    'fauteuils',
    'population_de_la_commune',
]
COLONNES_CAT = ['multiplexe', 'zone_de_la_commune']
TARGET = 'ae'

ARBRE_PARAMS = {"max_depth": 4, "random_state": 42}
FORET_PARAMS = {"n_estimators": 100, "random_state": 42}

ZONES_LABELS = {
    "B": "B - Banlieue",
    "C": "C - Centre-ville",
    "I": "I - Intermediaire",
    "R": "R - Rural",
}
