# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''
class Scr1Pipeline(object):
    def process_item(self, item, spider):
        return item
'''

import json  
import codecs  
import time  
  
class Scr1Pipeline(object):  
    def __init__(self):  
        self.file = codecs.open('src1_CN_%s.json'%time.strftime ('%Y_%m_%d_%H_%M',time.localtime()), 'wb', encoding='utf-8')  
  
    def process_item(self, item, spider):  
        line = json.dumps(dict(item)) + '\n'  
        # print line  
        self.file.write(line.decode("unicode_escape"))  
        return item 
        self.file.close()

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
headers = {
        
      
      "User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36',
      "Accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
      "Accept-Encoding":"gzip, deflate",
      "Referer":"http://www.zngirls.com/g/18333/",
 
    }

 
class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url,headers = headers)


    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
