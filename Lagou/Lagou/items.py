# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    city = scrapy.Field()
    companySize = scrapy.Field()
    companyShortName = scrapy.Field()
    positionName = scrapy.Field()
    salaryMax = scrapy.Field()
    salaryMin = scrapy.Field()
    salaryAvg = scrapy.Field()
    salary =scrapy.Field()
    positionAdvantage = scrapy.Field()
    companyLabelList = scrapy.Field()
    companyLogo = scrapy.Field()
    workYear = scrapy.Field()  # 工作年限
    education = scrapy.Field()  # 教育经历
    jobNature = scrapy.Field()  # 全职还是兼职
    financeStage = scrapy.Field()  # 成长型/c轮/d轮
    district = scrapy.Field()  # 朝阳区
    deliver = scrapy.Field()  # 统计 已提交简历
    createTime = scrapy.Field()  # 创建时间
    industryField = scrapy.Field()  # 行业
    appShow = scrapy.Field()
    pcShow = scrapy.Field()
    positionId = scrapy.Field()  # 职位id：positionId
    score = scrapy.Field()
    keyword = scrapy.Field()
    approve = scrapy.Field()
    adWord = scrapy.Field()
    companyId = scrapy.Field()
    businessZones = scrapy.Field()
    imState =scrapy.Field()
    lastLogin = scrapy.Field()
    publisherId =scrapy.Field()
    gradeDescription = scrapy.Field()
    companyFullName = scrapy.Field()
    formatCreateTime = scrapy.Field()
    plus = scrapy.Field()
    pass
