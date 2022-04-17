import pandas as pd
import os
import numpy as np

from math import radians, sin, cos, atan2, pow, sqrt
from matplotlib import pyplot as plt
from matplotlib import font_manager

plt.style.use('seaborn')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

r = 6371137


def cal_distance(lat1, long1, lat2, long2):
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    long1 = radians(long1)
    long2 = radians(long2)
    a = (lat1 - lat2) / 2
    b = (long1 - long2) / 2
    delta = sqrt(sin(a) * sin(a) + cos(lat1) * cos(lat2) * sin(b) * sin(b))
    return 2 * r * atan2(delta, 1-delta)

def est_distance(speed1, speed2,seconds):
    return 1.852*(speed1+speed2)*seconds/(2*3.6)

def head_outlier(data, thresh = 0):
    out = 0
    normal = pd.DataFrame(columns=data.columns)
    abnormal = pd.DataFrame(columns=data.columns)
    shape = data.shape[0]
    data1 = data.iloc[0]
    data2 = data.iloc[1]
    normal = pd.concat([pd.DataFrame(data1).T, normal], axis=0)
    for i in range(2, shape):
        data3 = data.iloc[i]
        t31 = (data3['time'] - data1['time']).total_seconds()
        t21 = (data2['time'] - data1['time']).total_seconds()
        c1 = data1['angle']
        c2 = data2['angle']
        c3 = data3['angle']
        if abs(c2 - c1) > thresh >= abs(c3 - c1) and abs(c2 - c3) > thresh:
            abnormal = pd.concat([pd.DataFrame(data2).T, abnormal], axis=0)
            out += 1

        else:
            normal = pd.concat([pd.DataFrame(data2).T, normal], axis=0)
        data1 = data2
        data2 = data3
    return out, normal, abnormal

def viusalize(data1, data2):
    plt.scatter(data1['long'], data1['lat'], marker='o', color='blue', edgecolors='black', label='原始数据')
    plt.scatter(data2['long'], data2['lat'], marker='x', color='red', label='异常数据')

def count_outliers(data):
    out = 0
    normal = pd.DataFrame(columns=data.columns)
    abnormal = pd.DataFrame(columns=data.columns)
    shape = data.shape[0]
    data1 = data.iloc[0]
    normal = pd.concat([pd.DataFrame(data1).T,normal] , axis=0)

    for i in range(1, shape):
        data2 = data.iloc[i]
        seconds = abs((data2['time'] - data1['time']).total_seconds())
        lat1 = data1['lat']
        long1 = data1['long']
        lat2 = data2['lat']
        long2 = data2['long']
        real = cal_distance(lat1, long1, lat2, long2)
        estimate = est_distance(data1['speed'], data2['speed'], seconds)
        # if seconds > 360:
        #     abnormal = pd.concat([pd.DataFrame(data2).T,abnormal] , axis=0)
        #     # plt.scatter(data2['long'], data2['lat'], marker='x', color='red')
        #     out += 1
        #     data1 = data2
        #     continue
        if abs(real-estimate) > 100 and real > estimate > 10:
            abnormal = pd.concat([pd.DataFrame(data2).T, abnormal], axis=0)
            out += 1
        # if not (113.43 < long2 < 115.04 and 29.55 < lat2 < 31.19):
        #     abnormal = pd.concat([pd.DataFrame(data2).T, abnormal], axis=0)
        #     out += 1
        else:
            normal = pd.concat([pd.DataFrame(data2).T,normal] , axis=0)

        data1 = data2
    return out,normal,abnormal

if __name__ == '__main__':
    path = u'dataset/normalized'
    os.chdir(path)
    for csv in os.listdir():
        if csv.endswith('17 (106).csv'):
            data = pd.read_csv(csv)
            data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')
            outliers, normal, abnormal = count_outliers(data)
            # outliers, normal, abnormal = head_outlier(data, 5)

            print(f'outliers : {outliers},writing to normalized2/{csv}')
            if outliers > -1:
                viusalize(normal, abnormal)
                # plt.xlim([114.2, 114.65])
                # plt.ylim([30.45, 30.70])
                plt.xlabel('经度/°')
                plt.ylabel('纬度/°')
                plt.legend()
                plt.show()


