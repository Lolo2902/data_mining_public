# Projet Data Mining — Cinémas Art & Essai 🎬

**App en ligne :** https://dataminingpublic-jywx2bjcrkdentlt49bbtc.streamlit.app/

## L'idée

À partir des données du **CNC** (Centre National du Cinéma), j'essaie de prédire si un cinéma a un profil **Art & Essai** ou non, en fonction de plusieurs critères : sa programmation, sa taille, sa localisation, etc.

Les données sont récupérées via une API publique :
https://data.culture.gouv.fr/explore/dataset/etablissements-cinematographiques/

## Ce que fait l'app

Il y a deux pages, accessibles depuis le menu à gauche :

- **Prédiction** : on remplit un petit formulaire (sliders + listes déroulantes) avec les caractéristiques d'un cinéma, et l'app dit s'il est probablement Art & Essai ou non.
- **Statistiques descriptives** : quelques chiffres et tableaux pour avoir une idée du parc de cinémas en France.

## Les modèles

J'ai entraîné deux modèles de classification avec scikit-learn :

- un **Arbre de décision**
- une **Random Forest**

Les deux donnent leur prédiction, et l'app indique si elles sont d'accord ou pas.

## Lancer l'app en local

```bash
pip install -r requirements.txt
python -m streamlit run app.py --server.port 8502
```

Puis ouvrir http://localhost:8502 dans le navigateur.

## Organisation du code

J'ai séparé le code en plusieurs dossiers pour que ce soit plus clair :

- `app.py` : l'app Streamlit principale (mise en page, onglets, formulaire)
- `frontend/processing/` : récupération et préparation des données
- `frontend/modeling/` : entraînement des modèles
- `frontend/prediction/` : prédiction à partir des entrées utilisateur
- `frontend/visualisation/` : tableau récap par zone

## Déploiement

L'app est déployée gratuitement sur **Streamlit Community Cloud**, qui est connecté à ce repo GitHub. Quand je fais un `git push`, l'app se met à jour automatiquement en ligne.
