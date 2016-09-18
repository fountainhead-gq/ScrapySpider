# -*- coding: utf-8 -*-
import scrapy
import json
import logging
from Lagou.items import LagouItem

logger = logging.getLogger()


class LagouspiderSpider(scrapy.Spider):
    name = "LagouSpider"
    #allowed_domains = ["lagou.com"]
    start_urls = (
        'http://www.lagou.com/zhaopin/',
    )
    url ="http://www.lagou.com/jobs/positionAjax.json?"
    headers = {
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Referer': 'http://www.lagou.com/',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    curpage = 1

    def start_requests(self):
        return [scrapy.http.FormRequest(self.url, formdata={'pn': '1'}, headers=self.headers, callback=self.parse)]

    def parse(self, response):
        try:
            item = LagouItem()
            html = json.loads(response.body.decode('utf-8'))
            if html.get('content').get('positionResult').get('resultSize') != 0:
                results = html.get('content').get('positionResult').get('result')
                for result in results:
                    item['keyword'] = response.meta.get('kd')
                    item['companyLogo'] = result.get('companyLogo')
                    item['salary'] = result.get('salary')
                    item['city'] = result.get('city')
                    item['financeStage'] = result.get('financeStage')
                    item['industryField'] = result.get('industryField')
                    item['approve'] = result.get('approve')  #
                    item['positionAdvantage'] = result.get('positionAdvantage')
                    item['positionId'] = result.get('positionId')
                    if isinstance(result.get('companyLabelList'), list):
                        item['companyLabelList'] = ','.join(result.get('companyLabelList'))
                    else:
                        item['companyLabelList'] = ''
                    item['score'] = result.get('score')
                    item['companySize'] = result.get('companySize')
                    item['adWord'] = result.get('adWord')  #
                    item['createTime'] = result.get('createTime')
                    item['companyId'] = result.get('companyId')  #
                    item['positionName'] = result.get('positionName')
                    item['workYear'] = result.get('workYear')
                    item['education'] = result.get('education')
                    item['jobNature'] = result.get('jobNature')
                    item['companyShortName'] = result.get('companyShortName')
                    item['district'] = result.get('district')
                    item['businessZones'] = result.get('businessZones')  #
                    item['imState'] = result.get('imState')  #
                    item['lastLogin'] = result.get('lastLogin')  #
                    item['publisherId'] = result.get('publisherId')  #
                    item['plus'] = result.get('plus')  #
                    item['pcShow'] = result.get('pcShow')
                    item['appShow'] = result.get('appShow')
                    item['deliver'] = result.get('deliver')
                    item['gradeDescription'] = result.get('gradeDescription')  #
                    item['companyFullName'] = result.get('companyFullName')  #
                    item['formatCreateTime'] = result.get('formatCreateTime')  #
                    salary = result.get('salary')
                    salary = salary.split('-')  #
                    if len(salary) == 1:
                        item['salaryMax'] = int(salary[0][:salary[0].find('k')])
                    else:
                        item['salaryMax'] = int(salary[1][:salary[1].find('k')])
                    item['salaryMin'] = int(salary[0][:salary[0].find('k')])
                    item['salaryAvg'] = (item['salaryMin'] + item['salaryMax']) / 2
                    yield item

                totalPageCount = html.get('content').get('positionResult').get('totalCount')

                if self.curpage <= totalPageCount:
                    self.curpage += 1  # 继续爬下一页
                    print(u"当前页{}".format(self.curpage))
                    yield scrapy.http.FormRequest(self.url, formdata={'pn': str(self.curpage)}, headers=self.headers, callback=self.parse)
        except:
            logger.error(response.body)
            logger.error(response.status)






