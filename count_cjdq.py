import pandas as pd
import os
import numpy as np
from detect_outlier import cal_distance
import datetime
from math import radians, sin, cos, atan2, pow, sqrt
from matplotlib import pyplot as plt
from matplotlib import font_manager

plt.style.use('seaborn')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

r = 6371137



def intersection(
        pt1,
        pt2,
        pt3=[114.2872, 30.5494],
        pt4=[114.2781, 30.5554]):
    x1 = pt1[0]
    x2 = pt2[0]

    y1 = pt1[1]
    y2 = pt2[1]

    x3 = pt3[0]
    x4 = pt4[0]

    y3 = pt3[1]
    y4 = pt4[1]
    det = lambda a, b, c, d: a * d - b * c
    d = det(x1 - x2, x4 - x3, y1 - y2, y4 - y3)
    p = det(x4 - x2, x4 - x3, y4 - y2, y4 - y3)
    q = det(x1 - x2, x4 - x2, y1 - y2, y4 - y2)
    if d != 0:
        lam, eta = p / d, q / d
        if not (0 <= lam <= 1 and 0 <= eta <= 1): return []
        return [lam * x1 + (1 - lam) * x2, lam * y1 + (1 - lam) * y2]
    if p != 0 or q != 0: return []
    t1, t2 = sorted([pt1, pt2]), sorted([pt3, pt4])
    if t1[1] < t2[0] or t2[1] < t1[0]: return []
    return max(t1[0], t2[0])

def count_intersection(data):
    out = 0
    normal = pd.DataFrame(columns=data.columns)
    abnormal = pd.DataFrame(columns=data.columns)
    shape = data.shape[0]
    data1 = data.iloc[0]
    normal = pd.concat([pd.DataFrame(data1).T, normal], axis=0)
    inter_pt = pd.DataFrame(columns=data.columns)
    for i in range(1, shape):
        data2 = data.iloc[i]
        seconds = (data2['time'] - data1['time']).total_seconds()
        lat1 = data1['lat']
        long1 = data1['long']
        lat2 = data2['lat']
        long2 = data2['long']
        inter = intersection([long1, lat1], [long2, lat2])
        if len(inter) > 0:
            inter_row = cal_time(data1, data2, inter)
            inter_row['long'] = inter[0]
            inter_row['lat'] = inter[1]
            inter_pt = pd.concat([inter_pt, inter_row], axis=0)
            out += 1
            abnormal = pd.concat([abnormal, pd.DataFrame(data2).T], axis=0)
            abnormal = pd.concat([abnormal, pd.DataFrame(data1).T], axis=0)
        else:
            normal = pd.concat([pd.DataFrame(data2).T, normal], axis=0)
        data1 = data2
    return out, normal, abnormal, inter_pt

def cal_time(data0, data1, pt):
    avg_speed = 1.852*(data0['speed'] +data1['speed'])/(2*3.6)
    if data0['time'] > data1['time']:
        time = (data0['time'] - data1['time']).total_seconds()
        predata = data1
    else:
        time = (data1['time'] - data0['time']).total_seconds()
        predata = data0

    total_distance = cal_distance(data0['lat'], data0['long'], data1['lat'], data1['long'])
    delta_distance = cal_distance(predata['lat'], predata['long'], pt[1], pt[0])
    new_time = predata['time'] + datetime.timedelta(seconds=time*(delta_distance/total_distance))
    insert_row = pd.DataFrame(predata, copy=True).T
    insert_row['time'] = new_time
    insert_row['speed'] = avg_speed
    return insert_row

if __name__ == '__main__':
    path = u'dataset/normalized'
    os.chdir(path)
    data = pd.read_csv('20161017 (1).csv')
    inter_all = pd.DataFrame(columns=data.columns)
    for csv in os.listdir():
        if csv.endswith('.csv') and csv.startswith('20161017'):
            data = pd.read_csv(csv)
            data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')
            inters, normal, abnormal, inter_pt = count_intersection(data)
            inter_all = pd.concat([inter_all,inter_pt], axis=0)
            print(f'intersections : {inters}')
            plt_raw = plt.scatter(data['long'], data['lat'],marker='o', color='blue', edgecolors='black')
            pt1 = [114.2872, 30.5494]
            pt2 = [114.2781, 30.5554]
            plt_bridge, = plt.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], linestyle='dotted', color='r')
            for i in range(0, abnormal.shape[0], 2):
                plt_line = abnormal.iloc[i:i+2]
                plt_route, = plt.plot(plt_line['long'], plt_line['lat'],
                         linestyle='dotted', color='lime')
            if inters > 0:
                for i in range(inter_pt.shape[0]):
                    plt_inter = plt.scatter(inter_pt.iloc[i]['long'],inter_pt.iloc[i]['lat'], marker='x', color='black')
                    pass_time = inter_pt.iloc[i]['time'].hour
                    plt.text(inter_pt.iloc[i]['long']+0.001,inter_pt.iloc[i]['lat'], f'过桥时间段：{inter_pt["date"].to_numpy()[0]}: {pass_time-1}-{pass_time}时')
                    print(f"time:{pass_time}")
            plt.xlim([114.2, 114.65])
            plt.ylim([30.45, 30.70])
            plt.xlabel('经度/°')
            plt.ylabel('纬度/°')
            # plt.title(f'{csv}')
            plt.legend([plt_raw, plt_bridge, plt_route, plt_inter],['原始数据', '长江大桥', '船舶路径', '交汇点'])
            # plt.legend([plt_raw, plt_bridge], ['原始数据', '长江大桥'])
            plt.show()

    # inter_all.to_csv('../all_inter')