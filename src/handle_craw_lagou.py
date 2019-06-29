#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/27 下午8:46
# @Author  : Mr_d
# @Site    : 
# @File    : handle_craw_lagou.py
import json
# 引入多进程
import multiprocessing
import re
import time

import requests

from src.logconfig import Logger

log = Logger()


class HandleLaGou(object):

    def __init__(self):
        # 使用session 保存cookies信息
        self.lagou_session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }
        self.city_list = ""

    # 获取全国所有城市列表
    def handle_city(self):
        # 正则匹配
        # city_search = re.compile(r'zhaopin/">(.*)</a>')
        city_search = re.compile(r'.?com\/.+\/.?">(.+)</a>')
        # 定义url
        city_url = "https://www.lagou.com/jobs/allCity.html"
        city_result = self.handle_request(method="GET", url=city_url)
        # 使用正则表达式获取城市列表
        self.city_list = city_search.findall(city_result)
        # 手动清理cookis
        self.lagou_session.cookies.clear()

    # 获取当前城市的工作列表
    def handle_city_job(self, city):
        first_request = \
            "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput=" % city
        first_response = self.handle_request(method="GET", url=first_request)
        try:
            total_page_search = re.compile(r'class="span\stotalNum">(\d+)</span>')
            total_page = total_page_search.search(first_response).group(1)
        # 没有岗位信息抛出的异常
        except:
            return
        else:
            # 返回页码
            for i in range(1, int(total_page) + 1):
                # 构造数据
                data = {
                    'pn': i,
                    'kd': 'python'
                }
                page_url = "https://www.lagou.com/jobs/positionAjax.json?city=%s&needAddtionalResult=false" % city
                referer_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=" \
                              "true&labelWords=&suginput=" % city
                # referer 需要encode
                self.headers['Referer'] = referer_url.encode()
                # 传入city
                response = self.handle_request("POST", url=page_url, data=data, info=city)
                json_data = json.loads(response)
                job_list = json_data["content"]["positionResult"]["result"]
                for job in job_list:
                    print(job)

    # 构造公共请求方法
    def handle_request(self, method, url, data=None, info=None):
        while True:
            # 加入阿布云代理（..视频作者有，我没有..）
            proxyinfo = "http://%s:%s@%s:%s" % ('username', 'password', 'ip', 'port')
            proxy = {
                "http": proxyinfo,
                "https": proxyinfo
            }
            try:
                if method == "GET":
                    # response = self.lagou_session.get(url=url, headers=self.headers, proxies=proxy, timeout=6)
                    response = self.lagou_session.get(url=url, headers=self.headers, timeout=6)
                elif method == "POST":
                    # 加入代理用
                    """
                    response = self.lagou_session.post(url=url, data=data,
                     headers=self.headers, proxies=proxy, timeout=6)
                    """
                    response = self.lagou_session.post(url=url, data=data, headers=self.headers, timeout=6)
            except:
                # 先清除cookis
                self.lagou_session.cookies.clear()
                # 传入info 中的city
                first_request = "https://www.lagou.com/jobs/list_python?" \
                                "city=%s&cl=false&fromSearch=true&labelWords=&suginput=" % info
                # 重新获取cookis
                first_response = self.handle_request(method="GET", url=first_request)
                # 休息10S 模拟人为操作
                time.sleep(10)
                continue
            response.encoding = 'utf-8'
            if "频繁" in response.text:
                print("频繁")
                # 先清除cookis
                self.lagou_session.cookies.clear()
                # 传入info 中的city
                first_request = "https://www.lagou.com/jobs/list_python?" \
                                "city=%s&cl=false&fromSearch=true&labelWords=&suginput=" % info
                # 重新获取cookis
                first_response = self.handle_request(method="GET", url=first_request)
                # 休息10S 模拟人为操作
                time.sleep(10)
                continue
            return response.text


if __name__ == '__main__':
    lagou = HandleLaGou()
    lagou.handle_city()
    # 实例化进程池 进程数2
    pool = multiprocessing.Pool(2)
    for city in lagou.city_list:
        pool.apply_async(lagou.handle_city_job, args=(city,))
    # 关闭进程池
    pool.close()
    pool.join()
