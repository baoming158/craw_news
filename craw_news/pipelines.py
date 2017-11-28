# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import pymysql

# this class for write file
class JsonWriterPipeline(object):
       '''保存到文件中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行'''
       def __init__(self):
        self.file = codecs.open('info.json', 'w', encoding='utf-8')#保存为json文件
       def process_item(self, item, spider):
            line = json.dumps(dict(item)) + "\n"#转为json的
            self.file.write(line)#写入文件中
            return item
       def spider_closed(self, spider):#爬虫结束时关闭文件
            self.file.close()

# this class for insert data to db
class insertDbPipeline(object):
        '''
        将内容保存到数据库中
        '''

        def process_item(self, item, spider):
            con = pymysql.connect(
                host='172.21.19.203',
                port=3306,
                user='ky',
                passwd='ky',
                db='video_dot',
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
            )
            # 使用cursor()方法获取操作游标
            cursor = con.cursor(pymysql.cursors.DictCursor)
            sql = ("insert into video_name(url,name,date,content)""values( %s,%s,%s,%s)")
            lis = (item['link'],item['title'],item['date'],item['content'])
            cursor.execute(sql, lis)
            con.commit()
            cursor.close()
            con.close()
            return item