#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# @Author   :triangle
# @Time     :2019/4/30 16:02
# @Filename :run.py

from flask import Flask, jsonify
from db import RedisClient
from scheduler import run_schedule
from settings import SERVER_HOST, SERVER_PORT, SERVER_ACCESS_LOG

myapp = Flask(__name__)
redis_conn = RedisClient()


@myapp.route("/")
def index():
    return jsonify({"Welcome": "This is a proxy pool system."},
                   {"if there has problem": "Please communicate with QQ:976264593"})


@myapp.route("/pop")
def pop_proxy():
    proxy = redis_conn.pop_proxy().decode("utf8")
    if proxy[:5] == "https":
        return jsonify({"https": proxy})
    else:
        return jsonify({"http": proxy})


@myapp.route("/get/<int:count>")
def get_proxy(count):
    res = []
    for proxy in redis_conn.get_proxies(count):
        if proxy[:5] == "https":
            res.append({"https": proxy})
        else:
            res.append({"http": proxy})
    return jsonify(res)


@myapp.route("/count")
def count_all_proxies():
    count = redis_conn.count_all_proxies()
    return jsonify({"count": str(count)})


@myapp.route("/count/<int:score>")
def count_score_proxies(score):
    count = redis_conn.count_score_proxies(score)
    return jsonify({"count": str(count)})


@myapp.route("/clear/<int:score>")
def clear_proxies(score):
    if redis_conn.clear_proxies(score):
        return jsonify({"Clear": "Successful"})
    return jsonify({"Clear": "Score should >= 0 and <= 10"})

if __name__ == "__main__":
    run_schedule()
    # 启动服务端 Flask app
    myapp.run(host=SERVER_HOST, port=SERVER_PORT, debug=SERVER_ACCESS_LOG)