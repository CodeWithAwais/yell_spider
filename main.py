# -*- coding: utf-8 -*-
import scrapy
import csv

links_list = []

# Opening the text file and iterating over the list of URLs
with open("real_estate.txt", "r") as links:
    for link in links:
        links_list.append(link)
    
        
class MainSpider(scrapy.Spider):
    name = 'main'
    start_urls = [link for link in links_list]
    

    def parse(self, response):
        lists = response.xpath('//div[@class="row businessCapsule--mainRow"]')
        for each in lists:
            links = each.xpath('.//a[@class="businessCapsule--title"]/@href').get()
            name = each.xpath('.//h2/span[@class="businessCapsule--name"]/text()').get()
            phone = each.xpath('.//span[@itemprop="telephone"]/text()').get()
            website = each.xpath('.//a/div[contains(@class," icon-Business-website")]/parent::a/@href').get()
            address = each.xpath('.//span[@itemprop="address"]/span/text()').getall()
            city = each.xpath('.//span[@itemprop="addressLocality"]/text()').get()
            zip = each.xpath('.//span[@itemprop="postalCode"]/text()').get()

            yield {
                "Links": links,
                "Name": name,
                "Phone": phone,
                "Website": website,
                "Address": address,
                "City": city,
                "Zip": zip
            }

        next_page = response.xpath('//a[contains(text(),"Next")]/@href').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)
