import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import csv

class KayakSpider(scrapy.Spider):
    name = "kayak"
# Désactiver Telnet Console

    def __init__(self, id=None, url=None,  *args, **kwargs):
        super(KayakSpider, self).__init__(*args, **kwargs)
        self.url = url
        self.id = id


    def start_requests(self):
        yield scrapy.Request(f'https://www.booking.com/hotel/fr/{self.url}')

    def parse(self, response):      

        kayak = response.css("div[class='hotelchars']")

        for canoe in kayak :
        # response is a Selector from the start url 
            yield {
            'Id' : self.id,
            #'town' : self.town,
            'hotel_name': canoe.css("h2[class='d2fee87262 pp-header__title']::text").get(),
            'hotel_lat' : canoe.css('a#map_trigger_header::attr(data-atlas-latlng)').get().split(',')[0],
            'hotel_long' : canoe.css('a#map_trigger_header::attr(data-atlas-latlng)').get().split(',')[1],
            'hotel_rating' : canoe.css("div[class='a3b8729ab1 d86cee9b25']::text").get(),
            'hotel_description': canoe.css("p[class='a53cbfa6de b3efd73f69']::text").get(),
            'hotel_facilities' : canoe.css("span[class='a5a5a75131']::text").getall()[0],
            'hotel_facilities_1' : canoe.css("span[class='a5a5a75131']::text").getall()[1],
            'hotel_facilities_2' : canoe.css("span[class='a5a5a75131']::text").getall()[2],
            'hotel_facilities_3' : canoe.css("span[class='a5a5a75131']::text").getall()[3],
            'hotel_facilities_4' : canoe.css("span[class='a5a5a75131']::text").getall()[4],
            }
 

filename = "ten_hotels_town_id_facilitie_f.json"

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
           #"indent": 4,  # JSON bien structuré
            #"ensure_ascii": False  # Garder les accents et caractères spéciaux
    },
    }
})

#hotel_url = []
#with open('ten_hotels_town_id.csv', mode='r', newline='', encoding='utf-8') as file:
#    url_reader = csv.reader(file)
#    next(url_reader)  # Ignorer l'en-tête
#    for row in url_reader:
#        if len(row) > 1:
#            hotel_url.append((row[0], row[1]))  # Stocker ID et URL correctement

#for id, (hotel_id, u) in enumerate(hotel_url): 

towns_final = []
with open('url_final.csv', mode ='r') as file:
    url = csv.reader(file)
    for u in url:
        print
        towns_final.append((u[0], u[1]))

for i in towns_final:
    process.crawl(KayakSpider, id=i[0], url=i[1])

process.start()
