#/bin/env python
#-*- coding: utf-8 -*-

import scrapy
from scr1.items import girlitem
from scrapy.selector import Selector
from scrapy.http import Request
import pickle
import json
import re
import logging
import urllib
import urllib2
import os


class DmozSpider(scrapy.Spider):
    name = "newgirl"
    allowed_domains = ["zngirls.com"]
    loger = logging.getLogger(__name__)
    
    #start_urls = ["http://www.zngirls.com/girl/"+str(num) for num in xrange(15714,17000)  #15829]
    start_urls = "http://www.zngirls.com/girl/"
    
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        #  "Referer":"http://www.zngirls.com/g/18333/",
    "Referer":"http://www.zngirls.com",
  }
    cookies = {
        'Hm_lpvt_1bb490b9b92efa278bd96f00d3d8ebb4':'1491990900',
        'Hm_lvt_1bb490b9b92efa278bd96f00d3d8ebb4':'1491573099,1491727384,1491927248,1491990900',
        


        }

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
    '''
    def start_requests(self):
        return []

     '''
    
       
    def start_requests(self):
        #for url in self.start_urls:
        rnum = 15929
        if os.path.isfile('x.p.txt'):
            f = open('x.p.txt')
            rnum = pickle.load(f)+1  #用默认参数来控制15829
            f.close()
        f = open('x.p.txt','w')
        for num in xrange(rnum,16000):
            url = self.start_urls + str(num)
            try:
                rnum = num
                f = open('x.p.txt','w')
                pickle.dump(rnum,f)
                                
                f.close()

                yield self.make_requests_from_url(url)
            except KeyboardInterrupt:
                print  u'中断退出了'


  
    
    def make_requests_from_url(self, url):
        
        req = Request(url,headers=self.headers,cookies=self.cookies,dont_filter=True)
        #print '++++++++++',req

        return req
      

    def parse(self, response):
            
            print "====BEGIN        %d       TIMES====" %self.startnum
            
            self.loger.info(u'第---%s---次,URL=%s',self.startnum,response.url)
            sel = Selector(response)
            item = girlitem()

            item["name"]=sel.xpath('//*[@id="post"]/div[2]/div/div[1]/h1/text()').extract()
            item['number'] = response.url
            
            #查询的信息，长度不一定
            zl = sel.xpath('//*[@id="post"]/div[2]/div/div[4]/table/tr/td/text()').extract()
            newzl = [zl[x*2]+zl[x*2+1] for x in range(0,len(zl)/2)]
            item['info'] = newzl

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
            
            
            account = sel.xpath('//*[@id="post"]/div[8]/div/div[3]/div/span/a/text()').extract()
            item["albumcount"] = account
            albums_link = sel.xpath('//*[@id="post"]/div[8]/div/div[3]/div/span/a/@href').extract() #专辑或者是图片入口链接
            #print "LINK--------------",albums_link,account

            self.startnum +=1 #计数器
            if item["name"] != [] and item["desc"] != []:
                if not account:
                    self.loger.info(u'相册链接%s，相册数量%s'%('None','None'))
                    item["albumtitle"] = [u'\u4ec0\u4e48\u90fd\u6ca1\u6709']
                    item["albumhref"] = [u'\u4ec0\u4e48\u90fd\u6ca1\u6709']
                    item["albuminfo"] = [u'\u4ec0\u4e48\u90fd\u6ca1\u6709']
                    yield item
                elif account[0][-1] == u'\u5f20':
                    #\u518c 为中文“册”,\u5f20 为“张”图像就不进入抓取
                    #print "come here=============================="
                    self.loger.info(u'图库链接:%s，图库张数:%s'%(self.d_url+ albums_link[0],account[0]))
                    item["albumtitle"] = [u'\u6ca1\u6709\u4e13\u8f91']
                    item["albumhref"] = self.d_url + albums_link[0]
                    item["albuminfo"] = [u'\u6ca1\u6709\u4e13\u8f91\u4fe1\u606f']
                    yield item
                else:
                    self.loger.info(u'相册链接:%s，相册数量:%s'%(self.d_url+ albums_link[0],account[0]))
                    self.loger.info(u'转向专辑页%s',self.d_url + albums_link[0])
                    yield  scrapy.Request(self.d_url + albums_link[0],meta = {'key':item },callback=self.get_all_album)
            else:
                self.loger.info(u'无数据 URL = %s',response.url)
                #print 'Empty url.......!'

    def get_all_album(self, response):
            #调用此函数的response都是有专辑页的
            
            sel = Selector(response)
            item = response.meta['key']
            albumtitle = sel.xpath('//*[@id="photo_list"]/ul/li[@class="igalleryli"]/div[2]/a/text()').extract()
            albumhref = sel.xpath('//*[@id="photo_list"]/ul/li[@class="igalleryli"]/div[2]/a/@href').extract()
            imgsrc = sel.xpath('//*[@id="photo_list"]/ul/li[@class="igalleryli"]/div[1]/a/img/@src').extract()
            imgtitle= sel.xpath('//*[@id="photo_list"]/ul/li[@class="igalleryli"]/div[1]/a/img/@alt').extract()
            self.loger.info(u'下载封面图像---%s---张...'%len(imgsrc))
            
            for i in range(0,len(imgsrc)):
                '''
                if re.match('img',imgsrc[i]):
                   imgsrc[i] = imgsrc[i].replace('img','t1')
                '''       
                
                self.loger.info(u'下载%s,当前第 %d 张',imgsrc[i],i+1)
                with open('p/%s.jpg'%imgtitle[i],'wb') as f:
                    src_req = urllib2.Request(imgsrc[i],headers = self.headers)

                    f.write(urllib2.urlopen(src_req).read())
                    
                


                
                #self.loger.info(u'下载%s',imgsrc[i])
                #urllib.urlretrieve(imgsrc[i],'p/%s.jpg'%imgtitle[i])

            #opener=urllib.request.build_opener()
            #opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            #urllib.request.install_opener(opener)
            #url = 'https://pic3.zhimg.com/v2-ba30be1e82f1767cf2057a1cdb35c956_200x112.jpg'
            #urllib.urlretrieve(url,'p/a.jpg')
                
            #将专辑加上全路径
            self.loger.info(u'提取专辑信息，专辑url=%s ',response.url)
            albumfullhref = [self.d_url + i for i in albumhref]
            item["albumtitle"] = albumtitle
            item["albumhref"] = albumfullhref
            item['image_urls'] = imgsrc
            item["albuminfo"] = zip(albumtitle,albumfullhref)
            self.loger.info(u'提取完毕，返回数据！')
            yield item
            















