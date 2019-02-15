import os

def read_last():
    '''读取存档数据，返回最近一条房源的发布时间和id'''

    csv_files = []
    for i in os.listdir():
        if i.endswith('.csv'):
            csv_files.append(i)
    # print('#####',csv_files)
    # 按文件名排序，打开日期最大的文件
    csv_files.sort()
    with open(csv_files[-1], 'r') as f:
        f.readline()  # 表头
        # 最近的一个房源
        last = f.readline().split(',')
        last_house = last[2]
        last_time = last[-3]
        # 当前工作目录为/Users/kk/PycharmProjects/Python3Scrapy/woaiwojia_2th/
        print('\n从存档文件<{}>获取最近一条数据：{}\n'.format(os.path.abspath(csv_files[-1]), (last_house, last_time)))
        return last_time, last_house
