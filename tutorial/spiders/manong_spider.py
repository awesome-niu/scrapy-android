# -*- coding:gbk -*-
import scrapy
from tutorial.items import MaNongItem
from urllib import unquote

class DmozSpider(scrapy.spiders.Spider):
    name = "manong"
    start_urls = [
        "http://weekly.manong.io/issues/",
    ]

    # def parse(self, response):
    #     print response
    #     links = response.xpath("//h4/a")
    #     for index, link in enumerate(links):
    #         url = link.xpath("@href").extract()
    #         if url:
    #             if link.xpath("text()").extract() and len(link.xpath("text()").extract()) == 1:
    #                 title = link.xpath("text()").extract()[0]
    #                 if 'android' in title or 'Android' in title and "job" not in url:
    #                     item = MaNongItem()
    #                     item['host'] =  response.url
    #                     item['title'] = title
    #                     item['link'] = url[0][35:]
    #                     item['tag'] = "android"
    #                     yield  item

    def parse(self, response):
        for each_weekly in response.xpath("//h4/a/@href").extract():
            yield scrapy.Request(each_weekly, callback=self.parse_android)

    def parse_android(self, response):
        result = response.xpath("//h4/a")
        for index, link in enumerate(result):
            url_source = link.xpath("@href").extract()
            title_source = link.xpath("text()").extract()
            if url_source and title_source:
                url = url_source[0]
                title = title_source[0]
                if 'android' in title or 'Android' in title and "job" not in url:
                    real_url = unquote(url[35:])
                    index = real_url.index("&aid")
                    item = MaNongItem()
                    item['host'] =  response.url
                    item['title'] = title
                    item['link'] = real_url[0:index]
                    item['tag'] = "android"
                    yield item