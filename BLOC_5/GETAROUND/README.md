# 🚗 GetAround Data Science Project

## Présentation en ligne de l'intégralité du projet format PPT (en ligne)

🚀 [Bloc_05 | GETAROUND | Présentation PPT](https://docs.google.com/presentation/d/1wCPI96G99YUsSORCYo2CMwiioSKZAElyQ0AroEtlyws/edit?usp=sharing) \
📁 [Bloc_05 | GETAROUND | Backup GitHub](https://github.com/eric-nguyen-jedha/CDSD/tree/main/BLOC_5/GETAROUND) \

## 🔗 Liens en production

- 📊 **Dashboard interactif** : [https://huggingface.co/spaces/ericjedha/getaroundST](https://huggingface.co/spaces/ericjedha/getaroundST)  
- 🤖 **API en production** : [https://ericjedha-getaroundapi.hf.space/](https://ericjedha-getaroundapi.hf.space/)  
- 📚 **Documentation API** : [https://ericjedha-getaroundapi.hf.space/docs](https://ericjedha-getaroundapi.hf.space/docs)  
- ⚙ **Serveur MLFLOW** : [https://huggingface.co/spaces/ericjedha/getaroundml](https://huggingface.co/spaces/ericjedha/getaroundml)  


> **Airbnb for cars** — Analyse de retard, dashboard interactif & API de prédiction de prix

Ce projet a été réalisé dans le cadre d’un cas réel proposé par **GetAround**, la plateforme de location de voitures entre particuliers. L’objectif est d’aider l’équipe produit à prendre des décisions éclairées concernant l’implémentation d’un **délai minimum entre deux locations** afin de réduire les retards, tout en minimisant l’impact sur les revenus.  
Nous proposons également une **API de prédiction de prix** basée sur un modèle de Machine Learning.


---

## 🎯 Objectif du projet

GetAround fait face à un problème récurrent : les **retards lors du checkout** des véhicules. Ces retards impactent fortement la satisfaction des prochains locataires, voire entraînent des annulations.

Nous devons aider l’équipe produit à décider :
- 🔹 **Quel seuil de délai minimum** imposer entre deux locations ?
- 🔹 **Pour quels types de véhicules** (tous ou uniquement les "Connect") activer cette fonctionnalité ?

En parallèle, nous développons une **API de prédiction de prix** pour optimiser la tarification des véhicules.

---

## 📂 Données utilisées

Deux jeux de données ont été utilisés :

1. **`getaround_delay_analysis.csv`**  
   → Analyse des retards de checkout, checkin, types de réservation, etc.

2. **`getaround_pricing_optimization.csv`**  
   → Données descriptives des véhicules utilisées pour la modélisation du prix.

---

## 📊 Dashboard interactif

### Outil d’aide à la décision

Un dashboard interactif a été développé avec **Streamlit** pour permettre à l’équipe produit de :
- Visualiser la **fréquence des retards**
- Estimer l’**impact du seuil de délai** sur le nombre de locations bloquées
- Comprendre l’**impact financier potentiel** sur les revenus des propriétaires
- Comparer les scénarios selon le **scope** (tous véhicules vs. Connect uniquement)

### Fonctionnalités clés
- 📅 Histogramme des retards de checkout
- 📈 Proportion de locations affectées selon le seuil
- 💰 Estimation de la perte de revenus potentielle
- 🎯 Nombre de conflits évités selon le seuil choisi
- 🔍 Filtres par type de véhicule (Connect / standard)

👉 **Accédez au dashboard ici** : [https://huggingface.co/spaces/ericjedha/getaroundST](https://your-dashboard-url.streamlit.app)

---

## 🤖 API de prédiction de prix

Une API REST a été déployée pour **prédire le prix optimal** d’un véhicule en fonction de ses caractéristiques.

### Endpoint : `/predict`

- **Méthode** : `POST`
- **URL** : `https://ericjedha-getaroundapi.hf.space/predict/`
- **Format d’entrée** : JSON avec une clé `"input"` contenant une liste de listes (features)
- **Sortie** : JSON avec une clé `"prediction"` contenant la liste des prix prédits

#### 🔧 Exemple d’appel avec `curl`

```bash
curl -i -H "Content-Type: application/json" \
     -X POST \
     -d '{
  "model_key": "Toyota",
  "mileage": 25000,
  "engine_power": 250,
  "fuel": "diesel",
  "paint_color": "green",
  "car_type": "convertible",
  "private_parking_available": true,
  "has_gps": true,
  "has_air_conditioning": true,
  "automatic_car": false,
  "has_getaround_connect": true,
  "has_speed_regulator": true,
  "winter_tires": false
}' \
     https://ericjedha-getaroundapi.hf.space/predict/

```
## cela devrait renvoyer cette information : 

HTTP/2 200 
date: Wed, 20 Aug 2025 12:41:56 GMT
content-type: application/json
content-length: 32
server: uvicorn
x-proxied-host: http://10.108.148.2
x-proxied-replica: slvu9wpm-9bjpi
x-proxied-path: /predict/
link: <https://huggingface.co/spaces/ericjedha/getaroundapi>;rel="canonical"
x-request-id: yCEWUt
vary: origin, access-control-request-method, access-control-request-headers
access-control-allow-credentials: true

{"prediction":213.4575958251953}% 

```

## 📁 Structure du projet 

```
├── GETAROUND_EDA_Threshold.ipynb                  # EDA et calcul du Seuil
├── AT&T_CNN.ipynb                                 # Model CNN Maison
├── GETAROUND_ML_MLFLOW.ipynb                      # Modèles de regression testé plus enregistrement dans MLFLOW
├── pages  
   ├── 1_EDA_GetAround.py                          # EDA
   ├── 2_Simulateur_Seuil.py                       # Simulateur de Seuil  
   ├── 3_Prediction_Prix.py                        # Prédiction Prix GetAround 
├── app_streamlit.py                               # Code Streamlit à copier dans le serveur Streamlit Hugging Face   
├── dockerfile_streamlit.txt                       # Dockerfile pour Streamlit sur Hugging Face    
├── README_streamlit.md                            # README de Streamlit sur Hugging Face
├── .streamlit/config.toml                         # Fichier de personnalisation de la mise en forme de Streamlit
├── app_ap.py                                      # code API à copier sur le serveur de l'API Hugging Face 
├── README_api.md                                  # README de l'API sur Hugging Face
├── dockerfile_appi.txt                            # Dockerfile pour l'API sur Hugging Face   
├── requirements_api.txt                           # Requirementst.txt pour l'API sur Hugging Face
├── dockerfile_mflow.txt                           # Dockkerfile MFLOW à recopier sur le serveur MFLOW Hugging Face
├── requirements_mlflow.txt                        # Requirements.txt pour MLFLOW sur Hugging Face
├── README_mlflow.md                               # README.md MLFLOW sur Hugging Face
├── img                                            # Ressources visuel Getaround
└── .env                                           

```

### Crédential à mettre dans .env

#AWS_ACCESS_KEY_ID=[VOSCREDENTIALS]
#AWS_SECRET_ACCESS_KEY=[VOSCREDENTIALS]
#AWS_DEFAULT_REGION=[VOSCREDENTIALS]
#ARTIFACT_STORE_URI=[URI_S3]
#BACKEND_STORE_URI=[URL_POSTGRESQL]

PS : ne pas oublier Gitignore



## 📁 Setting Hugging Frace pour l'API et MLFLOW

PORT = 7860
MLFLOW_S3_ENDPOINT_URL = [URI_S3]

# Secrets Key

AWS_DEFAULT_REGION=[REGION AWS]
BACKEND_STORE_URI=[URL_POSTGRESQL]
ARTIFACT_STORE_URI=[URI_S3]
AWS_SECRET_ACCESS_KEY=[VOSCREDENTIALS]
AWS_ACCESS_KEY_ID=[VOSCREDENTIALS]
HF_TOKEN = [VOTRE HUGGING FACE TOKEN]
MLFLOW_TRACKING_URI = [URL de MFLOW]