#!/usr/bin/env python3

import json
import config
import login
import sys
import requests
from bs4 import BeautifulSoup


def extract_contest_letter(filename):
    nm, lt = "", ""
    for c in filename:
        if c == '.':
            break
        if c in "0123456789":
            nm += c
        else:
            lt += c
    
    return nm, lt


def submit(filename):
    session = requests.Session()
    session.headers.clear()
    session.cookies.update(login.get_session())

    contest, letter = extract_contest_letter(filename)
    html = BeautifulSoup(session.get(config.URL_SUBMIT_FORM.format(contest=contest)).text, 'html.parser')
    token = html.find('input', {'name': 'csrf_token'})['value']

    f = open(filename)
    data = {
        'csrf_token': token,
        'action': 'submitSolutionFormSubmitted',
        'submittedProblemIndex': letter,
        'programTypeId': 1,
        'source': f.read(),
        'tabSize': 4,
        'sourceFile': '',
        '_tta': login.get_tta(session.cookies.get('39ce7'))
    }
    f.close()

    # print(json.dumps(data, indent=2, ensure_ascii=False))
    res = session.post(config.URL_SUBMIT_FORM.format(contest=contest), data=data, params={'csrf_token': token})
    print(res.status_code)
    print(res.text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No file especified.')
    
    
    for filename in sys.argv[1:]:
        submit(filename)

