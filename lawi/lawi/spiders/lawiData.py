import scrapy


class LawidataSpider(scrapy.Spider):
    name = 'lawiData'
    allowed_domains = ['landwirtschaftskammer.de']
    start_urls = ['https://www.landwirtschaftskammer.de/bildung/landwirt/betriebe/']

    def parse(self, response):
        regionenHrefsListe = response.css('.karte map area[shape=poly]::attr(href)')
        # regionenUrlListe = []
        #
        # for region in regionenHrefsListe:
        #     regionenUrlListe.append(response.url+region)
        #print(regionenUrlListe)
        #print(len(regionenUrlListe))
        #print(regionenHrefsListe)

        for href in regionenHrefsListe:
            yield response.follow(href.get(), callback=self.betriebsDaten)

    def betriebsDaten(self, response):
        print(response)
        betriebe = response.css('.betriebe tbody tr')
        for betrieb in betriebe:
            betriebsZweige = betrieb.css('td[data-title^=Betriebszweige]::text').get()
            #print(betriebsZweige)
            if 'Feldgemüse' in betriebsZweige:
                yield {
                    'Betriebsname': betrieb.css('td[data-title^=Betrieb]::text').get(),
#                    'Adresse': betrieb.css('.betriebe tbody tr td[data-title^=Betrieb] br[1]::text').get()  #pseudocode für Betriebsstraße
#                               + betrieb.css('.betriebe tbody tr td[data-title^=Betrieb] br[0]::text').get(),    #pseudocode für Betriebsort
#                    'Telefonnummer': betrieb.css('.betriebe tbody tr td[data-title^=Betrieb] br[2]::text').get(),   #pseudocode
#                    'Mobil': betrieb.css('.betriebe tbody tr td[data-title^=Betrieb] br[4]::text').get() #pseudocode
                    'E-Mail': betrieb.css('td[data-title^=Betrieb] a::attr(href)').get(),
                    'Betriebszweige': betrieb.css('td[data-title^=Betriebszweige]::text').get()
                    }


#todo: Sortierung nach Regionen einbauen (nicht gefordert!?)