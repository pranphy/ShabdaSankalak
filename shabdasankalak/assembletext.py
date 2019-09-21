#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 ft=python

# author : Prakash [प्रकाश]
# date   : 2019-09-19 19:30

import os
from pathlib import Path


import scrapy
from scrapy.crawler import CrawlerProcess

from .spiders import Kantipur

class NewsCrawler: 
    def __init__(self,opath):
        self.output = []
        self.process = CrawlerProcess(settings={'LOG_ENABLED': False}) # Enables/disables log
        self.path = opath
        self.exist = []

    def get_result(self):
        return self.output

    def yield_output(self, data):
        self.output.append(data)

        url = data['url']
        newsid = data['id']
        date = data['date']
        urlcat = data['urlcat']
        miti = data['miti']
        title = data['title']
        news = data['content']
        nepcat = data['category']
        author = data['author']

        pathdir = os.path.join(self.path,date,urlcat)
        filename = os.path.join(pathdir,newsid+'.txt')
        os.makedirs(pathdir, exist_ok=True)

        #print(f'making directory {pathdir}')
        #print(f'writing file {filename}')
        print(f'<- [{date}] :: {url} ... ')

        my_file = Path(filename)
        if not my_file.is_file():
            with open(filename,'w') as ofl:
                print(f'# url: {url}\n# title : {title}\n# date: {miti}\n# category: {nepcat}\n# author:{author}',file=ofl,end='\n')
                ofl.write(news)
        else:
            print(f'DUP: [####]:: {url}')
            self.exist.append(url)


    def crawl_news(self, spider,start_date=None,end_date=None):
        self.process.crawl(spider, start_date, end_date, callback_func=self.yield_output )
        self.process.start()

        print(f'there wer {len(self.exist)} duplicates ')



if __name__ == '__main__':
    start_date = '2019/01/01'
    end_date = '2019/01/01'
    opath = '../scrapped/kantipur'

    NC = NewsCrawler(opath)
    NC.crawl_news(Kantipur,start_date,end_date)
    op = NC.output



