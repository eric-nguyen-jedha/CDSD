import pandas as pd
import numpy as np
import mlflow
import mlflow.pyfunc
import logging
import os
import traceback
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- Configuration des logs ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Dictionnaire pour stocker les modèles chargés ---
# On le remplit au démarrage de l'application
ml_models = {}

# --- Configuration du Lifespan de l'application ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code exécuté au démarrage de l'application
    logger.info("Démarrage de l'application: chargement du modèle...")
    
    # 1. Configurer l'URI du serveur MLflow (LA PARTIE LA PLUS IMPORTANTE)
    #    Cette variable doit être définie dans les "Secrets" de votre Space FastAPI
    MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
    if not MLFLOW_TRACKING_URI:
        raise ValueError("La variable d'environnement MLFLOW_TRACKING_URI n'est pas définie !")
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    logger.info(f"MLflow tracking URI configuré sur: {MLFLOW_TRACKING_URI}")

    # 2. Configurer l'authentification si votre Space MLflow est privé
    #    Le token doit aussi être dans les "Secrets" du Space FastAPI
    HF_TOKEN = os.getenv("HF_TOKEN")
    if HF_TOKEN:
        os.environ['MLFLOW_TRACKING_USERNAME'] = "ericjedha" # ou tout autre nom d'utilisateur
        os.environ['MLFLOW_TRACKING_PASSWORD'] = HF_TOKEN
        logger.info("Authentification MLflow configurée avec un token.")

    # 3. Charger le modèle
    try:
        logged_model_uri = 'runs:/8d6657ebb69943f298f1124df0db622f/xgboost_ridge_pipeline'
        # Charger le modèle et le stocker dans notre dictionnaire
        ml_models["getaround_model"] = mlflow.pyfunc.load_model(logged_model_uri)
        logger.info("Modèle chargé avec succès et prêt à être utilisé.")
    except Exception as e:
        logger.error(f"Erreur critique lors du chargement du modèle: {e}")
        logger.error(traceback.format_exc())
        # Si le modèle ne se charge pas, l'application ne peut pas fonctionner.
        # On pourrait choisir d'arrêter l'application ici, mais pour l'instant on logue l'erreur.
    
    yield
    
    # Code exécuté à l'arrêt de l'application (cleanup)
    logger.info("Arrêt de l'application: nettoyage...")
    ml_models.clear()

# --- Initialisation de l'application FastAPI avec le lifespan ---
app = FastAPI(lifespan=lifespan)

# --- Modèle de données Pydantic pour la requête ---
class Item(BaseModel):
    model_key: str
    mileage: int 
    engine_power: int 
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: int
    has_gps: int
    has_air_conditioning: int
    automatic_car: int
    has_getaround_connect: int
    has_speed_regulator: int
    winter_tires: int

# --- Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de prédiction GetAround"}

@app.post("/predict/")
async def predict(item: Item):
    # Vérifier si le modèle est bien chargé
    if "getaround_model" not in ml_models:
        raise HTTPException(
            status_code=503, 
            detail="Le modèle n'est pas disponible. L'application n'a pas pu le charger au démarrage."
        )
    
    try:
        # Créer un DataFrame à partir des données de la requête
        car_df = pd.DataFrame([item.model_dump()])
        logger.info(f"Données reçues pour la prédiction : \n{car_df.to_string()}")

        # Utiliser le modèle DÉJÀ en mémoire pour faire la prédiction
        prediction = ml_models["getaround_model"].predict(car_df)
        
        # Formater la réponse
        response = {"prediction": prediction.tolist()[0]}
        
        logger.info(f"Prédiction effectuée : {response}")
        return response

    except Exception as e:
        logger.error(f"Erreur lors de la prédiction : {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erreur serveur lors de la prédiction : {str(e)}")