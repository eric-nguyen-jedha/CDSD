# 🧾 README – EDA sur le dataset TINDER (ex: Columbia Speed Dating)

## 🧾 Présentation du projet
Ce projet présente une analyse exploratoire des données (EDA) effectuée sur le célèbre dataset du speed dating de l’Université de Columbia datant de 2004, 
qui contient des informations sur les préférences, les perceptions, et les matchs entre participants lors d’événements de speed dating.
Il a été renommé **TINDER**. _L'objectif est de faire comme si un site de rencontre avait commandé une étude afin de dégager des insights business._ 

> **Objectif** : Explorer les facteurs d’attraction, comprendre les comportements sociaux, analyser les biais de perception et visualiser les tendances à travers un jeu de données riche et varié.

01_SPEED_DATING_TINDER/<br/>
|<br/>
| -- README.md #Ce fichier<br/>
| -- speed_Dating_Data.csv #Dataset<br/>
| -- Speed_Dating_Data_Key.doc #Documentation du dataset<br/>
| -- 01_SPEED_DATING_TINDER.ipynb #Notebook Jupyter avec l'analyse complète

## 🔍 Méthodologie

### 1. **Nettoyage des données**
- Gestion des valeurs manquantes
- Renommage des colonnes pour plus de lisibilité
- Transformation des données au format long pour visualisation si indispensable

### 2. **Analyse exploratoire**
- Distribution des âges, genres, domaines
- Analyse des traits recherchés (attractivité, sincérité, etc.)
- Perception de soi vs ce que l’on pense que les autres recherchent
- Corrélation entre préférences et succès du match
- Comparaison entre **match réel** et **match estimé**
- Analyse des séquences de rencontres (avant/pendant/après)

### 3. **Visualisation interactive**
- Graphiques Plotly Express : lignes, barres, boxplots, radar
- Graphiques ventilés par genre (Femme/couleur:'#ec4899' – Homme/couleur:'#646ffb')

---

## 🧪 Insights clés

### 1. **Attributs les moins désirables**
- L’ambition excessive ou le manque de sincérité apparaît comme les **traits les moins attrayants**
- Les femmes accordent généralement plus d’importance à la **sincérité**, tandis que les hommes privilégient davantage l’**attractivité**
- La **race** joue un rôle moindre comparé aux traits personnels

### 2. **Importance de l’attractivité**
- L’attractivité est souvent **surestimée** comme facteur décisif
- Les personnes jugées "moins attirantes" peuvent tout de même obtenir des matchs grâce à d'autres critères (sincérité, humour, intelligence)

### 3. **Centres d’intérêt vs Race**
- Les **centres d’intérêt communs** semblent jouer un rôle plus important que la **similarité raciale** dans la décision de match
- Toutefois, certains groupes accordent encore une importance notable à la race

### 4. **Auto-perception et réalité**
- Beaucoup de participants **surestiment ou sous-estiment** leur succès
- Ceux qui se jugent avec lucidité ont tendance à mieux anticiper leurs chances de match

### 5. **Position dans la soirée**
- Être **la première personne rencontrée** peut améliorer la probabilité de match (effet de fraîcheur)

---

## 📌 Technologies utilisées

- **Python** : langage principal sous notebook
- **Pandas** : manipulation des données
- **Plotly Express / Plotly Graph Objects** : visualisation interactive
- **Jupyter Notebook** (optionnel) : pour l’analyse exploratoire
- **Markdown / README** : documentation du projet

---

## 📁 Colonnes clés utilisées

| Colonne | Description |
|--------|-------------|
| `gender` | Genre du participant (0 = FEMALE, 1 = MALE) |
| `age` | Âge du participant |
| `attr1_1`, `sinc1_1`, `intel1_1`, etc. | Ce que le participant recherche chez l’autre (points distribués sur 100) |
| `attr3_1`, `sinc3_1`, `intel3_1`, etc. | Ce que le participant pense de lui-même (note sur 10) |
| `match` | Match réussi (0/1) |
| `match_es` | Estimation du nombre de matchs par le participant |
| `field` | Domaine d’étude ou professionnel |
| `position`, `order` | Ordre des rencontres pendant la soirée |

---

## 📈 Visualisations clés

- **Boxplots** : Distribution des traits recherchés (`attr1_1`, `sinc1_1`, etc.)
- **Barres groupées** : Comparaison homme/femme des préférences
- **Radar chart** : Ce que l'on pense que l'autre recherche
- **Graphiques interactifs** : tous les graphiques sont réalisés avec **Plotly**

---

## 🧰 Exemple de code pour démarrer

```bash
# Installer les dépendances
pip install pandas plotly matplotlib seaborn

# Lancer le notebook (si présent)
jupyter notebook notebook_eda.ipynb
