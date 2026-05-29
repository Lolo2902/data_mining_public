from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from frontend.processing.data_manager import charger_donnees
from frontend.processing.preprocessing import preparer_donnees

def entrainer_modeles(max_depth=4, n_estimators=100):
    df = charger_donnees()
    X_train, _, y_train, _, colonnes_modele = preparer_donnees(df)

    arbre = DecisionTreeClassifier(
        max_depth=max_depth, random_state=42
    ).fit(X_train, y_train)

    foret = RandomForestClassifier(
        n_estimators=n_estimators, random_state=42
    ).fit(X_train, y_train)

    return arbre, foret, colonnes_modele, df
