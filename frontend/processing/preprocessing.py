import pandas as pd
from sklearn.model_selection import train_test_split
from frontend.modeling.models_params import COLONNES_NUM, COLONNES_CAT, TARGET

def preparer_donnees(df):
    X = df[COLONNES_NUM + COLONNES_CAT].copy()
    y = df[TARGET]
    X = pd.get_dummies(X, columns=COLONNES_CAT, dtype=int)
    X = X.fillna(X.median(numeric_only=True))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test, X.columns.tolist()
