import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
import json
import urllib3
from util import getTime, is_number
from turn_color import turn_color
import warnings

# task1
def get_date_list_1():
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


def get_data_by_date_1(date):
    url = 'https://data.stats.gov.cn/tablequery.htm?code=AA020C'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    key={}#参数键值对
    key['m']='QueryData'
    key['code']='AA020C'
    key['wds']='[{"wdcode":"reg","valuecode":"000000"},{"wdcode":"sj","valuecode":"'+ date +'"}]'

    r=requests.get(url,headers=headers,params=key,verify=False)
    js=json.loads(r.text)
    return js


def get_data_task1():
    date_list = get_date_list_1()
    dic_by_date = {}
    variable_name_list = []
    for date in date_list:
        data_js = get_data_by_date_1(date)
        # 除去列名
        table_values = data_js['exceltable'][6:]
        # 计算指标数量
        variable_len = int(len(table_values) / 5)
        value_list = []
        if len(variable_name_list) == 0:
            for i in range(variable_len):
                variable_name_list.append(table_values[i * 5]['data'])

                if is_number(table_values[i * 5 + 1]['data']):
                    value_list.append(float(table_values[i * 5 + 3]['data']))
                else:
                    value_list.append(table_values[i * 5 + 3]['data'])

        else:
            for i in range(variable_len):
                if is_number(table_values[i * 5 + 1]['data']):
                    value_list.append(float(table_values[i * 5 + 3]['data']))
                else:
                    value_list.append(table_values[i * 5 + 3]['data'])
        if value_list == [' ' for j in range(variable_len)]:
            continue
        dic_by_date[date] = value_list

        # 除去指标左边空格
        for i in range(len(variable_name_list)):
            variable_name_list[i] = variable_name_list[i].lstrip()

        dataf = {'指标': variable_name_list}
        for key, value in dic_by_date.items():
            dataf[float(key)] = value
    data_frame = pd.DataFrame(data=dataf)
    return data_frame


# task 2
def get_date_list_2():
    # 获取时间列表
    url = 'https://data.stats.gov.cn/tablequery.htm?code=AA020D'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    key = {}  # 参数键值对
    key['m'] = 'OtherWds'
    key['code'] = 'AA020D'
    key['_'] = str(getTime())
    r_date = requests.get(url, headers=headers, params=key, verify=False)
    date_json = json.loads(r_date.text)

    date_list = [i['code'] for i in date_json[1]['nodes']]
    return date_list


def get_data_by_date_2(date):
    url = 'https://data.stats.gov.cn/tablequery.htm?code=AA020D'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    key={}#参数键值对
    key['m']='QueryData'
    key['code']='AA020D'
    key['wds']='[{"wdcode":"reg","valuecode":"000000"},{"wdcode":"sj","valuecode":"'+ date +'"}]'

    r=requests.get(url,headers=headers,params=key,verify=False)
    js=json.loads(r.text)
    return js


def get_data_task2():
    date_list = get_date_list_2()
    dic_by_date = {}
    variable_name_list = []
    for date in date_list:
        data_js = get_data_by_date_2(date)
        # 除去列名
        table_values = data_js['exceltable'][4:]
        # 计算指标数量
        variable_len = int(len(table_values) / 3)
        value_list = []
        if len(variable_name_list) == 0:
            for i in range(variable_len):
                variable_name_list.append(table_values[i * 3]['data'])
                if is_number(table_values[i * 3 + 1]['data']):
                    value_list.append(float(table_values[i * 3 + 1]['data']))
                else:
                    value_list.append(table_values[i * 3 + 1]['data'])
        else:
            for i in range(variable_len):
                if is_number(table_values[i * 3 + 1]['data']):
                    value_list.append(float(table_values[i * 3 + 1]['data']))
                else:
                    value_list.append(table_values[i * 3 + 1]['data'])

        if value_list == [' ' for j in range(variable_len)]:
            continue
        dic_by_date[date] = value_list

        # 除去指标左边空格
        for i in range(len(variable_name_list)):
            variable_name_list[i] = variable_name_list[i].lstrip()

        dataf = {'指标': variable_name_list}
        for key, value in dic_by_date.items():
            dataf[float(key)] = value
    data_frame = pd.DataFrame(data=dataf)
    return data_frame

# task 3
def get_net_list():
    url_first = 'http://www.stats.gov.cn/was5/web/search?page='
    url_second = '&channelid=288041&was_custom_expr=like%28%E5%85%A8%E5%9B%BD%E8%A7%84%E6%A8%A1%E4%BB%A5%E4%B8%8A%E5%B7%A5%E4%B8%9A%E4%BC%81%E4%B8%9A%29%2Fsen&perpage=10&outlinepage=10'
    http = urllib3.PoolManager();

    rlist = []
    for i in range(1, 11):
        url = url_first + str(i) + url_second
        r = http.request('GET', url)
        r_text = r.data.decode()
        r_html = bs(r_text)
        # 获取网站列表
        for trr in r_html.findAll('font', {'class': 'cont_tit03'}):
            net = trr.text.split("\'")[1]
            rlist.append(net)
    url_list = []
    for r in rlist:
        net_part = r.split('/')
        if len(net_part) == 7 and int(net_part[5][:6]) >= 201902 and net_part[4] == 'zxfb':
            url_list.append(r)
    return url_list


