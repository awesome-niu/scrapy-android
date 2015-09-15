# -*- coding:gbk -*-
import scrapy
from tutorial.items import MaNongItem
from urllib import unquote

class DmozSpider(scrapy.spiders.Spider):
    name = "techandroid"
    start_urls = [
        "http://www.androidweekly.cn//",
        "http://www.androidweekly.cn/page/2/",
        "http://www.androidweekly.cn/page/3/",
        "http://www.androidweekly.cn/page/4/",
        "http://www.androidweekly.cn/page/5/",
    ]

    # def parse(self, response):
    #     result1 = response.xpath("//li/p/a[2]")
    #
    #     for (index1,link1) in enumerate(result1):
    #         text1 = link1.xpath("text()").extract()
    #         if text1:
    #             print text1[0]
    #         print "--------------------------------------------------------------------------"

    # def parse(self, response):
    #     result1 = response.xpath("//li/p[last()]")
    #     result2 = response.xpath("//li/p/a[1]")
    #
    #     for ((index1,link1), (index2, link2)) in zip(enumerate(result1), enumerate(result2)):
    #         text1 = link1.xpath("text()").extract()
    #         text2 = link2.xpath("text()").extract()
    #         if text2:
    #             print text2[0]
    #         if text1:
    #             print text1[0]
    #         print "--------------------------------------------------------------------------"
    def parse(self, response):
        host = "http://www.androidweekly.cn"
        link =  response.xpath("//article[contains(@class, 'post')]/header[contains(@class, 'post-header')]/h2/a")
        for index, each_weekly in enumerate(link):
            url = host + each_weekly.xpath("@href").extract()[0]
            yield scrapy.Request(url, callback=self.parse_android)

    def parse_android(self, response):
        # result1 = response.xpath("//li/p[last()]")
        # result2 = response.xpath("//li/p/a")
        #
        # for ((index1,link1), (index2, link2)) in zip(enumerate(result1), enumerate(result2)):
        #     text1 = link1.xpath("text()").extract()
        #     text2 = link2.xpath("text()").extract()
        #      if text2:
        #         print text2[0]
        #     if text1:
        #         print text1[0]

        result = response.xpath("//li/p/a")
        for index, link in enumerate(result):
            url_source = link.xpath("@href").extract()
            title_source = link.xpath("text()").extract()

            if url_source and title_source:
                url = url_source[0]
                title = title_source[0]
                real_url = unquote(url)
                item = MaNongItem()
                item['host'] =  response.url
                item['title'] = title
                item['link'] = real_url
                item['tag'] = "android"
                yield item