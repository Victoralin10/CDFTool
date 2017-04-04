#!/usr/bin/env python3

import json
import requests
import os
import sys
import config
from bs4 import BeautifulSoup


def get_test_cases_link(link):
    session = requests.Session()
    session.headers.clear()

    html = BeautifulSoup(session.get(link).text, "html.parser")
    io = list(html.find('div', class_="sample-test").children)

    ans = []
    for i in range(0, len(io), 2):
        ans.append({
            "input": '\n'.join(list(io[i].pre.children)[0::2]),
            "output": '\n'.join(list(io[i+1].pre.children)[0::2])
        })
    return ans


def get_test_cases(contest, letter):
    return get_test_cases_link(config.URL_PROBLEM.format(contest=contest, letter=letter))


def get_problems(contest):
    session = requests.Session()
    session.headers.clear()

    html = BeautifulSoup(session.get(config.URL_PROBLEMS.format(contest=contest)).text, 'html.parser')
    table = html.find('table', class_="problems")

    problems = []
    first = True
    for row in table.find_all('tr'):
        if first:
            first = False
            continue
        cols = row.find_all('td')
        problems.append({
            'letter': cols[0].text.strip(),
            'link': config.URL + cols[0].a['href']
        })
    
    return problems


def download(contest):
    pbs = get_problems(contest)

    ans = {}
    for pb in pbs:
        ans[pb['letter']] = get_test_cases_link(pb['link'])

    return ans


if __name__ == "__main__":
    conf = config.get_config()

    print('Downloading test of contest', conf['contest'])
    with open(config.PATH_TEST_FILE.format(contest=conf['contest']), 'w') as f:
        f.write(json.dumps(download(conf['contest']), ensure_ascii=False))
