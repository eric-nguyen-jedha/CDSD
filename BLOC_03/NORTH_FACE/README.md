# 🧠 Unsupervised Machine Learning Project – The North Face E-commerce

## Présentation en ligne de l'intégralité du projet format PPT (en ligne)

🚀 [Bloc_03 | THE NORTH FACE | Présentation PPT](https://docs.google.com/presentation/d/1hfvY3ckot4buHsXQ9mwjAD1pvYWUfzSY81Htd5GqJoA/edit?usp=sharing) \
📁 [Bloc_03 | THE NORTH FACE | Présentation PPT](https://github.com/eric-nguyen-jedha/CDSD/tree/main/BLOC_03/NORTH_FACE) \

> *Analyse des descriptions produits pour construire un système de recommandation et découvrir des thèmes cachés dans le catalogue*

---

## 🏢 Description de l'entreprise 📇

**The North Face** est une entreprise américaine spécialisée dans les produits pour les activités de plein air, fondée en 1968 pour approvisionner les alpinistes. La marque conçoit des vêtements, des chaussures et du matériel d'extérieur. À la fin des années 1990, sa clientèle s'est élargie au-delà des passionnés d'activités outdoor, et dans les années 2000, elle est devenue un symbole de style, tout en conservant son expertise technique.

🌐 Site web : [https://www.thenorthface.fr/](https://www.thenorthface.fr/)

---

## 🚧 Présentation du projet

Le département marketing de The North Face souhaite exploiter les **méthodes d'apprentissage non supervisé** pour améliorer l'expérience utilisateur et augmenter les taux de conversion sur son site e-commerce. Deux axes principaux ont été identifiés :

1. **Système de recommandation** : Proposer aux utilisateurs des produits similaires via une section *"Vous pourriez aussi aimer..."* sur chaque page produit.
2. **Réorganisation du catalogue** : Utiliser la modélisation de thèmes (topic modeling) pour remettre en question les catégories existantes et améliorer la navigation sur le site.

Ce projet consiste à analyser les descriptions produits à l’aide de techniques de **clustering** et de **modélisation de thèmes** afin d’extraire des insights exploitables.

---

## 🎯 Objectifs

Le projet est divisé en trois étapes clés :

1. **Identifier des groupes de produits** aux descriptions similaires via un algorithme de clustering.
2. **Construire un système de recommandation simple** basé sur ces groupes.
3. **Appliquer une méthode de modélisation de thèmes (LSA)** pour découvrir automatiquement les sujets latents dans les descriptions.

---

## 🖼️ Périmètre du projet

- **Données** : Corpus de descriptions de produits extraites du catalogue The North Face.
- **Méthodes** : Traitement du langage naturel (NLP), vectorisation TF-IDF, clustering (DBSCAN), réduction de dimension (TruncatedSVD).
- **Outils** : Python, `pandas`, `scikit-learn`, `spacy`, `wordcloud`, `matplotlib`.

📥 **Jeu de données** : [👉 Catalogue produits The North Face 👈](#)  
*sample-data.csv*

---

## 🛠️ Méthodologie

### 1. Prétraitement du texte
- Nettoyage des descriptions (ponctuation, caractères spéciaux, etc.).
- Suppression des mots vides (stop words) et lemmatisation avec **spaCy**.
- Vectorisation des textes via la transformation **TF-IDF** (`TfidfVectorizer` de scikit-learn).

### 2. Partie 1 : Clustering des produits
- Application de l'algorithme **DBSCAN** sur la matrice TF-IDF.
- Utilisation de la **distance cosine** (adaptée aux textes).
- Ajustement des paramètres `eps` et `min_samples` pour obtenir **10 à 20 clusters** avec un minimum d’outliers.
- Visualisation des clusters via des **nuages de mots** pour interpréter leur contenu.

### 3. Partie 2 : Système de recommandation
- Code python simple qui retourne **5 produits similaires** appartenant au même cluster.
- Interaction utilisateur via `input()` pour tester le système en temps réel.
- Sortie : liste d’identifiants de produits suggérés.

### 4. Partie 3 : Modélisation de thèmes (Topic Modeling)
- Application de **TruncatedSVD** (Analyse Sémantique Latente - LSA) sur la matrice TF-IDF.
- Choix du nombre de composantes (`n_components`) pour extraire **10 à 20 thèmes**.
- Attribution du **thème principal** à chaque produit (celui avec le poids le plus élevé).
- Génération de **nuages de mots par thème** pour faciliter l’interprétation.
- Sauvegarde de la matrice transformée dans `topic_encoded_df`.

---

## 📬 Livrables

✅ Ce projet inclut les livrables suivants :

- [x] Un modèle de **clustering (DBSCAN)** entraîné sur les descriptions produits.
- [x] Des **nuages de mots par cluster** pour analyser les groupes.
- [x] Un **système de recommandation fonctionnel** utilisable en interaction.
- [x] Un modèle de **modélisation de thèmes (TruncatedSVD)** entraîné.
- [x] Des **nuages de mots par thème latent** pour interpréter les sujets découverts.

---


### Project Structure

the_north_face_ml/
│
├── sample-data.csv           #Les Données
├── THE_NORTH_FACE.ipynb      # Notebook avec Analyse de Cluster, Nuages de mots, système de recommandation  
└── README.md