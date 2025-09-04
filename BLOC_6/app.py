import os
import numpy as np
import gradio as gr
import cv2
import tensorflow as tf
import keras
from keras.models import Model
from keras.preprocessing import image
#from tensorflow.keras.preprocessing import image
from huggingface_hub import hf_hub_download
import pandas as pd
from PIL import Image
import plotly.express as px
import time
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

theme = gr.themes.Soft(
    primary_hue="purple",
    secondary_hue="yellow",
    text_size="sm",
)

css = """
/* Police lisible et compatible */
body {
    font-family: Arial, sans-serif !important;
}
/* Conteneur du diagnostic global */
.diagnostic-global {
    padding: 10px;
}
/* Style pour les badges Malin/Bénin */
.highlight.malin {
    background-color: #F54927;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    display: inline-block;
    font-weight: bold;
    font-size:24px;
    margin: 5px 0;
}
.highlight.benin {
    background-color: #34EA3A;
    color: black;
    padding: 4px 8px;
    border-radius: 4px;
    display: inline-block;
    font-weight: bold;
    font-size:24px;
    margin: 5px 0;
}
/* Conteneur pour le warning */
.warning-container {
    background-color: #f9f9f9;
    border-radius: 5px;
    padding: 0px;
    margin-bottom: 0px;
    border: 1px solid #e0e0e0;
}
/* Message d'avertissement */
.warning-message {
    background-color: #e9d5ff;
    border-radius: 3px;
    padding: 10px;
    border: 1px solid #d4b5ff;
    font-size: 14px;
    color: #333;
    font-family: Arial, sans-serif !important;
}
/* Pour les images dans le diagnostic */
.diagnostic-global img {
    max-width: 100%;
    height: auto;
    float: left;
    margin-right: 10px;
    margin-bottom: 10px;
}
.feedback-container {
    background-color: #f9f9f9;
    border-radius: 5px;
    padding: 0px;
    margin-bottom: 0px;
    border: 1px solid #e0e0e0;
    font-size:16px;
    font-family: Arial, sans-serif !important;
}
/* Clearfix pour les flottants */
.clearfix::after {
    content: "";
    display: table;
    clear: both;
}
"""

# Désactiver GPU et logs TensorFlow
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.config.set_visible_devices([], 'GPU')



# ==========================
# BIOMEDBERT 
# ==========================

from transformers import pipeline
import torch

# Dictionnaire des noms complets 
CLASS_NAMES_FULL = {
    "mel": "Melanoma",
    "bcc": "Basal Cell Carcinoma", 
    "akiec": "Actinic Keratosis",
    "bkl": "Benign Keratosis",
    "df": "Dermatofibroma",
    "nv": "Melanocytic Nevus",
    "vasc": "Vascular Lesion"
}

# Chargement simple du modèle [NOUVEAU CODE]
med_nlp = None
try:
    print("📥 Chargement du modèle médical BiomedBERT...")
    med_nlp = pipeline(
        "text-classification",
        model="microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract",
        framework="pt",
        device=0 if torch.cuda.is_available() else -1,
        return_all_scores=True
    )
    print("✅ BiomedBERT chargé avec succès")
except Exception as e:
    print(f"❌ Erreur BiomedBERT: {e}")
    med_nlp = None

    

# ---- Configuration ----
CLASS_NAMES = ['akiec', 'bcc', 'bkl', 'df', 'nv', 'vasc', 'mel']
label_to_index = {name: i for i, name in enumerate(CLASS_NAMES)}
diagnosis_map = {
    'akiec': 'Bénin', 'bcc': 'Malin', 'bkl': 'Bénin', 'df': 'Bénin',
    'nv': 'Bénin', 'vasc': 'Bénin', 'mel': 'Malin'
}
description = {
    "akiec": "Bénin : AKIEC ou - kératoses solaires - sont des excroissances précancéreuses provoquées par l'exposition solaire prolongée. Le risque de progression d'une Kératose Actinique vers un carcinome épidermoïde (cancer de la peau non mélanome) existe mais reste modéré",
    "bcc": "Malin : BCC ou - carcinome basocellulaire - est un type de cancer cutané. C’est le cancer de la peau le plus fréquent. Il se manifeste par la formation d'une masse, d'un bouton ou d'une lésion sur la couche externe de la peau. Selon Ameli.fr : Le carcinome basocellulaire est la forme la plus courante de cancer de la peau. Ce type de cancer de la peau ne se propage généralement pas, mais nécessite un traitement. Les carcinomes basocellulaires se développent le plus souvent dans les zones d'exposition de la peau au soleil.",
    "bkl": "Bénin : BKL ou - kératose séborrhéique -  se présente sous la forme d’une lésion pigmentée, en relief, verruqueuse (qui ressemble à une verrue), souvent croûteuse, de plus ou moins grande taille.",
    "df": "Bénin : DF ou - dermatofibrome - est une lésion papuleuse ou nodulaire ferme, le plus souvent de petite taille, de couleur rouge marron, de nature fibrohistiocytaire.",
    "nv": "Bénin : NV (Nevus) ou les - grains de beauté -, couramment appelés nevus mélanocytaires représentent une accumulation localisée de mélanocytes dans la peau",
    "vasc": "Bénin : VASC ou - lésion vasculaire - se traduit par la survenue d’anomalies visibles en surface de la peau et d’aspect variable : rougeurs, taches planes ou en relief, capillaires sanguins apparents",
    "mel": "Malin : MEL ou - Mélanome - est un nodule noir ou couleur « peau » présent sur n'importe quelle partie de la peau. Sa consistance est ferme et le nodule peut s'ulcérer, se couvrir d'une croûte, suinter ou saigner. Selon Ameli.fr : Le mélanome est un cancer de la peau peu fréquent, mais grave s'il n'est pas diagnostiqué tôt. L'exposition aux rayons ultraviolets (soleil ou lampe UV) est le principal facteur favorisant sa survenue."
}

