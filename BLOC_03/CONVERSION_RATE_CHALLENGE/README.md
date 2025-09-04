# 🚀 CONVERSION RATE CHALLENGE / Défi Machine Learning : Prédiction du taux de conversion d'une newsletter

## Présentation en ligne de l'intégralité du projet format PPT (en ligne)

🚀 [Bloc_03 | CONVERSION CHALLENGE RATE | Présentation PPT](https://docs.google.com/presentation/d/1l7D3cePxp5DkGZkV8FC5N3CG_gzhZjMiYuP-MLO1ebQ/edit?usp=sharing)

> *Prédire si un utilisateur va s'abonner à www.datascienceweekly.org*

---

## 📌 Présentation du projet

Ce projet s'inspire des compétitions de machine learning organisées sur des plateformes comme [Kaggle](https://www.kaggle.com/). L'objectif est de concevoir un modèle prédictif capable de déterminer si un visiteur du site **www.datascienceweekly.org** va s'abonner à la newsletter hebdomadaire.

La particularité de ce défi :
- Entraînement sur le fichier `data_train.csv` (données labelisées).
- Génération de prédictions sur `data_test.csv` (données sans labels).
- Soumission des prédictions à l’enseignant ou assistant qui évaluera les performances **de manière indépendante**.
- Un classement (leaderboard) est mis en place pour comparer les équipes selon le **score F1**.

Au-delà de la performance, ce projet vise à **comprendre les comportements des utilisateurs** et à proposer des recommandations concrètes pour améliorer le taux de conversion.

---

## 🏢 Contexte de l'entreprise

**www.datascienceweekly.org** est une newsletter populaire, créée et animée par des data scientists indépendants. Chaque semaine, elle envoie des actualités, articles et ressources sur le monde du data science à des milliers d’abonnés.

L’équipe souhaite mieux comprendre les profils des visiteurs de leur site et identifier quels facteurs incitent un utilisateur à s’abonner. Pour cela, ils ont ouvert un jeu de données anonymisé et lancé un défi de modélisation.

---

## 🎯 Objectifs du projet

Le projet se déroule en quatre étapes clés :

### Partie 1 : Analyse exploratoire et modèle de base
- Réaliser une **analyse exploratoire des données (EDA)**.
- Nettoyer et préparer les données (encodage, mise à l’échelle, gestion des valeurs manquantes).
- Entraîner un **modèle de base** (ex. : régression logistique) sur `data_train.csv`.
- Évaluer les performances avec le **F1-score** et la matrice de confusion.

### Partie 2 : Amélioration du modèle
- Explorer différentes approches : sélection de variables, création de features, modèles non linéaires (Random Forest, XGBoost, etc.).
- Optimiser les hyperparamètres (Grid Search, Random Search).
- Maximiser le **F1-score sur le jeu de validation**.

### Partie 3 : Soumission des prédictions
- Appliquer le meilleur modèle à `data_test.csv`.
- Générer un fichier de prédictions au format `.csv`.
- Soumettre les résultats à l’enseignant (comme sur Kaggle).
- Plusieurs soumissions possibles : itérez et améliorez !

### Partie 4 : Analyse et recommandations
- Interpréter les paramètres du meilleur modèle (coefficients, importance des variables).
- Identifier les leviers d’action pour **augmenter le taux de conversion**.
- Proposer des recommandations concrètes à l’équipe de la newsletter.

---

## 📊 Description du jeu de données

Le jeu de données est divisé en deux fichiers :

| Fichier             | Contenu |
|---------------------|--------|
| `conversion_data_train.csv`    | Données étiquetées : variables explicatives (`X`) + variable cible (`Y`) → pour l’entraînement. |
| `conversion_data_test.csv`     | Données non étiquetées : seulement les variables explicatives (`X`) → pour générer les prédictions. |

🔍 **Variable cible** : `subscribed` (0 = non abonné, 1 = abonné)  
🎯 **Métrique d’évaluation** : **F1-score** (pour bien équilibrer précision et rappel, surtout en cas de déséquilibre des classes)

---

## 🛠️ Méthodologie

### 1. Analyse exploratoire (EDA)
- Visualisation des distributions (histogrammes, boîtes à moustaches).
- Analyse de la corrélation entre variables.
- Étude de la balance des classes (abonnés vs non abonnés).
- Détection des valeurs manquantes ou aberrantes.

### 2. Prétraitement
- Encodage des variables catégorielles (One-Hot, Label Encoding).
- Mise à l’échelle des variables numériques.
- Séparation `X` / `y` et création d’un jeu de validation.

### 3. Entraînement & évaluation
- Comparaison de plusieurs modèles (Regression logistique, Random Forest, etc.).
- Validation croisée et optimisation des hyperparamètres.
- Suivi du F1-score sur le jeu de test.

### 4. Soumission
- Génération des prédictions sur `conversion_data_test.csv`.

### 5. Interprétation
- Analyse de l’importance des variables.
- Retour métier : que faut-il améliorer sur le site ?


---

## 📦 Livrables attendus

✅ Votre équipe doit fournir :

- [X] Des **visualisations pertinentes** issues de l’EDA.
- [X] Au moins un **modèle entraîné et évalué** (F1-score, matrice de confusion).
- [X] Au moins une **soumission de prédictions** (fichier `conversion_data_test_predictions_EXAMPLE.csv`).
- [X] Une **analyse des paramètres du meilleur modèle**.
- [X] Des **recommandations concrètes** pour améliorer le taux de conversion.

---

## 🧪 Résultats

cf. le powerpoint

🏆 **Meilleur F1-score (validation)** : `TBD`  
🏅 **Classement sur le leaderboard** : `18`

---

## 🔍 Analyse & Recommandations

cf. le powerpoint

### 🔑 Variables les plus importantes

- `source` : Ads, SEO, Direct.
- `pages_visited` : nombre de pages consultées, fortement corrélé à l’abonnement.
- `country` : certains pays montrent un intérêt plus marqué.

### 💡 Recommandations
1. **Optimiser l’expérience utilisateur** pour augmenter le temps passé sur le site.
2. **Cibler différemment les campagnes publicitaires** selon la source de trafic.
3. **Ajouter un call-to-action personnalisé** après un certain nombre de pages vues.
4. **Traduire la newsletter** dans les langues des pays à fort potentiel.

Ces actions pourraient augmenter significativement le taux de conversion à moyen terme.

---

---

## 📁 Structure du projet

```
├── Conversion_rate_challenge_EDA.ipynb                             # EDA sur Dataset conversion_data_train.csv (www.datascienceweekly.org)
├── Conversion_Rate_Challenge_First_Models.ipynb                    # Premiers models 
├── Conversion_Rate_Challenge_Outliers_Managed.ipynb                # Notebook Outliers
├── Conversion_Rate_Challenge_OverSampling_Managed.ipynb            # Notebook techniques oversampling
├── conversion_data_train.csv                                       # Fichier CSV dataset principal
├── conversion_data_test.csv                                        # jeu de test conversion_data_test.csv
├── conversion_predictions.csv                                      # Csv prédictions du meilleur modèle à partir de 
├── conversion_data_test_predictions_Eric-Nguyen-DS33-V1.csv        # CSV destiné au Leaderboard Jedha
├── tmp                                                             #fichier tmp de dfSummary
└── *.pkl                                                           # fichier de sauvegarde du meilleur modèle

```