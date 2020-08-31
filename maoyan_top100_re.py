#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/27 19:49
# @Author  : 一叶知秋
# @File    : maoyan_top100_re.py
# @Software: PyCharm
import json
import re
import time
import random
import requests
from requests.exceptions import RequestException


def get_one_page(url):
    """获取一页内容"""
    try:
        headers = {'User-Agent': 'BaiduSpider'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    """
    通过正则解析一页内容，
    提取出电影的排名、图片、标题、演员、时间、评分等内容
    """
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {'index': item[0],
               'image': item[1].split('@')[0],
               'title': item[2].lstrip().strip(),
               'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
               'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
               'score': item[5].strip() + item[6].strip()}


def write_to_file(content):
    """写入文件"""
    with open('result_re.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def run(offset):
    """执行函数"""
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


def main():
    """主函数"""
    # 获取Top100电影排名
    # 每页的偏移量为10
    for i in range(10):
        run(i * 10)
        delay = random.randint(1, 3)
        time.sleep(delay)


if __name__ == '__main__':
    main()
