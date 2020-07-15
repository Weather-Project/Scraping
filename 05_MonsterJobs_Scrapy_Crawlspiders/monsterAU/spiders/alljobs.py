# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AlljobsSpider(CrawlSpider):
    name = 'alljobs'
    allowed_domains = ["monster.com","job-openings.monster.com"]
    start_urls = ["https://www.monster.com/jobs/search?q=&cy=AU"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@id='SearchResults']//h2[@class='title']/a"), callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths="//a[@id='loadMoreJobs']"),follow=True)

    )

    def parse_item(self, response):
        item = {}
        item['JobTitle'] = response.xpath('//h1/text()').get()
        item['RefCode'] = response.xpath("//dd[@class='value text-muted']/text()").get()
        item['Location'] = response.xpath("//h2[@class='subtitle']/text()").get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
