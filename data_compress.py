import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import sqrt

plt.style.use('seaborn')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

path = u'dataset'
# os.chdir(path)

def distance(a, b):
    return  sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def point_line_distance(point, start, end):
    if (start.all == end.all):
        return distance(point, start)
    else:
        n = abs(
            (end[0] - start[0]) * (start[1] - point[1]) -
            (start[0] - point[0]) * (end[1] - start[1])
        )
        d = sqrt(
            (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
        )
        return n / d


def rdp(points, epsilon):
    """Reduces a series of points to a simplified version that loses detail, but
    maintains the general shape of the series.
    """
    dmax = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        d = point_line_distance(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d

    if dmax >= epsilon:
        results = rdp(points[:index+1], epsilon)[:-1] + rdp(points[index:], epsilon)
    else:
        results = [points[0], points[-1]]

    return results

if __name__ == '__main__':
    for csv in os.listdir():
        if csv.endswith('17 (106).csv'):
            data = pd.read_csv(csv)
            data['time'] = pd.to_datetime(data['time'], format='%H:%M:%S')
            # outliers, normal, abnormal = count_outliers(data)
            result = rdp(np.array([data['long'].to_numpy(), data['lat'].to_numpy()]).T, 0.01)
            result = np.array(result)
            plt.scatter(data['long'], data['lat'], marker='o', color='blue', edgecolors='black', label='原始数据')
            plt.scatter(result[:,0], result[:, 1], marker='*', color='orange', label='压缩数据')
            plt.title(f'压缩率{round(1-result.shape[0]/data.shape[0],4)*100}%')
            plt.xlabel('经度/°')
            plt.ylabel('纬度/°')
            plt.legend()
            plt.show()
