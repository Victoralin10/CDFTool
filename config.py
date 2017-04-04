#!/usr/bin/env python3

import json
import os
import sys


URL = "http://codeforces.com"

# LOGIN
URL_LOGIN = URL + "/enter"
SESSION_PATH_LOGIN_DATA = "login_data.json"
SESSION_PATH_FILE = "session.json"

# TESTING
URL_PROBLEM = URL + "/contest/{contest}/problem/{letter}"
URL_PROBLEMS = URL + "/contest/{contest}"
PATH_TEST_FILE = "{contest}.json"

URL_SUBMISIONS = URL + "/contest/{contest}/my"

# CONFIG
PATH_CONFIG = 'config.json'

# SUBMIT
URL_SUBMIT_FORM = URL + "/contest/{contest}/submit"


def get_config():
    if not os.path.exists(PATH_CONFIG):
        print('Config file does not exist.')
    with open(PATH_CONFIG) as f:
        return json.loads(f.read())


def main():
    contest = int(input('Enter Contest Number: '))
    conf = {
        'contest': contest
    }

    with open(PATH_CONFIG, 'w') as f:
        f.write(json.dumps(conf, ensure_ascii=False))


if __name__ == "__main__":
    main()
