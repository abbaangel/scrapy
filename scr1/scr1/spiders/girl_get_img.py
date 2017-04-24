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
import time


class DmozSpider(scrapy.Spider):
    name = "ggi"
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
        print u'开始初始化数据'
        self.startnum = 1
        print u'开始加载数据进度文件！'
        self.girlnum = pickle.load(open('num.txt','r'))
      
        

    def close(self):
            
        #结束时报存工作进度
        
      
        print "system stop,save the work,the work done"
       
        lastnum = self.girlnum + 1
        
        pickle.dump(lastnum,open('num.txt','w'))


       
    def start_requests(self):
        for num in xrange(self.girlnum,25000):
            #for num in xrange(16000,25000):
            url = self.start_urls + str(num)
            yield self.make_requests_from_url(url)


  
    
    def make_requests_from_url(self, url):
        
        req = Request(url,headers=self.headers,cookies=self.cookies,dont_filter=True)
        return req
      

    def parse(self, response):
            
            print "====BEGIN        %d       TIMES====" %self.startnum
            
            self.loger.info(u'第---%s---次,URL=%s',self.startnum,response.url)
            urlarr = response.url
            urlnum = urlarr.strip('/').split('/')[-1]   #去链接的进度，由于是多线程并发，要比较大小，防止先读大的后读小的

            #下面判断是否是最大的数，存档使用
            if urlnum > self.girlnum:
                self.girlnum = int(urlnum)
            sel = Selector(response)

            info = sel.xpath('//*[@id="post"]/div[8]/div/div[3]/div/span/a/text()').extract()
            href = sel.xpath('//*[@id="post"]/div[8]/div/div[3]/div/span/a/@href').extract()
            name = sel.xpath('//*[@id="post"]/div[2]/div/div[1]/h1/text()').extract()
            imgsrc =  sel.xpath('//ul[@class="photo_ul"]/li[1]/div/a/img/@data-original').extract()

            #info  is [u'\u517113\u518c']
            if info:
                #print 'get info!'
                '''
                info[0][0] == u'\u5171'#'共'字
                info[0][1]    #数量
                info[0][2]    # '张'或'册'字
                '''
                #print info[0],info[0][0],info[0][1],info[0][2],info[0][-1]

                if info[0][1] > 0 and info[0][-1]==u'\u518c':
                    print u'准备链接信息！'
                    
                    ablumcount = info[0][1]
                    href_to = self.d_url + href[0]
                    print u"获得相册链接与数量，调取下载进程"
                    self.logger.info(u"获得相册链接与数量，调取下载进程，地址：\n%s",response.url)
                    
                    yield  scrapy.Request(href_to,meta = {'ablumcount':ablumcount },callback=self.get_all_album)




                    
                else:
                    if imgsrc and name:
                        print u'是一些图片'
                        self.logger.info(u"是一些图片:%s",response.url)
                        #yield  scrapy.Request(href_to,meta = {'name':name[0] },callback=self.get_one_img)
                        #print '++++++',imgsrc,name
                        self.loger.info(u'下载1封面图像张')
                        print u'下载1张封面'
                        #self.loger.info(u'下载1张')
                        with open('p/%s.jpg'%name[0],'wb') as f:
                            src_req = urllib2.Request(imgsrc[0],headers = self.headers)

                            f.write(urllib2.urlopen(src_req,timeout=3).read())  #将读取的流写入文件保存
                        print u'此图像完成下载'
                        self.loger.info(u'下载1张完成')
                    else:
                        print u'没找到图像链接或名字'
       
            else:
                print u'没有相册的'
                self.logger.info(u"没有相册的:%s",response.url)
                
            self.startnum +=1
            
     

    def get_all_album(self, response):
            #调用此函数的response都是有专辑页的
            print u'这是下载进程--开始下载',response.url
            
            sel = Selector(response)
            
            imgsrc = sel.xpath('//*[@id="photo_list"]/ul/li[@class="igalleryli"]/div[1]/a/img/@src').extract()
            imgtitle= sel.xpath('//*[@id="photo_list"]/ul/li[@class="igalleryli"]/div[1]/a/img/@alt').extract()
            
            self.loger.info(u'下载封面图像,共---%s---张...'%len(imgsrc))
            print '1'
            for i in range(0,len(imgsrc)):
                #print '2'
                time.sleep (0.2)
                print u'共:%s 张，当前第--%d---张'%(len(imgsrc),i+1)
                self.loger.info(u'共:%s 张，当前第--%d---张'%(len(imgsrc),i+1))
                #print '3'
                #print imgtitle[i]
                #print '4'
                with open('p/%s.jpg' % imgtitle[i].encode('gbk'),'wb') as f:
                    #print '5'
                    src_req = urllib2.Request(imgsrc[i],headers = self.headers)
                    f.write(urllib2.urlopen(src_req,timeout=3).read())  #将读取的流写入文件保存,urllib2.urlopen(src_req,timeout =3 ) 超时了会报转码错误
                    #print '6'
                print u'此图像完成下载'
                self.loger.info(u'下载张完成第%d完成',i+1)
















