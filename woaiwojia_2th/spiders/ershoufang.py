# -*- coding: utf-8 -*-
import scrapy
from ..items import ErshoufangItem
from datetime import datetime, timedelta
from twisted.internet.error import TimeoutError
import math

class ErshoufangSpider(scrapy.Spider):
    name = 'ershoufang'
    allowed_domains = ['hz.5i5j.com']
    #start_urls = ['https://hz.5i5j.com/ershoufang/o8/']
    base_url = 'https://hz.5i5j.com/ershoufang/o8n{}'
    #根据房源数计算页数
    num = math.ceil(31472/30)

    custom_settings = {
        #以运行爬虫的日期命名csv文件
        'FEED_URI' : './{}.csv'.format(datetime.now().strftime('%Y%m%d')),
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING' : 'utf8'
    }


    def start_requests(self):
        # 分若干段下载，根据代理池可用代理数量来考虑
        offset = 500
        for n in range(0, self.num, offset):
            yield scrapy.Request(self.base_url.format(n+1), meta={'start':n, 'offset':offset}, dont_filter=True)

    def parse(self, response):
        divs= response.css('div.listCon')
        for d in divs:
            item = ErshoufangItem()
            item['title'] = d.css('h3 a::text').extract_first()
            item['href'] = d.css('h3 a::attr(href)').extract_first()
            item['tags'] = d.css('.listTag span::text').extract()
            item['price'] = d.css('.jia p.redC+p::text').extract_first()

            infos = d.css('.listX p::text')[0].extract().split('·')
            item['huxing'] = infos[0].strip()
            item['square'] = infos[1].strip(' 平米')
            item['orientation'] = infos[2].strip()
            item['floor'] = infos[3].strip()

            item['area'] = d.css('.listX p a::text').extract_first().split()[0]

            infos = d.css('.listX p::text')[2].extract().split('·')
            item['view'] = infos[1].strip()
            t = infos[2].strip(' 发布')
            if t == '今天':
                t = datetime.now()
            elif t == '昨天':
                t = datetime.now() - timedelta(days=1)
            else:
                t = datetime.strptime(t, '%Y-%m-%d')
            #日期转换为字符串格式
            item['time'] = t.strftime('%Y-%m-%d')
            yield item

        #分页
        next_p = response.css('.pageBox div.pageSty.rf').xpath('./a[contains(.,"下一页")]/@href').extract_first()
        cur_p = response.css('.pageBox div.pageSty.rf a.cur::text').extract_first()
        start = response.meta['start']
        offset = response.meta['offset']
        if next_p is not None and int(cur_p) < (start + offset):
            yield response.follow(next_p, callback=self.parse, meta={'start':start, 'offset':offset}, errback=self.errback_parse)
            self.logger.info('当前页<{}>已完成提取，有下一页:{}'.format(cur_p, next_p))
        else:
            self.logger.info('最后一页<{}>已完成提取'.format(cur_p))

    def errback_parse(self, failure):
        self.logger.error(repr(failure))

        if failure.check(TimeoutError):
            url = failure.request.url
            #不能加errback参数，否则无限循环
            self.logger.debug('超时，失败次数过多，重新发起一次该请求 {}'.format(url))
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)