# ---- Chargement des modèles ----
def load_models_safely():
    models = {}
    try:
        print("📥 Téléchargement ResNet50...")
        resnet_path = hf_hub_download(repo_id="ericjedha/resnet50", filename="Resnet50.keras")
        models['resnet50'] = keras.saving.load_model(resnet_path, compile=False)
        print("✅ ResNet50 chargé")
    except Exception as e:
        models['resnet50'] = None
    
    try:
        print("📥 Téléchargement DenseNet201...")
        densenet_path = hf_hub_download(repo_id="ericjedha/densenet201", filename="Densenet201.keras")
        models['densenet201'] = keras.saving.load_model(densenet_path, compile=False)
        print("✅ DenseNet201 chargé")
    except Exception as e:
        models['densenet201'] = None
    
    try:
        print("📥 Chargement Xception local...")
        if os.path.exists("Xception.keras"):
            models['xception'] = keras.saving.load_model("Xception.keras", compile=False)
            print("✅ Xception chargé")
        else:
            models['xception'] = None
    except Exception as e:
        models['xception'] = None
    
    loaded = {k: v for k, v in models.items() if v is not None}
    if not loaded:
        raise Exception("❌ Aucun modèle n'a pu être chargé!")
    
    print(f"🎯 Modèles chargés: {list(loaded.keys())}")
    return models

try:
    models_dict = load_models_safely()
    model_resnet50 = models_dict.get('resnet50')
    model_densenet = models_dict.get('densenet201') 
    model_xcept = models_dict.get('xception')
except Exception as e:
    print(f"🚨 ERREUR CRITIQUE: {e}")
    model_resnet50 = model_densenet = model_xcept = None

# ---- Préprocesseurs ----
from tensorflow.keras.applications.xception import preprocess_input as preprocess_xception
from tensorflow.keras.applications.resnet50 import preprocess_input as preprocess_resnet
from tensorflow.keras.applications.densenet import preprocess_input as preprocess_densenet

# ---- Utils ----
def _renorm_safe(p: np.ndarray) -> np.ndarray:
    p = np.clip(p, 0.0, None)  # Évite les valeurs négatives
    s = np.sum(p)
    if s <= 0:
        return np.ones_like(p, dtype=np.float32) / len(p)
    normalized = p / s
    return normalized / np.sum(normalized) if np.sum(normalized) > 1.0001 else normalized

def get_primary_input_name(model):
    if isinstance(model.inputs, list) and len(model.inputs) > 0:
        return model.inputs[0].name.split(':')[0]
    return "input_1" 

def _update_progress(progress, value, desc=""):
    """
    Met à jour la barre de progression.
    """
    if progress is not None:
        progress(value / 100.0, desc=desc)

