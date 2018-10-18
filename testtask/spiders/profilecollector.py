# -*- coding: utf-8 -*-
import scrapy
from testtask.items import ProfileItem
import random
from scrapy.http import Request
from scrapy.exceptions import CloseSpider


class ProfilecollectorSpider(scrapy.Spider):
    name = 'profilecollector'
    allowed_domains = ['e27.co/startup']
    random_index = None
    urls = None
    COUNT_PERRUN=250

    custom_settings = {
        'FEED_EXPORT_FIELDS': ["company_name", "request_url", "request_company_url", 
                               "location", "tags", "founding_date", "founders", "employee_range", 
                               "urls", "emails", "phones", "description_short", "description"
                               ],
    }

    def __init__(self, *args, **kwargs):
        filename = kwargs.pop('filename', None)
        if filename:
            with open(filename) as f: 
                _ = f.readline() 
                self.urls = [url.split(',')[0].strip() for url in f]
                self.random_index = random.sample(range(0, len(self.urls)), self.COUNT_PERRUN) 

    def start_requests(self):
        for index in self.random_index:
            url = self.urls[index] + '?json'
            yield Request(url)

    def parse(self, response):
        sel = response.xpath('//div[@class="row"]')

        if len(sel) >= 1:
            selector = sel[1]
        else:
            raise CloseSpider('Something goes wrong, rewrite me ...')

        company_name = selector.xpath('//h1/text()').extract()
        description_short = selector.xpath('//div[@style="font-size:16px;"]/text()').extract()
        founnding_date = selector.xpath('//p/span/text()').extract()
        tags = selector.xpath('//div[@style="word-wrap: break-word;"]/span/a/text()').extract()

        url_loc = selector.xpath('//div[@class="mbt"]/span')
        request_company_url = url_loc[0].xpath('./a/@href').extract() if url_loc else ''
        location = url_loc[2].xpath('./a/text()').extract() if len(url_loc) == 3 else ''
        
        if len(sel) >= 3:
            urls = response.xpath('//div[@class="row"]')[3].css('.socials').xpath('./a/@href').extract()
        else:
            urls = ''

        desc_sel = response.xpath('//p[@class="profile-desc-text"]//text()').extract()
        description = desc_sel[0].strip() if desc_sel else ''

        yield ProfileItem(company_name=company_name,
                          request_company_url=request_company_url,
                          request_url=response.url.rstrip('?json'),
                          location=location,
                          founnding_date = founnding_date,
                          description_short=description_short,
                          description=description,
                          urls=urls,
                          tags=tags,
                          )
