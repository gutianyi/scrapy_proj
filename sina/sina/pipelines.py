# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv

from itemadapter import ItemAdapter
from sqlalchemy import Column, create_engine, Text, DateTime, Integer, String
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    times = Column(DateTime)
    title = Column(Text())
    content = Column(Text())
    type = Column(Text())

class SinaPipeline:
    def __init__(self):
        self.file = None

        self.engine = create_engine('mysql+pymysql://root:gty082210@localhost:3306/sina', encoding="utf-8", pool_size=10,
                                max_overflow=-1, pool_recycle=1200)
        Base.metadata.create_all(self.engine)
        self.DBSession = sessionmaker(bind=self.engine)

    def process_item(self, item, spider):
        print(item['type'],  item['title'], item['times'])
        new = Data()
        new.title = item['title']
        new.times = item['times']
        new.content = item['desc']
        new.type = item['type']
        session = self.DBSession()
        session.add(new)
        session.commit()
        return item

        """  存在csv中
        cav_name = './result/'+str(item['type]) + '.csv'
        print('***' * 5, "ITEM", '***' * 5)
        desc = ''
        for line in list(item['desc']):
            line = line.replace('\u3000\u3000', '')
            desc += line
        with open(cav_name, 'a+', encoding='utf-8') as fp:
            writer = csv.writer(fp)

            writer.writerow([item['page'],item['title'], desc, item['times']])
        """

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