#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# @Author   :triangle
# @Time     :2019/4/29 21:45
# @Filename :crawler.py

import re

import pyquery

from utils import requests, requests_other
from db import RedisClient
from logger import logger


redis_conn = RedisClient()
all_funcs = []


def collect_funcs(func):
    """
    装饰器，用于收集爬虫函数
    """
    all_funcs.append(func)
    return func


class Crawler:
    """
        返回格式： http://host:port
    """
    @staticmethod
    def run():
        """
        启动收集器
        """
        logger.info("Crawler working...")
        for func in all_funcs:
            for proxy in func():
                redis_conn.add_proxy(proxy)
                logger.info("Crawler √ {}".format(proxy))
        logger.info("Crawler resting...")

    @staticmethod
    @collect_funcs
    def crawl_xici():
        """
        西刺代理：http://www.xicidaili.com
        """
        url = "http://www.xicidaili.com/{}"

        items = []
        for page in range(1, 21):
            items.append(("wt/{}".format(page), "http://{}:{}"))
            items.append(("wn/{}".format(page), "https://{}:{}"))

        for item in items:
            proxy_type, host = item
            html = requests(url.format(proxy_type))
            if html:
                doc = pyquery.PyQuery(html)
                for proxy in doc("table tr").items():
                    ip = proxy("td:nth-child(2)").text()
                    port = proxy("td:nth-child(3)").text()
                    if ip and port:
                        yield host.format(ip, port)

    @staticmethod
    @collect_funcs
    def crawl_zhandaye():
        """
        站大爷代理：http://ip.zdaye.com/dayProxy.html
        """
        url = 'http://ip.zdaye.com/dayProxy.html'
        html = requests(url)
        sttrs = re.findall('<H3 class="title"><a href="(.*?)">', html, re.S)
        for sttr in sttrs:
            new_url = url[:28] + sttr[9:]
            new_html = requests_other(new_url)
            get_div = re.search("<div class=\"cont\">(.*?)</div>", new_html, re.S).group(1)
            print(get_div)
            results = re.findall("<br>(.*?)@(.*?)#\[(.*?)\]", get_div, re.S)
            for result in results:
                yield "{}://{}".format(result[1].lower(), result[0])

    @staticmethod
    @collect_funcs
    def crawl_66ip():
        """
        66ip 代理：http://www.66ip.cn
        19-04-30可用
        """
        url = (
            "http://www.66ip.cn/nmtq.php?getnum=100&isp=0"
            "&anonymoustype=0&area=0&proxytype={}&api=66ip"
        )
        pattern = "\d+\.\d+.\d+\.\d+:\d+"

        items = [(0, "http://{}"), (1, "https://{}")]
        for item in items:
            proxy_type, host = item
            html = requests(url.format(proxy_type))
            if html:
                for proxy in re.findall(pattern, html):
                    yield host.format(proxy)


    @staticmethod
    @collect_funcs
    def crawl_kuaidaili():
        """
        快代理：https://www.kuaidaili.com
        每次30个
        19-04-13可用
        """
        url = "https://www.kuaidaili.com/free/inha/{}/"

        items = [p for p in range(1, 3)]
        for page in items:
            html = requests(url.format(page))
            if html:
                doc = pyquery.PyQuery(html)
                for proxy in doc(".table-bordered tr").items():
                    ip = proxy("[data-title=IP]").text()
                    port = proxy("[data-title=PORT]").text()
                    if ip and port:
                        yield "http://{}:{}".format(ip, port)

    @staticmethod
    @collect_funcs
    def crawl_ip3366():
        """
        云代理：http://www.ip3366.net
        每页10个，验证较快
        19-04-30可用
        """
        url = "http://www.ip3366.net/?stype=1&page={}"

        items = [p for p in range(1, 8)]
        for page in items:
            html = requests(url.format(page))
            if html:
                doc = pyquery.PyQuery(html)
                for proxy in doc(".table-bordered tr").items():
                    ip = proxy("td:nth-child(1)").text()
                    port = proxy("td:nth-child(2)").text()
                    schema = proxy("td:nth-child(4)").text()
                    if ip and port and schema:
                        yield "{}://{}:{}".format(schema.lower(), ip, port)

    @staticmethod
    @collect_funcs
    def crawl_data5u():
        """
        无忧代理：http://www.data5u.com/
        每次14个，验证时间比较新
        19-04-30可用
        """
        url = "http://www.data5u.com/free/index.html"

        html = requests(url)
        if html:
            doc = pyquery.PyQuery(html)
            for index, item in enumerate(doc(".wlist li .l2").items()):
                if index > 0:
                    ip = item("span:nth-child(1)").text()
                    port = item("span:nth-child(2)").text()
                    schema = item("span:nth-child(4)").text()
                    if ip and port and schema:
                        yield "{}://{}:{}".format(schema, ip, port)

    @staticmethod
    @collect_funcs
    def crawl_iphai():
        """
        ip 海代理：http://www.iphai.com
        爬取国内高匿、国外高匿、国外普通各10个
        19-04-30可用
        """
        url = "http://www.iphai.com/free/{}"

        items = ["ng", "np", "wg", "wp"]
        for proxy_type in items:
            html = requests(url.format(proxy_type))
            if html:
                doc = pyquery.PyQuery(html)
                for item in doc(".table-bordered tr").items():
                    ip = item("td:nth-child(1)").text()
                    port = item("td:nth-child(2)").text()
                    schema = item("td:nth-child(4)").text().split(",")[0]
                    if ip and port and schema:
                        yield "{}://{}:{}".format(schema.lower(), ip, port)

    @staticmethod
    @collect_funcs
    def crawl_swei360():
        """
        360 代理：http://www.swei360.com
        过期
        """
        url = "http://www.swei360.com/free/?stype={}"

        items = [p for p in range(1, 5)]
        for proxy_type in items:
            html = requests(url.format(proxy_type))
            if html:
                doc = pyquery.PyQuery(html)
                for item in doc(".table-bordered tr").items():
                    ip = item("td:nth-child(1)").text()
                    port = item("td:nth-child(2)").text()
                    schema = item("td:nth-child(4)").text()
                    if ip and port and schema:
                        yield "{}://{}:{}".format(schema.lower(), ip, port)


crawler = Crawler()