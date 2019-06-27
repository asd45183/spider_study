#!/usr/bin/env python
# 路径 settings/editer/file and code
# -*- coding: utf-8 -*-
# @Time    : 2019/6/27 下午8:46
# @Author  : Mr_d
# @Site    : 
# @File    : handle_craw_lagou.py
#        ┏┓　　　┏┓+ +
# 　　　┏┛┻━━━┛┻┓ + +
# 　　　┃　　　　　　　┃ 　
# 　　　┃　　　━　　　┃ ++ + + +
# 　　 ████━████ ┃+
# 　　　┃　　　　　　　┃ +
# 　　　┃　　　┻　　　┃
# 　　　┃　　　　　　　┃ + +
# 　　　┗━┓　　　┏━┛
# 　　　　　┃　　　┃　　　　　　　　　　　
# 　　　　　┃　　　┃ + + + +
# 　　　　　┃　　　┃　　　　Codes are far away from bugs with the animal protecting　　　
# 　　　　　┃　　　┃ + 　　　　神兽保佑,代码无bug　　
# 　　　　　┃　　　┃
# 　　　　　┃　　　┃　　+　　　　　　　　　
# 　　　　　┃　 　　┗━━━┓ + +
# 　　　　　┃ 　　　　　　　┣┓
# 　　　　　┃ 　　　　　　　┏┛
# 　　　　　┗┓┓┏━┳┓┏┛ + + + +
# 　　　　　　┃┫┫　┃┫┫
# 　　　　　　┗┻┛　┗┻┛+ + + +
import requests
import json
import re


class HandleLaGou(object):

    def __init__(self):
        # 使用session 保存cookies信息
        self.lagou_session = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
        self.city_list = ""

    # 获取全国所有城市列表
    def handle_city(self):

        # 正则匹配
        city_search = re.compile(r'zhaopin/">(.*)</a>')

        # 定义url
        city_url = "https://www.lagou.com/jobs/allCity.html"
        city_result = self.handle_request(method="GET", url=city_url)

        # 使用正则表达式获取城市列表
        self.city_list = city_search.findall(city_result)

        # 手动清理cookis
        self.lagou_session.cookies.clear()

    def handle_city_job(self, city):

        first_request = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&kabekwords=&suginput=" % city
        first_response = self.handle_request(method="GET", url=first_request)
        total_page_search = re.compile(r'class="span\stotalNum">(\d+)</span>')
        print(first_response)

    def handle_request(self, method, url, data=None, info=None):

        if method == "GET":
            response = self.lagou_session.get(url=url, headers=self.headers)
            response.encoding = 'utf8'

        elif method == "POST":
            response = self.lagou_session.get(url=url, data=data, headers=self.headers)
            response.encoding = 'utf8'

        return response.text


if __name__ == '__main__':
    lagou = HandleLaGou()

    # 获取所有城市
    lagou.handle_city()
    for city in lagou.city_list:
        lagou.handle_city_job(city)
