# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from urlparse import urljoin
from webspider.items import WebspiderPipelineIqiyiItem

class IqiyiSpider(scrapy.Spider):
    name = 'iqiyi'
    allowed_domains = ['iqiyi.com']
    page_pre = 'http://list.iqiyi.com'
    start_urls = ['http://list.iqiyi.com/']

    def parse(self, response):
        print response
        res = response.xpath('//a[starts-with(@class,"a1") and @data-key="down"]/@href').extract()
        if len(res) > 0:
            #print urljoin(self.page_pre, res[0])
            yield Request(url=urljoin(self.page_pre, res[0]), callback=self.parse)

        webiqiyi = WebspiderPipelineIqiyiItem()
        try:
            for item in response.xpath('//div[@class="wrapper-piclist"]//li'):
                #print item.xpath('.//a[@class="site-piclist_pic_link"]/@href').extract_first()
                webiqiyi['name'] = None
                name = item.xpath('.//div[@class="mod-listTitle_left"]/p/a/text()').extract_first()
                if name:
                    webiqiyi['name'] = name.strip()

                webiqiyi['score'] = None
                score = item.xpath('.//span[@class="score"]/strong/text()').extract_first()
                if score:
                    webiqiyi['score'] = score.strip()
                score = item.xpath('.//span[@class="score"]/text()').extract_first()
                if score:
                    webiqiyi['score'] += score.strip()

                vipinfo = item.xpath('*//span[@class="icon-vip-zx"]').extract()
                if len(vipinfo) > 0:
                    webiqiyi['isvip'] = "1"
                else:
                    webiqiyi['isvip'] = "0"

                actors = u'主演:'
                for actor in item.xpath('*//div[@class="role_info"]/em/a/text()').extract():
                    actors += actor.strip() + "+"
                webiqiyi['actors'] = actors
                yield webiqiyi
                #print u"=================== {0} {1} {2}".format(webiqiyi['name'], webiqiyi['score'], webiqiyi['actors'])
        except Exception as e:
            print "error {0}".format(e)
