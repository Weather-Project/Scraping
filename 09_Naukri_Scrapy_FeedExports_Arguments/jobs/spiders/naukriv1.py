# -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import urlencode

class Naukriv1Spider(scrapy.Spider):
    name = 'naukriv1'
    allowed_domains = ['www.naukri.com']
    #start_urls = ['https://www.naukri.com/jobapi/v3/search']
    base_url='https://www.naukri.com/jobapi/v3/search'
    custom_settings={
        'COOKIES_ENABLED':True,
        'ROBOTSTXT_OBEY': False,
        #adding feeds json and jsonlines format
        'FEEDS':{
            '%(name)s_%(time)s_j.json':{
                'format':'json'
            },
            '%(name)s_%(time)s_jl.json':{
                'format':'jsonlines'
            }

        }
    }
        
    def __init__(self,pages=1):
        #super().__init__(*args,**kwargs)
        self.pages=int(pages)
        headers={
            #"cookie": "_t_s=direct; _t_ds=136393d41594112963-143136393d4-0136393d4; _t_us=17328897A83; _t_sd=google; _t_ds=136393d41594112963-143136393d4-0136393d4; _ga=GA1.2.2115305322.1594112965; _gid=GA1.2.1584547417.1594112965; test=naukri.com; _fbp=fb.1.1594112965153.1574549816; __gads=ID=199ced96d225cffc:T=1594112965:S=ALNI_MbrfELZcUOS04QVBD300oMpcjCA-Q; _ff_ds=0657751001594112966-678E44D1958A-482C65D5771B; _ff_s=direct; _t_s=seo; _t_sd=google; _gat_UA-182658-1=1; _t_us=5F052461; _t_r=1091%2F%2F; HOWTORT=ul=1594172524454&r=https%3A%2F%2Fwww.naukri.com%2Fjobs-in-india&hd=1594172525386",
            "pragma": "no-cache",
            "referer": "https://www.naukri.com/jobs-in-india",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "systemid": "109",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "appid": "109",
            "clientid": "d3skt0p"
        }
        payload={
            "noOfResults": "50",
            "urlType": "search_by_location",
            "searchType": "adv",
            "location": "india",
            "seoKey": "jobs-in-india",
            "src": "jobsearchDesk",
            "latLong":"", 
        }
        self.headers=headers
        self.payload=payload

    def start_requests(self):
        url='https://www.naukri.com/jobapi/v3/search'+"?"+urlencode(self.payload)
        yield scrapy.Request(url=url,method='GET',headers=self.headers,callback=self.parse)
    
    def parse(self, response):
        l1_url='https://www.naukri.com/jobapi/v4/job/'
        j=json.loads(response.body)['jobDetails']
        print(json.loads(response.body)['seo']['title'])
        for item in j:
            job_url=l1_url+item['jobId']
            yield scrapy.Request(url=job_url,headers=self.headers,callback=self.parse_jobs)
        for i in range(2,self.pages+1):
            self.payload['pageNo']=str(i)
            pageurl=self.base_url+"?"+urlencode(self.payload)
            yield scrapy.Request(url=pageurl,method='GET',headers=self.headers,callback=self.parse)
    
    def parse_jobs(self,response):
        job=json.loads(response.body)['jobDetails']
        yield job

        
