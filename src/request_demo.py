#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/30 10:02
# @Author  : Mr_d
# @Site    : 
# @File    : request_demo.py
import requests
import re
import os

class RequestDemo(object):

    def __init__(self):
        # 使用session 保存cookies信息
        self.request_session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }
        self.jpg_list = ""
        self.base_url = "http://pic.netbian.com/"
        self.image_url = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    def request_all_jpg(self):
        # 正则匹配
        jpg_url = re.compile(r'title="(.*?)"\starget=".*?(\/uploads\/allimg/.*?\/.*?\.jpg)')
        response = self.common_request("GET", url=self.base_url)
        self.jpg_list = jpg_url.findall(response)
        for name,jpg in self.jpg_list:
            jpg_url = self.real_jpg_url(jpg)
            name = str(name).split()
            name = ''.join(name)
            self.dowload_jpg(name=name, jpg_url=jpg_url)

    def dowload_jpg(self, jpg_url, name):
        base_url = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

        response = requests.get(url=jpg_url, stream=True, headers=self.headers)
        file_name = base_url + "/files/jpg/" + name + ".jpg"
        with open(file_name, 'wb') as fd:
            for chunk in response.iter_content(128):
                fd.write(chunk)

    def common_request(self, method, url, data=None):
        if method == "GET":
            response = self.request_session.get(url=url, headers=self.headers, timeout=6)
        elif method == "POST":
            response = self.request_session.post(url=url, data=data, headers=self.headers, timeout=6)
        response.encoding = 'gbk'
        return response.text

    def real_jpg_url(self, jpg):
        return "".join([self.base_url, jpg])


if __name__ == '__main__':
    jpg = RequestDemo()
    jpg.request_all_jpg()
    # print(jpg.jpg_list)
