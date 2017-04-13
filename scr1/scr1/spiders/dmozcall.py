#/bin/env python
#-*- coding: utf-8 -*-

import scrapy
from scr1.items import zitem
import pickle
import json
import re


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    #allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.zngirls.com/girl/15642/"
    ]
    domanurl='http://www.zngirls.com'

    def parse(self, response):

        #获得页面的链接
        pages = response.xpath('//div[@class="gallery_wrapper"]/div/a/@href').extract()
        pages=pages[:-1]

        print "pages=====",pages
        for href in pages:
            #print "href====",href
            url = response.urljoin(href)
            print "url=====",url
            #item_src = self.parse_dir_contents(response)
            yield  scrapy.Request(url, callback=self.parse_dir_contents)



    def parse_dir_contents(self,response):
        #print "====================================="
        #print response.xpath('//title')
        for sel in response.xpath('//div[@class="gallery_wrapper"]'):
            item = zitem()
            item['title'] = sel.xpath('//h1[@id="htilte"]/text()').extract()
            #改成仅数据
            item['title'] =item['title'][0]
            item['src'] = sel.xpath('//div[@class="gallery_wrapper"]/ul/img/@src').extract()
            item['href'] = response.url
            #print "item====",item['title']
            yield item
'''    def parse_articles_follow_next_page(self, response):
        for article in response.xpath("//article"):
            item =zitem()
            item['title'] = sel.xpath('//h1[@id="htilte"]/text()').extract()
            item['src'] = sel.xpath('//div[@class="gallery_wrapper"]/ul/img/@src').extract()
            item['href'] = response.url
            yield item

        next_page = response.css("ul.navigation > li.next-page > a::attr('href')")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse_articles_follow_next_page)
'''
