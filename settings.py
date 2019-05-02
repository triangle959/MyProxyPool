#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# @Author   :triangle
# @Time     :2019/4/29 21:49
# @Filename :settings.py

# 请求超时时间（秒）
REQUEST_TIMEOUT = 15
# 请求延迟时间（秒）
REQUEST_DELAY = 0

# redis 地址
REDIS_HOST = "localhost"
# redis 端口
REDIS_PORT = 6379
# redis 密码
REDIS_PASSWORD = None
# redis set key
REDIS_KEY = "myproxies"
# redis 连接池最大连接量
REDIS_MAX_CONNECTION = 20
# REDIS SCORE 最大分数
MAX_SCORE = 10
# REDIS SCORE 最小分数
MIN_SCORE = 0
# REDIS SCORE 初始分数
INIT_SCORE = 5


# server web host
SERVER_HOST = "localhost"
# server web port
SERVER_PORT = 3289
# 是否开启日志记录
SERVER_ACCESS_LOG = True

#验证ip检查时间（分）
VALIDATOR_RUN_CYCLE = 15
#验证url
VALIDATOR_BASE_URL = "http://baidu.com"
#批量测试数量
VALIDATOR_BATCH_COUNT = 250

#爬取ip检查时间（分）
CRAWLER_RUN_CYCLE = 30
HEADERS = {
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}