#!/usr/bin/env python3

import json
import config
import requests
import config
import login
from bs4 import BeautifulSoup


def main(contest):
    session = requests.Session()
    session.headers.clear()
    session.cookies.update(login.get_session())

    html = BeautifulSoup(session.get(config.URL_SUBMISIONS.format(contest=contest)).text, 'html.parser')
    for table in html.find_all('table', class_='status-frame-datatable'):
        for tr in table.find_all('tr'):
            if tr.get('data-submission-id', None):
                sub_id = tr['data-submission-id']

                tds = tr.find_all('td')
                sub_date = tds[1].text.strip()
                sub_problem = tds[3].text.strip()
                sub_lang = tds[4].text.strip()
                sub_veredict = tds[5].text.strip()
                sub_time = tds[6].text.strip()
                sub_memory = tds[7].text.strip()
                a = "{:8}|{:19}|{:50}|{:10}|{:30}|{:6}|{:8}".format(sub_id, sub_date, sub_problem, sub_lang, sub_veredict, sub_time, sub_memory)
                print(a)


if __name__ == "__main__":
    conf = config.get_config()

    main(conf['contest'])
