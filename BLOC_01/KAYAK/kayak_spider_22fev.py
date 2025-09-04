import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import csv

class KayakSpider(scrapy.Spider):
    name = "kayak"

    def __init__(self, id=None, town=None,  *args, **kwargs): # on récupère ici le nom de la ville que l'on transmet tout au long du script
        super(KayakSpider, self).__init__(*args, **kwargs)
        self.town = town
        self.id = id

    def start_requests(self):
        yield scrapy.Request(f'https://www.booking.com/searchresults.fr.html?ss={self.town}&nflt=review_score%3D80')

    def parse(self, response):      

        kayak = response.css("div[class='c066246e13 d8aec464ca']")

        for canoe in kayak :

            yield {
            'Id' : self.id,
            'town' : self.town,
            'hotel_name': canoe.css("div[class='f6431b446c a15b38c233']::text").get(),
            'hotel_rating' : canoe.css("div[class='a3b8729ab1 d86cee9b25']::text").get(),
            'hotel_url' : canoe.css("[class='a78ca197d0']").css("a[href]::attr(href)").get() 
            }
 
        next_page = response.css("[class='a78ca197d0']").css("a[href]::attr(href)").get()


filename = "ten_hotels_town_id_24fev.json"

if filename in os.listdir(): # vérifier si dans mon dossier src j'ai un fichier du meme nom que filename qui existe
    os.remove(filename) # si vrai, alors je supprime le fichier

process = CrawlerProcess(settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'LOG_LEVEL': logging.DEBUG,
    'DEFAULT_REQUEST_HEADERS': {
        'Accept-Language': 'fr-FR,fr;q=0.9'
    },
    "FEEDS": {filename : {
            "format": "jsonlines",
            "encoding": "utf-8",

    },
    }
})

#towns = []

#with open('urls_hotels_05fev.csv', mode ='r') as file:
#    url = csv.reader(file)
 #   for u in url:
#        print
 #       towns.append(u[0])

towns = {20: 'Marseille',
 30: 'Toulouse',
 28: 'Carcassonne',
 18: 'Bormes-les-Mimosas',
 19: 'Cassis',
 33: 'Bayonne',
 32: 'Biarritz',
 1: 'Saint-Malo',
 21: 'Aix-en-Provence',
 34: 'La+Rochelle'}

for id, town in towns.items():
    process.crawl(KayakSpider, id=id, town=town)

process.start()
