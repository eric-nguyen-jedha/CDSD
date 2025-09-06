# 🧾 README – Analyse Exploratoire du Speed Dating TINDER

## Présentation en ligne de l'intégralité du projet format PPT (en ligne)

🚀 [Bloc_02 | TINDER | Présentation PPT](https://docs.google.com/presentation/d/1Blz8gw1r1zTDtSCQCbfhebbiJMEf2dZPgKpXxjYT65I/edit?usp=sharing) \
📁 [Bloc_02 | TINDER | Backup GitHub](https://github.com/eric-nguyen-jedha/CDSD/tree/main/BLOC_02/SPEED_DATING_TINDER)

> **Projet d’analyse de données** sur les facteurs d’attraction, les comportements sociaux et les biais de perception dans les speed datings.


---

## 📊 À propos du dataset

Ce dataset provient d’une étude menée par **Raymond Fisman et al.** à l’Université de Columbia. Il contient des données de **speed datings** réels, avec des informations sur :

- Les **préférences physiques et sociales** des participants
- Ce qu’ils recherchent chez l’autre
- Ce qu’ils pensent de leur propre attractivité
- Leurs décisions de matcher
- Les matchs réels
- Leurs comportements après l’événement (contact, second date)

> Ce dataset est largement utilisé en **data science**, **sociologie** et **analyse comportementale**.

---

## 🎯 Objectifs de l’EDA

L’objectif de ce projet est d’explorer les données pour répondre à des questions clés :

1. **Quels sont les attributs les moins désirables chez un partenaire masculin ? Cette perception varie-t-elle selon le genre ?**
2. **À quel point l’attractivité physique influence-t-elle le choix d’un partenaire, comparé à son impact réel sur les matchs ?**
3. **Les centres d’intérêt communs sont-ils plus importants qu’une appartenance raciale commune dans le processus de sélection ?**
4. **Les participants peuvent-ils correctement prédire leur valeur perçue sur le marché du dating ?**
5. **Pour obtenir un second rendez-vous, est-il préférable d’être le premier ou le dernier partenaire rencontré lors d’un speed dating ?**

---

## 🔍 Méthodologie

### 1. **Nettoyage des données**
- Gestion des valeurs manquantes
- Renommage des colonnes pour plus de lisibilité
- Correction des types de données
- Transformation des données au format long pour visualisation

### 2. **Analyse exploratoire**
- Distribution des âges, genres, domaines
- Analyse des traits recherchés (attractivité, sincérité, etc.)
- Perception de soi vs ce que l’on pense que les autres recherchent
- Corrélation entre préférences et succès du match
- Comparaison entre **match réel** et **match estimé**
- Analyse des séquences de rencontres (première/finale)

### 3. **Visualisation interactive**
- Graphiques Plotly Express : barres, boxplots, radar, camemberts
- Graphiques ventilés par genre (FEMALE/Rose – MALE/Bleu)
- Comparaison entre groupes (mêmes races, mêmes religions, etc.)

---

## 📈 Visualisations clés

- **Barres groupées** : Comparaison des critères d’attraction par genre
- **Radar charts** : Profil des traits recherchés
- **Camemberts** : Répartition des matchs (mêmes races, mêmes religions)
- **Boxplots** : Distribution des notes attribuées
- **Scatter plots** : Corrélation entre perception et réalité

---

## 🧪 Insights clés

### 1. **Critères d’attraction**
- L’**attractivité** est souvent le critère le plus valorisé
- Les **femmes** accordent plus d’importance à la **sincérité** et à l’**intelligence**
- Les **hommes** valorisent davantage l’**attractivité**

### 2. **Auto-perception vs Perception des autres**
- Beaucoup de participants **surestiment ou sous-estiment** leur attractivité
- Ceux qui ont une **auto-perception réaliste** ont tendance à mieux anticiper leurs chances de match

### 3. **Influence de la race et de la religion**
- Les matchs sont **plus fréquents entre personnes de même race**
- La **religion** joue un rôle moindre, mais significatif pour certains groupes

### 4. **Comportement après le match**
- Les **hommes** contactent plus souvent leurs matchs (`you_call`)
- Les **femmes** reçoivent plus de contacts (`them_cal`)
- Il y a une **tendance inversée**, mais pas une symétrie parfaite

### 5. **Séquence de rencontre**
- Être **le premier ou le dernier** partenaire peut influencer la probabilité de match (effet de fraîcheur ou de mémoire)

---

## 📌 Technologies utilisées

- **Python** : langage principal
- **Pandas** : manipulation des données
- **Plotly Express / Plotly Graph Objects** : visualisation interactive
- **Jupyter Notebook** (optionnel) : pour l’analyse exploratoire
- **Markdown / README** : documentation du projet

---

## 📁 Colonnes clés utilisées

| Colonne | Description |
|--------|-------------|
| `gender` | Genre du participant (FEMALE / MALE) |
| `age` | Âge du participant |
| `attr1_1`, `sinc1_1`, `intel1_1`, etc. | Ce que le participant recherche chez l’autre |
| `attr3_1`, `sinc3_1`, `intel3_1`, etc. | Ce que le participant pense de lui-même |
| `attr5_1`, `sinc5_1`, `intel5_1`, etc. | Ce que les autres pensent de lui |
| `match` | Match réussi (0/1) |
| `match_es` | Estimation du nombre de matchs par le participant |
| `dec` | Décision de matcher (1 = oui) |
| `dec_o` | Décision du partenaire |
| `you_call` | Nombre de matchs contactés après l’événement |
| `them_cal` | Nombre de matchs qui ont contacté le participant |
| `race`, `religion` | Identité raciale et religieuse |
| `samerace`, `samerelig` | Mêmes race/religion (si disponibles) |
| `attr`, `sinc`, `intel`, `fun`, `amb`, `shar` | Notes attribuées à chaque critère |

---

---

## 📁 Structure du projet

```
├── SPEED_DATING_TINDER.ipynb            # Le notebook servant à faire tous les EDA
├── Speed_Dating_Data_Key.doc               # La documentation officiel du Dataset
├── Speed_Dating_Data.csv                   # Le Dataset 
└── Tinder-Flame-Logo.wine.png              # Le logo de Tinder en png


```

## 📁 Exemple de code pour démarrer

```bash
# Installer les dépendances
pip install pandas plotly matplotlib seaborn

# Lancer le notebook 
jupyter notebook SPEED_DATING_TINDER.ipynb

