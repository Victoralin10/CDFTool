#!/usr/bin/env python3

import requests
import argparse
import math
import json
import os
from bs4 import BeautifulSoup

import config


session = requests.Session()
session.headers.clear()


def get_tta(cookie):
    ans = 0
    for i in range(0, len(cookie)):
        ans = (ans + (i+1)*(i+2)*ord(cookie[i]))%1009
        if i%3 == 0:
            ans += 1
        if i%2 == 0:
            ans *= 2
        if i > 0:
            ans -= (ord(cookie[i//2])//2)*(ans%5)
        while ans < 0:
            ans += 1009
        while ans >= 1009:
            ans -= 1009
    return ans


def get_login_data():
    if not os.path.exists(config.SESSION_PATH_LOGIN_DATA):
        raise "login_data file not configured"

    with open(config.SESSION_PATH_LOGIN_DATA) as f:
        return json.loads(f.read())


def login():
    html = BeautifulSoup(session.get(config.URL_LOGIN).text, 'html.parser')
    form = html.find('form', {'id': 'enterForm'})

    form = html.find('form', {'id': 'linkEnterForm'})
    token = form.find('input', {'name': 'csrf_token'})['value']

    login_data = get_login_data()
    data = {
        'csrf_token': token,
        'action': 'enter',
        'handle': login_data['username'],
        'password': login_data['password'],
        'remember': 'on',
        '_tta': get_tta(session.cookies.get('39ce7'))
    }

    session.post(config.URL_LOGIN, data=data).text

    with open(config.SESSION_PATH_FILE, "w") as f:
        f.write(json.dumps(dict(session.cookies)))


if __name__ == "__main__":
    login()
