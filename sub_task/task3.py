import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
import json
import urllib3


def get_net_list():
    url_first = 'http://www.stats.gov.cn/was5/web/search?page='
    url_second = '&channelid=288041&was_custom_expr=like%28%E6%9C%88%E4%BB%BD%E5%85%A8%E5%9B%BD%E8%A7%84%E6%A8%A1%E4%BB%A5%E4%B8%8A%E5%B7%A5%E4%B8%9A%E4%BC%81%E4%B8%9A%E5%88%A9%E6%B6%A6%29%2Fsen&perpage=10&outlinepage=10'
    http = urllib3.PoolManager();

    rlist = []
    for i in range(1, 11):
        url = url_first + str(i) + url_second
        r = http.request('GET', url)
        r_text = r.data.decode()
        r_html = bs(r_text)z
        # 获取网站列表
        for trr in r_html.findAll('font', {'class': 'cont_tit03'}):
            net = trr.text.split("\'")[1]
            rlist.append(net)
    url_list = []
    for r in rlist:
        net_part = r.split('/')
        if len(net_part) == 7 and int(net_part[5][:4]) >= 2019 and net_part[4] == 'zxfb':
            url_list.append(r)
    return url_list


def get_csv_name(url):
    date_pre = url.split('/')[5]
    year = int(date_pre[:4])
    month = date_pre[4:]
    month = int(month)-1
    if month == 0:
        year = str(year - 1)
        month = '12'
    else:
        if month < 10:
            month = "0" + str(month)
        else:
            month = str(month)
    year = str(year)
    month = str(month)

    csv_dir = "./data/task3/全国规模以上企业利润" + year + "年1-" + month + "月份" + ".csv"
    return csv_dir, year + "年1-" + month + "月份"


def get_data(url_list):
    http = urllib3.PoolManager();
    dataf = {}
    for url_index in range(len(url_list)):
        print(url_list[url_index])
        csv_dir, date = get_csv_name(url_list[url_index])
        r = http.request('GET',url_list[url_index])
        r_text = r.data.decode()
        r_bs = bs(r_text)
        for trr in r_bs.findAll('table', {'class': 'MsoNormalTable'}):
            table = trr

        table_all = table.text.split('\u3000')
        table_item = table_all[2:]
        table_head = table_all[1]
        table_zongji = table_head.split()

        shouru_1 = []
        shouru_2 = []
        chengben_1 = []
        chengben_2 = []
        lirun_1 = []
        lirun_2 = []
        hangye = []
        hangye.append(table_zongji[-7])
        shouru_1.append(table_zongji[-6])
        shouru_2.append(table_zongji[-5])
        chengben_1.append(table_zongji[-4])
        chengben_2.append(table_zongji[-3])
        lirun_1.append(table_zongji[-2])
        lirun_2.append(table_zongji[-1])

        for i in table_item:
            e = i.split()
            hangye.append(e[0])
            shouru_1.append(e[1])
            shouru_2.append(e[2])
            chengben_1.append(e[3])
            chengben_2.append(e[4])
            lirun_1.append(e[5])
            lirun_2.append(e[6])
        if url_index == 0:
            dataf['行业'] = hangye
        dataf[date+'营业收入'] = shouru_1
        dataf[date+'营业收入同比'] = shouru_2
        dataf[date+'营业成本'] = chengben_1
        dataf[date+'营业成本同比'] = chengben_2
        dataf[date+'利润总额'] = lirun_1
        dataf[date+'利润总额同比'] = lirun_2

    data_frame = pd.DataFrame(data=dataf)
    writer = pd.ExcelWriter("./result.xlsx")
    data_frame.to_excel(writer, index=False, encoding="GBK",sheet_name='2019-04-01')
    writer.save()


def main():
    url_list = get_net_list()
    get_data(url_list)


if __name__ == '__main__':
    main()
