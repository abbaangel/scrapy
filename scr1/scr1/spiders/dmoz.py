#/bin/env python
#*coding:utf8*
import scrapy
from scr1.items import zitem
import pickle
import json
import re


class DmozSpider(scrapy.Spider):
    name = "dmoz1"
    #allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.zngirls.com/g/22280/"
    ]
    domanurl='http://www.zngirls.com'

    def parse(self, response):
       
        items = []
        item = zitem()
        item['title'] = response.xpath('//h1[@id="htilte"]/text()').extract()
        item['desc'] = response.xpath('//div[@id="ddesc"]/text()').extract()
        #获得页面的链接
        item['nexthref'] = response.xpath('//div[@class="gallery_wrapper"]/div/a/@href').extract()
        item['nexthref']=item['nexthref'][1:-1]
        #items.append(item)

        #获取页面中图像链接
        for sel in response.xpath('//div[@class="gallery_wrapper"]'):
            item['src'] = sel.xpath('ul/img/@src|img/@alt').extract()

        items.append(item)
        print "1=====>>>",items
        for href in item['nexthref']:
            print "2=====>>>",href,response.urljoin(href)


    def getpage(self,response,href):
        '''
        组合为一个实际的链接
        可以用下面的方法
        yield response.urljoin(href)


        
        '''
        #手工组成一个链接
        num = re.findall ('(/\w+/\d+/)(\d+).html',nexthref)
        path1 = num[0][0]
        pagenum = num[0][1]
        for i in range(2,pagenum+1):
            yield self.domanurl+paht1+str(i)+'.html'
        

