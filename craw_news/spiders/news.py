# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from craw_news.items import newsItem


class NewsSpider(Spider):
    name = 'news'
    allowed_domains = ['he.people.com.cn']
    start_urls = ['http://he.people.com.cn/GB/197051/381128/index.html']
    # start_urls = ['http://he.people.com.cn']

    def parse(self, response):
        sel = Selector(response)
        # 获得下一篇文章的url
        urls = sel.xpath('/html/body/div[4]/div[1]/div[2]/div[3]/a/text()').extract()
        for url in urls:
            if url != '下一页':
                url = "http://he.people.com.cn/GB/197051/381128/index" + url + ".html"
                print(url)
                yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        sel = Selector(response)
        all_li = sel.xpath('/html/body/div[4]/div[1]/div[2]/ul/li')
        print(all_li.__len__())
        # items = []
        if all_li:
            for li in all_li:
                item = newsItem()
                vtitle = li.xpath('a/text()').extract()
                vdate = li.xpath('em/text()').extract()
                vlink = li.xpath('a/@href').extract()

                item['title'] = vtitle[0]
                item['date'] = vdate[0]
                item['link'] = 'http://he.people.com.cn'+vlink[0]
                # items.append(item)
                # yield item
                yield scrapy.Request(url=item['link'], meta={'item': item}, callback=self.parse_detail,
                                     dont_filter=True)

    def parse_detail(self, response):
            item = response.meta['item']
            item['content'] = response.xpath('/html/body/div[4]/div[1]/div[2]').extract()
            yield item

