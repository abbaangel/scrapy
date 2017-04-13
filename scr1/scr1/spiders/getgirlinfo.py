#/bin/env python
#-*- coding: utf-8 -*-

import scrapy
from scr1.items import girlitem
from scrapy.selector import Selector
import pickle
import json
import re
import pickle


class DmozSpider(scrapy.Spider):
    name = "girl"
    allowed_domains = ["zngirls.com"]
    
    start_urls = [
        "http://www.zngirls.com/girl/"+str(num) for num in xrange(25000,30000)
    ]


    d_url = "http://www.zngirls.com"
 

    def __init__(self):
        self.startnum = 1
        #15642

    def __del__(self):
            
        #结束时报存工作进度
      
        print "system stop,save the work"
        with open('num.txt','wb') as f:
            s = str(self.startnum)
            pickle.dump(s,f)
        print "save over,bye!"
    
        

    def parse(self, response):
            print "====BEGIN [ %d ] TIMES====" %self.startnum
        
           
            sel = Selector(response)
            item = girlitem()
            

            item["name"]=sel.xpath('//*[@id="post"]/div[2]/div/div[1]/h1/text()').extract()
            #item['number'] = self.d_url +r'/girl/'+ str(self.startnum)+r'/'
            item['number'] = response.url
            
            #查询的信息，长度不一定
            zl = sel.xpath('//*[@id="post"]/div[2]/div/div[4]/table/tr/td/text()').extract()
            newzl = [zl[x*2]+zl[x*2+1] for x in range(0,len(zl)/2)]
            item['info'] = newzl

            
            #item["info"]= newzl

            #找到3种情况的简介
            desc1 = sel.xpath('//*[@id="post"]/div[5]/div/div[1]/div[2]/p/text()').extract()
            desc2 = sel.xpath('//*[@id="post"]/div[5]/div/div[1]/div[2]/div/text()').extract()
            desc3 = sel.xpath('//*[@id="post"]/div[5]/div/div[1]/div[2]/text()').extract()
            descall = desc1+desc2 + desc3
            #将描述中的前后空格去掉，还有回车符号
            if len(descall)>0:
                item["desc"] = descall[0].strip()
            else:
                item["desc"]= desc1+desc2 + desc3
            
            item["albumcount"]= sel.xpath('//*[@id="post"]/div[8]/div/div[3]/div/span/a/text()').extract()
            
            albumtitle= sel.xpath('//*[@id="post"]/div[8]/div/div[3]/ul/li/div[2]/a/text()').extract()
            albumhref= sel.xpath('//*[@id="post"]/div[8]/div/div[3]/ul/li/div[2]/a/@href').extract()
            #将专辑加上全路径
            albumfullhref = [self.d_url + i for i in albumhref]
            item["albumtitle"] = albumtitle
            item["albumhref"] = albumfullhref
            item["albuminfo"] = zip(albumtitle,albumfullhref)
            self.startnum +=1
            if item["name"] != [] and item["desc"] != []:
                yield item

            #yield  scrapy.Request(url, callback=self.parse_dir_contents)


'''
    def parse_articles_follow_next_page(self, response):
        for sel in response.xpath("//article"):
            item = girlitem()
            item["name"]= sel.xpath('//*[@id="post"]/div[2]/div/div[1]/h1/text()').extract()[0]

            #查询的信息，长度不一定
            nl = sel.xpath('//*[@id="post"]/div[2]/div/div[4]/table/tr/td/text()').extract()
            newnl = [nl[x*2]+nl[x*2+1] for x in range(0,len(nl)/2)]
            item["info"]= newnl
            desc1 = sel.xpath('//*[@id="post"]/div[5]/div/div[1]/div[2]/p/text()').extract()
            desc2 = sel.xpath('//*[@id="post"]/div[5]/div/div[1]/div[2]/div/text()').extract()
            desc3 = sel.xpath('//*[@id="post"]/div[5]/div/div[1]/div[2]/text()').extract()
            #找到3种情况的简介
            item["desc"]= desc1+desc2 + desc3
            
            item["albumcount"]= sel.xpath('//*[@id="post"]/div[8]/div/div[3]/div/span/a/text()').extract()
            
            albumtitle= sel.xpath('//*[@id="post"]/div[8]/div/div[3]/ul/li/div[2]/a/text()').extract()
            albumhref= sel.xpath('//*[@id="post"]/div[8]/div/div[3]/ul/li/div[2]/a/@href').extract()
            #将专辑加上全路径
            albumfullhref = [d_url + i for i in albumhref]
            item["albumtitle"] = albumtitle
            item["albumhref"] = albumfullhref
            item["albuminfo"] = zip(albumtitle,albumfullhref)
            
            yield item
        
        next_page = response.css("ul.navigation > li.next-page > a::attr('href')")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse_articles_follow_next_page)
 '''