# ---- PREDICT SINGLE ----
def predict_single(img_input, weights=(0.45, 0.25, 0.3), normalize=True):
    print("🔍 DEBUG GRADIO HARMONISÉ - Début de la prédiction")

    # Chargement uniforme des images
    if isinstance(img_input, str):
        # Cas fichier local
        img_path = img_input
        print(f"📁 Chargement depuis fichier: {img_path}")
        
        img_raw_x = image.load_img(img_path, target_size=(299, 299))
        img_raw_r = image.load_img(img_path, target_size=(224, 224))
        img_raw_d = image.load_img(img_path, target_size=(224, 224))
        
    else:
        # Cas upload Gradio - AMÉLIORATION ICI
        print("📁 Chargement depuis upload Gradio")
        
        # Option 1: Éviter la sauvegarde temporaire en utilisant BytesIO
        from io import BytesIO
        import PIL.Image
        
        # Convertir en RGB si nécessaire (évite les problèmes de format)
        if img_input.mode != 'RGB':
            img_input = img_input.convert('RGB')
            print(f"🔄 Conversion en RGB effectuée")
        
        # Redimensionner directement depuis PIL
        img_raw_x = img_input.resize((299, 299), PIL.Image.Resampling.LANCZOS)
        img_raw_r = img_input.resize((224, 224), PIL.Image.Resampling.LANCZOS)
        img_raw_d = img_input.resize((224, 224), PIL.Image.Resampling.LANCZOS)
        
        # Alternative si vous voulez garder la sauvegarde temporaire
        # temp_path = "temp_debug_image.png"  # PNG pour éviter compression JPEG
        # img_input.save(temp_path, format='PNG')
        # img_raw_x = image.load_img(temp_path, target_size=(299, 299))
        # img_raw_r = image.load_img(temp_path, target_size=(224, 224))
        # img_raw_d = image.load_img(temp_path, target_size=(224, 224))
        # import os
        # os.remove(temp_path)

    # Conversion en arrays avec vérification
    array_x = image.img_to_array(img_raw_x)
    array_r = image.img_to_array(img_raw_r)
    array_d = image.img_to_array(img_raw_d)

    print(f"📸 Images loaded:")
    print(f"   Xception (299x299): {array_x.shape}")
    print(f"   ResNet (224x224): {array_r.shape}")
    print(f"   DenseNet (224x224): {array_d.shape}")

    print(f"🔧 Arrays avant preprocessing:")
    print(f"   X shape: {array_x.shape}, dtype: {array_x.dtype}, range: [{array_x.min()}, {array_x.max()}]")
    print(f"   R shape: {array_r.shape}, dtype: {array_r.dtype}, range: [{array_r.min()}, {array_r.max()}]")
    print(f"   D shape: {array_d.shape}, dtype: {array_d.dtype}, range: [{array_d.min()}, {array_d.max()}]")
    
    # Vérification de cohérence avec le local
    expected_range = (0, 255)
    actual_ranges = [
        (array_x.min(), array_x.max()),
        (array_r.min(), array_r.max()),
        (array_d.min(), array_d.max())
    ]
    
    print(f"🔍 Vérification des ranges:")
    for i, (min_val, max_val) in enumerate(actual_ranges):
        model_name = ['Xception', 'ResNet', 'DenseNet'][i]
        if min_val < expected_range[0] or max_val > expected_range[1]:
            print(f"   ⚠️  {model_name}: range inhabituel [{min_val}, {max_val}]")
        else:
            print(f"   ✅ {model_name}: range normal [{min_val}, {max_val}]")

    # Pré-traitement identique au local
    img_x = np.expand_dims(preprocess_xception(array_x), axis=0)
    img_r = np.expand_dims(preprocess_resnet(array_r), axis=0)
    img_d = np.expand_dims(preprocess_densenet(array_d), axis=0)
    
    print(f"🔧 Après preprocessing:")
    print(f"   Xception range: [{img_x.min():.6f}, {img_x.max():.6f}]")
    print(f"   ResNet range: [{img_r.min():.6f}, {img_r.max():.6f}]")
    print(f"   DenseNet range: [{img_d.min():.6f}, {img_d.max():.6f}]")

    # Suite du code identique...
    preds = {}
    if model_xcept is not None:
        preds['xception'] = model_xcept.predict(img_x, verbose=0)[0]
        print("\n--- Xception ---")
        for i, (class_name, prob) in enumerate(zip(CLASS_NAMES, preds['xception'])):
            print(f"{class_name}: {prob*100:.2f}%")

    if model_resnet50 is not None:
        preds['resnet50'] = model_resnet50.predict(img_r, verbose=0)[0]
        print("\n--- ResNet ---")
        for i, (class_name, prob) in enumerate(zip(CLASS_NAMES, preds['resnet50'])):
            print(f"{class_name}: {prob*100:.2f}%")

    if model_densenet is not None:
        preds['densenet201'] = model_densenet.predict(img_d, verbose=0)[0]
        print("\n--- DenseNet ---")
        for i, (class_name, prob) in enumerate(zip(CLASS_NAMES, preds['densenet201'])):
            print(f"{class_name}: {prob*100:.2f}%")

    # Combinaison pondérée
    ensemble = np.zeros(len(CLASS_NAMES), dtype=np.float32)
    if 'xception' in preds: ensemble += weights[0] * preds['xception']
    if 'resnet50' in preds: ensemble += weights[1] * preds['resnet50']
    if 'densenet201' in preds: ensemble += weights[2] * preds['densenet201']

    print("\n--- Ensemble avant mel boost ---")
    for i, (class_name, prob) in enumerate(zip(CLASS_NAMES, ensemble)):
        print(f"{class_name}: {prob*100:.2f}%")
    print("Ensemble sum avant mel boost:", np.sum(ensemble))

    # Ajustement pour "mel"
    mel_idx = label_to_index['mel']
    if 'densenet201' in preds:
        old_mel_prob = ensemble[mel_idx]
        ensemble[mel_idx] = 0.5 * ensemble[mel_idx] + 0.5 * preds['densenet201'][mel_idx]
        print(f"\nMel boost: {old_mel_prob*100:.2f}% -> {ensemble[mel_idx]*100:.2f}%")

    print("\n--- Ensemble après mel boost ---")
    for i, (class_name, prob) in enumerate(zip(CLASS_NAMES, ensemble)):
        print(f"{class_name}: {prob*100:.2f}%")

    if normalize:
        ensemble_before_norm = ensemble.copy()
        ensemble = _renorm_safe(ensemble)
        print("\n--- Ensemble final après normalisation ---")
        for i, (class_name, prob) in enumerate(zip(CLASS_NAMES, ensemble)):
            print(f"{class_name}: {prob*100:.2f}%")
        print("Ensemble sum final:", np.sum(ensemble))

    preds['ensemble'] = ensemble
    return preds


