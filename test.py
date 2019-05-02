#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# @Author   :triangle
# @Time     :2019/4/30 16:49
# @Filename :test.py
import requests
import pyquery
import re

headers = {
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }

url = "http://www.swei360.com/free/?stype={}"

items = [p for p in range(1, 5)]
for proxy_type in items:
    response = requests.get(url.format(proxy_type))
    html = response.text
    if html:
        doc = pyquery.PyQuery(html)
        for item in doc(".table-bordered tr").items():
            ip = item("td:nth-child(1)").text()
            port = item("td:nth-child(2)").text()
            schema = item("td:nth-child(4)").text()
            if ip and port and schema:
                print(schema.lower(), ip, port)