
import csv
import matplotlib.pyplot as plt
import seaborn as sbn
from collections import defaultdict
from datetime import datetime, timedelta
import re
from glob import glob

plt.style.use('classic')
#创建图形和轴，也可以省略，会自动创建
fig = plt.figure()
ax = plt.axes()

class MyAnalysis:
    def __init__(self):
        self.guapai = defaultdict(int)
        self.total_price = defaultdict(list)  # 用于计算junjia
        self.junjia = defaultdict(int)

    def do_by_month(self):
        # 找到csv文件并分析
        csvfile = glob('*.csv')[0]
        print('开始分析 ' + csvfile)
        with open(csvfile, 'r') as f:
            reader = csv.reader(f)
            # csv表头对应的索引
            time, price = -3, -6
            for row in reader:
                # 跳过表头首行, csv行编码从1开始
                if reader.line_num != 1:
                    # 按月统计
                    month = row[time][:7]
                    # 每月挂牌数量
                    self.guapai[month] += 1
                    # 每月挂牌均价
                    p = int(re.match(r'单价(\d+)元', row[price]).group(1))
                    self.total_price[month].append(p)
                    # print(sorted(guapai))
                    # print(total_price)

        # 计算每月挂牌均价
        for key in self.total_price:
            self.junjia[key] = sum(self.total_price[key]) / len(self.total_price[key])
        # print(junjia)

        for fig, type, title, order, ylable in zip([self.guapai, self.junjia], ['-r', '--b'],
                                                   ['Number of second_hand Houses Trend Graph',
                                                    'Average Price Trend Graph'], [1, 2], ['number', 'avg_price']):
            # 键列表，按时间顺序
            f = sorted(fig)
            x = [datetime.strptime(k, '%Y-%m') for k in f]
            y = [fig[k] for k in f]
            plt.subplot(2, 1, order)
            plt.title(title)
            plt.xlabel('date')
            plt.ylabel(ylable)
            plt.plot(x, y, type)

        fig_name = csvfile.split('.')[0] + '.jpg'
        plt.savefig(fig_name, dpi=300)
        plt.show()

if __name__ == '__main__':
    a = MyAnalysis()
    a.do_by_month()