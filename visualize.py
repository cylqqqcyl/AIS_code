import os
import pandas as pd
from matplotlib import pyplot as plt
plt.style.use('seaborn')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
path = u'dataset'
os.chdir(path)


def visualize_graph():
    for csv in os.listdir():
        if csv.startswith('20161021'):
            data = pd.read_csv(csv)
            plt.scatter(data['prelong'], data['prelat'])
            plt.scatter(data['long'], data['lat'])
            plt.show()

def visualize_data():
    for csv in os.listdir():
        if csv.startswith('20161021'):
            data = pd.read_csv(csv)
            for row in data.iterrows():
                plt.plot(data['speed'])
                plt.show()



if __name__ == '__main__':
    by_hour = pd.read_csv(u'hour_table.csv')
    del by_hour['Unnamed: 0']
    new_time = pd.DataFrame(columns=['0-7', '7-15', '15-23'])
    for i in range(3):
        sumcolumn = by_hour[f"{i * 8}"]
        for j in range(1, 8):
            column = i*8+j
            sumcolumn += by_hour[f"{column}"]
        new_time.iloc[:, i] = sumcolumn
    # for i in range(24):
    #     column = i
    #     if column == 0:
    #         continue
    #     sumcolumn += by_hour[f"{column}"]
    #     new_time = pd.concat([new_time,sumcolumn],axis=0)
    # for i in range(9):
    #     by_hour[f'{i+17}'].plot.bar()
    #     plt.show()
    # by_hour.to_csv(u'hour_table.csv')
    new_time.plot()
    plt.xticks([i for i in range(9)],['17', '18', '19', '20', '21', '22', '23', '24', '25'])
    plt.xlabel('日期')
    plt.ylabel('交通量（单位：艘）')
    plt.legend(title='时间段')
    plt.show()
    new_time.to_csv(u'new_time.csv')
    # latex = by_hour.to_latex()
    # print(latex)