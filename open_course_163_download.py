#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
import sys
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool
from subprocess import call


YOU_GET_PATH = '~/.oh-my-zsh/custom/plugins/you-get/you-get'
NUM_PROCESSES = 4


def download(url):
    headers = {'User-Agent' : 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    return response.content


def parse_courses(html_content):
    soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
    courses = soup.find_all('a', href=re.compile(r'http://open\.163\.com/movie/*'))
    urls = set()
    for course in courses:
        urls.add(course['href'])
    return urls


def you_get(url):
    cmd = ' '.join([YOU_GET_PATH, url])
    call(cmd, shell=True)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise RuntimeError("Please input a 163 open course url.")

    courses = []
    for url in sys.argv[1:]:
        html_content = download(url)
        courses += list(parse_courses(html_content))

    with Pool(processes=NUM_PROCESSES) as pool:
        pool.map(you_get, courses)
