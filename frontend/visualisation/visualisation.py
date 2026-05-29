import pandas as pd

def description_zones(df_cinema):
    return pd.DataFrame({
        'code': ['C', 'B', 'I', 'R'],
        'signification': [
            'Centre-ville (grande agglomeration)',
            'Banlieue (grande agglomeration)',
            'Intermediaire (ville moyenne)',
            'Rural (petite commune, campagne)',
        ],
        'nb_cinemas': [
            (df_cinema['zone_de_la_commune'] == 'C').sum(),
            (df_cinema['zone_de_la_commune'] == 'B').sum(),
            (df_cinema['zone_de_la_commune'] == 'I').sum(),
            (df_cinema['zone_de_la_commune'] == 'R').sum(),
        ],
    })