# ---- Helpers Grad-CAM ----
LAST_CONV_LAYERS = {
    "xception": "block14_sepconv2_act", 
    "resnet50": "conv5_block3_out", 
    "densenet201": "conv5_block32_concat"
}

def find_last_dense_layer(model):
    for layer in reversed(model.layers):
        if isinstance(layer, keras.layers.Dense):
            return layer
    raise ValueError("Aucune couche Dense trouvée dans le modèle.")

# ---- GRAD-CAM AVEC PROGRESSION OPTIMISÉE ----
def make_gradcam(image_pil, model, last_conv_layer_name, class_index, progress=None):
    """
    Grad-CAM avec progression fluide grâce aux micro-pauses
    """
    if model is None: 
        return np.array(image_pil)
    
    try:
        steps = [
            (5, "🔄 Initialisation..."),
            (10, "🖼️ Analyse de l'image..."),
            (15, "⚙️ Configuration du preprocesseur..."),
            (20, "📐 Redimensionnement image..."),
            (25, "🧠 Configuration du modèle..."),
            (30, "🔗 Création du gradient model..."),
            (35, "⚡ Préparation du calcul..."),
            (40, "🔥 Forward pass..."),
            (45, "📊 Calcul des activations..."),
            (50, "🎯 Extraction classe cible..."),
            (55, "⚡ Calcul du gradient..."),
            (60, "📈 Traitement des gradients..."),
            (70, "📊 Pooling des gradients..."),
            (75, "🎨 Construction heatmap..."),
            (80, "🌡️ Normalisation heatmap..."),
            (85, "🎯 Application colormap..."),
            (90, "🖼️ Redimensionnement final..."),
            (95, "✨ Superposition images..."),
            (100, "✅ Terminé !")
        ]

        step = 0
        def next_step():
            nonlocal step
            if step < len(steps):
                val, desc = steps[step]
                _update_progress(progress, val, desc)
                time.sleep(0.02)  # Micro-pause pour permettre la mise à jour
                step += 1

        next_step()  # 5% - Initialisation

        # Détermination de la taille d'entrée et du preprocesseur
        input_size = model.input_shape[1:3]
        if 'xception' in model.name.lower(): 
            preprocessor = preprocess_xception
        elif 'resnet50' in model.name.lower(): 
            preprocessor = preprocess_resnet
        elif 'densenet' in model.name.lower():
            preprocessor = preprocess_densenet
        else:
            preprocessor = preprocess_densenet

        next_step()  # 10% - Analyse image
        next_step()  # 15% - Config preprocesseur

        # Préparation de l'image
        img_np = np.array(image_pil.convert("RGB"))
        img_resized = cv2.resize(img_np, input_size)
        img_array_preprocessed = preprocessor(np.expand_dims(img_resized, axis=0))

        next_step()  # 20% - Redimensionnement
        next_step()  # 25% - Config modèle

        # Configuration du modèle pour Grad-CAM
        try:
            conv_layer = model.get_layer(last_conv_layer_name)
        except ValueError:
            return img_resized

        grad_model = Model(model.inputs, [conv_layer.output, model.output])
        input_name = get_primary_input_name(model)
        input_for_model = {input_name: img_array_preprocessed}

        next_step()  # 30% - Gradient model
        next_step()  # 35% - Préparation calcul
        next_step()  # 40% - Forward pass

        # Le calcul critique avec étapes intermédiaires
        with tf.GradientTape() as tape:
            next_step()  # 45% - Calcul activations
            
            last_conv_layer_output, preds = grad_model(input_for_model, training=False)
            
            next_step()  # 50% - Extraction classe
            
            if isinstance(preds, list): 
                preds = preds[0]
            class_channel = preds[:, int(class_index)]

        next_step()  # 55% - Calcul gradient

        grads = tape.gradient(class_channel, last_conv_layer_output)
        if grads is None:
            return img_resized

        next_step()  # 60% - Traitement gradients
        next_step()  # 70% - Pooling

        # Pooling des gradients
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        last_conv_layer_output = last_conv_layer_output[0]

        next_step()  # 75% - Construction heatmap

        # Construction de la heatmap
        heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.maximum(heatmap, 0)
        max_val = tf.math.reduce_max(heatmap)
        
        if max_val == 0:
            heatmap = tf.ones_like(heatmap) * 0.5
        else:
            heatmap = heatmap / max_val

        next_step()  # 80% - Normalisation
        next_step()  # 85% - Colormap

        # Conversion et application du colormap
        heatmap_np = heatmap.numpy()
        heatmap_np = np.clip(heatmap_np.astype(np.float32), 0, 1)

        heatmap_resized = cv2.resize(heatmap_np, (img_resized.shape[1], img_resized.shape[0]))
        heatmap_uint8 = np.uint8(255 * heatmap_resized)
        heatmap_colored = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)

        next_step()  # 90% - Redimensionnement
        next_step()  # 95% - Superposition

        # Superposition des images
        img_bgr = cv2.cvtColor(img_resized, cv2.COLOR_RGB2BGR)
        superimposed_img = cv2.addWeighted(img_bgr, 0.6, heatmap_colored, 0.4, 0)

        next_step()  # 100% - Terminé

        return cv2.cvtColor(superimposed_img, cv2.COLOR_BGR2RGB)

    except Exception as e:
        import traceback
        traceback.print_exc()
        _update_progress(progress, 100, "❌ Erreur")
        return np.array(image_pil)

