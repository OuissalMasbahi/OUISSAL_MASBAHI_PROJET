import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# =====================================================
# Configuration générale de l'application
# =====================================================

st.set_page_config(
    page_title="Détection des défauts batteries",
    page_icon="🔋",
    layout="wide"
)

# =====================================================
# Chemins des fichiers
# =====================================================

MODEL_PATH = Path("models") / "best_battery_defect_model.pkl"
DATA_PATH = Path("data") / "ev_battery_qc_data_2026_kaggle.csv"

# =====================================================
# Chargement du modèle et des données
# =====================================================

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    # Création de la variable cible binaire
    # 0 = cellule conforme
    # 1 = cellule avec défaut
    df["Has_Defect"] = df["Defect_Type"].apply(
        lambda x: 0 if pd.isna(x) else 1
    )

    return df

model = load_model()
df_data = load_data()

# =====================================================
# Titre principal
# =====================================================

st.title("🔋 Détection prédictive des défauts qualité des cellules de batteries")

st.write(
    "Cette application permet de prédire si une cellule de batterie présente un risque de défaut qualité "
    "à partir de ses caractéristiques de production et de contrôle."
)

# =====================================================
# Menu latéral
# =====================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choisir une page",
    [
        "Prédiction manuelle",
        "Prédiction par fichier",
        "Dashboard dataset",
        "Informations projet"
    ]
)

# =====================================================
# Page 1 : Prédiction manuelle
# =====================================================

if page == "Prédiction manuelle":
    st.header("Prédiction manuelle d’une cellule")

    st.write("Renseignez les caractéristiques de la cellule à analyser.")

    col1, col2, col3 = st.columns(3)

    with col1:
        production_line = st.selectbox(
            "Ligne de production",
            ["Line_1", "Line_2", "Line_3"]
        )

        shift = st.selectbox(
            "Shift",
            ["Morning", "Evening", "Night"]
        )

        supplier = st.selectbox(
            "Fournisseur",
            ["ChemCorp", "LithioMat", "VoltIndustries"]
        )

    with col2:
        ambient_temp = st.number_input(
            "Température ambiante (°C)",
            value=22.0,
            step=0.1
        )

        anode_overhang = st.number_input(
            "Anode Overhang (mm)",
            value=0.13,
            step=0.001,
            format="%.3f"
        )

        electrolyte_volume = st.number_input(
            "Volume électrolyte (ml)",
            value=15.0,
            step=0.1
        )

    with col3:
        internal_resistance = st.number_input(
            "Résistance interne (mOhm)",
            value=14.5,
            step=0.1
        )

        capacity = st.number_input(
            "Capacité (mAh)",
            value=3000.0,
            step=10.0
        )

        retention = st.number_input(
            "Rétention après 50 cycles (%)",
            value=95.0,
            step=0.1
        )

    input_data = pd.DataFrame({
        "Production_Line": [production_line],
        "Shift": [shift],
        "Supplier": [supplier],
        "Ambient_Temp_C": [ambient_temp],
        "Anode_Overhang_mm": [anode_overhang],
        "Electrolyte_Volume_ml": [electrolyte_volume],
        "Internal_Resistance_mOhm": [internal_resistance],
        "Capacity_mAh": [capacity],
        "Retention_50Cycle_Pct": [retention]
    })

    st.subheader("Données saisies")
    st.dataframe(input_data, width="stretch")

    if st.button("Lancer la prédiction"):
        prediction = model.predict(input_data)[0]

        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(input_data)[0][1]
        else:
            proba = None

        if prediction == 1:
            st.error("Résultat : cellule avec risque de défaut qualité")
        else:
            st.success("Résultat : cellule conforme")

        if proba is not None:
            st.write(f"Probabilité estimée de défaut : **{proba:.2%}**")

# =====================================================
# Page 2 : Prédiction par fichier
# =====================================================

elif page == "Prédiction par fichier":
    st.header("Prédiction à partir d’un fichier CSV")

    st.write(
        "Importez un fichier CSV contenant les mêmes variables que celles utilisées lors de l’entraînement du modèle."
    )

    uploaded_file = st.file_uploader("Choisir un fichier CSV", type=["csv"])

    expected_columns = [
        "Production_Line",
        "Shift",
        "Supplier",
        "Ambient_Temp_C",
        "Anode_Overhang_mm",
        "Electrolyte_Volume_ml",
        "Internal_Resistance_mOhm",
        "Capacity_mAh",
        "Retention_50Cycle_Pct"
    ]

    if uploaded_file is not None:
        df_upload = pd.read_csv(uploaded_file)

        st.subheader("Aperçu du fichier importé")
        st.dataframe(df_upload.head(), width="stretch")

        missing_columns = [
            col for col in expected_columns if col not in df_upload.columns
        ]

        if missing_columns:
            st.error(f"Colonnes manquantes : {missing_columns}")
            st.write("Les colonnes attendues sont :")
            st.write(expected_columns)
        else:
            df_predict = df_upload[expected_columns]
            predictions = model.predict(df_predict)

            df_upload["Prediction_Has_Defect"] = predictions
            df_upload["Statut_prediction"] = df_upload["Prediction_Has_Defect"].map({
                0: "Conforme",
                1: "Défaut"
            })

            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(df_predict)[:, 1]
                df_upload["Probabilite_defaut"] = probabilities

            st.subheader("Résultats des prédictions")
            st.dataframe(df_upload, width="stretch")

            defect_rate = df_upload["Prediction_Has_Defect"].mean() * 100

            st.metric(
                "Taux de défauts prédits",
                f"{defect_rate:.2f} %"
            )

            csv_result = df_upload.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Télécharger les résultats",
                data=csv_result,
                file_name="resultats_predictions_batteries.csv",
                mime="text/csv"
            )

