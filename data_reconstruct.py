import datetime
from scipy import interpolate
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
path = u'dataset'
os.chdir(path)

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

def viusalize(data1, data2):
    plt.scatter(data1['long'], data1['lat'], marker='o', color='blue', edgecolors='black', label='原始数据')
    plt.scatter(data2['long'], data2['lat'], marker='o', color='orange', edgecolors='black', label='插入数据')

def insert_data(data):
    out = 0
    normal = pd.DataFrame(columns=data.columns)
    abnormal = pd.DataFrame(columns=data.columns)
    shape = data.shape[0]
    data1 = data.iloc[0]
    normal = pd.concat([pd.DataFrame(data1).T,normal] , axis=0)
    mask = []
    for i in range(1, shape):
        data2 = data.iloc[i]
        seconds = (data2['time']-data1['time']).total_seconds()
        if seconds > 360:
            abnormal = pd.concat([pd.DataFrame(data2).T,abnormal] , axis=0)
            # plt.scatter(data2['long'], data2['lat'], marker='x', color='red')
            mask.append(i)

        # if abs(real-estimate) > 140:
        #     abnormal = pd.concat([pd.DataFrame(data2).T, abnormal], axis=0)
        #     out += 1
        # if not (113.43 < long2 < 115.04 and 29.55 < lat2 < 31.19):
        #     abnormal = pd.concat([pd.DataFrame(data2).T, abnormal], axis=0)
        #     out += 1
        else:
            normal = pd.concat([pd.DataFrame(data2).T,normal] , axis=0)
        data1 = data2
    insert = pd.DataFrame(columns=data.columns)
    for point in mask:
        data1 = data.iloc[point]
        data2 = data.iloc[point-1]
        lat1 = data1['lat']
        long1 = data1['long']
        lat2 = data2['lat']
        long2 = data2['long']
        real = cal_distance(lat1, long1, lat2, long2)
        estimate = est_distance(data1['speed'], max(data2['speed'],1), 360)
        k = max(np.floor(real/estimate), 2)
        lati = (lat1-lat2)/k
        longi = (long1-long2)/k

        for i in range(int(k)):
            out += 1
            insert_row = pd.DataFrame(data1, copy=True).T
            insert_row['long'] = long1-(i+1)*longi
            insert_row['lat'] = lat1-(i+1)*lati
            insert_row['time'] = data1['time']  + datetime.timedelta(seconds=360)
            insert = pd.concat([insert,insert_row], axis=0)
    return insert, out




if __name__ == '__main__':
    for csv in os.listdir():
        if csv.endswith('(106).csv') and csv.startswith('20161017'):
            data = pd.read_csv(csv)
            data['time'] = pd.to_datetime(data['time'], format='%H:%M:%S')

            insert, inserts = insert_data(data)
            print(f'inserts : {inserts}')
            viusalize(data,insert)
            # plt.xlim([114.2, 114.65])
            # plt.ylim([30.45, 30.70])
            # plt.xlabel('经度/°')
            # plt.ylabel('纬度/°')
            # plt.legend()
            # plt.show()

            newdf = pd.concat([data,insert],axis=0)
            from data_compress import rdp
            result = rdp(np.array([newdf['long'].to_numpy(), newdf['lat'].to_numpy()]).T, 0.001)
            result = np.array(result)
            # plt.scatter(data['long'], data['lat'], marker='o', color='blue', edgecolors='black', label='原始数据')
            plt.scatter(result[:, 0], result[:, 1], marker='*', color='white', label='压缩数据')
            plt.title(f'压缩率{round(1 - result.shape[0] / data.shape[0], 4) * 100}%')
            plt.xlabel('经度/°')
            plt.ylabel('纬度/°')
            plt.legend()
            plt.show()