# 🔋 Détection prédictive des défauts qualité des cellules de batteries

## 📌 Présentation du projet

Ce projet a été développé dans le cadre d'une thèse professionnelle en Mastère Data et Intelligence Artificielle à Nexa Campus Bordeaux.

Il s'inscrit dans le contexte industriel d'Automotive Cells Company (ACC) et vise à développer une solution d'aide à la décision permettant de prédire les risques de défauts qualité sur des cellules de batteries électriques.

**Le projet constitue une preuve de concept (POC)** basée sur un jeu de données synthétique. Aucune donnée industrielle confidentielle d'ACC n'a été utilisée.

## 🎯 Objectifs

- Analyser et préparer les données de contrôle qualité.
- Structurer les données dans une base SQLite.
- Construire et comparer plusieurs modèles de classification supervisée.
- Identifier les variables influençant la prédiction.
- Développer une application web avec Streamlit.
- Permettre des prédictions individuelles ou à partir de fichiers CSV.

## 📊 Dataset

**Source :** [EV Battery QC Synthetic Defect Dataset — Kaggle](https://www.kaggle.com/datasets/kanchana1990/ev-battery-qc-synthetic-defect-dataset)

- 20 000 observations
- 14 variables initiales
- Format CSV
- Données synthétiques

La variable cible `Has_Defect` correspond à :

- `0` : cellule conforme
- `1` : cellule présentant un défaut qualité

## 🛠️ Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python | Développement et analyse |
| Pandas / NumPy | Manipulation des données |
| SQLite | Stockage et structuration |
| Scikit-learn | Machine learning |
| Joblib | Sauvegarde du modèle |
| Streamlit | Application web |
| Matplotlib | Visualisation |

## 🧠 Modélisation

Quatre modèles supervisés ont été comparés :

- Logistic Regression
- Decision Tree
- K-Nearest Neighbors
- Random Forest

**Modèle retenu : Random Forest Classifier**

| Métrique | Résultat |
|---|---:|
| Accuracy | 98,42 % |
| Précision — défaut | 98,33 % |
| Rappel — défaut | 92,57 % |
| F1-score — défaut | 95,36 % |

Ces résultats ont été obtenus sur le jeu de test synthétique et ne constituent pas une validation industrielle.

## 🖥️ Fonctionnalités de l'application

L'application Streamlit comporte quatre pages :

1. **Prédiction manuelle :** saisie des caractéristiques d'une cellule et estimation du risque de défaut.
2. **Prédiction par fichier :** import d'un CSV, prédictions multiples et téléchargement des résultats.
3. **Dashboard dataset :** exploration des observations et indicateurs descriptifs.
4. **Informations projet :** présentation du modèle, des limites et des mesures de protection des données.

## 🚀 Installation et exécution

### Prérequis

- Python et pip installés
- Accès à un terminal
- Navigateur web
- Fichiers du modèle et du dataset présents dans les dossiers correspondants

### Installation

Cloner le dépôt :

```bash
git clone https://github.com/OuissalMasbahi/Projet.git
cd Projet
```

Installer les dépendances :

```bash
python3 -m pip install -r requirements.txt
```

### Lancement de l'application

```bash
python3 -m streamlit run app.py
```

Ouvrir ensuite :

http://localhost:8501

L'application est exécutée localement : cette adresse n'est pas un lien public accessible à distance.

## 📁 Structure du projet

```text
Projet/
├── app.py
├── requirements.txt
├── README.md
├── 01_exploitation_donnees_batterie.ipynb
├── data/
│   └── ev_battery_qc_data_2026_kaggle.csv
├── models/
│   └── best_battery_defect_model.pkl
├── outputs/
│   └── battery_qc.sqlite
└── figures/
```

## 🔒 Sécurité et limites

- Données synthétiques et publiques.
- Aucune donnée personnelle ou confidentielle ACC.
- Application destinée à la démonstration.
- Validation humaine nécessaire avant toute décision qualité.
- Utilisation de données industrielles réelles et validation métier indispensables avant une éventuelle mise en production.

L'application ne nécessite pas d'identifiants de test ni de compte administrateur dans sa version actuelle.

## 🚀 Perspectives

- Intégration de données industrielles réelles, sous réserve d'autorisation.
- Connexion à une base de données centralisée.
- Authentification des utilisateurs.
- Surveillance des performances et de la dérive du modèle.
- Prédiction du type exact de défaut.

## 👩‍💻 Auteure

**Ouissal MASBAHI**  
Mastère Data et Intelligence Artificielle — Nexa Campus Bordeaux  
Thèse professionnelle 2025–2026
