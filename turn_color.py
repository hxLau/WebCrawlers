import pandas as pd
import xlrd
from xlutils.copy import copy
import xlwt
from util import is_number


def turn_color(path, dir_path):
    # 第一步  把原表格中的数据拷贝一份
    book = xlrd.open_workbook(path)
    #  book = xlrd.open_workbook(path, formatting_info=True)
    #  设置 formatting_info=True ，当打开表格是保存表格原有的样式，进行保存时，
    #  原来的样式不会丢失

    wb = copy(book)
    # 第二步  设置样式
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 2 		 # 5 背景颜色为黄色
    #1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon,
    # 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray

    style = xlwt.XFStyle()
    style.pattern = pattern

    pattern_down = xlwt.Pattern()
    pattern_down.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern_down.pattern_fore_colour = 3  # 5 背景颜色为黄色
    # 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon,
    # 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray

    style_down = xlwt.XFStyle()
    style_down.pattern = pattern_down

    # '工业主要产品产量及增长速度'
    ws_1 = wb.get_sheet(0)
    df_1 = pd.read_excel(path, sheet_name='工业主要产品产量及增长速度')

    # 相差15
    for i in range(df_1.shape[0]):
        item = df_1.loc[i].values[1:]
        for j in range(item.shape[0]-1):
            if is_number(str(item[j])) and is_number(str(item[j+1])):
                if (item[j] - item[j+1]) >= 15.0:
                    ws_1.write(i+1, j+1, float(item[j]), style)

    for i in range(df_1.shape[0]):
        item = df_1.loc[i].values[1:]
        for j in range(item.shape[0]-1):
            if is_number(str(item[j])) and is_number(str(item[j+1])):
                if (item[j] - item[j+1]) <= -15.0:
                    ws_1.write(i+1, j+1, float(item[j]), style_down)

    # 连三负转正
    for i in range(df_1.shape[0]):
        item = df_1.loc[i].values[1:]
        for j in range(item.shape[0]-4):
            if is_number(str(item[j])) and is_number(str(item[j+1])) and is_number(str(item[j+2])) and is_number(str(item[j+3])):
                if item[j]>0 and item[j+1]<0 and item[j+2]<0 and item[j+3]<0:
                    ws_1.write(i+1, j+1, float(item[j]), style)

    # 连三正转负
    for i in range(df_1.shape[0]):
        item = df_1.loc[i].values[1:]
        for j in range(item.shape[0]-4):
            if is_number(str(item[j])) and is_number(str(item[j+1])) and is_number(str(item[j+2])) and is_number(str(item[j+3])):
                if item[j]<0 and item[j+1]>0 and item[j+2]>0 and item[j+3]>0:
                    ws_1.write(i+1, j+1, float(item[j]), style_down)

    # '工业分大类行业增加值增长速度'
    ws_2 = wb.get_sheet(1)
    df_2 = pd.read_excel(path, sheet_name='工业分大类行业增加值增长速度')

    # 相差15
    for i in range(df_2.shape[0]):
        item = df_2.loc[i].values[1:]
        for j in range(item.shape[0]-1):
            if is_number(str(item[j])) and is_number(str(item[j+1])):
                if (item[j] - item[j+1]) >= 15.0:
                    ws_2.write(i+1, j+1, float(item[j]), style)

    for i in range(df_2.shape[0]):
        item = df_2.loc[i].values[1:]
        for j in range(item.shape[0]-1):
            if is_number(str(item[j])) and is_number(str(item[j+1])):
                if (item[j] - item[j+1]) <= -15.0:
                    ws_2.write(i+1, j+1, float(item[j]), style_down)

    # 连三负转正
    for i in range(df_2.shape[0]):
        item = df_2.loc[i].values[1:]
        for j in range(item.shape[0]-4):
            if is_number(str(item[j])) and is_number(str(item[j+1])) and is_number(str(item[j+2])) and is_number(str(item[j+3])):
                if item[j]>0 and item[j+1]<0 and item[j+2]<0 and item[j+3]<0:
                    ws_2.write(i+1, j+1, float(item[j]), style)

    # 连三正转负
    for i in range(df_2.shape[0]):
        item = df_2.loc[i].values[1:]
        for j in range(item.shape[0]-4):
            if is_number(str(item[j])) and is_number(str(item[j+1])) and is_number(str(item[j+2])) and is_number(str(item[j+3])):
                if item[j]<0 and item[j+1]>0 and item[j+2]>0 and item[j+3]>0:
                    ws_2.write(i+1, j+1, float(item[j]), style_down)

    # '全国规模以上企业利润'
    ws_3 = wb.get_sheet(2)
    df_3 = pd.read_excel(path, sheet_name='全国规模以上企业利润')

    month_number = int((df_3.shape[1] - 1) / 3)

    # 相差15
    for i in range(df_3.shape[0]):
        item = df_3.loc[i].values[1:]
        for j in range(month_number - 1):
            for k in range(3):
                if is_number(str(item[(j * 3 + k)])) and is_number(str(item[((j + 1) * 3 + k)])):
                    if (item[(j * 3 + k)] - item[((j + 1) * 3 + k)]) >= 15:
                        ws_3.write(i + 1, (j * 3 + k) + 1, float(item[(j * 3 + k)]), style)

    for i in range(df_3.shape[0]):
        item = df_3.loc[i].values[1:]
        for j in range(month_number - 1):
            for k in range(3):
                if is_number(str(item[(j * 3 + k)])) and is_number(str(item[((j + 1) * 3 + k)])):
                    if (item[(j * 3 + k)] - item[((j + 1) * 3 + k)]) <= -15:
                        ws_3.write(i + 1, (j * 3 + k) + 1, float(item[(j * 3 + k)]), style_down)

    # 连三负转正
    for i in range(df_3.shape[0]):
        item = df_3.loc[i].values[1:]
        for j in range(month_number - 4):
            if is_number(str(item[(j * 3 + k)])) and is_number(
                    str(item[((j + 1) * 3 + k)])) and is_number(
                    str(item[((j + 2) * 3 + k)])) and is_number(str(item[((j + 3) * 3 + k)])):
                if item[(j * 3 + k)] > 0 and item[((j + 1) * 3 + k)] < 0 and \
                        item[((j + 2) * 3 + k)] < 0 and item[((j + 3) * 3 + k)] < 0:
                    ws_3.write(i + 1, (j * 3 + k) + 1, float(item[(j * 3 + k)]), style)

    # 连三正转负
    for i in range(df_3.shape[0]):
        item = df_3.loc[i].values[1:]
        for j in range(month_number - 4):
            if is_number(str(item[(j * 3 + k)])) and is_number(
                    str(item[((j + 1) * 3 + k)])) and is_number(
                    str(item[((j + 2) * 3 + k)])) and is_number(str(item[((j + 3) * 3 + k)])):
                if item[(j * 3 + k)] < 0 and item[((j + 1) * 3 + k)] > 0 and \
                        item[((j + 2) * 3 + k)] > 0 and item[((j + 3) * 3 + k)] > 0:
                    ws_3.write(i + 1, (j * 3 + k) + 1, float(item[(j * 3 + k)]), style_down)

    wb.save(dir_path)
