# coding: utf8

import requests
import base64
import xmltodict
import time
import json
import sys
import os

s = requests.Session()

def writetofile(data):
    try:
        file_path = sys.argv[1]
    except Exception,e:
        return False,e

    if not os.path.exists(file_path):
        return False,"{} not exist.".format(file_path)

    file_name = '{}{}.log'.format(file_path, data['nbiot_create_time'])
    with open(file_name, 'w') as f:
        json.dump(data, f)

    return True,file_name

def process(host, username, password):
    # session start
    auth_base64 = base64.b64encode('{}:{}'.format(username, password))
    auth_session_url = 'http://{}/xmlapi/session/begin'.format(host)
    headers = {
        "Authorization": "Basic {}".format(auth_base64)
    }
    # request sesion.
    r = s.post(auth_session_url, headers=headers, allow_redirects=True, verify=False)
    if r.status_code != 204:
        return False, ''
    # request status xml
    r = s.get('http://{}/status.xml'.format(host), verify=False)
    if r.status_code != 200:
        return False, 'get status error'

    try:
        # xml string to python dict
        data = json.dumps(xmltodict.parse(r.text))
        data = json.loads(data)['Status']
        dcts = int(time.time())
        data['nbiot_create_time'] = dcts
        data['nbiot_kind'] = "视频会议终端"
        data['nbiot_company'] = "cisco"
        data['nbiot_type'] = "dx80"
        _, errinfo = writetofile(data)
        print errinfo

    finally:
        # end session
        close_session_url = 'http://{}/xmlapi/session/end'.format(host)
        r = s.post(close_session_url, headers=headers, verify=False)
        print r.status_code


if __name__ == '__main__':
    configure = [
        {'username': 'admin', 'password': '11111111', 'host': '172.17.17.9'},
    ]

    for i in configure:
        process(i['host'], i['username'], i['password'])