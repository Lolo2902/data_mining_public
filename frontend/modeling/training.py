from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from frontend.processing.data_manager import charger_donnees
from frontend.processing.preprocessing import preparer_donnees
from frontend.modeling.models_params import ARBRE_PARAMS, FORET_PARAMS

def entrainer_modeles():
    df = charger_donnees()
    X_train, _, y_train, _, colonnes_modele = preparer_donnees(df)

    arbre = DecisionTreeClassifier(**ARBRE_PARAMS).fit(X_train, y_train)
    foret = RandomForestClassifier(**FORET_PARAMS).fit(X_train, y_train)

    return arbre, foret, colonnes_modele, df
