#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 ft=python

# author : Prakash [प्रकाश]
# date   : 2019-09-14 21:33



import json
import scrapy

from urllib.parse import urlsplit
from bs4 import BeautifulSoup

from datetime import timedelta
from datetime import datetime


class Kantipur(scrapy.Spider):
    name = "kantipur"
    domain = "https://www.ekantipur.com"
    categories = [
        'Art',
        'bibidha',
        'blog',
        'business',
        'cricket-world-cup-2019',
        'destination',
        'diaspora',
        'entertainment',
        'feature',
        'health',
        'hello-sukrabar',
        'interesting',
        'Interview',
        'kopila',
        'koseli',
        'lifestyle',
        'literature',
        'local-elections-2017',
        'nari-nepali',
        'national',
        'national',
        'nepal-elections-2074',
        'news',
        'opinion',
        'Other',
        'our-nepal',
        'pathakmanch',
        'phadko',
        'pradesh-1',
        'pradesh-2',
        'pradesh-3',
        'pradesh-4',
        'pradesh-5',
        'pradesh-6',
        'pradesh-7',
        'printedition',
        'sports',
        'technology',
        'world',
    ]

    start_date ="2019/09/01"
    end_date = "2019/09/01"

    def __init__(self,start_date,end_date,callback_func):
        self.output_callback = callback_func
        self.start_date = start_date
        self.end_date = end_date


    def start_requests(self):
        date_format = '%Y/%m/%d'

        cur_date = datetime.strptime(self.start_date,date_format)
        last_date = datetime.strptime(self.end_date,date_format).date()

        if cur_date.date() <= last_date:
            cur_date = cur_date + timedelta(days=1)
            cur_date_str = cur_date.strftime(date_format)

            for cat in self.categories: 
                yield scrapy.Request(url=f"{self.domain}/{cat}/{cur_date_str}", callback=self.get_categories)

    def get_categories(self, response):
        parts = response.request.url.split('/')
        # 0 http: 1 '' 2  ekantipur.com 3 category 4 year 5 month 6 day

        date = f'{parts[4]}/{parts[5]}/{parts[6]}'
        cat = parts[3]

        for article in response.css('article'): 
            url = article.css("h2 a::attr(href)").extract_first()
            yield scrapy.Request(url=f"{self.domain}{url}", callback=self.get_news)


    def get_news(self,response): 
        """
        This extracts the news content and returns all the info

        :type    response: scrapy response object
        :param   response: the response object when visiging the provided url

        """

        parts = response.request.url.split('/')
        # 0 http: 1 '' 2  ekantipur.com 3 category 4 year 5 month 6 day 7 newsid 
        date = f'{parts[4]}/{parts[5]}/{parts[6]}'
        urlcat = parts[3]
        newsid = parts[7].replace('.html','')

        # This has to be one of the insane piece of code to get the news from kantipur article.
        # so the story is that the html of news at kantipur website is malformed for some reason
        # if i get the text from this description tag, it gives text from other news section
        # at the end of page too. Because for some reason one of the tags is not properly
        # closed. (article). Now Every news ends at a span class 'published-at' so I use 
        # beautifulsoup to chop off this description at that tag and  remove all the html tags 
        # to get the news text
        this_news = response.css('article div.row div.description').extract_first()
        this_news = this_news[:this_news.find('published-at')]
        this_news_bs = BeautifulSoup(this_news)

        news = this_news_bs.get_text()

        yield_dict =  {
            'url':  response.request.url ,
            'id':newsid,
            'date':date,
            'urlcat':urlcat,
            'miti': response.css('article time::text').extract_first(),
            'author': response.css('article span.author a::text').extract_first(),
            'title': response.css("article div.article-header h1::text").extract_first(),
            'content':news,
            'category': response.css("article div.article-header div.cat_name a::text").extract_first(),
        }

        self.output_callback(yield_dict)
        yield yield_dict

