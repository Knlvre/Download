import requests
import urllib3
import time
import sys
import os
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "Connection":"close",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Sec-Fetch-Site": "same-origin",
    "Referer": "https://dns.aizhan.com/",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "_csrf=938dc864deae8c2955c6ef0de7c6d296061de204633d782e219644443cc6b513a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22Dy-kdF9NOyJpwnn-jefIbnP8JchiuwId%22%3B%7D; Hm_lvt_b37205f3f69d03924c5447d020c09192=1581833140; allSites=www.zjrarj.com%2C0; Hm_lpvt_b37205f3f69d03924c5447d020c09192=1581841964"
}
ex_str = '暂无域名解析到该IP'
fil_href_list = []
href_list = []
file_name = sys.argv[1]
tar_file = open(file_name,'r')
file_lines = tar_file.readlines()
try:
    os.mkdir('./output')
except:
    pass

for target in file_lines:
    tar = target.strip()
    ori_url = "https://dns.aizhan.com/" + tar + "/"
    url_num = 1
    cou = 0
    res = requests.get(url=ori_url + str(url_num) + '/',headers=headers,verify=False)
    bs = BeautifulSoup(res.text,'lxml')

    if ex_str in str(bs):
        print(tar + '：' + ex_str)
    else:
        while ex_str not in str(bs):
            for item in bs.find_all('a'):
                if 'nofollow' in str(item) and 'ICP' not in str(item):
                    href_list.append(str(item.get('href')))
                    cou +=1

            #收集完当前界面，跳转下一页继续收集
            url_num += 1
            url = ori_url + str(url_num) + '/'
            res = requests.get(url=url, headers=headers, verify=False)
            bs = BeautifulSoup(res.text, 'lxml')
            time.sleep(1)

        res_file_name = '[' + str(cou) + '] ' + tar + '.txt'
        res_file = open('./output/' + res_file_name,'w')

        for res in href_list:
            res_file.write(res + '\n')
        res_file.close()

        print('[+] ' + tar + '：' + '收集到' + str(cou) + '条记录')