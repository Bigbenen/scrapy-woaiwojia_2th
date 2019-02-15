'''用于有序合并该目录内的csv文件'''
import os
#import logging
import pandas as pd
from datetime import datetime


class CsvIntegrate:
    def __init__(self):
        self.saving_name = datetime.now().strftime('%Y%m%d') + '.csv'

    def integrate(self):
        '''整合项目内到csv数据文件'''
        csv_files = []
        print('所在目录有文件：',os.listdir())
        for i in os.listdir():
            if i.endswith('.csv'):
                csv_files.append(i)
        print('csv文件:',csv_files)
        if self.saving_name in csv_files:
            self.saving_name = '9' + self.saving_name

        #按文件名排序
        csv_files.sort()
        # 默认每次下载数据后（2个csv文件）应合并一次，超出2个或不足2个会报错
        if len(csv_files) == 2:
            # 先写入最近更新的文件(1.csv),保留表头
            df = pd.read_csv(csv_files[0])
            df.to_csv(self.saving_name, index=False)
            # 写入旧文件（以日期命名的），不要表头
            df = pd.read_csv(csv_files[1])
            df.to_csv(self.saving_name, header=False, mode='a+', index=False)
            print('\n已整合文件{}-->{}\n'.format(csv_files, self.saving_name))

            self._remove(csv_files)
        else:
            print('csv文件数量不符！不具备更新条件，请手动检查！')

    #删除整合后的过期文件
    def _remove(self, files):
        for i in files:
            if i != self.saving_name and os.path.exists(i) and i.endswith('.csv'):
                os.remove(i)
                print('\n已删除{}\n'.format(i))

if __name__ == '__main__':
    m = CsvIntegrate()
    m.integrate()