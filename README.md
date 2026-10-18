# 🔋 Détection prédictive des défauts qualité des cellules de batteries

## 📌 Présentation du projet

Ce projet a été réalisé dans le cadre d'une thèse professionnelle en Mastère Data et Intelligence Artificielle à Nexa Campus Bordeaux.

Il s'inscrit dans le contexte industriel d'Automotive Cells Company (ACC) et vise à développer une solution d'aide à la décision permettant de prédire les risques de défauts qualité sur les cellules de batteries électriques.

**Il s'agit d'une preuve de concept (POC)** développée à partir de données synthétiques. Aucune donnée industrielle confidentielle d'ACC n'a été utilisée.

## 🌐 Accès au projet

**Application Streamlit publique :**

https://masbahi-ouissal-project.streamlit.app/

**Dépôt GitHub :**

https://github.com/OuissalMasbahi/OUISSAL_MASBAHI_PROJET

**URL de clonage :**

https://github.com/OuissalMasbahi/OUISSAL_MASBAHI_PROJET.git

L'application est accessible en ligne sans installation locale et ne nécessite pas de compte utilisateur.

## 🎯 Objectifs

- Analyser les données de contrôle qualité des batteries.
- Nettoyer et structurer les données dans SQLite.
- Construire et comparer plusieurs modèles supervisés.
- Prédire la conformité ou le risque de défaut d'une cellule.
- Développer une application Streamlit.
- Permettre des prédictions manuelles et par fichier CSV.

## 📊 Dataset

