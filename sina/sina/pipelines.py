# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv

from itemadapter import ItemAdapter
from .items import ZongyiItem,GuoneiItem,DianyingItem

class SinaPipeline:
    def __init__(self):
        self.file = None


    def process_item(self, item, spider):
        cav_name = './result/'+str(item.__class__).split('.')[-1][:-6] + '_headless.csv'
        print('***' * 5, "ITEM", '***' * 5)
        desc = ''
        for line in list(item['desc']):
            line = line.replace('\u3000\u3000', '')
            desc += line
        with open(cav_name, 'a+', encoding='utf-8') as fp:
            writer = csv.writer(fp)
            print(item['page'],str(item.__class__).split('.')[-1][:-6],item['title'], item['times'])
            writer.writerow([item['page'],item['title'], desc, item['times']])

        '''
        desc = ''
        for line in list(item['desc']):
            line = line.replace('\u3000\u3000','')
            desc += line
        item_csv = item['title']+','+ item['times']+','+ desc
        self.file.write(item_csv)
        '''

    def open_spider(self,spider):
        '''self.file = open('./sina-test.csv','a',encoding='utf-8')
        self.file.write('title'+','+ 'times'+','+ 'desc'+'\n')'''
        pass

    def close_spider(self,spider):
        '''self.file.close()'''
        pass

    # @classmethod
    # def from_crawler(self,cls,crawler):
    #     pass