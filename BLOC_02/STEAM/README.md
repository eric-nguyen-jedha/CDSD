# 🎮 Analyse du marché des jeux vidéo sur STEAM

## Présentation en ligne de l'intégralité du projet

    - 🚀 [Bloc_02 | STEAM | Présentation PPT](https://docs.google.com/presentation/d/1iA0d8a61Xe0CGdzGdr_txMafjTKgjHRIpyGMY0GhXVs/edit?usp=sharing)

    🔗 [Notebook STEAM Databricks : Analyse exploratoire et macro-tendances](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/1888944128040884/2162191964142929/4822527639717588/latest.html)  


## 📌 Description du projet

Ce projet a été réalisé dans le cadre d'une mission pour **Ubisoft**, éditeur de jeux vidéo français. L'objectif est d'analyser l'écosystème des jeux disponibles sur la plateforme **Steam** afin d'identifier les tendances actuelles du marché, comprendre les facteurs influençant la popularité ou les ventes des jeux, et fournir des insights stratégiques pour le lancement d’un nouveau jeu révolutionnaire.

L’analyse s’appuie sur un jeu de données extrait de la plateforme Steam et est réalisée à l’aide de **PySpark** sur **Databricks**, avec des visualisations intégrées via l’outil de dashboarding de Databricks.

---




## 🧠 Objectifs

- Comprendre les tendances globales du marché des jeux vidéo sur Steam.
- Identifier les facteurs influençant la popularité ou les ventes d’un jeu.
- Réaliser une analyse multi-niveaux :
  - **Analyse macro** : Éditeurs, notes, dates de sortie, tarifs, langues, classification par âge.
  - **Analyse par genre** : Genres les plus présents, ratio de critiques positives/négatives, éditeurs spécialisés, rentabilité.
  - **Analyse par plateforme** : Disponibilité selon OS, répartition des genres par plateforme.

---

## 🛠️ Technologies utilisées

- **PySpark** pour le traitement distribué des données
- **Databricks** pour l’environnement de développement et les visualisations
- Données stockées sur **AWS S3** :  
  `s3://full-stack-bigdata-datasets/Big_Data/Project_Steam/steam_game_output.json`

---

## 📊 Visualisations

Les visualisations ont été créées à l’aide de l’outil de dashboarding intégré à Databricks. Elles sont accessibles via les liens ci-dessous :

🔗 [Notebook 1 : Analyse exploratoire et macro-tendances](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/1888944128040884/2162191964142929/4822527639717588/latest.html)  


---

## 📁 Structure du projet


├── STEAM_Eric_NGUYEN.ipynb                         # copie notebook Databricks à exécuter dans Databricks
└── STEAM_Eric_NGUYEN.html                          # Export en HTML du Notebook et des graphiques