def get_date_by_url(url):
    date_pre = url.split('/')[5]
    year = int(date_pre[:4])
    month = date_pre[4:]
    month = int(month)-1
    if month == 0:
        year = str(year - 1)
        month = '12'
    else:
        month = str(month)
    year = str(year)
    month = str(month)

    return year + "年1-" + month + "月份"


def get_data_pre(url_list):
    http = urllib3.PoolManager()
    dataf = {}
    for url_index in range(len(url_list)):
        #print(url_list[url_index])
        r = http.request('GET',url_list[url_index])
        r_text = r.data.decode()
        r_bs = bs(r_text)
        title = r_bs.findAll('title')[0].text

        if title.find('年全国规模以上工业企业利润') == -1 and title.find('月份全国规模以上工业企业利润') == -1:
            continue

        date = title[:title.find('全')]
        if len(date)==5:
            date = date[:4] + str(12)
        else:
            item_pre = date[:9]
            item_year = item_pre[:4]
            if is_number(item_pre[-1]):
                item_month = item_pre[-2:]
            else:
                item_month = '0' + item_pre[-2]
            date = item_year + item_month
        #print(date)

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
        shouru_1.append(float(table_zongji[-6]))
        shouru_2.append(float(table_zongji[-5]))
        chengben_1.append(float(table_zongji[-4]))
        chengben_2.append(float(table_zongji[-3]))
        lirun_1.append(float(table_zongji[-2]))
        lirun_2.append(float(table_zongji[-1]))

        for i in table_item:
            e = i.split()
            hangye.append((e[0]))
            shouru_1.append(float(e[1]))
            shouru_2.append(float(e[2]))
            chengben_1.append(float(e[3]))
            chengben_2.append(float(e[4]))
            lirun_1.append(float(e[5]))
            if is_number(e[6]):
                lirun_2.append(float(e[6]))
            else:
                lirun_2.append(0.0)
        if url_index == 0:
            dataf['行业'] = hangye
        dataf[date+'营业收入'] = shouru_1
        #dataf[date+'营业收入同比'] = shouru_2
        dataf[date+'营业成本'] = chengben_1
        #dataf[date+'营业成本同比'] = chengben_2
        dataf[date+'利润总额'] = lirun_1
        #dataf[date+'利润总额同比'] = lirun_2

    data_frame = pd.DataFrame(data=dataf)
    return data_frame


def get_data(df):
    var_list_pre = df.columns[1:]

    month_number = int((df.shape[1] - 1) / 3)

    dic = {}
    var_list = []

    for i in range(month_number - 1):
        if int(float(var_list_pre[i * 3][:6])) - int(float(var_list_pre[(i + 1) * 3][:6])) == 1:
            for j in range(3):
                dic[var_list_pre[i * 3 + j]] = df[var_list_pre[i * 3 + j]].values - df[
                    var_list_pre[(i + 1) * 3 + j]].values
                var_list.append(var_list_pre[i * 3 + j])
    hangye = df['行业'].values
    df_dic = {'行业': hangye}
    # wutongbi = ['' for i in range(len(hangye))]

    for i in range(len(var_list)):
        item_name = var_list[i]
        # df_dic[item_name] = dic[item_name]
        date = int(item_name[:6])
        last_year_date = str(date - 100)
        last_year_name = last_year_date + item_name[6:]
        if last_year_name in dic.keys():
            df_dic[item_name + '同比'] =np.around((dic[item_name] / dic[last_year_name] - 1) * 100, 2)
        #else:
        #    df_dic[item_name + '同比'] = wutongbi

    data_frame = pd.DataFrame(data=df_dic)
    data_frame.replace([np.inf, -np.inf], 0.00, inplace=True)
    return data_frame


def get_data_task3():
    url_list = get_net_list()
    data_pre = get_data_pre(url_list)
    return get_data(data_pre)


def main():
    warnings.filterwarnings("ignore")
    date = time.strftime("%Y-%m-%d", time.localtime())
    print("---开始下载截止到"+date+"发布了的数据---")
    print("---开始下载'工业主要产品产量及增长速度数据'数据---")
    df_task1 = get_data_task1()
    print("最新数据是到" + str(int(df_task1.columns.values[1])))
    print("---开始下载'工业分大类行业增加值增长速度'数据---")
    df_task2 = get_data_task2()
    print("最新数据是到" + str(int(df_task2.columns.values[1])))
    print("---开始下载'全国规模以上企业利润'数据---")
    df_task3 = get_data_task3()
    print("最新数据是到" + str(df_task3.columns.values[1][:6]))
    print("---下载数据完毕---")

    date = time.strftime("%Y-%m-%d", time.localtime())
    excel_dir = "./data/" + date + ".xls"
    writer = pd.ExcelWriter(excel_dir)
    print("---生成excel文件,文件名字为"+ excel_dir + " ---")
    df_task1.to_excel(writer, index=False, encoding="GBK", sheet_name='工业主要产品产量及增长速度')
    df_task2.to_excel(writer, index=False, encoding="GBK", sheet_name='工业分大类行业增加值增长速度')
    df_task3.to_excel(writer, index=False, encoding="GBK", sheet_name='全国规模以上企业利润')
    writer.save()
    turn_color(path=excel_dir, dir_path=excel_dir)
    print("---结束！！！---")


if __name__ == '__main__':
    main()





