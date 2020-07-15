# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
#from scrapy.loader import ItemLoader
from slikdeals.items import games
#from scrapy_selenium import SeleniumRequest

class GamedealsSpider(scrapy.Spider):
    name = 'gamedeals'
    allowed_domains = ['slickdeals.net']
    #start_urls = ['http://slickdeals.net/video-game-deals/']

    def start_requests(self):
        return [Request(url='https://slickdeals.net/video-game-deals',
        callback=self.parse,
        meta={"Selenium":True}
        )]

    def parse(self, response):
        #item=games()
        products=response.xpath("//div[@class='fpItem  ']")
        for product in products:
            #item.name=product.xpath(".//a[@class='itemTitle bp-c-link']/text()").get()
            #item.price=product.xpath(".//div[@class='itemPrice  wide ']").get()
            #yield item
            yield {
                'name':product.xpath(".//a[@class='itemTitle bp-c-link']/text()").get(),
                'price':product.xpath(".//div[@class='itemPrice  wide ']/div/text()").get()
            }
        next_page=response.xpath("//a[@data-role='next-page']/@href").get()
        main_url='https://slickdeals.net/'
        if next_page:
            page_url=main_url+next_page
            yield Request(url=page_url,callback=self.parse)