# 🌿 Projet Skin Care : Détection du Cancer de la Peau avec HAM10000

## Présentation en ligne de l'intégralité du projet format PPT (en ligne)

🚀 [Bloc_06 | SKIN CARE | Présentation PPT](https://docs.google.com/presentation/d/1jjPDLllbmfmCwJi0SOWlGYPsyd-dTxhHc0USfRqngQU/edit?usp=sharing)\
📁 [Bloc_06 | SKIN CARE | Backup GitHub](https://github.com/eric-nguyen-jedha/CDSD/tree/main/BLOC_6)\
💻 [App Desktop conseillé](https://huggingface.co/spaces/ericjedha/skin_care)

> **Développé par** : [ERIC NGUYEN] | **Date** : 2025


## 📚 Résumé

Ce projet vise à développer un système d'IA capable de détecter automatiquement les cancers de la peau (notamment le mélanome) à partir d'images dermatoscopiques. En utilisant le jeu de données **HAM10000**, nous entraînons un ou plusieurs modèles de deep learning pour classifier 7 types de lésions cutanées. L'objectif final est de déployer une application web permettant aux utilisateurs de charger une image de lésion et d'obtenir une prédiction en temps réel.

---

## 📁 Sources et Historique du jeu de données HAM10000

Le jeu de données **HAM10000 (Human Against Machine with 10000 training images)** est l'un des jeux de données les plus utilisés dans la recherche sur la détection automatique du cancer de la peau. Il a été publié en 2018 par une équipe internationale de chercheurs en dermatologie et en intelligence artificielle.

### 🔍 Origine
- **Plateforme** : [Kaggle](https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000)
- **Nom du dataset** : *Skin Cancer MNIST: HAM10000*
- **Auteurs** : K. Codella, V. Rotemberg, P. Tschandl, et al.
- **Publication associée** :  
  > Tschandl, P., Rosado, B., & Kittler, H. (2018). *The HAM10000 dataset: A large collection of multi-source dermatoscopic images of common pigmented skin lesions*. Scientific Data, 5, 180161.

### 🧾 Description du dataset
- **Nombre d'images** : ~10 000 images en 600x450 pixels (RGB)
- **Classes** : 7 types de lésions :
  1. **Melanoma (mel)** – Mélanome (cancer grave)
  2. **Melanocytic nevus (nv)** – Névi mélanocytaire (bénin)
  3. **Basal cell carcinoma (bcc)** – Carcinome basocellulaire
  4. **Actinic keratosis (akiec)** – Kératose actinique
  5. **Benign keratosis (bkl)** – Kératose bénigne
  6. **Dermatofibroma (df)** – Dermatofibrome
  7. **Vascular lesion (vasc)** – Lésion vasculaire

- **Origines** : Images collectées à partir de plusieurs sources (BCN, MSD, etc.) et harmonisées par sur-échantillonnage pour équilibrer les classes.

---

## 🎯 Objectifs du Projet

1. **Prétraiter** le dataset HAM10000 (nettoyage, augmentation, normalisation)
2. **Entraîner** plusieurs modèles de deep learning (CNN, ResNet, EfficientNet, Xception etc.)
3. **Évaluer** les performances (précision, rappel, F1-score, matrice de confusion)
4. **Sélectionner** le meilleur modèle ou combiner plusieurs modèles (ensemble learning)
5. **Déployer** une application web interactive (Flask, Streamlit ou FastAPI + React)

---

## ✅ Livrables

| Numéro | Livrable | Description |
|--------|---------|-------------|
| 1 | Modèle(s) d'IA entraîné(s) | Fichiers [Xception.keras - 428mo](https://huggingface.co/spaces/ericjedha/skin_care/resolve/main/Xception.keras), [Resnet50.kears - 493mo](https://huggingface.co/ericjedha/resnet50/resolve/main/Resnet50.keras), [Densenet201 - 337 mo](https://huggingface.co/ericjedha/densenet201/resolve/main/Densenet201.keras)|
| 2 | Pipeline de prétraitement & entrainement| Notebooks (Jupyter)|
| 3 | Scripts d'entraînement & évaluation | Notebooks (Jupyter) ou scripts Python bien documentés |
| 4 | Application de détection | Interface web ou mobile Gradio sur Hugging Face |
| 5 | Documentation complète | Ce fichier `README.md`, rapport technique, guide d'installation |

---

## 🛠️ Technologies Utilisées

- **Langage** : Python 3.10
- **Deep Learning** : TensorFlow 
- **Librairies** : NumPy, Pandas, OpenCV, Scikit-learn, Matplotlib, Seaborn
- **Déploiement** : Flask / Streamlit / FastAPI + HTML/CSS/JS
- **Hébergement** : Hébergement Hugging Face, GRADIO

---

Note : j'ai fait des centaines des notebook pour ce projet et des centaines de modèles, mais je ne mets en ligne que les plus emblématiques.

## 📁 Structure du projet 
```
├── SKIN_CARE_EDA.ipynb                            # EDA HAM10000
├── ISIC_0024627.jpg                               # Image d'Exemple
├── ISIC_0025539.jpg                               # Image d'Exemple
├── ISIC_0031410.jpg                               # Image d'Exemple
├── mel.webp                                       # image pour indiquer qu'il y a un "Melanome"
├── mel-modere.webp                                # image pour indiquer qu'il y a un risque de "Melanome" modéré
├── mel.webp                                       # image pour indiquer qu'il y a un risque de "Melanome" avéré
├── Protocole-S-Xception-C.ipynb                   # Notebook du modèle Xception
├── Protocole-S-Resnet50-C.ipynb                   # Notebook du modèle Resnet50
├── Protocole-S-Densenet201-C.ipynb                # Notebook du modèle Desnet201
├── Protocole-S-Test-MODELS.ipynb                  # Test des modèles enregistrés et création d'ENSEMBLE
├── README_SkinCare.md                             # README.md Appli Skin Care
├── requirements.txt                               # Requirements pour faire fonctionner l'application Gradio
├── BLOC_06_Skin_Care.pdf                          # Version PDF de la présentation PPT
└── README.md                                          

```
