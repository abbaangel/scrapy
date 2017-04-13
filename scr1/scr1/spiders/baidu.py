# -*- coding: utf-8 -*-
import scrapy

from  scr1.items import baiduitem
from scrapy.selector  import Selector

class baidu(scrapy.Spider):
    name = "baidu"
    #allowed_domains = ["news.baidu.com"]
    start_urls = ['http://news.baidu.com/']

    def parse(self, response):

        sel = Selector(response)
        
        #get hot news
        title = sel.xpath('//*[@id="pane-news"]/div/ul/li/strong/a/text()').extract()
        href = sel.xpath('//*[@id="pane-news"]/div/ul/li/strong/a/@href').extract()
        for i in range(0,len(href)):
            item = baiduitem()
            item["title"] = title[i]
            #print "===========",item["title"] #此处与下面传过去的不一样
            item["href"] = href[i]
            #print "***************",item
            yield scrapy.Request(href[i],meta={'key':item,'title':title[i],'href':href[i]},callback=self.sub_getcont)

    def sub_getcont(self,response):
        #item = baiduitem()
        #item["title"] = response.meta['title']
        #item["href"] = response.meta['href']
        #print "+++++++++++++++++",item["title"] #此处是上面传过来最后一条的值
        #print "+++++++++++++++++",item["href"]
        item = response.meta['key']
        content = response.selector.xpath('//p/text()').extract()
        item["content"] = content
        #item["href"] = response.url
        yield item
    
        