# ===============================================
# ANALYSE MÉDICALE SIMPLIFIÉE BiomedBERT
# ===============================================

def get_medical_analysis_simple(top_class_name, confidence, mel_prob):
    """
    Analyse médicale simplifiée et claire
    """
    global med_nlp
    
    if med_nlp is None:
        return get_fallback_analysis(top_class_name, confidence, mel_prob)
    
    try:
        # Texte médical simple et direct
        medical_text = f"""
        Skin lesion diagnosis: {CLASS_NAMES_FULL.get(top_class_name, top_class_name)}
        Diagnostic confidence: {confidence:.0f}%
        Melanoma risk: {mel_prob:.1f}%
        Clinical assessment required for {top_class_name} lesion evaluation.
        """
        
        # Analyse avec BiomedBERT
        result = med_nlp(medical_text)
        print("DEBUG RESULT:", result)  # debug utile

        if result and len(result) > 0:
            # Gestion des sorties imbriquées : [ [ {label, score}, ... ] ]
            candidates = result[0] if isinstance(result[0], list) else result

            # On prend juste le meilleur score
            best_score = max(candidates, key=lambda x: x['score'])['score']
            
            # Interprétation simple
            bert_assessment = get_simple_bert_assessment(best_score, top_class_name, confidence, mel_prob)
            
            return {
                "status": "success",
                "assessment": bert_assessment['message'],
                "urgency": bert_assessment['urgency'],
                "recommendation": bert_assessment['recommendation']
            }
        else:
            return get_fallback_analysis(top_class_name, confidence, mel_prob)
            
    except Exception as e:
        print(f"Erreur BiomedBERT: {e}")
        return get_fallback_analysis(top_class_name, confidence, mel_prob)


def get_simple_bert_assessment(bert_score, class_name, confidence, mel_prob):
    """
    Assessment cohérent SkinAI + BiomedBERT
    """
    # Cas SkinAI très confiant
    if confidence >= 95:
        message = "✅ Diagnostic confirmé - forte confiance du modèle principal"
        urgency_modifier = ""
    
    # Cas SkinAI moyennement confiant
    elif confidence >= 70:
        if bert_score > 0.6:
            message = "👍 Diagnostic probable - SkinAI et BiomedBERT convergent"
            urgency_modifier = ""
        else:
            message = "⚠️ Diagnostic possible - SkinAI confiant mais BiomedBERT reste incertain"
            urgency_modifier = " (évaluation complémentaire recommandée)"
    
    # Cas SkinAI peu confiant
    else:
        if bert_score > 0.6:
            message = "🤝 Diagnostic appuyé par BiomedBERT malgré faible confiance SkinAI"
            urgency_modifier = ""
        else:
            message = "🔍 Diagnostic incertain - ni SkinAI ni BiomedBERT ne sont sûrs"
            urgency_modifier = " (consultation urgente pour clarification)"
    
    # Urgence de base (selon pathologie + risque mélanome)
    base_urgency = get_base_urgency_simple(class_name, mel_prob)
    
    # Ajustement si vraiment incertain
    if confidence < 70 and bert_score <= 0.6:
        if "routine" in base_urgency.lower():
            urgency = "Consultation sous 2 semaines"
        elif "semaines" in base_urgency:
            urgency = "Consultation sous 1 semaine"
        else:
            urgency = base_urgency
    else:
        urgency = base_urgency
    
    # Recommandation simple
    recommendation = get_simple_recommendation(class_name, mel_prob, bert_score < 0.6 and confidence < 95)
    
    return {
        "message": message,
        "urgency": urgency + urgency_modifier,
        "recommendation": recommendation
    }


def get_base_urgency_simple(class_name, mel_prob):
    """
    Urgence simple selon pathologie
    """
    if class_name == "mel" or mel_prob > 20:
        return "Consultation immédiate (24-48h)"
    elif class_name in ["bcc", "akiec"] or mel_prob > 10:
        return "Consultation sous 2-3 semaines"
    elif mel_prob > 5:
        return "Consultation sous 1 mois"
    else:
        return "Surveillance de routine"

