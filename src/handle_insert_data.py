#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/29 23:39
# @Author  : Mr_d
# @Site    : 
# @File    : handle_insert_data.py
from src.create_lagou_tables import LaGouTables
from src.create_lagou_tables import Seesion
import time


# 定义数据存储类
class HandleLagouData(object):
    def __init__(self):
        self.mysql_session = Seesion()

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
            crawl_date=date
        )
        # 判断表中是否存在类似的数据
        # 按照日期，岗位ID 来查询 '与'的关系
        query_result = self.mysql_session.query(LaGouTables).\
            filter(LaGouTables.crawl_date == date, LaGouTables.positionId == iterm["positionId"]).first()
        if query_result:
            print('已存在相同的岗位信息:%s:%s:%s' % (iterm["city"], iterm["positionId"], iterm["positionName"]))
        else:
            # 插入数据
            self.mysql_session.add(data)
            # 提交数据
            self.mysql_session.commit()
            print('新增岗位信息:%s' % (iterm["positionId"]))

# 创建类的实例
lagou_mysql = HandleLagouData()