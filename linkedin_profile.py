import json
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

client = requests.Session()

HOMEPAGE_URL = 'https://www.linkedin.com'
LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'

html = client.get(HOMEPAGE_URL).content
soup = BeautifulSoup(html, 'lxml')
csrf = soup.find(id="loginCsrfParam-login")['value']

login_information = {
    'session_key': sys.argv[1],"" #enter your email id here
    'session_password': sys.argv[2],"" #enter your password here
    'loginCsrfParam': csrf,
}

client.post(LOGIN_URL, data=login_information)
time.sleep(10)
cookie = client.cookies.get_dict()
print (cookie)
bcookie = cookie.get('bcookie')
bscookie = cookie.get('bscookie')
lidc = cookie.get('lidc')
visit = cookie.get('visit')
leo_auth = cookie.get('leo_auth_token')
lang = cookie.get('lang')
JSESSIONID = cookie.get('JSESSIONID')
li_at=cookie.get('li_at')
liap=cookie.get('liap')
sl=cookie.get('sl')
JSESSIONID = JSESSIONID[1:-1]

headers = {
    'accept-encoding': 'gzip, deflate, sdch, br',
    'x-li-lang': 'en_US',
    'accept-language': 'en-IN,en-GB;q=0.8,en-US;q=0.6,en;q=0.4',
    'x-requested-with': 'XMLHttpRequest',
    'cookie': 'bcookie=' + bcookie + '; bscookie=' + bscookie + '; _ga=GA1.2.2031948949.1505287936; join_wall=v=3&AQHD97456159aAAAAWDPGQ3M3Aq3_rLnrrKVlLylSXdBQfIey_uaWr_eJdf_Iv3pXIXRasL3MnYYxBNzU4JT110ze90bP7cnpwR2RT-gyw3TzY4m8lDwwg8zN7b_1IA8E_4opY5OI_WHYkujFFxolT9dpJ7FqB53bo9v49gNLxjVqdLyfzxwr1_uPLQrjIPZLt2-l8DYqxIjiTltSKo5dBlsiYDR5g; visit=' + visit + '; JSESSIONID="' + JSESSIONID + '"; lang=' + lang + '; leo_auth_token=' + leo_auth + '; sl=' + sl + '; li_at=' + li_at + '; liap=' + liap + '; _gat=1; _lipt=CwEAAAFg0JRRaEURBUySp_H7rUHhlKUvxHByf26SW8DjXFfJLqDfaJ2Ur45U2McgAnKXEkrZ3p7HcB7nIM48TDnstalQUSxh8KVxod9RCLP2cm1uHtJDyEPpa9nFqNOMnq44ccWIRfdGpMqOp9L8cvZf-PYMQLpUpMGqtDlVx1sm; lidc=' + lidc,
    'x-restli-protocol-version': '2.0.0',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'x-li-page-instance': 'urn:li:page:d_flagship3_profile_view_base;XE3O9JZkRMid61xrZtseTg==',
    'accept': 'application/vnd.linkedin.normalized+json',
    'csrf-token': JSESSIONID,
    'x-li-track': '{"clientVersion":"1.1.5418","osName":"web","timezoneOffset":5.5,"deviceFormFactor":"DESKTOP","mpName":"voyager-web"}',
    'authority': 'www.linkedin.com',
    'referer': 'https://www.linkedin.com/feed/',
}
print ('login done')


f = open(r"C:\Users\Ayra.Rosella\Desktop\LI4.txt")

list_profile_info = []
lines = f.readlines()

for line in lines:
    profile = line.split('/')[-1].strip()
    done_profiles = [p['profile'] for p in list_profile_info]
    if profile in done_profiles:
        continue
    response = requests.get('https://www.linkedin.com/voyager/api/identity/profiles/{}/profileView'.format(profile), headers=headers)
    if response.status_code != 200:
        print('got invalid response for {}'.format(profile))
        continue
    res = json.loads(response.text)
    res = res['included']
    info = {}
    info['profile'] = profile
    info['profile_url'] = line
    for r in res:
        if 'firstName' in r:
            info['first_name'] = r['firstName']
        if 'lastName' in r:
            info['last_name'] = r['lastName']
        if 'occupation' in r:
            info['occupation'] = r['occupation']
        if 'locationName' in r:
            info['location'] = r['locationName']
        if 'companyName' in r:
            info['company_name'] = r['companyName']
        if 'title' in r:
            info['title'] = r['title']
    list_profile_info.append(info)
    print('got {}'.format(profile))
    time.sleep(2)

df = pd.DataFrame(list_profile_info)
f.close()
df.to_csv(r"C:\Users\Ayra.Rosella\Desktop\LI_LIVE\LITEST.xlsx")