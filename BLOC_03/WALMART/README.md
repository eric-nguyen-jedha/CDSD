# Projet de Machine Learning Supervisé : Prévision des Ventes Hebdomadaires chez Walmart

## Présentation en ligne de l'intégralité du projet format PPT (en ligne)

🚀 [Bloc_03 | WALMART | Présentation PPT](https://docs.google.com/presentation/d/1AW_Dl0PJczreMpkSzYcI1ZHUWg9_bnoHy80Ia5PpUYU/edit?usp=sharing)

## 🏢 Description de l'entreprise
Walmart Inc. est une entreprise multinationale américaine spécialisée dans le commerce de détail, exploitant un réseau d’hypermarchés, de grands magasins à prix réduits et d’épiceries. Fondée par Sam Walton en 1962, l’entreprise est basée à Bentonville, Arkansas.

Le service marketing de Walmart souhaite disposer d’un modèle de machine learning capable d’estimer avec précision les **ventes hebdomadaires** dans ses magasins. Ce modèle permettra de mieux comprendre l’impact des indicateurs économiques sur les ventes et d’optimiser la planification des futures campagnes marketing.

---

## 🎯 Objectifs du projet
Ce projet vise à construire un modèle prédictif fiable pour estimer les ventes hebdomadaires de Walmart. Il se décompose en trois grandes étapes :

1. **Analyse exploratoire et préparation des données** (EDA & preprocessing)
2. **Entraînement d’un modèle de régression linéaire** (modèle de base)
3. **Réduction du surapprentissage** via un modèle de régression régularisée (Ridge ou Lasso)

---

## 🖼️ Périmètre du projet
Le jeu de données utilisé contient des informations sur les ventes hebdomadaires de plusieurs magasins Walmart, ainsi que des variables économiques et contextuelles telles que :
- Le taux de chômage
- Le prix du carburant
- L’indice des prix à la consommation (CPI)
- Les jours fériés
- Des informations temporelles (date)

> 🔎 **Source** : Données issues d’un concours Kaggle, modifiées et fournies via la plateforme JULIE. Assurez-vous d’utiliser **le jeu de données personnalisé : Walmart_Store_Sales.csv** fourni.

---

## 📬 Livrables attendus
Pour valider ce projet, votre équipe devra fournir les éléments suivants :

- [X] Des **visualisations pertinentes** issues de l’analyse exploratoire
- [X] Un **modèle de régression linéaire entraîné** sur les données
- [X] Une **évaluation des performances** du modèle avec une métrique adaptée (ex: R², RMSE)
- [X] Une **interprétation des coefficients** pour identifier les variables les plus influentes
- [X] Un **modèle régularisé (Ridge ou Lasso)** pour réduire le surapprentissage
- [X] (Optionnel) Une **recherche d’hyperparamètres** via `GridSearchCV`

---

## 🛠️ Étapes détaillées du projet

### Partie 1 : Analyse exploratoire et prétraitement des données

#### 🔍 Analyse exploratoire (EDA)
Avant toute modélisation, réalisez une analyse exploratoire approfondie :
- Affichez les **premières lignes** du jeu de données
- Vérifiez les **types de données**, les **valeurs manquantes**, les **doublons**
- Calculez des **statistiques descriptives**
- Créez des **visualisations** :
  - Distribution des ventes hebdomadaires
  - Corrélations entre variables
  - Évolution des ventes dans le temps
  - Impact des jours fériés sur les ventes

#### 🧹 Prétraitement des données

##### ✅ Nettoyage avec `pandas`
- **Supprimer les lignes où `Weekly_Sales` est manquant**  
  → *On n’impute jamais la variable cible !*
- **Extraire des informations temporelles à partir de la colonne `Date`** :
  - Année (`Year`)
  - Mois (`Month`)
  - Jour (`Day`)
  - Jour de la semaine (`DayOfWeek`)
- **Supprimer les outliers** pour les variables numériques suivantes :
  - `Temperature`, `Fuel_Price`, `CPI`, `Unemployment`
  - Utiliser le seuil : \( [\bar{X} - 3\sigma, \bar{X} + 3\sigma] \)

##### 🔄 Transformation avec `scikit-learn`
- **Séparation des variables explicatives (X) et de la cible (y)** :
  - Cible : `Weekly_Sales`
- **Identification des types de variables** :
  - Variables **catégorielles** : `Store`, `Holiday_Flag`
  - Variables **numériques** : `Temperature`, `Fuel_Price`, `CPI`, `Unemployment`, `Year`, `Month`, `Day`, `DayOfWeek`
- **Pipeline de preprocessing** :
  - Utiliser `ColumnTransformer` pour appliquer :
    - `OneHotEncoder` sur les variables catégorielles
    - `StandardScaler` (ou pas) sur les numériques selon le modèle utilisé

---

### Partie 2 : Modèle de base (Régression linéaire)

#### 📐 Entraînement du modèle
- Utiliser `LinearRegression` de `scikit-learn`
- Diviser les données en **train/test** (ex: 80%/20%)
- Entraîner le modèle sur l’ensemble d’entraînement

#### 📊 Évaluation des performances
Utiliser les métriques suivantes :
- **Coefficient de détermination (R²)** : `model.score(X_test, y_test)`
- **RMSE (Root Mean Squared Error)** : `np.sqrt(mean_squared_error(y_test, y_pred))`
- Comparer les scores **train** et **test** pour détecter un éventuel surapprentissage

#### 🔎 Interprétation des coefficients
- Accéder aux coefficients via `model.coef_`
- Associer chaque coefficient à sa variable (attention à l’ordre après encodage)
- Identifier les variables **positivement/négativement corrélées** aux ventes
- Exemple d’interprétation :  
  > "Une augmentation de 1 point du CPI est associée à une baisse moyenne de X dollars de ventes."

---

### Partie 3 : Lutte contre le surapprentissage (Modèle régularisé)

#### 🛡️ Choix du modèle régularisé
Deux options possibles :
- **Ridge** : régularisation L2 → réduit l’amplitude des coefficients
- **Lasso** : régularisation L1 → peut annuler certains coefficients (utile pour la sélection de variables)

> 📚 Références :
> - [Ridge Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html)
> - [Lasso Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html)

#### 🧪 Entraînement du modèle
- Entraîner un modèle `Ridge` ou `Lasso`
- Choisir une valeur initiale pour le paramètre `alpha` (ex: 1.0)
- Comparer les performances avec le modèle linéaire de base

#### 🔍 Ajustement des hyperparamètres (Bonus)
Utiliser `GridSearchCV` pour trouver le meilleur `alpha` :
```python
from sklearn.model_selection import GridSearchCV

param_grid = {'alpha': [0.1, 1, 10, 100]}
grid_search = GridSearchCV(Ridge(), param_grid, cv=5, scoring='r2')
grid_search.fit(X_train, y_train)

best_alpha = grid_search.best_params_['alpha']
best_model = grid_search.best_estimator_

## 📁 Structure du projet

```
├── WALMART.ipynb                           # Le notebook servant à faire tous les EDA & le modèle
└── Walmart_Store_Sales.csv                 # Le Dataset 

```