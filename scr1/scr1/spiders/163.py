# -*- coding: utf-8 -*-
import scrapy

from  scr1.items import item163
from scrapy.selector  import Selector

class baidu(scrapy.Spider):
    name = "163"
    #allowed_domains = ["news.baidu.com"]
    start_urls = ['http://news.163.com/special/0001386F/rank_news.html']

    def parse(self, response):

        #sel = Selector(response)
        
        #get hot news
        t = response.selector.xpath('//div/div/div/table/tr/td/a/text()').extract()
        h = response.selector.xpath('//div/div/div/table/tr/td/a/@href').extract()
        for i in range(0,len(t)):
            item = item163()
            item["title"] = t[i]
            item["href"] = h[i]
            yield scrapy.Request(h[i],meta={'key':item,'title':t[i],'href':h[i]},callback=self.sub_getcont)

    def sub_getcont(self,response):
        #get url h[i] content
        item = response.meta['key']
        
        c = response.selector.xpath('//div[@class="post_text"]/p/text()').extract()
        if not c:
            c = response.selector.xpath('//div[@class="post_text"]/p/font/text()').extract()
        item["content"] = c
        yield item
    
        