def get_simple_recommendation(class_name, mel_prob, bert_uncertain):
    """
    Recommandation simple et claire
    """
    recommendations = {
        "mel": "🚨 **URGENT** : Rendez-vous dermatologue immédiat pour suspicion de mélanome",
        "bcc": "⚠️ **Important** : Consultation dermatologue pour traitement du carcinome",
        "akiec": "📋 **Surveillance** : Suivi dermatologique pour lésion précancéreuse",
        "bkl": "✅ **Bénin** : Surveillance habituelle, pas d'urgence",
        "df": "📋 **Suivi** : Consultation si changement d'aspect",
        "nv": "✅ **Routine** : Surveillance standard des grains de beauté",
        "vasc": "📋 **Évaluation** : Consultation pour caractérisation complète"
    }
    
    base_rec = recommendations.get(class_name, "📋 Consultation dermatologique recommandée")
    
    # Ajout selon risque mélanome
    if mel_prob > 15:
        base_rec += f"\n⚠️ **Attention** : Risque mélanome élevé ({mel_prob:.0f}%)"
    elif mel_prob > 8:
        base_rec += f"\n📊 Risque mélanome modéré ({mel_prob:.0f}%)"
    
    # Ajout si BERT incertain
    if bert_uncertain:
        base_rec += "\n🔍 **Note** : Présentation atypique détectée, avis spécialisé recommandé"
    
    return base_rec

def get_fallback_analysis(class_name, confidence, mel_prob):
    """
    Analyse de secours si BiomedBERT indisponible
    """
    return {
        "status": "fallback",
        "assessment": "📋 Analyse standard (BiomedBERT indisponible)",
        "urgency": get_base_urgency_simple(class_name, mel_prob),
        "recommendation": get_simple_recommendation(class_name, mel_prob, False)
    }

# --- Fin Bert Doctor



# ---- GESTION ASYNCHRONE / ÉTAT ----
current_image = None
current_predictions = None

# ---- Fonctions pour l'UI Gradio ----
import plotly.graph_objects as go
import numpy as np
import gradio as gr

def quick_predict_ui(image_pil):
    global current_image, current_predictions
    if image_pil is None:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="Veuillez uploader une image pour voir les probabilités",
            height=450,
            template="plotly_white",
            showlegend=False
        )
        
        return (
            '<div class="diagnostic-global"><h2>Veuillez uploader une image.</h2></div>',
            "",
            gr.update(value="", visible=False),
            empty_fig,
            "❌ Erreur: Aucune image fournie.",
            ""
        )
    
    try:
        current_image = image_pil
        all_preds = predict_single(image_pil)
        current_predictions = all_preds
        ensemble_probs = all_preds["ensemble"]
        top_class_idx = int(np.argmax(ensemble_probs))
        top_class_name = CLASS_NAMES[top_class_idx]
        global_diag = diagnosis_map[top_class_name]
        
        mel_idx = CLASS_NAMES.index("mel")
        mel_prob = ensemble_probs[mel_idx] * 100
        confidence = ensemble_probs[top_class_idx] * 100
        
        # ANALYSE MÉDICALE SIMPLIFIÉE 
        medical_analysis = get_medical_analysis_simple(top_class_name, confidence, mel_prob)
        
        desc_top = description.get(top_class_name, "")
        
       
        # HTML diagnostic global
        if global_diag == "Malin":
            global_diag_html = f'''
            <div class="diagnostic-global clearfix">
                <img src="https://huggingface.co/spaces/ericjedha/skin_care/resolve/main/mel.webp" width="150" style="float:left;margin-right:10px;">
                <div>
                    <span style="font-size:16px;font-weight:bold;">Diagnostic Global</span><br>
                    <div class="highlight malin">
                        {global_diag} : {ensemble_probs[top_class_idx]*100:.2f}% ▪ {top_class_name.upper()}*
                    </div>
                </div>
            </div>
            '''
        else:
            img_src = "non-mel.webp" if global_diag == "Bénin" else "mel.webp"
            global_diag_html = f'''
            <div class="diagnostic-global clearfix">
                <img src="https://huggingface.co/spaces/ericjedha/skin_care/resolve/main/{img_src}" width="150" style="float:left;margin-right:10px;">
                <div>
                    <span style="font-size:16px;font-weight:bold;">Diagnostic Global</span><br>
                    <div class="highlight benin">
                        {global_diag} : {ensemble_probs[top_class_idx]*100:.2f}% ▪ {top_class_name.upper()}*
                    </div>
                </div>
            </div>
            '''
        
        output_text_html = f'<div class="warning-message"><strong>* Explication du résultat</strong> : {desc_top}</div>'
        
        warning_visible = False
        warning_html = ""
        if mel_prob > 5 and top_class_name != "mel":
            warning_html = f'''
            <div class="warning-message">
                <img src="https://huggingface.co/spaces/ericjedha/skin_care/resolve/main/mel-modere.webp" width="150" style = "float:left"> Le modèle a détecté un risque modéré de mélanome <strong>({mel_prob:.1f}%)</strong>.
                <strong>Veuillez consulter votre médecin pour lever tout doute</strong>.
            </div>
            '''
            warning_visible = True
        
        # HTML MÉDICAL SIMPLIFIÉ 
        biomed_html = format_simple_medical_html(medical_analysis)
        
        # Graphique (inchangé) 
        probabilities = [round(ensemble_probs[i] * 100, 2) for i in range(len(CLASS_NAMES))]
        colors = ['#ff6b6b' if name == top_class_name else '#4ecdc4' for name in CLASS_NAMES]
        
        fig = go.Figure(data=[
            go.Bar(
                x=CLASS_NAMES,
                y=probabilities,
                text=[f'{p:.2f}%' for p in probabilities],
                textposition='outside',
                marker_color=colors,
                hovertemplate='<b>%{x}</b><br>Probabilité: %{y:.2f}%<extra></extra>'
            )
        ])
        
        fig.update_layout(
            xaxis_title="Classes",
            yaxis_title="Probabilité (%)",
            yaxis=dict(range=[0, max(probabilities) * 1.15]),
            height=450,
            template="plotly_white",
            showlegend=False,
            font=dict(size=12),
            margin=dict(l=50, r=50, t=70, b=100)
        )
        
        fig.update_xaxes(tickangle=45)
        
        return (
            global_diag_html,
            output_text_html,
            gr.update(value=warning_html, visible=warning_visible),
            fig,
            "✅ Analyse terminée.",
            biomed_html  # HTML SIMPLIFIÉ
        )
        
    except Exception as e:
        error_fig = go.Figure()
        error_fig.update_layout(
            title=f"Erreur lors de la création du graphique: {str(e)}",
            height=450,
            template="plotly_white",
            showlegend=False
        )
        
        error_biomed_html = f'''
        <div class="medical-analysis" style="background: #ffebee; color: #d32f2f; padding: 15px; border-radius: 10px; border: 1px solid #ef9a9a;">
            <h3>🧬 Analyse Médicale</h3>
            <p>❌ Erreur lors de l'analyse</p>
        </div>
        '''
        
        return (
            f'<div class="diagnostic-global"><h2>Erreur: {str(e)}</h2></div>',
            "",
            gr.update(value=f'''
            <div class="warning-message" style="background-color:#ffebee;border:1px solid #ef9a9a;">
                ❌ Une erreur est survenue : {str(e)}
            </div>
            ''', visible=True),
            error_fig,
            f"❌ Erreur: {str(e)}",
            error_biomed_html
        )
        
