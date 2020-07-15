# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
from scrapy import Request

class HorrorNovelsSpider(scrapy.Spider):
    name = 'horror_novels'
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/account/login']

    def parse(self, response):
        yield FormRequest.from_response(
            response,
            formxpath="//form[@id='register']",
            formdata={
                'username':'retmad11@gmail.com',
                'password':'hclIt@123',
                'redirect':r"https://openlibrary.org/",
                'debug_token':'',
                'login':'Log In',
                'has_fulltext':'true'
            },
            callback=self.after_login
        )
    #
    def after_login(self,response):
        t=response.xpath("//ul[1]//form/a/text()").get()
        print(t," button exists")