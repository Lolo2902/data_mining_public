import pandas as pd

def construire_entree(colonnes_modele, pdm_fr, pdm_us, pdm_eu, nb_films,
                     nb_inedits, ecrans, fauteuils, population, multiplexe, zone):
    entree = {c: 0 for c in colonnes_modele}
    entree['pdm_en_entrees_des_films_francais'] = pdm_fr
    entree['pdm_en_entrees_des_films_americains'] = pdm_us
    entree['pdm_en_entrees_des_films_europeens'] = pdm_eu
    entree['nombre_de_films_programmes'] = nb_films
    entree['nombre_de_films_inedits'] = nb_inedits
    entree['ecrans'] = ecrans
    entree['fauteuils'] = fauteuils
    entree['population_de_la_commune'] = population
    entree[f'multiplexe_{multiplexe}'] = 1
    entree[f'zone_de_la_commune_{zone}'] = 1
    return pd.DataFrame([entree])[colonnes_modele]