def format_simple_medical_html(medical_analysis):
    """
    HTML simple et clair pour l'analyse médicale
    """
    
    if medical_analysis['status'] == 'error':
        return f'''
        <div class="medical-analysis" style="background: #ffebee; color: #d32f2f; padding: 15px; border-radius: 10px;">
            <h3>🧬 Analyse Médicale</h3>
            <p>❌ Erreur lors de l'analyse</p>
        </div>
        '''
    
    # Couleur selon le type d'assessment
    if "✅" in medical_analysis['assessment']:
        bg_color = "linear-gradient(135deg, #4caf50 0%, #66bb6a 100%)"
    elif "⚠️" in medical_analysis['assessment']:
        bg_color = "linear-gradient(135deg, #ff9800 0%, #ffb74d 100%)"
    elif "🔍" in medical_analysis['assessment']:
        bg_color = "linear-gradient(135deg, #f44336 0%, #ef5350 100%)"
    else:
        bg_color = "linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)"
    
    html = f'''
    <div class="medical-analysis" style="background: {bg_color}; color: white; padding: 20px; border-radius: 12px; margin-top: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
        <h3 style="margin: 0 0 15px 0; font-size: 18px;">
            🤖 BiomedBERT : 2<sup>e<sup> avis
        </h3>
        
        <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px; margin-bottom: 15px;">
            <strong>🎯 Évaluation IA :</strong><br>
            <div style="margin-top: 8px; font-size: 16px;">{medical_analysis['assessment']}</div>
        </div>
        
        <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px; margin-bottom: 15px;">
            <strong>⏰ Délai recommandé :</strong><br>
            <div style="margin-top: 8px; font-size: 16px; font-weight: bold;">{medical_analysis['urgency']}</div>
        </div>
        
        <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 8px; border-left: 4px solid #ffd700;">
            <strong>💡 Recommandations :</strong><br>
            <div style="margin-top: 10px; line-height: 1.6; white-space: pre-line;">{medical_analysis['recommendation']}</div>
        </div>
    </div>
    '''
    
    return html

def generate_gradcam_ui(progress=gr.Progress()):
    global current_image, current_predictions
    if current_image is None or current_predictions is None:
        return None, "❌ Aucun résultat précédent — lance d'abord l'analyse rapide."
    
    try:
        ensemble_probs = current_predictions["ensemble"]
        top_class_idx = int(np.argmax(ensemble_probs))

        # Sélection des modèles disponibles
        candidates = []
        if model_xcept is not None:
            candidates.append(("xception", model_xcept, current_predictions["xception"][top_class_idx]))
        if model_resnet50 is not None:
            candidates.append(("resnet50", model_resnet50, current_predictions["resnet50"][top_class_idx]))
        if model_densenet is not None:
            candidates.append(("densenet201", model_densenet, current_predictions["densenet201"][top_class_idx]))

        if not candidates:
            return None, "❌ Aucun modèle disponible pour Grad-CAM."

        # Choix du meilleur modèle
        explainer_model_name, explainer_model, conf = max(candidates, key=lambda t: t[2])
        explainer_layer = LAST_CONV_LAYERS.get(explainer_model_name)

        # Génération Grad-CAM avec progression fluide
        gradcam_img = make_gradcam(
            current_image,
            explainer_model,
            explainer_layer,
            class_index=top_class_idx,
            progress=progress
        )

        return gradcam_img, f"✅ Grad-CAM généré avec {explainer_model_name} (confiance: {conf:.1%})"

    except Exception as e:
        import traceback
        traceback.print_exc()
        return None, f"❌ Erreur: {e}"