**Source :** [EV Battery QC Synthetic Defect Dataset — Kaggle](https://www.kaggle.com/datasets/kanchana1990/ev-battery-qc-synthetic-defect-dataset)

| Caractéristique | Valeur |
|---|---|
| Observations | 20 000 |
| Variables initiales | 14 |
| Format | CSV |
| Nature | Données synthétiques |
| Variable cible | `Has_Defect` |

La variable cible prend deux valeurs :

- `0` : cellule conforme ;
- `1` : cellule présentant un défaut qualité.

## 🛠️ Technologies utilisées

| Technologie | Rôle |
|---|---|
| Python | Développement et traitement des données |
| Pandas / NumPy | Manipulation et nettoyage |
| SQLite | Stockage des données |
| Scikit-learn | Entraînement des modèles |
| Joblib | Sauvegarde et chargement du modèle |
| Matplotlib | Visualisations |
| Streamlit | Interface web |

## 🧠 Modélisation et résultats

Quatre modèles de classification supervisée ont été évalués :

- Logistic Regression
- Decision Tree
- K-Nearest Neighbors
- Random Forest

**Modèle retenu : Random Forest Classifier**

| Métrique | Résultat |
|---|---:|
| Accuracy | 98,42 % |
| Précision défaut | 98,33 % |
| Rappel défaut | 92,57 % |
| F1-score défaut | 95,36 % |

Les résultats correspondent au jeu de test synthétique. Ils ne constituent pas une validation sur une ligne de production industrielle réelle.

## 🖥️ Fonctionnalités de l'application

L'application comprend quatre pages principales :

1. **Prédiction manuelle :** saisie des caractéristiques d'une cellule et affichage du résultat avec la probabilité estimée de défaut.
2. **Prédiction par fichier CSV :** import d'un fichier, analyse de plusieurs cellules et téléchargement des prédictions.
3. **Dashboard dataset :** indicateurs de qualité, répartition des défauts et statistiques descriptives.
4. **Informations projet :** fonctionnement du modèle, sécurité, limites et accessibilité.

## 📁 Structure du projet

```text
OUISSAL_MASBAHI_PROJET/
├── app.py
├── requirements.txt
├── README.md
├── 01_exploitation_donnees_batterie.ipynb
├── data/
│   └── ev_battery_qc_data_2026_kaggle.csv
├── models/
│   └── best_battery_defect_model.pkl
├── outputs/
│   ├── battery_qc.sqlite
│   └── battery_qc_dump.sql
└── figures/
```

**Remarque :** `battery_qc_dump.sql` doit être généré et ajouté au dossier `outputs/` avant la livraison finale.

## 🚀 Prérequis et installation

### Prérequis

- Python 3
- pip
- Git
- Navigateur web
- Connexion Internet pour installer les dépendances

### 1. Cloner le dépôt

```bash
git clone https://github.com/OuissalMasbahi/OUISSAL_MASBAHI_PROJET.git
cd OUISSAL_MASBAHI_PROJET
```

### 2. Installer les dépendances

```bash
python3 -m pip install -r requirements.txt
```

Pour exécuter le notebook qui télécharge les données Kaggle, installer également :

```bash
python3 -m pip install kagglehub
```

### 3. Lancer l'application

```bash
python3 -m streamlit run app.py
```

Ouvrir ensuite :

http://localhost:8501

L'application peut également être utilisée directement via son URL publique :

https://masbahi-ouissal-project.streamlit.app/

## 🗄️ Base de données SQL

**Système de gestion :** SQLite

**Fichier de base de données :** `outputs/battery_qc.sqlite`

**Tables principales :**

- `battery_qc_raw` : données initiales ;
- `battery_qc_clean` : données préparées.

### Connexion à la base de données

La base SQLite fonctionne localement et ne nécessite pas de serveur SQL.

| Paramètre | Valeur |
|---|---|
| SGBD | SQLite |
| Fichier | `outputs/battery_qc.sqlite` |
| Hôte | Non applicable |
| Port | Non applicable |
| Identifiant SQL | Non requis |
| Mot de passe SQL | Non requis |

### Export SQL (dump)

Le dump permet de reconstruire la base de données à partir d'un script SQL.

Pour générer le fichier `outputs/battery_qc_dump.sql`, exécuter depuis le dossier racine du projet :

```bash
python3 -c "import sqlite3; c=sqlite3.connect('outputs/battery_qc.sqlite'); f=open('outputs/battery_qc_dump.sql','w'); f.write('\n'.join(c.iterdump())+'\n'); f.close(); c.close()"
```

Pour restaurer la base dans un nouveau fichier :

```bash
sqlite3 batterie_restauree.sqlite < outputs/battery_qc_dump.sql
```

## ⚙️ Configuration

Le projet utilise principalement :

- `requirements.txt` : liste des dépendances Python ;
- `app.py` : configuration de l'application et chemins des fichiers ;
- `models/best_battery_defect_model.pkl` : modèle entraîné ;
- `data/ev_battery_qc_data_2026_kaggle.csv` : dataset utilisé ;
- `outputs/battery_qc.sqlite` : base SQLite.

Aucun identifiant de service externe n'est nécessaire pour lancer l'application à partir des fichiers déjà présents.

## 🔑 Identifiants de test et accès administrateur

| Élément demandé | Informations |
|---|---|
| URL de test | https://masbahi-ouissal-project.streamlit.app/ |
| Identifiant utilisateur | Non requis |
| Mot de passe utilisateur | Non requis |
| Identifiant SQL | Non requis — SQLite locale |
| Mot de passe SQL | Non requis |
| Accès administrateur au back-office | Non applicable dans cette version du POC |

L'application est accessible directement sans authentification. Aucun back-office administrateur distinct n'a été développé.

Les fonctions de prédiction et de visualisation sont accessibles depuis l'interface principale.

## 🔒 Sécurité, éthique et limites

- Dataset public et synthétique.
- Aucune donnée confidentielle ACC utilisée.
- Aucune authentification nécessaire pour le POC.
- Exclusion de `QC_Grade` afin de limiter les risques de fuite d'information dans la modélisation.
- Prédictions utilisées uniquement comme aide à la décision.
- Validation humaine nécessaire avant toute décision opérationnelle.
- Modèle non validé sur des données industrielles réelles.

## 🚀 Perspectives d'évolution

- Intégration de données industrielles réelles sous autorisation.
- Connexion à une base de données industrielle.
- Authentification et gestion des rôles utilisateurs.
- Surveillance des performances et de la dérive du modèle.
- Réentraînement périodique.
- Prédiction du type exact de défaut.

## 👩‍💻 Auteure

**Ouissal MASBAHI**

Mastère Data et Intelligence Artificielle  
Nexa Campus Bordeaux  
Thèse professionnelle — Année universitaire 2025–2026
