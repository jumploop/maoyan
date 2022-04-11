#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/29 20:38
# @Author  : 一叶知秋
# @File    : maoyan_top100_lxml.py
# @Software: PyCharm

import json
from bs4 import BeautifulSoup
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
    通过BeautifulSoup解析一页内容，
    提取出电影的排名、图片、标题、演员、时间、评分等内容
    """
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('dd')
    print(len(items))
    for item in items:
        index = item.i.get_text()
        image = item.a.find('img', class_="board-img")['data-src']
        title = item.a['title']
        actor = item.find('p', class_="star").get_text(strip=True)
        time = item.find('p', class_="releasetime").get_text(strip=True)
        score = item.find('p', class_="score").get_text(strip=True)
        yield {'index': index,
               'image': image.split('@')[0],
               'title': title,
               'actor': actor,
               'time': time,
               'score': score}


def write_to_file(content):
    """写入文件"""
    with open('result_bs4.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def run(offset):
    """执行函数"""
    url = f'http://maoyan.com/board/4?offset={str(offset)}'
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
