# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import json
from testtask.items import LinkItem
from scrapy.http import Request
from scrapy.exceptions import CloseSpider


class LinkcollectorSpider(scrapy.Spider):
    name = 'linkcollector'
    allowed_domains = ['e27.co']
    STOP_WORDS = "we couldn't find any startup"
    url_template = 'https://e27.co/startups/load_startups_ajax?all&per_page={}&append=1'
    page_counter = 0
    continue_ = True

    def start_requests(self):
        while self.continue_:
            self.page_counter += 1
            yield Request(url=self.url_template.format(self.page_counter))

    def parse(self, response):
        pagecontent = json.loads(response.text).get('pagecontent')
        if not pagecontent or self.STOP_WORDS in pagecontent:
            raise CloseSpider('Finished..')
        links = Selector(text=pagecontent) \
                .xpath('//div[@class="col-xs-12 col-sm-12 col-md-4 col-lg-4"]/a/@href') \
                .extract()
        for link in links:
            yield LinkItem(link=link)

