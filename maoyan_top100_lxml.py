#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/29 20:38
# @Author  : 一叶知秋
# @File    : maoyan_top100_lxml.py
# @Software: PyCharm

import json
from lxml import etree
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
    通过lxml解析一页内容，
    提取出电影的排名、图片、标题、演员、时间、评分等内容
    """
    html = etree.HTML(html)
    items = html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd')
    print(items)
    print(len(items))
    for item in items:
        index = item.xpath('.//i[contains(@class,"board-index board-index-")]/text()')[0]
        image = item.xpath('.//a/img[@class="board-img"]/@data-src')[0]
        title = item.xpath('.//div[@class="movie-item-info"]/p/a/text()')[0]
        actor = item.xpath('.//div[@class="movie-item-info"]/p[@class="star"]/text()')[0]
        time = item.xpath('.//div[@class="movie-item-info"]/p[@class="releasetime"]/text()')[0]
        score = item.xpath('.//div[@class="movie-item-number score-num"]/p[@class="score"]/i/text()')
        yield {'index': index,
               'image': image.split('@')[0],
               'title': title.strip(),
               'actor': actor.strip(),
               'time': time,
               'score': ''.join(score)}


def write_to_file(content):
    """写入文件"""
    with open('result_lxml.txt', 'a', encoding='utf-8') as f:
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
