# Kayak Recommandation de Destinations - Kayak

## Présentation en ligne de l'intégralité du projet

🚀 [Bloc_01 | KAYAK | Présentation PPT](https://docs.google.com/presentation/d/1CRRkYLIsHckPqy6gtIFrKen3oyNKXz50BFBCODDNMXE/edit?usp=sharing)


## 📇 Description de l'entreprise

Kayak est un moteur de recherche de voyage qui aide les utilisateurs à planifier leur prochain voyage au meilleur prix.

Fondée en 2004 par Steve Hafner & Paul M. English, Kayak a été acquise par Booking Holdings qui gère aujourd'hui :
- Booking.com
- Kayak
- Priceline
- Agoda
- RentalCars
- OpenTable
- OpenTable


## 🚧 Projet

L'équipe Marketing de Kayak souhaite créer une application qui recommandera où les gens devraient planifier leurs prochaines vacances. L'application devrait être basée sur des données réelles concernant :

- La météo
- Les hôtels dans la région

L'application devrait alors pouvoir recommander les meilleures destinations et hôtels basés sur les variables ci-dessus à tout moment donné.

## 🎯 Objectifs

Comme le projet vient de démarrer, votre équipe ne dispose d'aucune donnée pouvant être utilisée pour créer cette application. Par conséquent, votre mission sera de :

1. **Scraper les données des destinations**
2. **Récupérer les données météorologiques de chaque destination**
3. **Récupérer les informations sur les hôtels de chaque destination**
4. **Stocker toutes les informations ci-dessus dans un Bucket S3**
5. **Extraire, transformer et charger les données nettoyées depuis votre lac de données vers une Base de Données PostGresql**

## 📁 Structure du projet

```
├── API_geo_KAYAK.ipynb                             # récupération des coordonnées villes françaises, sélection 10 villes françaises avec les meilleurs températures
├── kayak_town_geo.csv                              # Fichier CSV de sauvegarde des coordonnées GPS des 30 villes françaises
├── kayak_id.csv                                    # Le même fichier CSV de kayak_town_geo.csv  mais avec une colonne Id
├── Kayak_Weather_Forecast.ipynb                    # Notebook qui permet la récupération du Forecast météo pour 30 villes française
├── kayak_forecast.csv                              # Fichier CSV de forecast méto des 30 villes françaises
├── Town_Geo_Forcast.csv                            # Fusion entre les fichiers kayak_town_geo.csv et kayak_forecast.csv 
├── ten_hotels_town_id.csv                          # URLS de des hotels des 10 villes sélectionnées
├── kayak_spider_22fev.py                           # Spider pour récupérer les URLs des hotels pour les 10 villes sélectionnées
├── ten_hotels_town_id_24fev.json                   # fichiers json avec les noms des villes, les hotels, la note des avis > 8, les URLs des hotels
├── kayak_spider_hotel_GPS_22fev.py                 # 2e spider pour scraper le nom, les coordonnées GPS, la notation, la description, les facilities
├── ten_hotels_town_id_facilitie_f.json             # Fichiers JSON avec le nom, les coordonnées GPS, la notation, la description, les facilities
├── url_final.csv                                   # fichier intermédiaire d'URL des hotels 
├── Best-Town-Weather-ForeCast-Best-Hotels.ipynb    # - Notebook final - génération de graphiques et fichiers CSV finalisé destiné à l'équipe Marketing  
├── towns_temp_forecast_best_hotels.csv             # Fichier final destiné à être sur S3 et sur RedShift pour partage 
└── .env.example                                    # fichier exemple d'un point .env à créer

```

## 🖼️ Périmètre du projet

L'équipe marketing souhaite se concentrer d'abord sur les meilleures villes à visiter en France. Selon One Week In.com, voici les 35 principales villes à visiter en France :

[//]: # ("Mont Saint Michel","Saint Malo","Bayeux","Le Havre","Rouen","Paris","Amiens","Lille","Strasbourg","Chateau du Haut Koenigsbourg","Colmar","Eguisheim","Besancon","Dijon","Annecy","Grenoble","Lyon","Gorges du Verdon","Bormes les Mimosas","Cassis","Marseille",
"Aix en Provence","Avignon","Uzes","Nimes","Aigues Mortes","Saintes Maries de la mer","Collioure","Carcassonne","Ariege","Toulouse","Montauban","Biarritz","Bayonne","La Rochelle")

### Les coordonnées GPS sont récupéré grâce à la librairie Nominatim

### Récupération des données météorologiques via API OPENWEATHER
Il est nécessaire de créer un compte et de générer un token appid = "XXXX"
url : https://openweathermap.org/api


### Booking : site de voyage à scraper

url : https://www.booking.com/