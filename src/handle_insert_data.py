#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/29 23:39
# @Author  : Mr_d
# @Site    : 
# @File    : handle_insert_data.py
import time
from collections import Counter

from sqlalchemy import func

from src.create_lagou_tables import LaGouTables
from src.create_lagou_tables import Seesion


# 定义数据存储类
class HandleLagouData(object):
    def __init__(self):
        self.mysql_session = Seesion()
        self.date = time.strftime("%Y-%m-%d", time.localtime())

    # 定义数据存储方法
    def insert_iterm(self, iterm):
        # 定义数据
        date = time.strftime("%Y-%m-%d", time.localtime())
        data = LaGouTables(
            # 岗位ID,非空字段，唯一性
            positionId=iterm['positionId'],
            # 岗位名称
            positionName=iterm['positionName'],
            # 创建时间
            createTime=iterm['createTime'],
            # 发布时间
            formatCreateTime=iterm['formatCreateTime'],
            # 工资
            salary=iterm['salary'],
            # 岗位性质
            jobNature=iterm['jobNature'],
            # 岗位标签
            positionAdvantage=iterm['positionAdvantage'],
            # 学历
            education=iterm['education'],
            # 工作年限
            workYear=iterm['workYear'],
            # 公司简称
            companyShortName=iterm['companyShortName'],
            # 公司全称
            companyFullName=iterm['companyFullName'],
            # 公司类型
            financeStage=iterm['financeStage'],
            # 业务方向
            industryField=iterm['industryField'],
            # 公司规模
            companySize=iterm['companySize'],
            # 公司福利标签
            companyLabelList=','.join(iterm['companyLabelList']),
            # 公司所在城市
            city=iterm['city'],
            # 公司所在区
            district=iterm['district'],
            # 地铁
            subwayline=iterm['subwayline'],
            # 地点
            stationname=iterm['stationname'],
            # 经度
            longitude=iterm['longitude'],
            # 纬度
            latitude=iterm['latitude'],
            # 爬取日期
            crawl_date=date,
            # 爬取的岗位类型
            thirdType=iterm['thirdType']
        )
        # 判断表中是否存在类似的数据
        # 按照日期，岗位ID 来查询 '与'的关系
        query_result = self.mysql_session.query(LaGouTables). \
            filter(LaGouTables.crawl_date == date, LaGouTables.positionId == iterm["positionId"]).first()
        if query_result:
            print('已存在相同的岗位信息:%s:%s:%s' % (iterm["city"], iterm["positionId"], iterm["positionName"]))
        else:
            # 插入数据
            self.mysql_session.add(data)
            # 提交数据
            self.mysql_session.commit()
            print('新增岗位信息:%s' % (iterm["positionId"]))

    # 行业信息
    def query_industryfield_result(self):
        info = {}
        # 查询今日抓取到的行业信息数据 .filter(
        #             LaGouTables.crawl_date == self.date
        #         )
        result = self.mysql_session.query(LaGouTables.industryField).all()
        result_list1 = [x[0].split(',')[0] for x in result]
        result_list2 = [x for x in Counter(result_list1).items() if x[1] > 150]
        # 填充的是series里面的data
        data = [{"name": x[0], "value": x[1]} for x in result_list2]
        name_list = [name['name'] for name in data]
        info['x_name'] = name_list
        info['data'] = data
        return info

    # 查询薪资情况
    def query_salary_result(self):
        info = {}
        # 查询今日抓取到的薪资数据 .filter(LaGouTables.crawl_date == self.date)
        result = self.mysql_session.query(LaGouTables.salary).all()
        # 处理原始数据
        result_list1 = [x[0] for x in result]
        # 计数,并返回
        result_list2 = [x for x in Counter(result_list1).items() if x[1] > 100]
        result = [{"name": x[0], "value": x[1]} for x in result_list2]
        name_list = [name['name'] for name in result]
        info['x_name'] = name_list
        info['data'] = result
        return info

    # 查询工作年限情况
    def query_workyear_result(self):
        info = {}
        # 查询今日抓取到的薪资数据 .filter(LaGouTables.crawl_date == self.date)
        result = self.mysql_session.query(LaGouTables.workYear).all()
        # 处理原始数据
        result_list1 = [x[0] for x in result]
        # 计数,并返回
        result_list2 = [x for x in Counter(result_list1).items()]
        result = [{"name": x[0], "value": x[1]} for x in result_list2 if x[1] > 15]
        name_list = [name['name'] for name in result]
        info['x_name'] = name_list
        info['data'] = result
        return info

    # 查询学历信息
    def query_education_result(self):
        info = {}
        # 查询今日抓取到的薪资数据 .filter(LaGouTables.crawl_date == self.date)
        result = self.mysql_session.query(LaGouTables.education).all()
        # 处理原始数据
        result_list1 = [x[0] for x in result]
        # 计数,并返回
        result_list2 = [x for x in Counter(result_list1).items()]
        result = [{"name": x[0], "value": x[1]} for x in result_list2]
        name_list = [name['name'] for name in result]
        info['x_name'] = name_list
        info['data'] = result
        return info

    # 岗位发布数量,折线图
    def query_job_result(self):
        info = {}
        result = self.mysql_session.query(LaGouTables.crawl_date, func.count('*').label('c')).group_by(
            LaGouTables.crawl_date).filter(LaGouTables.thirdType == 'python').all()
        result1 = [{"name": x[0], "value": x[1]} for x in result]
        name_list = [name['name'] for name in result1]
        info['x_name'] = name_list
        info['data'] = result1
        return info

    # 根据城市计数
    def query_city_result(self):
        info = {}
        # 查询今日抓取到的薪资数据 .filter(
        #             LaGouTables.crawl_date == self.date)
        result = self.mysql_session.query(LaGouTables.city, func.count('*').label('c')).group_by(LaGouTables.city).all()
        result1 = [{"name": x[0], "value": x[1]} for x in result]
        name_list = [name['name'] for name in result1]
        info['x_name'] = name_list
        info['data'] = result1
        return info

    # 融资情况
    def query_financestage_result(self):
        info = {}
        # 查询今日抓取到的薪资数据 .filter(LaGouTables.crawl_date == self.date)
        result = self.mysql_session.query(LaGouTables.financeStage).all()
        # 处理原始数据
        result_list1 = [x[0] for x in result]
        # 计数,并返回
        result_list2 = [x for x in Counter(result_list1).items()]
        result = [{"name": x[0], "value": x[1]} for x in result_list2]
        name_list = [name['name'] for name in result]
        info['x_name'] = name_list
        info['data'] = result
        return info

    # 公司规模
    def query_companysize_result(self):
        info = {}
        # 查询今日抓取到的薪资数据 .filter(LaGouTables.crawl_date == self.date)
        result = self.mysql_session.query(LaGouTables.companySize).all()
        # 处理原始数据
        result_list1 = [x[0] for x in result]
        # 计数,并返回
        result_list2 = [x for x in Counter(result_list1).items()]
        result = [{"name": x[0], "value": x[1]} for x in result_list2]
        name_list = [name['name'] for name in result]
        info['x_name'] = name_list
        info['data'] = result
        return info

    # 任职情况
    def query_jobNature_result(self):
        info = {}
        # 查询今日抓取到的薪资数据 .filter(LaGouTables.crawl_date == self.date)
        result = self.mysql_session.query(LaGouTables.jobNature).all()
        # 处理原始数据
        result_list1 = [x[0] for x in result]
        # 计数,并返回
        result_list2 = [x for x in Counter(result_list1).items()]
        result = [{"name": x[0], "value": x[1]} for x in result_list2]
        name_list = [name['name'] for name in result]
        info['x_name'] = name_list
        info['data'] = result
        return info

    # 抓取数量
    def count_result(self):
        info = {}
        info['all_count'] = self.mysql_session.query(LaGouTables).count()
        info['today_count'] = self.mysql_session.query(LaGouTables).filter(LaGouTables.crawl_date == self.date).count()
        return info

    # def query_city_salary_industryfidle(self):
    #     result = self.mysql_session.query(func.lower(func.substring_index(Lagoutables.industryField,',',1)),
    #                                       Lagoutables.city,
    #                                       func.avg(func.replace(func.lower(func.substring_index(Lagoutables.salary,'-',2)),'k','')),
    #                                       func.count(func.lower(func.substring_index(Lagoutables.industryField,',',1))).label('c')).filter(
    #         Lagoutables.crawl_date == self.date
    #     ).group_by(func.lower(func.substring_index(Lagoutables.industryField,',',1)),
    #                Lagoutables.city).all()
    #     result_list = [{"industry":item[0],"city":item[1],"salary_avg":int(item[2]),"value":item[3]} for item in result if item[3] >10]
    #     info = {}
    #     # city_list = set([city[1] for city in result])
    #     city_list = set([city['city'] for city in result_list])
    #     # industryfield_list = set([industry[0] for industry in result])
    #     industryfield_list = set([x['industry'] for x in result_list])
    #     series_list = []
    #     for city in city_list:
    #         series_item = {}
    #         series_data_list = []
    #         series_item['name'] = city
    #         series_item['type'] = "bar"
    #         for item in industryfield_list:
    #             series_data_item = {}
    #             series_data_item['name'] = item
    #             value = [x['salary_avg'] for x in result_list if x['industry'] == item and x['city'] == city]
    #             if value:
    #                 series_data_item['value'] = value[0]
    #                 series_data_list.append(series_data_item)
    #         series_item['data'] = series_data_list
    #         series_list.append(series_item)
    #     info['x_name'] = list(industryfield_list)
    #     info['legend_data'] = list(city_list)
    #     info['data'] = series_list
    #     return info


# 实例化类
lagou_mysql = HandleLagouData()

