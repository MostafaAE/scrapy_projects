# -*- coding: utf-8 -*-
import scrapy
import logging


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):

        countries = response.xpath("//td/a")
        for country in countries:
            title = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()
            
            # absolute_link = f"https://www.worldometers.info{link}"
            # absolute_link = response.urljoin(link)
            # print(title)
            # print(link)
            # print(absolute_link)
            # yield scrapy.Request(url=absolute_link)
            yield response.follow(url=link, callback = self.parse_country, meta ={'country_name':title})

    def parse_country (self, response):
        # logging.info(response.url)
        country_name = response.request.meta['country_name']
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yield {
                'country_name':country_name,
                'year' : year,
                'population' : population
            }

