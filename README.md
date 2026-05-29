# Prédiction Art & Essai 🎬

Application Streamlit qui prédit si un cinéma a un profil **Art & Essai** à partir de ses caractéristiques (programmation, taille de la salle, localisation, etc.).

## Données

Les données proviennent de l'API du **CNC** (Centre National du Cinéma) :
[etablissements-cinematographiques](https://data.culture.gouv.fr/explore/dataset/etablissements-cinematographiques/)

Elles sont chargées automatiquement au lancement de l'app (puis mises en cache).

## Modèles

Deux modèles de classification sont entraînés et comparés :

- **Arbre de décision** (`DecisionTreeClassifier`, profondeur max 4)
- **Random Forest** (`RandomForestClassifier`, 100 arbres)

Les variables utilisées :

- Parts de marché des films français / américains / européens
- Nombre de films programmés et inédits
- Nombre d'écrans et de fauteuils
- Population de la commune
- Multiplexe (OUI/NON)
- Zone de la commune (Banlieue / Centre-ville / Intermédiaire / Rural)

## Utilisation

L'utilisateur renseigne les caractéristiques d'un cinéma via des sliders et menus déroulants, puis clique sur **« Lancer la prediction »**. L'app affiche :

- La prédiction de chaque modèle (OUI / NON)
- Les probabilités associées
- Un indicateur de cohérence entre les deux modèles

## Prérequis

- Python 3.10+
- Bibliothèques : `streamlit`, `pandas`, `requests`, `scikit-learn`

Installation des dépendances :

```bash
pip install streamlit pandas requests scikit-learn
```

## Lancement

```bash
python -m streamlit run app.py --server.port 8502
```

L'app est ensuite accessible sur [http://localhost:8502](http://localhost:8502).

## Structure du projet

```
data_mining/
├── app.py        # Application Streamlit
├── test.ipynb    # Notebook d'exploration / tests
└── README.md
```
