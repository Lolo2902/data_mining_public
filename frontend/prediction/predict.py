import pandas as pd

def predire(arbre, foret, X_user):
    pred_arbre = arbre.predict(X_user)[0]
    proba_arbre = arbre.predict_proba(X_user)[0]
    pred_foret = foret.predict(X_user)[0]
    proba_foret = foret.predict_proba(X_user)[0]

    classes = list(arbre.classes_)
    idx_oui = classes.index('OUI')

    resultats = pd.DataFrame({
        "Modele": ["Arbre simple", "Random Forest"],
        "Prediction": [pred_arbre, pred_foret],
        "Proba OUI": [f"{proba_arbre[idx_oui]:.0%}", f"{proba_foret[idx_oui]:.0%}"],
        "Proba NON": [f"{proba_arbre[1 - idx_oui]:.0%}", f"{proba_foret[1 - idx_oui]:.0%}"],
    })
    return pred_arbre, pred_foret, proba_arbre, proba_foret, idx_oui, resultats

