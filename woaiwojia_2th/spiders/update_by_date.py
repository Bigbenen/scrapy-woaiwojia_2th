# -*- coding: utf-8 -*-
import scrapy
from ..items import ErshoufangItem
from datetime import datetime, timedelta
from ..update_by_date_utils import read_last

class UpdateByDateSpider(scrapy.Spider):
    '''检查更新新上二手房源，适用于每日/周等小数据量更新。'''
    # update_by_date.py的输出，应该为局部设置
    custom_settings = {
        'FEED_URI' : './1.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING' : 'utf8'
    }

    name = 'update_by_date'
    allowed_domains = ['hz.5i5j.com']
    start_urls = ['https://hz.5i5j.com/ershoufang/o8']
    base_url = 'https://hz.5i5j.com/ershoufang/o8n{}'

    #读取本地存档,获得最近一条数据
    last_time, last_house = read_last()
    find_last = False

    def parse(self, response):
        #调试时可启用终端
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
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
            item['time'] = t.strftime('%Y-%m-%d')
            #判断是否到达上次爬取到位置
            if item['time'] == self.last_time and item['href'] == self.last_house:
                self.find_last = True
                self.logger.info('到达上次提取结束位置{}'.format(dict(item)))
                break
            yield item

        cur_p = response.css('.pageBox div.pageSty.rf a.cur::text').extract_first()
        if not self.find_last:
            # 分页
            next_p = response.css('.pageBox div.pageSty.rf').xpath('./a[contains(.,"下一页")]/@href').extract_first()
            if next_p is not None:
                yield response.follow(next_p, callback=self.parse)
                self.logger.info('当前页<{}>已完成提取，有下一页:{}'.format(cur_p, next_p))
            else:
                self.logger.info('最后一页<{}>已完成提取'.format(cur_p))
        else:
            self.logger.info('已到达上次提取结束位置<第{}页>，更新完毕!'.format(cur_p))
            #整合数据文件,但操作feed exports产生但文件会报错，因为文件处于未关闭状态

