#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

class Shuyi:
    def __init__(self):
        self.url = 'https://scrm-prod.shuyi.org.cn/saas-gateway/api/agg-trade/v1/signIn/insertSignInV2' # 书亦签到url

    def post(self):
        with open('headers.json') as headers: # 读取headers
            headers = json.load(headers)
        response = requests.get(self.url, headers = headers) # 请求签到
        return response

if __name__ == '__main__':
    sy = Shuyi()
    print(sy.post().text) # 打印签到结果


