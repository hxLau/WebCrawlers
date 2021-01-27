import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import time
import json


def getTime():
    return int(round(time.time() * 1000))


def get_date_list():
    # 获取时间列表
    url = 'https://data.stats.gov.cn/tablequery.htm?code=AA020C'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    key = {}  # 参数键值对
    key['m'] = 'OtherWds'
    key['code'] = 'AA020C'
    key['_'] = str(getTime())
    r_date = requests.get(url, headers=headers, params=key, verify=False)
    date_json = json.loads(r_date.text)

    date_list = [i['code'] for i in date_json[1]['nodes']]
    return date_list

def get_data_by_date(date):
    url = 'https://data.stats.gov.cn/tablequery.htm?code=AA020C'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    key={}#参数键值对
    key['m']='QueryData'
    key['code']='AA020C'
    key['wds']='[{"wdcode":"reg","valuecode":"000000"},{"wdcode":"sj","valuecode":"'+ date +'"}]'

    r=requests.get(url,headers=headers,params=key,verify=False)
    js=json.loads(r.text)
    return js


def main(csv_dir="./data/task1/result.csv"):
    date_list = get_date_list()
    dic_by_date = {}
    variable_name_list = []
    for date in date_list:
        data_js = get_data_by_date(date)
        # 除去列名
        table_values = data_js['exceltable'][6:]
        # 计算指标数量
        variable_len = int(len(table_values) / 5)
        value_list = []
        if len(variable_name_list) == 0:
            for i in range(variable_len):
                variable_name_list.append(table_values[i * 5]['data'])
                value_list.append(table_values[i * 5 + 3]['data'])
        else:
            for i in range(variable_len):
                value_list.append(table_values[i * 5 + 3]['data'])

        dic_by_date[date] = value_list

        # 除去指标左边空格
        for i in range(len(variable_name_list)):
            variable_name_list[i] = variable_name_list[i].lstrip()

        dataf = {'指标': variable_name_list}
        for key, value in dic_by_date.items():
            dataf[key] = value
    data_frame = pd.DataFrame(data=dataf)
    data_frame.to_csv(csv_dir, index=False, encoding="GBK")


if __name__ == '__main__':
    date = time.strftime("%Y-%m-%d", time.localtime())
    csv_dir = "./data/工业主要产品产量及增长速度" + date + ".csv"
    main(csv_dir)