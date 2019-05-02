#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# @Author   :triangle
# @Time     :2019/4/30 14:04
# @Filename :utils.py


import asyncio

import aiohttp

from settings import HEADERS, REQUEST_TIMEOUT, REQUEST_DELAY


LOOP = asyncio.get_event_loop()


async def _get_page(url, sleep):
    """
    获取并返回网页内容
    """
    async with aiohttp.ClientSession() as session:
        try:
            await asyncio.sleep(sleep)
            async with session.get(
                url, headers=HEADERS, timeout=REQUEST_TIMEOUT
            ) as resp:
                return await resp.text()
        except:
            return ""

async def _get_other_page(url, sleep):
    """
    站大爷代理专用，防止跳转
    """
    async with aiohttp.ClientSession() as session:
        try:
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Host': 'ip.zdaye.com',
                'Referer': 'http://ip.zdaye.com/dayProxy.html',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
            }
            await asyncio.sleep(sleep)
            async with session.get(
                url, headers=headers, timeout=REQUEST_TIMEOUT
            ) as resp:
                return await resp.text()
        except:
            return ""


def requests(url, sleep=REQUEST_DELAY):
    """
    请求方法，用于获取网页内容

    :param url: 请求链接
    :param sleep: 延迟时间（秒）
    """
    html = LOOP.run_until_complete(asyncio.gather(_get_page(url, sleep)))
    if html:
        return "".join(html)


def requests_other(url, sleep=REQUEST_DELAY):
    """
    请求方法，用于获取网页内容

    :param url: 请求链接
    :param sleep: 延迟时间（秒）
    """
    html = LOOP.run_until_complete(asyncio.gather(_get_other_page(url, sleep)))
    if html:
        return "".join(html)
