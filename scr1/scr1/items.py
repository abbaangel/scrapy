# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class baiduitem(scrapy.Item):
    title = scrapy.Field()
    href = scrapy.Field()
    content = scrapy.Field()

class get37item(scrapy.Item):
    	idhref = scrapy.Field() 
        idnum = scrapy.Field() 
        orderid = scrapy.Field()
        bankname = scrapy.Field()
        devtype = scrapy.Field()
        devcount = scrapy.Field()
        send = scrapy.Field() 
        arrive = scrapy.Field()
class item163(scrapy.Item):
    title = scrapy.Field()
    href = scrapy.Field()
    content = scrapy.Field()




class Scr1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    src = scrapy.Field()
    link = scrapy.Field()
    #pass

class testitem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    td = scrapy.Field()
   


class zitem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    alt = scrapy.Field()
    src = scrapy.Field()
    href = scrapy.Field()
    desc = scrapy.Field()
    #pass
class girlitem(scrapy.Item):
    name = scrapy.Field()
    number = scrapy.Field()
    info = scrapy.Field()
    desc = scrapy.Field()
    image_urls = scrapy.Field()
    albumcount =scrapy.Field()
    albuminfo = scrapy.Field()
    albumtitle = scrapy.Field()
    albumhref = scrapy.Field()
    image_paths = scrapy.Field()
    
