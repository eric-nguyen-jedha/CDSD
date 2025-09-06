# Projet Deep Learning : Détecteur de SMS Spam pour AT&T 🕵️‍♀️

## Présentation en ligne de l'intégralité du projet format PPT (en ligne)

🚀 [Bloc_04 | AT&T | Présentation PPT](https://docs.google.com/presentation/d/1_qHooQ-wBEsJn40m6o-F9Ewuvo7-AgexCJdcCrQiLg4/edit?usp=sharing) \
🚀 [Bloc_04 | AT&T | Backup GitHub](https://github.com/eric-nguyen-jedha/CDSD/tree/main/BLOC_04/AT%26T) \

![AT&T Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/AT%26T_logo.svg/1200px-AT%26T_logo.svg.png)

## 📇 Description de l'entreprise

**AT&T Inc.** est une entreprise américaine multinationale de télécommunications, dont le siège social est situé à Dallas, Texas. Elle est classée comme la plus grande entreprise de télécommunications au monde en termes de chiffre d’affaires et constitue le troisième plus grand fournisseur de services téléphoniques mobiles aux États-Unis.

En 2022, AT&T figurait à la **13ᵉ position** du classement Fortune 500 des plus grandes entreprises américaines, avec un chiffre d’affaires s’élevant à **168,8 milliards de dollars**. 🚀

## 🚧 Contexte du projet

L’un des principaux défis auxquels sont confrontés les utilisateurs d’AT&T est l’**afflux constant de messages indésirables (spams)** via SMS. Bien que l’entreprise ait mis en place un système de signalement manuel, celui-ci s’avère lent, inefficace à grande échelle et incapable de réagir en temps réel.

Afin d’améliorer l’expérience utilisateur et de renforcer la sécurité, AT&T souhaite **automatiser la détection des spams** à partir du contenu des messages texte.

## 🎯 Objectif

Concevoir un **modèle de détection de spam basé sur le Deep Learning**, capable d’analyser automatiquement le contenu d’un SMS et de prédire s’il s’agit d’un **spam** ou d’un message légitime (**ham**).

Le modèle devra être précis, rapide et déployable à grande échelle dans l’infrastructure d’AT&T.

## 🖼️ Périmètre du projet

Le projet se concentre sur l’analyse de messages texte (SMS) à l’aide de techniques de **Deep Learning**. Nous utiliserons un jeu de données public largement reconnu dans le domaine de la classification de textes :

🔗 **[Télécharger le jeu de données](https://full-stack-bigdata-datasets.s3.eu-west-3.amazonaws.com/Deep+Learning/project/spam.csv",encoding='Windows-1252)**  
*(Dataset "SMS Spam Collection" - UCI Machine Learning Repository)*

Ce jeu de données contient :
- **5 574 SMS** étiquetés
- Deux catégories : `spam` ou `ham` (message légitime)
- Texte brut en anglais

## 🦮 Conseils & Bonnes Pratiques

### ✅ Commencez simple
Un bon modèle de Deep Learning n’a pas besoin d’être complexe dès le départ. Commencez par des architectures basiques (ex : LSTM, GRU) avant d’ajouter de la complexité.

### 🔁 Utilisez le transfert d’apprentissage (Transfer Learning)
Étant donné la taille modeste du jeu de données, envisagez d’utiliser des modèles pré-entraînés sur de grands corpus textuels :
- **BERT**, **DistilBERT**
- Utilisation via `Hugging Face Transformers` ou `Pytorch`

Cela permettra de tirer parti de représentations linguistiques riches, même avec peu de données.

### 🧹 Prétraitement du texte
Assurez-vous de bien nettoyer les données :
- Suppression des ponctuations, chiffres, caractères spéciaux
- Passage en minuscules
- Tokenisation
- Suppression des stopwords (facultatif)
- Lemmatisation ou stemming (optionnel)

### 📊 Évaluation du modèle
Mesurez les performances à l’aide des métriques suivantes :
- **Précision (Precision)**
- **Rappel (Recall)**
- **F1-Score**
- **Matrice de confusion**

> Le rappel est particulièrement important : il est crucial de **ne pas manquer de spams** (faux négatifs coûteux et dangereux).

## 📬 Livrables attendus


1. **Un notebook Jupyter (`.ipynb`)** contenant :
   - Le chargement et l’analyse exploratoire des données (EDA)
   - Le prétraitement du texte
   - L’entraînement d’**au moins un modèle de Deep Learning**
   - L’évaluation des performances
   - Des visualisations claires (ex : courbes de perte, matrice de confusion)

2. **Une description claire des performances** obtenues :
   - Précision, Rappel, F1
   - Comparaison entre modèles (si plusieurs implémentés)


## 📁 Structure du projet 
```
├── AT&T_EDA.ipynb                           # EDA 
├── AT&T_CNN.ipynb                           # Model CNN Maison
├── AT&T_GRU.ipynb                           # Modèle sous GRU
├── Bert-Pytorch.ipynb                       # Modèle sous Bert/Pytorch  
├── distilbert_ATT/                             # Répertoire du modèle sauvegardé
│   ├── config.json                             # Configuration du modèle
│   ├── model.safetensors                       # Poids du modèle (format sécurisé)
│   ├── tokenizer_config.json                   # Configuration du tokeniseur
│   ├── tokenizer.json                          # Tokeniseur (règles et vocabulaire)
│   ├── vocab.txt                               # Vocabulaire complet
│   ├── special_tokens_map.json                 # Mappage des tokens spéciaux
│   └── metadata.tsv                            # Métadonnées optionnelles
├── models/                                   # Répertoire des modèles sauvegardés
│   ├── spam_model_CNN.h5                        # Modèle CNN
│   ├── models/spam_model_GRU.h5                 # Mdoèle GRU
│   ├── tokenizer_config.json                   # Configuration du tokeniseur
└── README.md                                   # fichier README.md

```