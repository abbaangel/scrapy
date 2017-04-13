#/bin/env python
# coding utf-8

import scrapy
from scrapy.selector import Selector
from scr1.items import get37item


class MySpider(scrapy.Spider):
    name = 'myspider'
    url = 'http://10.100.251.37'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}
    cookies = {}
    def start_requests(self):
        return [scrapy.FormRequest("http://10.100.251.37/index.html",callback=self.logged_in)]

    def logged_in(self, response):
        print "begin login in"
        print response.url
        return [scrapy.FormRequest.from_response(response,method="POST",
                                                 headers = self.headers,
                                                 formdata={'username':'zh','pwd': '222222'},
                                                 callback=self.parse,dont_filter=True
                                                 )]

    def parse(self,response):
        
        sel = Selector(response)
        #title = sel.xpath('/html/head/title/text()').extract()
        print "######",response.url
        print sel.xpath('//title/text()').extract()[0]
        '''
        html = sel.xpath('//table[@class="right_table2_in"][1]/tr/th[1]/a/@href').extract()
        for i in xrange(0,500):
            try:
                print html[i]
            except UnicodeEncodeError:
                continue
            except IndexError:
                break
        '''       
        
        if response.url == 'http://10.100.251.37/adminsite/center_user.php':
            item = get37item()
            #td = sel.xpath('//td/text()').extract()
            #name = sel.xpath('/html/body/table[1]/tr/td[3]/table/tr/td/span[1]/span/text()').extract()
            #print name
            idhref = sel.xpath('//table[@class="right_table2_in"][1]/tr/th[1]/a/@href').extract()
            idnum = sel.xpath('//table[@class="right_table2_in"][1]/tr/th[1]/a/text()').extract()
            orderid = sel.xpath('//table[@class="right_table2_in"][1]/tr/th[2]/text()').extract()
            bankname = sel.xpath('//table[@class="right_table2_in"][1]/tr/th[3]/text()').extract()
            devtype = sel.xpath('//table[@class="right_table2_in"][1]/tr/th[4]/text()').extract()
            devcount = sel.xpath('//table[@class="right_table2_in"][1]/tr/th[5]/text()').extract()
            send = sel.xpath('//table[@class="right_table2_in"][1]/tr/th[6]/text()').extract()
            arrive = sel.xpath('//table[@class="right_table2_in"][1]/tr/th[7]/text()').extract()
            print "@@@@@@@@@@@",idnum
            
            for i in range(0,len(idnum)):
                
                item["idhref"] =  idhref[i]
                item["idnum"] =  idnum[i]
                item["orderid"] = orderid[i]
                item["bankname"] = bankname[i]
                item["devtype"] = devtype[i]
                item["devcount"] = devcount[i]
                item["send"] =  send[i]
                item["arrive"] =  arrive[i]
                yield item
        else:
            print '*******login fail********'
