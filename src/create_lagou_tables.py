#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/29 23:05
# @Author  : Mr_d
# @Site    : 
# @File    : create_lagou_tables.py
# 连接数据库用
from sqlalchemy import create_engine
# 建表需要导入字段类型
from sqlalchemy import Integer, Float, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column

# 创建数据库连接
engin = create_engine\
    ("mysql+pymysql://root:root@localhost:3306/lagou?charset=utf8")
# 操作数据库，创建一个session
Seesion = sessionmaker(bind=engin)
# 生命基类用来生成数据表
Base_Class = declarative_base()


# 创建数据表
class LaGouTables(Base_Class):
    # 指定表的名称
    __tablename__ = "lagou_data"
    # id 设为主键，自增
    id = Column(Integer, primary_key=True, autoincrement=True)
    # ****** -------岗位信息 ------- ******
    # 岗位ID,非空字段，唯一性
    positionId = Column(Integer, nullable=False, unique=True)
    # 岗位名称
    positionName = Column(String(length=50), nullable=False)
    # 创建时间
    createTime = Column(String(length=50), nullable=True)
    # 发布时间
    formatCreateTime = Column(String(length=20), nullable=True)
    # 工资
    salary = Column(String(length=20), nullable=False)
    # 岗位性质
    jobNature = Column(String(length=20), nullable=True)
    # 岗位标签
    positionAdvantage = Column(String(length=200), nullable=True)
    # 学历
    education = Column(String(length=20), nullable=False)
    # 工作年限
    workYear = Column(String(length=50), nullable=False)
    # ** ** ** -------公司信息 - ------ ** ** **
    # 公司简称
    companyShortName = Column(String(length=50), nullable=True)
    # 公司全称
    companyFullName = Column(String(length=200), nullable=True)
    # 公司类型
    financeStage = Column(String(length=30), nullable=True)
    # 业务方向
    industryField = Column(String(length=30), nullable=True)
    # 公司规模
    companySize = Column(String(length=30), nullable=True)
    # 公司福利标签
    companyLabelList = Column(String(length=200), nullable=True)
    # 公司所在城市
    city = Column(String(length=10), nullable=True)
    # 公司所在区
    district = Column(String(length=20), nullable=True)
    # 地铁
    subwayline = Column(String(length=20),nullable=True)
    # 地点
    stationname = Column(String(length=50),nullable=True)
    # 经度
    longitude = Column(Float, nullable=False)
    # 纬度
    latitude = Column(Float, nullable=False)
    # ** ** ** -------爬取信息 - ------ ** ** **
    # 抓取日期
    crawl_date = Column(String(length=20), nullable=False)

    # 爬取的职位类别（python/java？）
    thirdType = Column(String(length=10), nullable=False)


if __name__ == '__main__':
    # 创建数据表
    LaGouTables.metadata.create_all(engin)