# =====================================================
# Page 3 : Dashboard dataset
# =====================================================

elif page == "Dashboard dataset":
    st.header("📊 Dashboard descriptif du jeu de données")

    st.write(
        "Cette page présente une vue synthétique du dataset utilisé pour entraîner le modèle de prédiction."
    )

    # Indicateurs principaux
    col1, col2, col3, col4 = st.columns(4)

    total_rows = df_data.shape[0]
    total_cols = df_data.shape[1]
    defect_count = df_data["Has_Defect"].sum()
    conform_count = total_rows - defect_count
    defect_rate = defect_count / total_rows * 100

    with col1:
        st.metric(
            "Nombre d'observations",
            f"{total_rows:,}".replace(",", " ")
        )

    with col2:
        st.metric(
            "Nombre de variables",
            total_cols
        )

    with col3:
        st.metric(
            "Cellules conformes",
            f"{conform_count:,}".replace(",", " ")
        )

    with col4:
        st.metric(
            "Taux de défauts",
            f"{defect_rate:.2f} %"
        )

    st.subheader("Aperçu du dataset")
    st.dataframe(df_data.head(10), width="stretch")

    st.subheader("Répartition des cellules conformes et défectueuses")

    defect_distribution = df_data["Has_Defect"].map({
        0: "Conforme",
        1: "Défaut"
    }).value_counts()

    st.bar_chart(defect_distribution)

    st.subheader("Répartition des types de défauts")

    defect_type_distribution = (
        df_data["Defect_Type"]
        .fillna("Unknown")
        .value_counts()
    )

    st.bar_chart(defect_type_distribution)

    st.subheader("Analyse par ligne de production")

    production_line_distribution = df_data["Production_Line"].value_counts()
    st.bar_chart(production_line_distribution)

    st.subheader("Analyse par fournisseur")

    supplier_distribution = df_data["Supplier"].value_counts()
    st.bar_chart(supplier_distribution)

    st.subheader("Analyse par shift")

    shift_distribution = df_data["Shift"].value_counts()
    st.bar_chart(shift_distribution)

    st.subheader("Statistiques descriptives des variables numériques")

    numeric_columns = [
        "Ambient_Temp_C",
        "Anode_Overhang_mm",
        "Electrolyte_Volume_ml",
        "Internal_Resistance_mOhm",
        "Capacity_mAh",
        "Retention_50Cycle_Pct"
    ]

    st.dataframe(
        df_data[numeric_columns].describe(),
        width="stretch"
    )

    st.subheader("Analyse moyenne selon le statut qualité")

    mean_by_status = df_data.groupby("Has_Defect")[numeric_columns].mean()
    mean_by_status.index = mean_by_status.index.map({
        0: "Conforme",
        1: "Défaut"
    })

    st.dataframe(mean_by_status, width="stretch")

# =====================================================
# Page 4 : Informations projet
# =====================================================

else:
    st.header("Informations sur le projet")

    st.write("""
    Cette application a été développée dans le cadre d’une thèse professionnelle en Data et Intelligence Artificielle.
    
    L’objectif est de proposer une solution d’aide à la décision permettant de prédire les défauts qualité 
    des cellules de batteries électriques à partir de données de production et de contrôle qualité.
    """)

    st.subheader("Modèle utilisé")

    st.write("""
    Le modèle retenu est un **Random Forest Classifier**. 
    Il a été choisi car il présente le meilleur compromis entre accuracy, précision, rappel et F1-score 
    pour la classe défaut.
    """)

    st.subheader("Fonctionnement de la prédiction")

    st.write("""
    L’application charge le modèle sauvegardé au format `.pkl` à l’aide de la librairie `joblib`.
    Lorsqu’un utilisateur saisit les caractéristiques d’une cellule, les données sont transmises au modèle, 
    qui retourne une classe prédite :
    
    - `0` : cellule conforme ;
    - `1` : cellule avec risque de défaut qualité.
    
    La probabilité affichée correspond à la probabilité estimée par le modèle pour la classe défaut.
    """)

    st.subheader("Mesures de protection des données")

    st.write("""
    - Le dataset utilisé est synthétique.
    - Aucune donnée personnelle n’est collectée.
    - Aucune donnée interne confidentielle d’ACC n’est utilisée.
    - Les fichiers importés servent uniquement à produire une prédiction.
    - L’application est destinée à un usage de démonstration et d’aide à la décision.
    - Le modèle ne remplace pas la validation humaine des équipes qualité.
    """)

    st.subheader("Accessibilité")

    st.write("""
    Plusieurs mesures ont été prises pour rendre l’application plus accessible :
    
    - navigation simple depuis le menu latéral ;
    - libellés explicites pour chaque champ de saisie ;
    - affichage textuel des résultats en plus des couleurs ;
    - structure claire des pages ;
    - tableaux lisibles et organisés ;
    - messages d’erreur explicites en cas de fichier CSV non conforme.
    """)