# ---- INTERFACE GRADIO ----

example_paths = ["ISIC_0024627.jpg", "ISIC_0025539.jpg", "ISIC_0031410.jpg"]

import pandas as pd
import gradio as gr

with gr.Blocks(theme=theme, title="Analyse de lésions", css=css) as demo:
    gr.Markdown("# 🔬 Skin Care : analyse de lésions cutanées")
    
    models_status = []
    if model_resnet50:
        models_status.append("☑ ResNet50")
    if model_densenet:
        models_status.append("☑ DenseNet201")
    if model_xcept:
        models_status.append("☑ Xception")
    
    gr.Markdown(f"**Avertissement 🚨** cette application est un projet d'étudiant. **Seul votre médecin est habilité à vous donner un diagnostic**.")
    gr.Markdown(f"**Étape 1️⃣** L'analyse rapide vous donnera le diagnostic global en 10s. **Étape 2️⃣**: le rendu de la carte colorée de votre lésion peut pendre jusqu'à 60s.")
  
    
    with gr.Row():
        with gr.Column(scale=1):
            input_image = gr.Image(type="pil", label="📸 Uploader une image")
            
            with gr.Row():
                quick_btn = gr.Button("Analyse Rapide", variant="primary")
                gradcam_btn = gr.Button("Carte colorée (option)", variant="secondary")
            
            gr.Examples(examples=example_paths, inputs=input_image)
            output_gradcam = gr.Image(label="🔍 Carte Colorée Grad-CAM")
            output_status = gr.Textbox(label="Statut", interactive=False)
            
        
        with gr.Column(scale=2):
            output_label = gr.HTML(
                value='<h3 class="output-class">Pour obtenir un diagnostic, uploadez une image ou prenez une photo.</h3>',
                elem_classes="diagnostic-global"
            )
            
            #gr.Markdown("### 💡 Explication")
            output_text = gr.HTML(
                value="",
                elem_classes="warning-container"
            )
            
            output_warning = gr.HTML(
                value="",
                elem_classes="warning-container",
                visible=False
            )
            
            # CORRECTION : Configuration simplifiée du BarPlot
            # Créer un DataFrame initial vide ou avec des valeurs par défaut
            initial_df = pd.DataFrame({
                'Classes': CLASS_NAMES,
                'Probabilités (%)': [0] * len(CLASS_NAMES)
            })
            
          # Configuration correcte du BarPlot
            output_plot = gr.Plot(label="Probabilités par classe")
            # NOUVEAU: Output pour l'analyse BiomedBERT
            output_medical = gr.HTML(label="🧬 Analyse Médicale Avancée")

    gr.HTML(value="""<div><hr style="width:50%; border-top: 2px #a855f7; height: 10px; border-style:dotted; margin: auto;"></div>""")
    gr.Markdown(f"Ensemble de modèles utilisés : {', '.join(models_status) if models_status else 'AUCUN'}")
    gr.HTML(value="""
      
           <strong>☷ Dataset utilisé</strong> pour l'entrainement des modèles SkinAI : HAM10000, ce dataset HAM10000 a été créé par une équipe internationale dirigée par des chercheurs autrichiens, allemands et australiens.  <br>
          <strong> 🤖 Les modèles de Machine Learning SkinAI : </strong> <em> 🤖 Xception</em> - Réseau de convolution profond (CNN), <em> 🤖 ResNet50</em> - Réseau résiduel (Residual Network), 🤖 DenseNet201 - Réseau dense (Dense Convolutional Network). <br> 
        <strong> 🤖 BiomedBERT : </strong> : Microsoft BiomedBERT est un modèle de langage spécialisé dans le domaine biomédical, développé par Microsoft. Il vient en soutient pour des conseils sur les données de la prédiction. <br> 
<strong>🏛️ RGPD & Digital Act </strong> : 
                Ce dataset ne peut pas être utilisé pour des cas réels aujourd'hui notamment du fait qu'il ne comporte qu'essentiellement des peaux de populations européennes (allemands et autrichiens). <br>Cette application ne collecte pas vos données personnelles. <b>Les images uploadées ne sont pas stockées</b>. <br>La politique de Cookies 🍪 est gérée par <a href='https://huggingface.co/privacy'>Hugging Face disponible ici</a>.
            """)
    
    # Configuration des événements
    quick_btn.click(
        fn=quick_predict_ui,
        inputs=input_image,
        outputs=[output_label, output_text, output_warning, output_plot, output_status, output_medical], 
    )
    
    gradcam_btn.click(
        fn=generate_gradcam_ui,
        inputs=[],
        outputs=[output_gradcam, output_status]
    )

demo.launch()